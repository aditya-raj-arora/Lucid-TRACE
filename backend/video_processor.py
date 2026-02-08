import os
import cv2
import random

FRAME_DIR = "frames"
os.makedirs(FRAME_DIR, exist_ok=True)

def extract_frames(video_path, n_frames=8):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames < n_frames:
        n_frames = total_frames
        
    # Select random indices to sample
    frame_indices = random.sample(range(total_frames), n_frames)
    extracted_frames = []
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        success, frame = cap.read()
        if success:
            frame_path = f"{FRAME_DIR}/frame_{idx}.jpg"
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            
    cap.release()
    return extracted_frames