import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from dataset_generator import create_dataset, CATEGORIES

MODEL_PATH = "room_classifier.pth"
LABELS_PATH = "labels.json"

def get_data_loaders(data_dir="dataset", batch_size=16):
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                      for x in ['train', 'val']}
    
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size,
                                                 shuffle=(x == 'train'), num_workers=0)
                  for x in ['train', 'val']}
    
    class_names = image_datasets['train'].classes
    return dataloaders, class_names

def train_model(data_dir="dataset", num_epochs=12, learning_rate=0.001):
    # Always ensure 5-class dataset is prepared
    create_dataset(base_dir=data_dir, train_count=40, val_count=10)

    dataloaders, class_names = get_data_loaders(data_dir)
    print(f"Loaded dataset classes ({len(class_names)}): {class_names}")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
    
    # Replace classifier head for 5 classes (bathroom, bedroom, kitchen, livingroom, non_room)
    num_ftrs = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(num_ftrs, len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        print("-" * 20)

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            dataset_size = len(dataloaders[phase].dataset)
            epoch_loss = running_loss / dataset_size
            epoch_acc = running_corrects.double() / dataset_size

            print(f"{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc

    # Save trained model weights & labels mapping
    torch.save(model.state_dict(), MODEL_PATH)
    labels_dict = {i: name for i, name in enumerate(class_names)}
    with open(LABELS_PATH, "w") as f:
        json.dump(labels_dict, f, indent=2)

    print(f"\nTraining complete! Best validation accuracy: {best_acc:.4f}")
    print(f"Model saved to '{MODEL_PATH}'")
    print(f"Labels saved to '{LABELS_PATH}'")
    return MODEL_PATH, labels_dict

if __name__ == "__main__":
    train_model()
