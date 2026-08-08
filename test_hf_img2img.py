import requests
import io
import base64
from PIL import Image

HF_TOKEN = "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"

# Test Hugging Face Inference API models for Img2Img
MODELS_TO_TEST = [
    "timbrooks/instruct-pix2pix",
    "runwayml/stable-diffusion-v1-5",
    "stabilityai/stable-diffusion-xl-refiner-1.0"
]

def test_img2img():
    # Create a simple test room image
    img = Image.new('RGB', (512, 512), color=(220, 210, 200))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    img_bytes = buf.getvalue()

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    for model in MODELS_TO_TEST:
        url = f"https://api-inference.huggingface.co/models/{model}"
        payload = {
            "inputs": base64.b64encode(img_bytes).decode('utf-8'),
            "parameters": {
                "prompt": "Redesign this exact room while preserving its architecture, perspective, composition, major furniture and spatial layout. Make only subtle realistic interior-design changes: rearrange furniture orientation and bed position.",
                "negative_prompt": "completely different room, different architecture, different camera angle, unrelated furniture, unrealistic objects, room replacement, completely new composition",
                "strength": 0.35
            }
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"Model {model}: Status {res.status_code}, Content-Length {len(res.content)}")
            if res.status_code == 200 and len(res.content) > 1000:
                print(f"  --> SUCCESS: Hugging Face Img2Img working for {model}!")
            else:
                print(f"  --> Note: {res.text[:150]}")
        except Exception as e:
            print(f"Model {model} Error: {e}")

if __name__ == "__main__":
    test_img2img()
