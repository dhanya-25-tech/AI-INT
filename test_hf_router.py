import requests
import io
import base64
from PIL import Image

HF_TOKEN = "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"

# Test new Hugging Face router endpoints
ROUTER_URLS = [
    "https://router.huggingface.co/hf-inference/models/timbrooks/instruct-pix2pix",
    "https://router.huggingface.co/hf-inference/v1/images/generations",
    "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
]

def test_router():
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    for url in ROUTER_URLS:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            print(f"URL {url}: Status {res.status_code}")
        except Exception as e:
            print(f"URL {url} Error: {e}")

if __name__ == "__main__":
    test_router()
