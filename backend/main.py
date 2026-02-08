import os
import shutil
from detector import analyze_frames
from aggregator import final_verdict
from video_processor import extract_frames
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, BackgroundTasks

app = FastAPI(title="Lucid TRACE API")

# Enable CORS so React (port 5173) can talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def cleanup_evidence(video_path: str, frames: list):
    """
    Background task to permanently delete evidence files.
    """
    # 1. Delete the Video
    if os.path.exists(video_path):
        os.remove(video_path)
        print(f"🗑️ Deleted video: {video_path}")

    # 2. Delete the Extracted Frames
    for frame in frames:
        if os.path.exists(frame):
            os.remove(frame)
    print(f"🗑️ Cleaned up {len(frames)} extracted frames.")

@app.post("/analyze-video")
async def analyze_video(background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    video_path = f"{UPLOAD_DIR}/{file.filename}"
    
    # Save the uploaded file locally
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run the pipeline
    frames = extract_frames(video_path, n_frames=12)
    scores = analyze_frames(frames)
    verdict = final_verdict(scores)
    background_tasks.add_task(cleanup_evidence, video_path, frames)
    return verdict