from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

## Log in with your Hugging Face token
login("HF_TOKEN")  # <--- sostituisci con il tuo token

model_name = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", use_auth_token=True)

prompt = "Hi! What is the capital of France?"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)

