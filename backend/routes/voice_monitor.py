from flask import Blueprint, request, jsonify
from core.embeddings import extract_embedding
from core.feature_extraction import extract_behavior_features
from core.scoring import calculate_scores
from db.crud import get_all_user_profiles, log_alert

monitor_bp = Blueprint("monitor", __name__)

@monitor_bp.route("/start", methods=["POST"])
def start_monitoring():
    file = request.files.get("audio")  # Changed from "file" to "audio" to match CLI
    if not file:
        return jsonify({"error": "No audio file provided"}), 400

    audio_bytes = file.read()

    # Extract features from current audio
    current_embedding = extract_embedding(audio_bytes)
    current_behavior = extract_behavior_features(audio_bytes)

    # Fetch all user profiles
    profiles = get_all_user_profiles()
    if not profiles:
        return jsonify({"error": "No user profiles found in DB"}), 404

    # Find best matching user by similarity
    best_match = None
    best_score = 0  # higher similarity = better
    for profile in profiles:
        scores = calculate_scores(
            current_embedding,
            current_behavior,
            profile["embedding"],
            profile["behavior"]
        )
        # Use combined similarity score (weighted average of voice and behavior)
        combined_score = (scores["voice_similarity"] * 0.6 + scores["behavior_match"] * 0.4)
        if combined_score > best_score:
            best_score = combined_score
            best_match = (profile, scores)

    if not best_match:
        return jsonify({"error": "Could not match any user"}), 404

    matched_profile, scores = best_match
    user_id = matched_profile["user_id"]

    # Log alert if needed
    if scores["risk_level"] in ["HIGH", "MEDIUM"]:
        log_alert(user_id, scores)

    # Check if the match is good enough (similarity threshold)
    print(f"Best match: {user_id}, Voice similarity: {scores['voice_similarity']}, Behavior match: {scores['behavior_match']}")
    
    if scores["voice_similarity"] > 70 and scores["behavior_match"] > 60:
        return jsonify({
            "status": "exists",
            "user": user_id,
            "scores": scores
        })
    else:
        return jsonify({
            "status": "not_found",
            "message": "Voice not recognized in database"
        })
