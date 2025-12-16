from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__)
CORS(app)

ytmusic = YTMusic()

@app.route("/")
def home():
    return {"status": "OK", "message": "Music backend running"}

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return []

    results = ytmusic.search(q, filter="songs", limit=12)

    return [{
        "title": r.get("title"),
        "artist": r["artists"][0]["name"] if r.get("artists") else "Unknown",
        "videoId": r.get("videoId"),
        "thumb": r["thumbnails"][-1]["url"] if r.get("thumbnails") else ""
    } for r in results]

@app.route("/play")
def play():
    videoId = request.args.get("videoId")
    if not videoId:
        return "Missing videoId", 400

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "nocheckcertificate": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f"https://music.youtube.com/watch?v={videoId}",
            download=False
        )
        return redirect(info["url"], code=302)
