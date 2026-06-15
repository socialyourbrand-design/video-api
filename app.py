import os
import uuid
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    script = data.get("script", [])
    images = data.get("images", [])
    voice = data.get("voice", "")

    job_id = str(uuid.uuid4())

    file_path = os.path.join(OUTPUT_DIR, f"{job_id}.txt")

    with open(file_path, "w") as f:
        f.write(str(script))
        f.write(str(images))
        f.write(str(voice))

    return jsonify({
        "video_url": f"/download/{job_id}.txt",
        "job_id": job_id
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
