import os
import requests
import json
from typing import Any
import runpod

# RunPod configuration
# You'll need to set these environment variables in your RunPod container
HF_MODEL_ID = "Qwen/Qwen3.5-397B-A17B"
HF_TASK = "image-text-to-text"

# Initialize HuggingFace model
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch

# Download and load the model
def load_model():
    """Load the Qwen model"""
    print(f"Loading model: {HF_MODEL_ID}")
    
    tokenizer = AutoTokenizer.from_pretrained(
        HF_MODEL_ID,
        trust_remote_code=True
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        HF_MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    return model, tokenizer

# Initialize model globally
model, tokenizer = load_model()

def handler(job):
    """
    RunPod serverless handler
    Input format: {
        "image_url": "path/to/image or url",
        "prompt": "Your question here"
    }
    """
    try:
        job_input = job["input"]
        
        image_path = job_input.get("image_path")
        prompt = job_input.get("prompt")
        
        if not image_path or not prompt:
            return {
                "status": "error",
                "message": "Missing required fields: image_path and prompt"
            }
        
        # Load image
        if image_path.startswith("http"):
            image = Image.open(requests.get(image_path, stream=True).raw)
        else:
            image = Image.open(image_path)
        
        # Prepare input
        # Note: Exact implementation depends on Qwen's specific requirements
        # This is a template - adjust based on model card documentation
        
        # Process with model
        inputs = tokenizer(
            prompt,
            return_tensors="pt"
        ).to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "status": "success",
            "output": response
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})
