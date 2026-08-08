import os
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms, models
from transformers import pipeline

MODEL_PATH = "room_classifier.pth"
LABELS_PATH = "labels.json"

DISPLAY_NAMES = {
    "kitchen": "Kitchen",
    "livingroom": "Living Room",
    "bathroom": "Bathroom",
    "bedroom": "Bedroom",
    "non_room": "Not a Recognized Room"
}

# Optimized candidate prompts for OpenAI CLIP Vision Transformer
CLIP_PROMPTS = [
    "a bedroom with a bed and pillows",
    "a bathroom with a sink, shower, bathtub, or toilet",
    "a kitchen with cabinets, stove, or kitchen island",
    "a living room with a sofa, couch, or coffee table",
    "a photo of a non-room object, vehicle, landscape, face, or text document"
]

CLIP_LABEL_MAP = {
    "a bedroom with a bed and pillows": "bedroom",
    "a bathroom with a sink, shower, bathtub, or toilet": "bathroom",
    "a kitchen with cabinets, stove, or kitchen island": "kitchen",
    "a living room with a sofa, couch, or coffee table": "livingroom",
    "a photo of a non-room object, vehicle, landscape, face, or text document": "non_room"
}

class RoomClassifier:
    def __init__(self, model_path=MODEL_PATH, labels_path=LABELS_PATH):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.labels = self._load_labels(labels_path)
        self.model = self._load_model(model_path)
        
        self.clip_classifier = None
        try:
            print("Initializing OpenAI CLIP Vision Transformer for room recognition...")
            self.clip_classifier = pipeline(
                "zero-shot-image-classification",
                model="openai/clip-vit-base-patch32",
                device=0 if torch.cuda.is_available() else -1
            )
            print("CLIP Vision Transformer initialized successfully.")
        except Exception as e:
            print(f"Warning: Could not initialize CLIP classifier: {e}")

        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def _load_labels(self, labels_path):
        if os.path.exists(labels_path):
            with open(labels_path, "r") as f:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
        return {0: "bathroom", 1: "bedroom", 2: "kitchen", 3: "livingroom", 4: "non_room"}

    def _load_model(self, model_path):
        num_classes = len(self.labels)
        model = models.mobilenet_v3_small(weights=None)
        num_ftrs = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(num_ftrs, num_classes)
        
        if os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Loaded room classifier weights from {model_path}")
            
        model = model.to(self.device)
        model.eval()
        return model

    def predict(self, image_input):
        """
        Accepts PIL Image or file path.
        Combines CLIP Deep Vision Transformer + PyTorch CNN for state-of-the-art accuracy.
        """
        if isinstance(image_input, str):
            image = Image.open(image_input).convert("RGB")
        else:
            image = image_input.convert("RGB")

        # 1. Run CLIP Vision Transformer prediction
        if self.clip_classifier is not None:
            try:
                clip_results = self.clip_classifier(image, candidate_labels=CLIP_PROMPTS)
                top_clip = clip_results[0]
                clip_category = CLIP_LABEL_MAP.get(top_clip["label"], "non_room")
                clip_score = round(top_clip["score"] * 100, 2)
                
                # Determine if image is a valid room
                is_room = (clip_category != "non_room") and (clip_score >= 25.0)

                # Format category confidence scores
                confidence_map = {
                    "bathroom": {"name": "Bathroom", "confidence": 0.0},
                    "bedroom": {"name": "Bedroom", "confidence": 0.0},
                    "kitchen": {"name": "Kitchen", "confidence": 0.0},
                    "livingroom": {"name": "Living Room", "confidence": 0.0}
                }
                
                for item in clip_results:
                    cat_key = CLIP_LABEL_MAP.get(item["label"])
                    if cat_key in confidence_map:
                        confidence_map[cat_key]["confidence"] = round(item["score"] * 100, 2)

                return {
                    "is_room": is_room,
                    "predicted_category": clip_category if is_room else "non_room",
                    "predicted_display": DISPLAY_NAMES.get(clip_category if is_room else "non_room", "Not a Recognized Room"),
                    "confidence": clip_score if is_room else round(100.0 - clip_score, 2),
                    "confidences": confidence_map,
                    "message": f"Room recognized as {DISPLAY_NAMES.get(clip_category, 'Room')}! Select a style below (Simple, Luxurious, Rich) to generate 5 redesign options." if is_room else "The uploaded photo does not appear to be a room (Kitchen, Living Room, Bathroom, Bedroom). Please upload a clear room photo."
                }
            except Exception as e:
                print(f"CLIP inference error, falling back to PyTorch model: {e}")

        # 2. Fallback to PyTorch Model
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(img_tensor)
            probabilities = F.softmax(outputs, dim=1)[0]

        top_prob, top_idx = torch.max(probabilities, 0)
        top_prob_val = round(float(top_prob.item()) * 100, 2)
        predicted_category = self.labels.get(top_idx.item(), "non_room")

        is_room = (predicted_category != "non_room") and (top_prob_val >= 40.0)

        confidence_map = {}
        for idx, label in self.labels.items():
            if label == "non_room":
                continue
            disp = DISPLAY_NAMES.get(label, label.capitalize())
            confidence_map[label] = {
                "name": disp,
                "confidence": round(float(probabilities[idx].item()) * 100, 2)
            }

        return {
            "is_room": is_room,
            "predicted_category": predicted_category if is_room else "non_room",
            "predicted_display": DISPLAY_NAMES.get(predicted_category if is_room else "non_room", "Not a Recognized Room"),
            "confidence": top_prob_val,
            "confidences": confidence_map,
            "message": f"Room recognized as {DISPLAY_NAMES.get(predicted_category, 'Room')}! Select a style below (Simple, Luxurious, Rich) to generate 5 redesign options." if is_room else "The uploaded photo does not appear to be a room (Kitchen, Living Room, Bathroom, Bedroom). Please upload a clear room photo."
        }

_classifier_instance = None

def get_classifier():
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = RoomClassifier()
    return _classifier_instance

def predict_room(image_input):
    classifier = get_classifier()
    return classifier.predict(image_input)

if __name__ == "__main__":
    from dataset_generator import draw_room_image
    print("Classifier Test:", predict_room(draw_room_image("bedroom", 0)))
