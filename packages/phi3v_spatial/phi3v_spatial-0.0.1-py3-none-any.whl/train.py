

import re

import datasets
import requests
import torch
from datasets import Features, Image, Value, load_dataset, interleave_datasets
from PIL import Image as PILImage
from transformers import AutoModelForCausalLM, AutoProcessor, Trainer, TrainingArguments
from spatial_data.features import PHI_FEATURES
from phi3v_spatial.processing_phi3_v import Phi3VProcessor
from phi3v_spatial.modeling_phi3_v import Phi3VForCausalLM
model_path = "mbodiai/phi3v-spatial"
device = "cuda:1"

kwargs = {}
kwargs['torch_dtype'] = torch.bfloat16

processor: Phi3VProcessor = AutoProcessor.from_pretrained(model_path,  trust_remote_code=True)
model: Phi3VForCausalLM = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map=device,
                                             attn_implementation='flash_attention_2')
user_prompt = '<|user|>\n'
assistant_prompt = '<|assistant|>\n'
prompt_suffix = "<|end|>\n"

SYSTEM_PROMPT = """"When requested for actions, you output the next absolute poses and grasps (in m and radians) to move the robot's end-effector in order to complete the requested task.\n
You remember that x means forward, y means left and z means up.\n

For example, if the robot's end-effector is at {x=0.3, y=0.1, z=0.4, roll=3.0, pitch=0.0, yaw=-0.1, grasp=1.0} and the task is to grasp the object directly below, you output the following:\n

    {"x":0.3,"y":0.1,"z":0.3,"roll":3.0,"pitch":1.57,"yaw":-0.1,"grasp":1.0} # Move Down, Pitch 90 degrees down
    {"x":0.3,"y":0.1,"z":0.3,"roll":3.0,"pitch":1.57,"yaw":-0.1,"grasp":0.0}  # Gripper Close


REMEMBER: Only output the actions if actions were requested. An  example request is "What are the next set of actions to move the cup to the right?"
"""

def convert_to_messages(input_obj: dict) -> list:
    """Convert input object to message format required by the application.

    Args:
        input_obj (dict): Input object containing role and content list.

    Returns:
        list: A list containing a single dictionary per role and combined content string.

    Raises:
        ValueError: If the role is invalid.
    """
    content_list = input_obj["content"]
    combined_content = []
    role = input_obj["role"]
    

    
    if any("Estimate the pose" in line for line in content_list):
        return [{"role": input_obj["role"], "content": "Given <|image_1|>, estimate the pose of the robot's end effector."}]
    
    if role == "assistant":
        for line in content_list:
            # Round off the floating point numbers to 3 decimal places
            line = re.sub(r"(\d+\.\d{3})\d+", r"\1", line)  # noqa: PLW2901
            combined_content.append(line)
    elif role == "user":
        for line in content_list:
            # Correct image token and prompting.
            line = re.sub(r"Image (\d+): <image>, ", r"<|image_\1|>, ", line)
            line = re.sub(r"Action (\d+):","", line)
            line = re.sub(r"(\d+\.\d{3})\d+", r"\1", line)
            line = re.sub("Predict the following actions to complete the task successfully", "What are the next set of actions to continue successful completion of the task", line)
            combined_content.append(line)
    else:
        raise ValueError(f"Invalid role: {role}")
    
    content_string = " ".join(combined_content)
    
    return [{"role": input_obj["role"], "content": content_string}]

def map_xarm(data):
    user_messages = convert_to_messages(data["user"])
    assistant_messages = convert_to_messages(data["assistant"])
    example = {}
    example["messages"] = user_messages + assistant_messages
    example["messages"].insert(0, {"role": "assistant", "content": "Got it."})
    example["messages"].insert(0, {"role": "user", "content": SYSTEM_PROMPT})
    example["images"] = data["images"]

    return example


def map_images_question_answer(data):
    example = {}
    messages = []
    # pprint(data)
    
    question = data["question"]
    # print(f"Question: {question}")
    image_tags = [f"<|image_{i+1}|>" for i in range(len(data["image"]))]
    image_tags = ",".join(image_tags)
    messages.append({"role": "user", "content": f"Given {image_tags}, {question}"})
    messages.append({"role": "assistant","content": data["answer"]} )
    example["images"] = data["image"]
    example["messages"] = messages
    return example


from spatial_data.datasets.rlaif import RlaifDataset
from spatial_data.datasets.vqasynth import VqaSynthDataset
from spatial_data.datasets.mimicit import MimicitDataset
from spatial_data.datasets.vsr import VsrDataset

rlaif = RlaifDataset()
vqasynth = VqaSynthDataset()
mimicit = MimicitDataset()
vsr = VsrDataset()

xarm = load_dataset("mbodiai/utokyo_xarm_pick_and_place_chat_ml", split="1_past_frame_4_future_frames", streaming=True).map(map_xarm, remove_columns=["user", "assistant", "metadata"],
                                                                                                    features=PHI_FEATURES)


from pprint import pprint
# print("rlaif", rlaif.load().features)
print("vqasynth")
pprint(vqasynth.load().features)
# print("vsr", vsr.load().features)
print("mimicit", mimicit.load().features)
print("xarm", xarm)

vsr = vsr.to_image_question_answer().map(map_images_question_answer, features=PHI_FEATURES)
mimicit = mimicit.to_image_question_answer().map(map_images_question_answer, features=PHI_FEATURES)
rlaif = rlaif.to_image_question_answer().map(map_images_question_answer, features=PHI_FEATURES)
vqasynth = vqasynth.to_image_question_answer().map(map_images_question_answer, features=PHI_FEATURES)


dataset = interleave_datasets([vsr, mimicit, rlaif, xarm, vqasynth], probabilities=[0.1, 0.2, 0.2,0.2, 0.3])

train_dataset = dataset
eval_dataset = dataset.take(100)




class DataCollator:
    def __init__(self, processor: Phi3VProcessor):
        self.processor: Phi3VProcessor = processor
        self.assistant_token = self.processor.tokenizer.convert_tokens_to_ids("<|assistant|>")

    def __call__(self, examples, print_=False):
        # input_ids_list = []
        # pixel_values_list = []
        # attention_mask_list = []
        # labels_list = []
        # image_sizes_list = []
        # assert len(examples) == 1, "Only one example is supported for now"
        images = []
        texts = []
        for i, example in enumerate(examples):
            messages = example["messages"]
            text = processor.tokenizer.apply_chat_template(messages, tokenize=False, padding=False, add_generation_prompt=False)
            # text = re.sub(r"<\|image_(\d+)\|>", r"<|image_{}|>".format(i+1), text)

            if print_:
                print(f"DC Text: {text}, length: {len(text)}")
            # need to remove last <|endoftext|> if it is there, which is used for training, not inference. For training, make sure to add <|endoftext|> in the end
            if not text.endswith("<|endoftext|>"):
                text += "<|endoftext|>"
            texts.append(text)
            images.append(example["images"])
        
        inputs = self.processor(text=texts, images=images, return_tensors="pt").to(device)
        input_ids: list = inputs["input_ids"]
        if print_:  
            print(f"DC input ids: {input_ids}")
            
            # Labels start after <|assistant|> and up to and including the <|end|> token
        labels = inputs["input_ids"][:, torch.where(inputs["input_ids"] == self.assistant_token)[0][0]:].clone()
        if print_:
            print(f"DC input ids: {inputs['input_ids']}, size: {inputs['input_ids'].size()}")
            print(f"DC labels: {labels}, size: {labels.size()}")
            
        labels[labels == self.processor.tokenizer.pad_token_id] = -100
        labels[labels == self.processor.tokenizer.eos_token_id] = -100
        labels[labels < 0] = -100
        
        inputs["labels"] = labels

            # input_ids_list.append(inputs["input_ids"])
            # pixel_values_list.append(inputs["pixel_values"])
            # attention_mask_list.append(inputs["attention_mask"])
            # labels_list.append(inputs["labels"])
            # image_sizes_list.append(inputs["image_sizes"])
                   
            # inputs = self.processor(text=text, images=example["images"], padding='longest', return_tensors="pt")
            # input_ids: list = inputs["input_ids"].tolist()[0]

        return inputs


# convos = []
# images = []
# chat = eval_dataset.take(5)
# from pprint import pprint
# for example in chat:
#     pprint(example)
#     messages = example["messages"]
#     if messages[-1]['role'] == 'assistant':
#         messages = messages[:-1]
#     convos.append(messages)
#     images.append(example['images'])



# from time import time
# tic = time()

# for i, messages in enumerate(convos):
#     print(f"Message {i}: {messages}")
#     prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
#     print(f"Prompt: {prompt}")
#     # need to remove last <|endoftext|> if it is there, which is used for training, not inference. For training, make sure to add <|endoftext|> in the end.
#     if prompt.endswith("<|endoftext|>"):
#         prompt = prompt.removesuffix("<|endoftext|>")
        
#     print(f">>> Prompt stripped\n{prompt}")
#     inputs = processor([prompt], images[i], return_tensors="pt", padding='max_length')
#     generate_ids = model.generate(**inputs, 
#                                 max_new_tokens=1000,
#                                 eos_token_id=processor.tokenizer.eos_token_id,
#                                 )
#     generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
#     response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
#     print(f'>>> Response\n{response}')
#     toc = time()
#     print(f'Execution time: {toc-tic:.2f} seconds')




datacollator = DataCollator(processor)

# test_data_processed = datacollator(chat, print_=True)


model.train()
training_args = TrainingArguments(
    bf16=True, # specify bf16=True instead when training on GPUs that support bf16
    do_eval=True,
    do_train=True,
    evaluation_strategy="epoch",
    gradient_accumulation_steps=128,
    gradient_checkpointing=True,
    output_dir="phi3v_spatial/",
    gradient_checkpointing_kwargs={"use_reentrant": False},
    learning_rate=5.0e-05,
    log_level="info",
    logging_steps=20,
    logging_strategy="steps",
    lr_scheduler_type="cosine",
    max_steps=20000,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=1,
    num_train_epochs=10,
    overwrite_output_dir=True,
    push_to_hub=True,
    hub_strategy="every_save",
    save_steps=25,
    report_to="wandb",
    save_strategy="steps",
    save_total_limit=3,
    seed=42,
    hub_private_repo=True,
    remove_unused_columns=False,
    save_safetensors=False,
    dataloader_pin_memory=False,
)



trainer = Trainer(
    args=training_args,
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=datacollator,
)

trainer.train()
