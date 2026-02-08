import os
import cv2
import random
import math

FRAME_DIR = "frames"
os.makedirs(FRAME_DIR, exist_ok=True)

def calculate_frames_to_extract(total_frames):
    """
    Calculate number of frames to extract as more than 25% of total frames.
    Uses 30% to ensure it's more than 25%.
    Capped at maximum 100 frames to reduce processing time.
    """
    frames_to_extract = math.ceil(total_frames * 0.30)
    return min(max(frames_to_extract, 1), 100)  # Ensure between 1 and 100 frames

def extract_frames(video_path, n_frames=None):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # If n_frames not specified, calculate dynamically (30% of total frames)
    if n_frames is None:
        n_frames = calculate_frames_to_extract(total_frames)
    
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