from flask import Flask, request, jsonify, send_from_directory
import uuid
import os

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

    file_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

    # ⚠️ هذا مؤقت (لأنك ما عندك توليد فيديو فعلي بعد)
    with open(file_path, "w") as f:
        f.write("FAKE VIDEO FILE")

    return jsonify({
        "status": "processing",
        "job_id": job_id,
        "video_url": f"/download/{job_id}.mp4"
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
