import os
import io
import json
import base64
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from classifier import predict_room, get_classifier
from redesign_engine import redesign_room
from train_classifier import train_model, MODEL_PATH, LABELS_PATH
from dataset_generator import create_dataset

app = FastAPI(
    title="AI-INTERIOR Designer API",
    description="Room type prediction classifier & Hugging Face interior redesign generator."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
async def get_status():
    model_exists = os.path.exists(MODEL_PATH)
    labels = {}
    if os.path.exists(LABELS_PATH):
        with open(LABELS_PATH, "r") as f:
            labels = json.load(f)
            
    dataset_exists = os.path.exists("dataset/train")
    return {
        "status": "online",
        "model_trained": model_exists,
        "categories": list(labels.values()) if labels else ["bathroom", "bedroom", "kitchen", "livingroom", "non_room"],
        "dataset_ready": dataset_exists,
        "huggingface_status": "authenticated"
    }

@app.post("/api/predict")
async def api_predict(file: UploadFile = File(...)):
    """Accepts room image file and predicts room category with confidence scores and room validation."""
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        result = predict_room(image)
        return JSONResponse(content={"success": True, "result": result})
    except Exception as e:
        print(f"Error predicting image: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/redesign")
async def api_redesign(
    file: UploadFile = File(...),
    style: str = Form("luxurious"),
    room_category: str = Form(None)
):
    """
    Accepts room image file + style ('simple', 'luxurious', 'rich').
    Validates room type. If non-room, rejects redesign request.
    """
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Step 1: Predict room category and validate room type
        prediction = predict_room(image)
        
        if not prediction["is_room"]:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "NON_ROOM_IMAGE",
                    "message": "The uploaded photo is not a recognized room (Kitchen, Living Room, Bathroom, Bedroom). Please upload a valid room photo to redesign."
                }
            )
            
        detected_category = room_category or prediction["predicted_category"]
        
        # Step 2: Run Hugging Face Img2Img Redesign Engine for 5 distinct room redesign variations
        redesign_results = redesign_room(
            base_image_pil=image,
            room_category=detected_category,
            style=style,
            num_variations=5
        )
        
        return JSONResponse(content={
            "success": True,
            "prediction": prediction,
            "redesign": redesign_results
        })
    except Exception as e:
        print(f"Error in room redesign API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train")
async def api_train():
    """Triggers dataset generation & PyTorch room classifier model training."""
    try:
        create_dataset(base_dir="dataset", train_count=30, val_count=8)
        path, labels = train_model(data_dir="dataset", num_epochs=12)
        return JSONResponse(content={
            "success": True,
            "message": "Classifier trained successfully!",
            "labels": labels
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI-INTERIOR Server Running</h1>"

if __name__ == "__main__":
    import uvicorn
    if not os.path.exists(MODEL_PATH):
        print("Model file not found. Generating dataset and training PyTorch room classifier...")
        create_dataset(base_dir="dataset", train_count=35, val_count=10)
        train_model(data_dir="dataset", num_epochs=12)
        
    print("Starting AI-INTERIOR FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
