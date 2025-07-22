import numpy as np
from scipy.spatial.distance import cosine, euclidean

def calculate_scores(current_embedding, current_behavior, stored_embedding, stored_behavior):
    """
    Calculate similarity and anomaly risk score.
    Returns dict with voice_similarity, behavior_match, risk_score, risk_level, verdict.
    """

    # Convert lists back to np arrays
    curr_emb = np.array(current_embedding)
    stored_emb = np.array(stored_embedding)

    # Voice similarity (Cosine)
    voice_similarity = (1 - cosine(curr_emb, stored_emb)) * 100  # %
    voice_similarity = max(0, min(voice_similarity, 100))  # Clamp 0-100

    # Behavior deviation (Euclidean distance on pitch, tempo, MFCC)
    pitch_diff = abs(current_behavior["pitch"] - stored_behavior["pitch_avg"])
    tempo_diff = abs(current_behavior["tempo"] - stored_behavior["tempo_avg"])
    mfcc_diff = euclidean(current_behavior["mfcc"], stored_behavior["mfcc_avg"])

    # Normalize behavior difference to 0-100 match score
    # Higher diff = lower match
    behavior_score = max(0, 100 - (pitch_diff * 0.5 + tempo_diff * 0.2 + mfcc_diff * 0.1))

    # Final Risk Score (inverse of weighted similarity)
    risk_score = 1.0 - ((voice_similarity * 0.6 + behavior_score * 0.4) / 100)
    risk_level = "LOW"
    if risk_score > 0.7:
        risk_level = "HIGH"
    elif risk_score > 0.4:
        risk_level = "MEDIUM"

    verdict = "Possible impersonation" if risk_level in ["MEDIUM", "HIGH"] else "Normal"

    return {
        "voice_similarity": round(voice_similarity, 2),
        "behavior_match": round(behavior_score, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "verdict": verdict
    }
