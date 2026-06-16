from flask import Flask, request, jsonify, send_from_directory
import os, uuid

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    caption = data.get("caption", [])
    images = data.get("images", [])
    voice = data.get("voice", "")

    job_id = str(uuid.uuid4())
    file_path = os.path.join(OUTPUT_DIR, f"{job_id}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("CAPTION:\n" + str(caption) + "\n\n")
        f.write("IMAGES:\n" + str(images) + "\n\n")
        f.write("VOICE:\n" + str(voice))

    return jsonify({
        "status": "ok",
        "job_id": job_id,
        "video_url": f"/download/{job_id}.txt"
    })

@app.route("/download/<file>")
def download(file):
    return send_from_directory(OUTPUT_DIR, file)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
