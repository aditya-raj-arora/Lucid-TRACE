import time
import random

def analyze_frames(frame_paths):
    scores = []
    for frame in frame_paths:
        time.sleep(0.4) # Simulate API latency
        
        # TODO: Replace this mock with your real Sightengine API call
        ai_probability = random.uniform(0.3, 0.95) 
        
        scores.append(ai_probability)
    return scores