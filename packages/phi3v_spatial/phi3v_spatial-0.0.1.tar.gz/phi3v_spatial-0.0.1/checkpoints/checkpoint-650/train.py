

import re

import datasets
import requests
import torch
from datasets import Features, Image, Value, load_dataset
from PIL import Image as PILImage
from transformers import AutoModelForCausalLM, AutoProcessor, Trainer, TrainingArguments

model_path = "."
device = "cuda:6"
kwargs = {}
kwargs['torch_dtype'] = torch.bfloat16

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map=device,
                                             attn_implementation='flash_attention_2')
user_prompt = '<|user|>\n'
assistant_prompt = '<|assistant|>\n'
prompt_suffix = "<|end|>\n"

SYSTEM_PROMPT = """"When requested for actions, you output the next absolute poses and grasps (in m and radians) to move the robot's end-effector in order to complete the requested task.\n
You remember that x means forward, y means left and z means up.\n

For example, if the robot's end-effector is at {x=0.3, y=0.1, z=0.4, roll=3.0, pitch=-0.0, yaw=-0.1, grasp=0.0} and the task is to grasp the object directly below, you output the following:\n

[
    {"x":0.3,"y":0.1,"z":0.3,"roll":3.0,"pitch":-0.0,"yaw":-0.1,"grasp":1.0}, # Move Down
    {"x":0.3,"y":0.1,"z":0.3,"roll":3.0,"pitch":-0.0,"yaw":-0.1,"grasp":0.0}, # Close Gripper
]
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
            line = re.sub(r"Image (\d+): <image>, ", r"<|image_\1|>", line)
            line = re.sub(r"(\d+\.\d{3})\d+", r"\1", line)
            line = re.sub("Predict the following actions to complete the task successfully", "Predict the next set of actions to continue successful completion of the task", line)
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



def map_vsr(data):
    example = {}
    messages = []
    messages.append({"role": "user", "content": "<|image_1|> What is the image about?"})
    messages.append({"role": "assistant", "content": data["caption"]})
    messages.append({"role": "user", "content": "What is the spatial relationship in this image?"})
    messages.append({"role": "assistant", "content": data["relation"]})
    example["images"] = [PILImage.open(requests.get(data["image_link"], stream=True).raw)]
    example["messages"] = messages
    return example

vsr = load_dataset("cambridgeltl/vsr_random", split='train').map(map_vsr, remove_columns=['image', 'image_link', 'caption', 'label', 'relation', 'annotator_id', 'vote_true_validator_id', 'vote_false_validator_id', 'reference_frame'],
                                                                          features=Features({"messages": [{"role": Value('string'),"content": Value('string')}],
                                                                                                         "images": [Image()] }))



xarm = load_dataset("mbodiai/utokyo_xarm_pick_and_place_chat_ml", split="1_past_frame_4_future_frames").map(map_xarm, remove_columns=["user", "assistant", "metadata"],
                                                                                                    features=Features({"messages": [{"role": Value('string'),"content": Value('string')}],
                                                                                                        "images": [Image()] }))
                                                                                                    
train_vsr = vsr.train_test_split(test_size=0.1)["train"]
train_xarm = xarm.train_test_split(test_size=0.1)["train"]

train_dataset = datasets.interleave_datasets([train_vsr, train_xarm], probabilities=[0.5, 0.5])

eval_vsr = vsr.train_test_split(test_size=0.1)["test"]
eval_xarm = xarm.train_test_split(test_size=0.1)["test"]
eval_dataset = datasets.interleave_datasets([eval_vsr, eval_xarm], probabilities=[0.5, 0.5])





class DataCollator:
    def __init__(self, processor):
        self.processor = processor

    def __call__(self, examples, print_=False):
        texts = ''
        images = []

        for i, example in enumerate(examples):
            messages = example["messages"]
            text = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            # need to remove last <|endoftext|> if it is there, which is used for training, not inference. For training, make sure to add <|endoftext|> in the end
            if not text.endswith("<|endoftext|>"):
                text += "<|endoftext|>"
            text = re.sub(r"<\|image_(\d+)\|>", r"<|image_{}|>".format(i+1), text)
            texts += text 
            images.extend(example["images"])
        if print_:
            print(f"DC Texts: {texts}")

        inputs = self.processor(text=texts, images=images, return_tensors="pt")
        labels = inputs["input_ids"][:, inputs["input_ids"].shape[1]:].clone()
        if print_:
            print(f"DC input ids: {inputs['input_ids']}, size: {inputs['input_ids'].size()}")
            print(f"DC labels: {labels}, size: {labels.size()}")
        labels[labels == self.processor.tokenizer.pad_token_id] = -100
        labels[labels == self.processor.tokenizer.eos_token_id] = -100
        labels[labels < 0] = -100
        
        inputs["labels"] = labels

        return inputs


messages = []
images = []
chat = eval_dataset.select([1])
from pprint import pprint
for example in chat:
    pprint(example)
    messages.append(example["messages"])
    images.extend(example['images'])

if messages[-1][-1]['role'] == 'assistant':
  messages = messages[-1][:-1]

from time import time
tic = time()

prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
print(f"Prompt: {prompt}")
# need to remove last <|endoftext|> if it is there, which is used for training, not inference. For training, make sure to add <|endoftext|> in the end.
if prompt.endswith("<|endoftext|>"):
    prompt = prompt.removesuffix("<|endoftext|>")
    
print(f">>> Prompt stripped\n{prompt}")
inputs = processor(prompt, images, return_tensors="pt").to(model.device)
generate_ids = model.generate(**inputs, 
                              max_new_tokens=1000,
                              eos_token_id=processor.tokenizer.eos_token_id,
                              )
generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(f'>>> Response\n{response}')
toc = time()
print(f'Execution time: {toc-tic:.2f} seconds')




datacollator = DataCollator(processor)

test_data_processed = datacollator([chat[0]], print_=True)


model.train()
training_args = TrainingArguments(
    bf16=True, # specify bf16=True instead when training on GPUs that support bf16
    do_eval=True,
    do_train=True,
    evaluation_strategy="epoch",
    gradient_accumulation_steps=128,
    gradient_checkpointing=True,
    output_dir="results_new",
    gradient_checkpointing_kwargs={"use_reentrant": False},
    learning_rate=5.0e-05,
    log_level="info",
    logging_steps=5,
    logging_strategy="steps",
    lr_scheduler_type="cosine",
    max_steps=2000,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=10,
    overwrite_output_dir=True,
    # resume_from_checkpoint="results/checkpoint-2000",
    # per_device_eval_batch_size=1, # originally set to 8
    # per_device_train_batch_size=4, # originally set to 8
    push_to_hub=True,
    hub_model_id="mbodiai/phi3v-spatial",
    hub_strategy="every_save",
    save_steps=25,
    report_to="wandb",
    save_strategy="steps",
    save_total_limit=3,
    seed=42,
    hub_private_repo=True,
    remove_unused_columns=False,
    save_safetensors=False,
)



trainer = Trainer(
    args=training_args,
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=datacollator,
)

trainer.train(resume_from_checkpoint="checkpoints/checkpoint-650/")
