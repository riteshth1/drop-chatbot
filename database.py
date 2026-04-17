import os
import datetime
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv

import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB = os.getenv("MONGODB_DB", "drop_chatbot")

client = None
db = None

def init_db():
    global client, db
    client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
    db = client[MONGODB_DB]
    # create index for session_id to be unique
    db.sessions.create_index("session_id", unique=True)
    db.messages.create_index("session_id")
    # optional: index on topic for faster search
    db.messages.create_index("topic")

def save_message(session_id, role, content, topic=None):
    if client is None:
        init_db()
        
    db.sessions.update_one(
        {"session_id": session_id},
        {"$setOnInsert": {"session_id": session_id, "created_at": datetime.datetime.utcnow()}},
        upsert=True
    )
    
    db.messages.insert_one({
        "session_id": session_id,
        "role": role,
        "content": content,
        "topic": topic,
        "timestamp": datetime.datetime.utcnow()
    })

def get_conversation(session_id):
    if client is None:
        init_db()
        
    cursor = db.messages.find({"session_id": session_id}).sort("timestamp", 1)
    history = []
    for doc in cursor:
        history.append({
            "role": doc["role"],
            "content": doc["content"],
            "topic": doc.get("topic"),
            "timestamp": doc["timestamp"].isoformat()
        })
    return history

def search_by_topic(topic):
    if client is None:
        init_db()
        
    # User said: "searches MongoDB for past conversations by topic as extra context"
    cursor = db.messages.find({
        "topic": topic, 
        "role": "assistant"
    }).sort("timestamp", -1).limit(5)
    
    past_msgs = []
    for doc in cursor:
        past_msgs.append({
            "role": doc["role"],
            "content": doc["content"],
            "topic": doc.get("topic"),
            "timestamp": doc["timestamp"].isoformat()
        })
    return past_msgs

def get_all_sessions():
    if client is None:
        init_db()
    cursor = db.sessions.find().sort("created_at", -1)
    sessions = []
    for doc in cursor:
        sessions.append({
            "session_id": doc["session_id"],
            "created_at": doc["created_at"].isoformat() if "created_at" in doc else None
        })
    return sessions
