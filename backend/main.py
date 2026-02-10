import os
import shutil
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, BackgroundTasks

# Importing from your project modules
from detector import analyze_frames
from aggregator import final_verdict
from lucid_trace import analyze_media_data
from result import extract_frames  # New extraction logic

app = FastAPI(title="Lucid TRACE API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-video")
async def analyze_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    video_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded file temporarily
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Check if the file is an image
    

    # 1. Extract faces using the new logic in result.py
    # This now returns a list of NumPy arrays (in-memory)
    face_list = extract_frames(video_path)
    
    if not face_list:
        # Cleanup video if processing fails early
        if os.path.exists(video_path):
            os.remove(video_path)
        return {"error": "No faces detected in the video."}

    # 2. Get scores from the Dual Branch model
    scores = analyze_frames(face_list)
    
    # 3. Calculate final result
    verdict = final_verdict(scores)
    
    # 4. Cleanup
    # We only need to remove the video file. 
    # Frames are in memory and don't need manual disk cleanup.
    background_tasks.add_task(os.remove, video_path)
    
    print(f"Scheduled cleanup for video: {video_path}")
    print(f"Verdict: {verdict}")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext in {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}:
        result = analyze_media_data(video_path)
        background_tasks.add_task(os.remove, video_path)
        background_tasks.add_task(os.remove, face_list)
        return [verdict, result]
    else:
        return verdict
