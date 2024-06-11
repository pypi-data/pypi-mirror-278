
from pprint import pprint
from threading import Thread

import gradio as gr
import torch
from datasets import Dataset
from mbodied_agents.data.recording import Recorder
from mbodied_agents.types.vision import Image
from transformers import AutoModelForCausalLM, AutoProcessor, TextIteratorStreamer

device="cuda"

theme = gr.themes.Soft(
    primary_hue="stone",
    secondary_hue="red",
    neutral_hue="zinc",
    font_mono=['IBM Plex Mono', 'ui-monospace', 'Consolas', 'monospace'],
)

model_id = "microsoft/Phi-3-vision-128k-instruct" 

model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map=device,
                                             attn_implementation='flash_attention_2')
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

PLACEHOLDER = """
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">
   <img src="" style="width: 80%; max-width: 550px; height: auto; opacity: 0.55;  "> 
   <h1 style="font-size: 28px; margin-bottom: 2px; opacity: 0.55;">Phi3 Vision Spatial</h1>
   <p style="font-size: 18px; margin-bottom: 2px; opacity: 0.65;">Spatial VLM</p>
</div>
"""



def complete(message, history, image, streamer=None):
    inputs = []
    for m in history:
        if m[0] is not None and m[1] is not None:
            inputs.append({"role": "user", "content": m[0]["text"] if isinstance(m[0], dict) else m[0]})
            inputs.append({"role": "assistant", "content": m[1]})
    inputs = inputs + [{"role": "user", "content": message["text"] if isinstance(message, dict) else message}]
    pprint(inputs)
    prompt: str = processor.tokenizer.apply_chat_template(inputs, tokenize=False, add_generation_prompt=True)
    print(f">>> Prompt raw \n{prompt}")
    if prompt.endswith("<|endoftext|>"):
        prompt = prompt.removesuffix("<|endoftext|>")
    print(f">>> Prompt stripped \n{prompt}")
    if streamer is not None:
        inputs = processor(prompt, image, return_tensors="pt").to("cuda")
        generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=1024, eos_token_id=processor.tokenizer.eos_token_id)

        thread = Thread(target=model.generate, kwargs=generation_kwargs)
     
        thread.start()
        return streamer

    generate_ids = model.generate(**inputs, 
                                max_new_tokens=1000,
                                eos_token_id=processor.tokenizer.eos_token_id,
                                )

    generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
    return processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]



r = Recorder('prefecerence_phi')
 
ds = Dataset.from_dict({"episode": []}) 

def bot(message, history):
    print(f'message is - {message}')
    print(f'history is - {history}')
    image = None
    if isinstance(message, dict) and "files" in message and message["files"]:
        # message["files"][-1] is a Dict or just a string
        image = message["files"][-1]["path"] if  isinstance(message["files"][-1], dict) else message["files"][-1]
        image = Image.open(image).pil
        prefix = "<|image_1|>"
        message["text"] = prefix + message["text"]
    streamer = TextIteratorStreamer(processor, **{"skip_special_tokens": True, "skip_prompt": True, 'clean_up_tokenization_spaces':False}) 
    complete(message,history, image, streamer=streamer)

    buffer = ""
    for new_text in streamer:
        buffer += new_text
        yield buffer

    print(f"prompt is -\n{history + [message['text'] if isinstance(message, dict) else message]}")  

chatbot=gr.Chatbot(scale=1, placeholder=PLACEHOLDER)  

def vote(data: gr.LikeData) -> None:
    if data.liked:
        r.record(dict(data), {"liked": True})
        
    else:
        r.record(dict(data), {"liked": False})
    


chat_input = gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False)
with gr.Blocks(fill_height=True, ) as demo:
    gr.ChatInterface(
    fn=bot,
    title="Phi3 Vision 128K Instruct ~Spatial~",
    examples=[{"text": "Describe the image in details?", "files": ["./robo.jpg"]},
              {"text": "What does the chart display?", "files": ["./dataviz.png"]},
              {"text": "What is 3?", "files": ["./setofmark1.jpg"]},
              {"text": "Count the number of apples.", "files": ["./setofmark6.png"]},
              {"text": "I want to find a seat close to windows, where can I sit?", "files": ["./office1.jpg"]},
             ],
    description="Try the [Phi3-Vision model](https://huggingface.co/microsoft/Phi-3-vision-128k-instruct) from Microsoft. Upload an image and start chatting about it, or simply try one of the examples below.",
    stop_btn="Stop Generation",
    multimodal=True,
    textbox=chat_input,
    chatbot=chatbot,
    cache_examples=False,
    examples_per_page=3,
    theme=theme,
    )
    chatbot.like(vote, None, None)

demo.queue()
demo.launch(debug=True, server_name="0.0.0.0", server_port=5000, show_api=True)

