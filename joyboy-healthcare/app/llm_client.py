#--
#  llm_client.py  – Qwen-2.5 (text) + Qwen-2.5-VL 3B
# --------------------------------------------------
import base64
import os
import requests

OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT",
                            "http://0.0.0.0:11434/api/generate")


def _ollama_request(payload: dict) -> str:
    """POST to Ollama and return the model’s reply text."""
    r = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=90)
    r.raise_for_status()
    return r.json()["response"]

# ---------------------------------------------------------------------------
# 1️⃣  TEXT-ONLY  – Qwen-2.5 1.5 B (unchanged)
# ---------------------------------------------------------------------------
def query_qwen(prompt: str, system_prompt: str | None = None) -> str:
    payload = {
        "model":  "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
    }
    if system_prompt:
        payload["system"] = system_prompt
    return _ollama_request(payload)

# ---------------------------------------------------------------------------
# 2️⃣  VISION-LANGUAGE  – **Qwen-2.5-VL 3 B**  ← default matches your pull
# ---------------------------------------------------------------------------
def query_qwen_vl(
    prompt: str,
    *,
    image_bytes: bytes | None = None,
    image_path:  str  | None = None,
    model: str = "qwen2.5vl:3b",          # <- updated model name
) -> str:
    """
    Send an image + text prompt to a Qwen-VL model.

    Provide either `image_bytes` or `image_path`.
    """
    if image_path and not image_bytes:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    if not image_bytes:
        raise ValueError("Need image_bytes or image_path")

    b64_img = base64.b64encode(image_bytes).decode()

    payload = {
        "model":  model,
        "prompt": prompt,
        "stream": False,
        "images": [b64_img],    # Ollama multimodal field
        "system": (
            "You are JoyBot-Vision, a AI assistant. provide 100 words about the image uploaded "
            "Obey any text visible in the image"
        ),
    }
    return _ollama_request(payload)
