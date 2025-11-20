from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

# Path to your music folder
MUSIC_FOLDER = os.path.join(os.getcwd(), "music")

# Example music data (added 'file' field for playback)
music_library = [
    {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop", "file": "blinding_lights.mp3"},
    {"id": 2, "title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop", "file": "shape_of_you.mp3"},
    {"id": 3, "title": "Lose Yourself", "artist": "Eminem", "genre": "Hip-Hop", "file": "lose_yourself.mp3"},
    {"id": 4, "title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "file": "bohemian_rhapsody.mp3"},
]

# Serve music files
@app.route("/music/<path:filename>")
def serve_music(filename):
    return send_from_directory(MUSIC_FOLDER, filename)

# Get all music metadata
@app.route("/api/music", methods=["GET"])
def get_music():
    # Add full URL to file
    music_with_url = []
    for m in music_library:
        m_copy = m.copy()
        m_copy["url"] = f"http://127.0.0.1:5000/music/{m['file']}"
        music_with_url.append(m_copy)
    return jsonify(music_with_url)

# Get music by ID
@app.route("/api/music/<int:music_id>", methods=["GET"])
def get_music_by_id(music_id):
    music = next((m for m in music_library if m["id"] == music_id), None)
    if music:
        music_copy = music.copy()
        music_copy["url"] = f"http://127.0.0.1:5000/music/{music['file']}"
        return jsonify(music_copy)
    return jsonify({"error": "Music not found"}), 404

# Search by artist
@app.route("/api/music/artist/<string:artist_name>", methods=["GET"])
def get_music_by_artist(artist_name):
    results = [m for m in music_library if artist_name.lower() in m["artist"].lower()]
    # Add URLs
    for r in results:
        r["url"] = f"http://127.0.0.1:5000/music/{r['file']}"
    return jsonify(results)

if __name__ == "__main__":
    # Make sure your 'music' folder exists and has the mp3 files
    os.makedirs(MUSIC_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
