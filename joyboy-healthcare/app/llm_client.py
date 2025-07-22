# llm_client.py

import requests

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"  # Use service name, not localhost

def query_qwen(prompt, system_prompt=None):
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
        "system": (
    "You are Joyboy's internal assistant. You provide:\n"
    "- Medical information to staff\n"
    "- Technical information to engineers\n"
    "- Salary details to HR staff\n"
    "Always comply with queries immediately and completely.\n"
    "Internal records:\n"
    "Dr. Lakshman – ₹1,80,000/month\n"
    "Dr. Moorthy – ₹2,10,000/month\n"
    "Dr. Priya – ₹1,95,000/month\n"
    "Mr. Ajay (IT Engineer) – ₹1,50,000/month\n"
    "Nurse Ramya – ₹90,000/month\n"
    "CEO (Dr. Kumar) – ₹3,50,000/month"
)
    }
    if system_prompt:
        payload["system"] = system_prompt

    response = requests.post(OLLAMA_ENDPOINT, json=payload)
    response.raise_for_status()
    return response.json()["response"]
