from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from recognize import recognize

app = FastAPI()

UPLOAD_DIR = Path("queries")

UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/recognize")
def recognize_audio(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    #below opens the write binary stream
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    song, score = recognize(str(file_path))

    return {
        "match": song,
        "confidence": round(score, 3)
    }