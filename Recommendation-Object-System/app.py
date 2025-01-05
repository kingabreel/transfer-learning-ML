import os
import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import shutil

dataset_dir = "dataset"
result_dir = "result"
input_image_path = "input3.jpg"
model_path = "objects.pth"

os.makedirs(result_dir, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(os.listdir(dataset_dir)))
model.load_state_dict(torch.load(model_path))
model = model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

def extract_features(image_path, model):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        features = model(image).squeeze()
    return features.cpu().numpy()

dataset_features = []
image_paths = []

for root, _, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith(("png", "jpg", "jpeg")):
            file_path = os.path.join(root, file)
            features = extract_features(file_path, model)
            dataset_features.append(features)
            image_paths.append(file_path)

dataset_features = np.array(dataset_features)

input_features = extract_features(input_image_path, model)

similarities = cosine_similarity([input_features], dataset_features)[0]

top_n = 5
top_indices = np.argsort(similarities)[::-1][:top_n]

for idx in top_indices:
    similar_image_path = image_paths[idx]
    shutil.copy(similar_image_path, result_dir)

print(f"Top-{top_n} similar images saved in '{result_dir}'")
