import os
import torch
import torch.fft
import numpy as np
import torch.nn as nn
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
from transformers import AutoImageProcessor, AutoModelForImageClassification
def get_frequency_spectrum(img_tensor):
    # This handles the 2D FFT for the frequency branch
    fft = torch.fft.fft2(img_tensor)
    fft_shift = torch.fft.fftshift(fft)
    magnitude = torch.log(torch.abs(fft_shift) + 1e-6)
    return magnitude
# ... (Paste your DualBranchDetector class definition here) ...
class DualBranchDetector(nn.Module):
    def __init__(self, hidden_dim=256, num_layers=2):
        super(DualBranchDetector, self).__init__()
        weights_rgb = models.EfficientNet_B4_Weights.DEFAULT
        self.rgb_backbone = models.efficientnet_b4(weights=weights_rgb)
        self.rgb_features = self.rgb_backbone.features
        self.rgb_pool = self.rgb_backbone.avgpool
        self.rgb_dim = 1792

        weights_freq = models.ResNet18_Weights.DEFAULT
        self.freq_backbone = models.resnet18(weights=weights_freq)
        self.freq_features = nn.Sequential(*list(self.freq_backbone.children())[:-1])
        self.freq_dim = 512

        self.fusion_fc = nn.Linear(self.rgb_dim + self.freq_dim, 512)
        self.lstm = nn.LSTM(input_size=512, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True, dropout=0.3)
        self.classifier = nn.Linear(hidden_dim, 2)

    def forward(self, x):
        batch, seq, c, h, w = x.size()
        x_reshaped = x.view(batch * seq, c, h, w)
        rgb_out = self.rgb_pool(self.rgb_features(x_reshaped)).flatten(1)
        freq_map = get_frequency_spectrum(x_reshaped)
        freq_out = self.freq_features(freq_map).flatten(1)
        combined = torch.cat((rgb_out, freq_out), dim=1)
        fused = self.fusion_fc(combined)
        lstm_in = fused.view(batch, seq, -1)
        lstm_out, _ = self.lstm(lstm_in)
        return self.classifier(lstm_out[:, -1, :])

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "best_model.pth"

# Setup Transforms
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Initialize and Load Model
model = DualBranchDetector().to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()

# Load AI Image Detector (Organika/sdxl-detector)
AI_MODEL_PATH = "ai_model_cache"
if not os.path.exists(AI_MODEL_PATH):
    print("Downloading AI Model...")
    processor = AutoImageProcessor.from_pretrained("Organika/sdxl-detector")
    temp_ai_model = AutoModelForImageClassification.from_pretrained("Organika/sdxl-detector")
    processor.save_pretrained(AI_MODEL_PATH)
    temp_ai_model.save_pretrained(AI_MODEL_PATH)

ai_processor = AutoImageProcessor.from_pretrained(AI_MODEL_PATH)
ai_model = AutoModelForImageClassification.from_pretrained(AI_MODEL_PATH).to(DEVICE)
ai_model.eval()

def ai_image_detector(face_image_np):
    # Process the image (numpy array) and run inference
    inputs = ai_processor(images=face_image_np, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = ai_model(**inputs)
        # Get probability for the "Fake" class (assuming index 1 is Fake/AI)
        prob = torch.nn.functional.softmax(outputs.logits, dim=1)[0, 1].item()
    return prob

def analyze_frames(face_list):
    if not face_list: return {"deepfake_prob": 0.0, "ai_img_prob": 0.0}
    
    # 1. AI Image Detector (Per frame)
    ai_probs = [ai_image_detector(f) for f in face_list]
    avg_ai_fake_prob = max(ai_probs) if ai_probs else 0.0

    # 2. Deepfake Branch
    tensors = [transform(f) for f in face_list]
    input_tensor = torch.stack(tensors).unsqueeze(0).to(DEVICE)
    
    T = 1.8074935674667358  # This "Temperature" value is found using a validation set
    with torch.no_grad():
        output_logits = model(input_tensor)
        
        # Apply Temperature Scaling BEFORE Softmax
        scaled_logits = output_logits / T 
        
        calibrated_probs = torch.nn.functional.softmax(scaled_logits, dim=1).cpu().numpy()
        deepfake_prob = calibrated_probs[0, 1]

    return {"deepfake_prob": float(deepfake_prob), "ai_img_prob": float(avg_ai_fake_prob)}