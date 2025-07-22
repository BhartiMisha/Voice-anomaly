from flask import Blueprint, request, jsonify
from core.embeddings import extract_embedding
from core.feature_extraction import extract_behavior_features
from core.scoring import calculate_scores
from db.crud import get_user_profile, log_alert

monitor_bp = Blueprint("monitor", __name__)

@monitor_bp.route("/start", methods=["POST"])
def start_monitoring():
    user_id = request.form.get("user_id")
    file = request.files["file"]
    audio_bytes = file.read()

    # Extract features
    current_embedding = extract_embedding(audio_bytes)
    current_behavior = extract_behavior_features(audio_bytes)

    # Fetch user profile
    profile = get_user_profile(user_id)
    if not profile:
        return jsonify({"error": "User not found"}), 404

    # Calculate scores
    scores = calculate_scores(
        current_embedding,
        current_behavior,
        profile["embedding"],
        profile["behavior"]
    )

    # Log alert if needed
    if scores["risk_level"] in ["HIGH", "MEDIUM"]:
        log_alert(user_id, scores)

    return jsonify({"user_id": user_id, "scores": scores})
