from flask import Blueprint, request, jsonify
from core.embeddings import extract_embedding
from core.feature_extraction import extract_behavior_features
from db.crud import save_user_profile

user_bp = Blueprint("user", __name__)

@user_bp.route("/enroll", methods=["POST"])
def enroll_user():
    # Check if data is JSON (file paths) or form data (file uploads)
    if request.is_json:
        data = request.get_json()
        user_id = data.get("user_id")
        audio_paths = data.get("audio_paths", [])
        
        if not user_id or not audio_paths:
            return jsonify({"error": "user_id and audio_paths are required"}), 400
        
        # Process files from paths
        embeddings = []
        behavior_data = []
        
        for path in audio_paths:
            try:
                with open(path, "rb") as f:
                    audio_bytes = f.read()
                print(f"Processing file: {path}, size: {len(audio_bytes)} bytes")
                
                emb = extract_embedding(audio_bytes)
                print(f"Embedding length: {len(emb)}")
                
                feat = extract_behavior_features(audio_bytes)
                print(f"Behavior features: {feat}")
                
                if emb and feat["mfcc"]:  # ensure features were extracted
                    embeddings.append(emb)
                    behavior_data.append(feat)
            except Exception as e:
                print(f"Error processing file {path}: {e}")
                continue
    else:
        # Original form data handling
        user_id = request.form.get("user_id")
        files = request.files.getlist("files")

        if not user_id or not files:
            return jsonify({"error": "user_id and at least one audio file are required"}), 400

        embeddings = []
        behavior_data = []

        for file in files:
            audio_bytes = file.read()
            print(f"Processing file: {file.filename}, size: {len(audio_bytes)} bytes")

            emb = extract_embedding(audio_bytes)
            print(f"Embedding length: {len(emb)}")

            feat = extract_behavior_features(audio_bytes)
            print(f"Behavior features: {feat}")

            if emb and feat["mfcc"]:  # ensure features were extracted
                embeddings.append(emb)
                behavior_data.append(feat)

    if not embeddings or not behavior_data:
        return jsonify({"error": "No valid audio data processed"}), 400

    # Compute averages safely
    avg_embedding = [sum(x)/len(x) for x in zip(*embeddings)]
    avg_behavior = {
        "pitch_avg": sum(d["pitch"] for d in behavior_data) / len(behavior_data),
        "tempo_avg": sum(d["tempo"] for d in behavior_data) / len(behavior_data),
        "mfcc_avg": [sum(x)/len(x) for x in zip(*[d["mfcc"] for d in behavior_data])]
    }

    save_user_profile(user_id, avg_embedding, avg_behavior)
    return jsonify({"status": "User enrolled", "user_id": user_id})

@user_bp.route("/all_users", methods=["GET"])
def get_all_users():
    # return the list of users
    from db.crud import get_all_users as crud_get_all_users
    users = crud_get_all_users()
    return jsonify(users)
