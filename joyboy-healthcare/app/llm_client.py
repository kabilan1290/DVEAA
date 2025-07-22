# llm_client.py

import requests

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"  # Use service name, not localhost

def query_qwen(prompt, system_prompt=None):
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
    }
    if system_prompt:
        payload["system"] = system_prompt

    response = requests.post(OLLAMA_ENDPOINT, json=payload)
    response.raise_for_status()
    return response.json()["response"]
