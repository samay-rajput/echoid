# EchoID - Audio Recognition Service

A Shazam-like audio fingerprinting and recognition service that identifies songs from audio samples.

🔗 **Demo:** [echoid.vercel.app](https://echoid.vercel.app)

## Features

- 🎵 **Audio Fingerprinting** - Uses spectrogram peak-picking and landmark hashing
- 🔍 **Song Identification** - Matches audio samples against a fingerprint database
- 🎧 **Spotify Integration** - Returns song metadata with Spotify links
- 🌐 **React Frontend** - Clean UI for recording and identifying songs

## Tech Stack

**Backend:** FastAPI, MongoDB, NumPy, SoundFile  
**Frontend:** React, Vite  
**Audio Processing:** FFT-based spectrogram analysis, landmark generation

## Project Structure

```
├── backend/
│   └── time_offset_approach/    # Main backend (deployed)
│       ├── app.py               # FastAPI endpoints
│       ├── spectogram.py        # Spectrogram generation
│       ├── peak_picking.py      # Peak detection
│       ├── landmark_generation.py
│       ├── match_from_db.py     # Song identification
│       └── db.py                # MongoDB connection
│
└── frontend/
    └── audio-identify-ui/       # React frontend
        └── src/App.jsx
```

## Getting Started

### Backend

```bash
cd backend/time_offset_approach
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend

```bash
cd frontend/audio-identify-ui
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint    | Description                    |
|--------|-------------|--------------------------------|
| POST   | `/identify` | Identify a song from audio     |
| POST   | `/upload`   | Add new song to the database   |
| GET    | `/health`   | Health check                   |

## How It Works

1. **Record** - User records audio via browser microphone
2. **Fingerprint** - Audio converted to spectrogram → peaks detected → landmarks generated
3. **Match** - Landmarks hashed and matched against MongoDB database using time-offset voting
4. **Return** - Best match returned with Spotify metadata

