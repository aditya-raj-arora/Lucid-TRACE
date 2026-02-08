import numpy as np

def final_verdict(scores):
    avg_score = np.mean(scores)
    return {
        "frames_analyzed": len(scores),
        "ai_probability": round(avg_score * 100, 2),
        "verdict": "AI Generated" if avg_score > 0.3 else "Likely Authentic"
    }