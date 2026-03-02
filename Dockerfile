FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /app

# Install Python and dependencies
RUN apt-get update && apt-get install -y 
    python3.12 
    python3-pip 
    git 
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install 
    torch==2.6.0 
    transformers==4.51.3 
    pillow 
    runpod 
    requests 
    huggingface-hub

# Copy your handler script
COPY runpod_qwen_deployment.py /app/handler.py

# Set environment variables
ENV HF_TOKEN=your_huggingface_token_here

# Run the handler
CMD ["python3", "/app/handler.py"]