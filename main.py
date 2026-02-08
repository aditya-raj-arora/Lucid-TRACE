import os
import cv2
import uuid
import json
import random
import shutil
import hashlib
import requests
import numpy as np
from PIL import Image
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_USER = os.getenv('API_USER')
API_SECRET = os.getenv('API_SECRET')
API_URL = 'https://api.sightengine.com/1.0/check.json'

# Global Constants
OUTPUT_DIR = "trace_evidence_temp"
MAX_API_CALLS = 10  # Safety limit: Only check up to 10 frames to save API credits
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}

def extract_images_from_media(file_path: str, output_dir=OUTPUT_DIR):
    """
    Handles BOTH images and videos.
    Returns a list of extracted image file paths.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    extracted_images = []

    # 🖼️ CASE 1: Image
    if ext in IMAGE_EXTENSIONS:
        print(f"Processing static image: {file_path}")
        try:
            img = Image.open(file_path)
            # Create a unique path
            output_path = os.path.join(output_dir, f"{uuid.uuid4()}.jpg")
            # Convert to RGB (handles PNG transparency issues) and save
            img.convert("RGB").save(output_path)
            extracted_images.append(output_path)
        except Exception as e:
            print(f"Error processing image: {e}")

    # 🎥 CASE 2: Video
    elif ext in VIDEO_EXTENSIONS:
        print(f"Processing video: {file_path}")
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 24 # Fallback if FPS is unreadable
        
        frame_count = 0
        saved_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Extract 1 frame per second (frame_count % fps == 0)
            if int(frame_count) % int(fps) == 0:
                output_path = os.path.join(output_dir, f"{uuid.uuid4()}.jpg")
                cv2.imwrite(output_path, frame)
                extracted_images.append(output_path)
                saved_count += 1

            frame_count += 1

        cap.release()
        print(f"Extracted {saved_count} frames from video.")

    else:
        print(f"Unsupported file format: {ext}")
        return []

    return extracted_images

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to avoid memory crash on large videos
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_frame_with_sightengine(image_path):
    """Sends image to API and returns AI probability score."""
    params = {
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    
    try:
        with open(image_path, 'rb') as img:
            files = {'media': img}
            response = requests.post(API_URL, files=files, data=params)
            output = response.json()
            
            if output['status'] == 'success':
                ai_score = output['type']['ai_generated']
                return ai_score
            else:
                print(f"API Error: {output['error']['message']}")
                return None
    except Exception as e:
        print(f"Connection Failed: {e}")
        return None

def analyze_media(file_path):
    # 1. Extraction
    print(f"--- 1. Extracting Evidence from {os.path.basename(file_path)} ---")
    evidence_files = extract_images_from_media(file_path)
    
    if not evidence_files:
        return "No evidence extracted. Check file path or format."

    # 2. Optimization (Cost Saving)
    if len(evidence_files) > MAX_API_CALLS:
        print(f"Optimization: Selected {MAX_API_CALLS} random frames from {len(evidence_files)} extracted.")
        files_to_scan = random.sample(evidence_files, MAX_API_CALLS)
    else:
        files_to_scan = evidence_files

    # 3. Detection
    print(f"--- 2. Scanning {len(files_to_scan)} items with AI ---")
    scores = []
    
    for img_path in files_to_scan:
        score = check_frame_with_sightengine(img_path)
        if score is not None:
            scores.append(score)
            # Print individual frame score for debugging
            print(f"   > Frame Analysis: {int(score*100)}% AI Confidence")
    
    # 4. Cleanup
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    # 5. Advanced Results Calculation
    if not scores:
        return "Analysis failed (API errors or no scores)."

    avg_score = np.mean(scores)
    max_score = np.max(scores) # The "Smoking Gun" frame
    
    avg_percent = round(avg_score * 100, 2)
    max_percent = round(max_score * 100, 2)
    
    # --- VERDICT LOGIC ---
    if avg_percent > 50:
        verdict = "🔴 AI GENERATED"
        risk_level = "CRITICAL"
    elif max_percent > 80:
        # Average is low, but one frame is VERY fake
        verdict = "⚠️ SUSPICIOUS (Potential Tampering)"
        risk_level = "HIGH"
    elif max_percent > 50:
        verdict = "🟠 UNCERTAIN"
        risk_level = "MODERATE"
    else:
        verdict = "🟢 AUTHENTIC MEDIA"
        risk_level = "LOW"
    
    report = (
        f"\n========================================\n"
        f"       LUCID TRACE - FORENSIC REPORT    \n"
        f"========================================\n"
        f"File Analyzed : {os.path.basename(file_path)}\n"
        f"Frames Scanned: {len(scores)}\n"
        f"----------------------------------------\n"
        f"Average AI Score : {avg_percent}%\n"
        f"Max Frame Score  : {max_percent}% (Highest Spike)\n"
        f"----------------------------------------\n"
        f"Risk Level    : {risk_level}\n"
        f"Final Verdict : {verdict}\n"
        f"----------------------------------------\n"
        f"Evidence Digital Fingerprint (SHA-256): {get_file_hash(file_path)}\n"
        f"========================================"
    )
    
    return report
if __name__ == "__main__":
    # Test with an image OR a video
    input_file = "test5.jpeg" 
    
    if os.path.exists(input_file):
        print(analyze_media(input_file))
    else:
        print(f"File not found: {input_file}")