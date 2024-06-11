IMAGE_TOKEN_INDEX = -200
IGNORE_INDEX = -100
LLaVA_IMAGE_TOKEN = "<image>"
DEFAULT_IMAGE_TOKEN = "<|image_1|>"
local_rank = None
def rank0_print(*args):
    if local_rank == 0 or local_rank == '0' or local_rank is None:
        print(*args)


@dataclass
class DataArguments:
    args = parser.parse_args()

    data_path: str = field(
        default=None, metadata={"help": "Path to the training data."}
    )
    lazy_preprocess: bool = False
    is_multimodal: bool = False
    image_folder: Optional[str] = field(default=None)
    max_seq_length: int = field(
        default=2048, metadata={"help": "Maximum sequence length."}
    )




def llava_to_openai(data):
    role_mapping = {"human": "user", "gpt": "assistant"}

    transformed_data = []
    for entry in data:
        transformed_entry = {
            "role": role_mapping.get(entry["from"], entry["from"]),
            "content": entry["value"].replace(LLaVA_IMAGE_TOKEN, DEFAULT_IMAGE_TOKEN),
        }
        transformed_data.append(transformed_entry)

    return transformed_data




class LazySupervisedDataset(Dataset):
    """Dataset for supervised fine-tuning."""

    def __init__(
        self,
        data_path: str | list,
        processor: transformers.PreTrainedTokenizer,
        data_args: DataArguments,
        padding=True,
    ):
        super(LazySupervisedDataset, self).__init__()
        if isinstance(data_path, str):
            list_data_dict = json.load(open(data_path, "r"))
        else:
            list_data_dict = data_path

        rank0_print("Formatting inputs...Skip in lazy mode")
        self.processor = processor
        self.list_data_dict = list_data_dict
        self.data_args = data_args
        self.padding = padding
        self.max_seq_length = data_args.max_seq_length

    def __len__(self):
        return len(self.list_data_dict)

    def __getitem__(self, i) -> Dict[str, torch.Tensor]:
        sources = self.list_data_dict[i]
        if isinstance(i, int):
            sources = [sources]
        assert len(sources) == 1, "Don't know why it is wrapped to a list"  # FIXME
        processor = self.processor
        if "image" in sources[0]:
            image_file = self.list_data_dict[i]["image"]
            image_folder = self.data_args.image_folder

            if not os.path.exists(image_file):
                image_file = os.path.join(image_folder, image_file)
            image = [Image.open(image_file).convert("RGB")]
        else:
            image = None
        sources = copy.deepcopy([e["conversations"] for e in sources])
        for i in range(len(sources)):
            sources[i] = llava_to_openai(sources[i])

        prompt = processor.tokenizer.apply_chat_template(
            sources[0], tokenize=False, add_generation_prompt=True
        )
        data_dict = processor(prompt, image, return_tensors="pt")

        if self.padding:
            training_length = self.max_seq_length
            # data_dict = processor.tokenizer.pad(
            #     data_dict,
            #     padding="max_length",
            #     max_length=training_length,
            #     return_tensors="pt",
            # )
            if 'pixel_values' not in data_dict:
                data_dict['pixel_values'] = torch.zeros([1, 17, 3, 336, 336], dtype=torch.bfloat16)
                data_dict['image_sizes'] = torch.zeros([1, 2], dtype=torch.int64)
            data_dict = dict(
                input_ids=data_dict["input_ids"][0],
                attention_mask=data_dict["attention_mask"][0],
                pixel_values=data_dict["pixel_values"][0],
                image_sizes=data_dict["image_sizes"][0],
                labels=data_dict["labels"][0],
                # labels=processor.tokenizer.pad(
                #     {"input_ids": data_dict["labels"][0]},
                #     padding="max_length",
                #     max_length=training_length,
                #     return_tensors="pt",
                # ).input_ids,
            )
        else:
            data_dict = dict(
                input_ids=data_dict["input_ids"][0],
                attention_mask=data_dict["attention_mask"][0],
                pixel_values=data_dict["pixel_values"][0],
                image_sizes=data_dict["image_sizes"][0],
                labels=data_dict["labels"][0],
            )
        return data_dict

@dataclass
class DataCollatorForSupervisedDataset(object):
    """Collate examples for supervised fine-tuning."""

    tokenizer: transformers.PreTrainedTokenizer

    def __call__(self, instances: Sequence[Dict]) -> Dict[str, torch.Tensor]:
        input_ids, labels = tuple([instance[key] for instance in instances]
                                  for key in ("input_ids", "labels"))
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids,
            batch_first=True,
            padding_value=self.tokenizer.pad_token_id)
        labels = torch.nn.utils.rnn.pad_sequence(
            labels,
            batch_first=True,
            padding_value=IGNORE_INDEX)
        input_ids = input_ids[:, :self.tokenizer.model_max_length]
        labels = labels[:, :self.tokenizer.model_max_length]

        pixel_values = [instance["pixel_values"] for instance in instances]
        pixel_values = torch.stack(pixel_values, dim=0)
        image_sizes = [instance["image_sizes"] for instance in instances]
        image_sizes = torch.stack(image_sizes, dim=0)

        batch = dict(
            input_ids=input_ids,
            labels=labels,
            pixel_values=pixel_values,
            image_sizes=image_sizes,
            attention_mask=input_ids.ne(self.tokenizer.pad_token_id),
        )
        return batch

## Training
def find_target_linear_names(model, num_lora_modules=-1, lora_namespan_exclude=["self_attn", "lm_head"], verbose=True):
    linear_cls = torch.nn.Linear
    # lora_module_names = set()
    lora_module_names = []
    lora_namespan_exclude += ["vision_model", "img_projection"]
    for name, module in model.named_modules():
        if any(ex_keyword in name for ex_keyword in lora_namespan_exclude):
            continue
        if isinstance(module, linear_cls):
            lora_module_names.append(name)
    
    if num_lora_modules > 0:
        lora_module_names = lora_module_names[-num_lora_modules:]
    if verbose:
        rank0_print(f"Found {len(lora_module_names)} lora modules: {lora_module_names}")
    return lora_module_names


def train():
    global local_rank
    local_rank = int(os.environ["LOCAL_RANK"])
    ACCELERATE_USE_FSDP = os.environ.get("ACCELERATE_USE_FSDP", "false") == "true"

    args = parser.parse_args()
    rank0_print('Procession args\033[91m', args, '\033[0m')
    if torch.cuda.is_bf16_supported():
        compute_dtype = torch.bfloat16
    else:
        compute_dtype = torch.float16
    rank0_print('compute_dtype', compute_dtype)

    config = Phi3VConfig.from_pretrained(args.model_id)
    if args.disable_flash_attn2:
        config._attn_implementation = "eager"

    quantization_config = None
    config.use_cache = False
    if args.quantization:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            llm_int8_skip_modules=["img_projection"],
        )
    
    model = Phi3VForCausalLM.from_pretrained(
        args.model_id,
        torch_dtype=compute_dtype, 
        device_map=f"cuda:{local_rank}",
        # trust_remote_code=True, 
        # low_cpu_mem_usage=True,
        config=config,
        quantization_config=quantization_config
    )
    processor = Phi3VProcessor.from_pretrained(args.model_id)

    if args.quantization:
        model.config.torch_dtype = torch.bfloat16
        from peft import prepare_model_for_kbit_training
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=args.gradient_checkpointing, gradient_checkpointing_kwargs={"use_reentrant": False})
    
    if args.gradient_checkpointing:
        if args.deepspeed_config is not None and 'zero2' in args.deepspeed_config:
            warnings.warn("``zero2` with `gradient_checkpointing` may lead to errors in some situations, so we disable `gradient_checkpointing` for `zero2` by default. You are welcome to hack this logic and test if the process works as expected (and you may need to comment `model.enable_input_require_grads()`).")
        else:
            if ACCELERATE_USE_FSDP:
                warnings.warn("``gradient_checkpointing`` may not work well with ``fsdp``. We will enable it for you. Please be sure you know what you are doing and aware of the potential errors.")
            model.enable_input_require_grads()
            model.model.gradient_checkpointing = True
            rank0_print("Gradient checkpointing:", model.model.gradient_checkpointing)

    lora_namespan_exclude = eval(args.lora_namespan_exclude)
    peft_config = LoraConfig(
        r=args.lora_rank,
        lora_alpha=args.lora_alpha,
        target_modules=find_target_linear_names(model, lora_namespan_exclude=lora_namespan_exclude, num_lora_modules=args.num_lora_modules),
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    # with open(f'tmp/debug_{local_rank}.txt', 'w') as f:
    #     for name, param in model.named_parameters():
    #         print(f'{name} {param.shape} {param.dtype} {param.device} {param.requires_grad}', file=f)

    # TODO: make it conpatible with SFTConfig (`from trl import SFTConfig`)
    # for `trl` of newer version, `TrainingArguments` leads to an error of agument name mismatch,
    # and we should use `SFTConfig` instead.
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        optim=args.optimizer,
        learning_rate=args.learning_rate,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type=args.lr_scheduler_type,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        bf16=True,
        deepspeed=args.deepspeed_config,
        dataloader_num_workers=args.dataloader_num_workers,
        report_to=args.report_to,
        logging_dir=args.logging_dir,
        logging_steps=args.logging_steps,
    )

    # Prepare Dataset
    # Load LLaVA formatted dataset, this step may take a while if the dataset is large
    data_args = DataArguments(
        data_path=args.data_path,
        is_multimodal=True,
        image_folder=args.image_folder,
        max_seq_length=args.max_seq_length,
    )
    sft_dataset = LazySupervisedDataset(
        data_path=args.data_path, processor=processor, data_args=data_args
    )
    data_collator = DataCollatorForSupervisedDataset(tokenizer=processor.tokenizer)

    trainer = SFTTrainer(
        model=model,
        tokenizer=None,
        args=training_args,
        train_dataset=sft_dataset,
        data_collator=data_collator,
        eval_dataset=None,
        peft_config=peft_config,
        max_seq_length=args.max_seq_length,
        packing=True,
        # model_init_kwargs=dict(
        #     trust_remote_code=True,
        #     torch_dtype=compute_dtype,
        #     _attn_implementation="eager",
        #     quantization_config=quantization_config,
        # ),
    )
    rank0_print('is_deepspeed_enabled', trainer.is_deepspeed_enabled)
    rank0_print('is_fsdp_enabled', trainer.is_fsdp_enabled)

    trainer.train()
    used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
    print(f"Peak reserved memory in GPU {local_rank} = {used_memory} GB.")

    model.config.use_cache = True
    trainer.save_model(args.output_dir)


if __name__ == "__main__":
    train()