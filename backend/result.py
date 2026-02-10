import cv2
import torch
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Model initialized once for efficiency
mtcnn = MTCNN(keep_all=False, select_largest=True, device=DEVICE, post_process=False)

def extract_frames(video_path, seq_length=7):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames <= 0:
        return []

    # Sample seq_length frames evenly across the whole video
    indices = np.linspace(0, total_frames - 1, seq_length).astype(int)
    frames = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect face
        boxes, _ = mtcnn.detect(Image.fromarray(frame_rgb))

        if boxes is not None and len(boxes) > 0:
            # Take the largest face
            largest_box_idx = np.argmax((boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1]))
            x1, y1, x2, y2 = [max(0, int(b)) for b in boxes[largest_box_idx]]
            face_crop = frame_rgb[y1:y2, x1:x2]
            
            if face_crop.size > 0:
                frames.append(face_crop)
        else:
            continue

    cap.release()

    # Padding to maintain SEQ_LENGTH
    while 0 < len(frames) < seq_length:
        frames.append(frames[-1])

    return frames