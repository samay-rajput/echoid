import os
from pathlib import Path
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load .env from the same directory as this script
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Read Mongo URI from environment variable
uri = os.getenv("MONGO_URI")

if not uri:
    raise RuntimeError("MONGO_URI is not set")

# Create MongoDB client
client = MongoClient(uri, server_api=ServerApi("1"))

# Optional: ping only for local debug
try:
    client.admin.command("ping")
    print("MongoDB connected")
except Exception as e:
    print("MongoDB connection failed:", e)

db = client.audio_matcher

songs_col = db.songs
fingerprints_col = db.fingerprints



#to check the collection!

# for doc in fingerprints_col.find({'song_id': 'Uchhal Matt'}).limit(15):
#     print(doc)

# for doc in songs_col.find():
#     print(doc)


# count = songs_col.count_documents({})


# print(count)

if __name__ == "__main__": 
    print(songs_col.count_documents({}))
    print(fingerprints_col.count_documents({}))

    # songs_col.insert_one({"test": "hello"})


