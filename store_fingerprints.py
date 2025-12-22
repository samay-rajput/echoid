from pymongo import MongoClient
from fingerprint import extract_fingerprint
from pathlib import Path

"""
storing the metadata of all songs in db from dir: known_songs
like,
-song_name
-path
-duration
-fingerprint
"""

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["music_recognition"]
songs_col = db["songs"]

SONG_DIR = "known_songs"


#check for diff audio extensions
valid_extensions = {".mp3", ".m4a", ".wav"}

for path in Path(SONG_DIR).glob("*"):

    if path.suffix in valid_extensions:
        song_name = path.stem

        # avoid duplicates
        if songs_col.find_one({"song_name": song_name}):
            print(f"{song_name} already exists, skipping")
            continue

        duration, fingerprint = extract_fingerprint(str(path))

        #schema
        doc = {
            "song_name": song_name,
            "path": str(path),
            "duration": duration,
            "fingerprint": fingerprint
        }

        songs_col.insert_one(doc)
        print(f"Inserted {song_name}")

    else: 
        print(f"{path.stem} has an invalid audio extension.")
