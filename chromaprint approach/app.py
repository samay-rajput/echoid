from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil
from fingerprint import extract_fingerprint
from recognize import recognize
from db import songs_collection

app = FastAPI()

UPLOAD_QUERY_DIR = Path("queries")
UPLOAD_QUERY_DIR.mkdir(exist_ok=True)


@app.post("/recognize")
def recognize_audio(file: UploadFile = File(...)):

    file_path = UPLOAD_QUERY_DIR / file.filename

    #below opens the write binary stream
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    song, score, status = recognize(str(file_path))

    return {
        "match": song,
        "confidence": round(score, 3), 
        "status" : status
    }

#to upload any new song into the DB
UPLOAD_NEW_DIR = Path("known_songs")
UPLOAD_NEW_DIR.mkdir(exist_ok=True)


@app.post("/upload_song")
def upload_new_song(file: UploadFile = File(...)):
    file_path = UPLOAD_NEW_DIR / file.filename

    #below opens the write binary stream
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    valid_extensions = {".mp3", ".m4a", ".wav"}

    file_ext = Path(file.filename).suffix
    file_stem = Path(file.filename).stem

    if file_ext in valid_extensions:
        songs_col = songs_collection()
        song_name = file_stem

        if songs_col.find_one({"song_name": song_name}):
            return {"song": song_name, "status": "already exits"}
        
        duration, fingerprint = extract_fingerprint(str(file_path))

        doc = {
            "song_name": song_name,
            "path": str(UPLOAD_NEW_DIR),
            "duration": duration,
            "fingerprint": fingerprint
        }
        songs_col.insert_one(doc)
        return {"song": song_name, "status": "uploaded!"}
    else:
        return {"status": "invalid file type!"}


