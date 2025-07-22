from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["voiceguard_ai"]

users_collection = db["users"]
alerts_collection = db["alerts"]
