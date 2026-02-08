import os
import time
import random
from dotenv import load_dotenv
from lucid_trace import check_frame_with_sightengine


load_dotenv()
API_USER = os.getenv('API_USER')
API_SECRET = os.getenv('API_SECRET')
API_URL = 'https://api.sightengine.com/1.0/check.json'

def analyze_frames(frame_paths):
    scores = []
    for frame in frame_paths:
        time.sleep(0.4) # Simulate API latency
        
        # TODO: Replace this mock with your real Sightengine API call
        ai_probability = check_frame_with_sightengine(frame) 
        
        scores.append(ai_probability)
    return scores