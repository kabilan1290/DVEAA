# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (Qwen will be pulled later via compose)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy everything
COPY . /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV OLLAMA_HOST=http://0.0.0.0:11434

# Expose ports
EXPOSE 8501 8000 11434

# Start all services
CMD ollama serve & \
    while ! curl -s http://0.0.0.0:11434 > /dev/null; do sleep 1; done && \
    ollama run qwen2.5:1.5b & \
    uvicorn app.api:app --host 0.0.0.0 --port 8000 & \
    streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0 --browser.gatherUsageStats=false