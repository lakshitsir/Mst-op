from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()

# CORS (GitHub Pages ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ytmusic = YTMusic()

@app.get("/")
def home():
    return {"status": "OK", "message": "Music backend running"}

# 🔍 SEARCH API
@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    results = ytmusic.search(q, filter="songs", limit=10)
    data = []
    for r in results:
        data.append({
            "title": r.get("title"),
            "artist": r["artists"][0]["name"] if r.get("artists") else "Unknown",
            "videoId": r.get("videoId"),
            "thumb": r["thumbnails"][-1]["url"] if r.get("thumbnails") else ""
        })
    return data

# ▶️ STREAM API (audio only)
@app.get("/stream")
def stream(videoId: str):
    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f"https://music.youtube.com/watch?v={videoId}",
            download=False
        )
        return {
            "url": info["url"],
            "title": info.get("title")
        }
