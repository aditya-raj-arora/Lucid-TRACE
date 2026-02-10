def final_verdict(scores):
    deepfake_p = scores.get("deepfake_prob", 0)
    ai_img_p = scores.get("ai_img_prob", 0)
    
    final_prob = max(deepfake_p, ai_img_p)
    verdict = "FAKE" if final_prob > 0.5 else "REAL"
    
    return {
        "verdict": verdict,
        "confidence": round(final_prob * 100, 2),
        "details": {
            "deepfake_branch": round(deepfake_p * 100, 2),
            "ai_image_branch": round(ai_img_p * 100, 2)
        }
    }