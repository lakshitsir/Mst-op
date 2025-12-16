from flask import Flask, request, jsonify
from flask_cors import CORS
from ytmusicapi import YTMusic
import yt_dlp

def create_app():
    app = Flask(__name__)
    CORS(app)

    ytmusic = YTMusic()

    @app.route("/")
    def home():
        return jsonify({
            "status": "OK",
            "message": "app.py is running"
        })

    @app.route("/search")
    def search():
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify([])

        results = ytmusic.search(q, filter="songs", limit=10)
        data = []

        for r in results:
            data.append({
                "title": r.get("title"),
                "artist": r["artists"][0]["name"] if r.get("artists") else "Unknown",
                "videoId": r.get("videoId"),
                "thumb": r["thumbnails"][-1]["url"] if r.get("thumbnails") else ""
            })

        return jsonify(data)

    @app.route("/stream")
    def stream():
        videoId = request.args.get("videoId")
        if not videoId:
            return jsonify({"error": "videoId missing"})

        ydl_opts = {
            "format": "bestaudio",
            "quiet": True,
            "noplaylist": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://music.youtube.com/watch?v={videoId}",
                download=False
            )

        return jsonify({
            "title": info.get("title"),
            "url": info["url"]
        })

    return app
