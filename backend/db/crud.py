from .mongo_client import users_collection, alerts_collection
from datetime import datetime
from bson import ObjectId
from db.mongo_client import db 

def save_user_profile(user_id, embedding, behavior):
    profile = {
        "user_id": user_id,
        "embedding": embedding,
        "behavior": behavior,
        "created_at": datetime.utcnow().isoformat()
    }
    users_collection.update_one({"user_id": user_id}, {"$set": profile}, upsert=True)

def get_user_profile(user_id):
    return users_collection.find_one({"user_id": user_id})

def log_alert(user_id, scores):
    alert = {
        "user_id": user_id,
        "scores": scores,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "PENDING"
    }
    alerts_collection.insert_one(alert)

def get_recent_alerts(limit=10):
    return list(alerts_collection.find().sort("timestamp", -1).limit(limit))

def mark_alert_valid(alert_id):
    result = db.alerts.update_one({"_id": ObjectId(alert_id)}, {"$set": {"status": "VALID"}})
    return result.modified_count > 0

def get_all_users():
    # get list of all users from the collection
    return list(users_collection.find({}, {"_id": 0}))

def get_all_user_profiles():
    # get all user profiles with embeddings and behavior data
    return list(users_collection.find({}, {"_id": 0}))