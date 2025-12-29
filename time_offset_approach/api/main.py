from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile, os, subprocess
from fastapi.params import Form
from match_from_db import identify_song
from db import songs_col
from index_to_db import index_song

app = FastAPI(title="Audio Fingerprinting API")



@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/identify")
async def identify(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp_path = tmp.name
        tmp.write(await file.read())

    # convert to wav (important)
    wav_path = tmp_path + ".wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", tmp_path, wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        song, votes, offset = identify_song(wav_path)
    finally:
        os.remove(tmp_path)
        os.remove(wav_path)

    if song is None:
        return {
            "match": False,
            "reason": "NO_MATCH"
        }

    return {
        "match": True,
        "song_id": song,
        "votes": votes,
        "offset": offset
    }


@app.post("/upload")
async def upload_song(
    file: UploadFile = File(...),
    song_id: str = Form(...)
):
    """
    Upload a new song and index it into the fingerprint database.

    This endpoint is meant for ADMIN / SYSTEM use, not end users.
    """


    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No audio file uploaded")

    if not song_id.strip():
        raise HTTPException(status_code=400, detail="song_id is required")

    

    existing_song = songs_col.find_one({ "song_id": song_id })
    if existing_song:
        raise HTTPException(
            status_code=409,
            detail="Song already exists in database"
        )


    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp_path = tmp.name
        tmp.write(await file.read())

    

    #convert to .wav
    wav_path = tmp_path + ".wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", tmp_path, wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

        #index the given song
    try:
        index_song(wav_path, song_id)

        # store song metadata
        songs_col.insert_one({
            "song_id": song_id
        })

    finally:
        #cleanup
        os.remove(tmp_path)
        os.remove(wav_path)

    # return confirmation 
    return {
        "status": "indexed",
        "song_id": song_id
    }
