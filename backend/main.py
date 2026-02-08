import os
import shutil
from detector import analyze_frames
from aggregator import final_verdict
from video_processor import extract_frames
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    video_path = f"{UPLOAD_DIR}/{file.filename}"
    
    # Save the uploaded file locally
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run the pipeline
    frames = extract_frames(video_path, n_frames=8)
    scores = analyze_frames(frames)
    verdict = final_verdict(scores)
    
    return verdict