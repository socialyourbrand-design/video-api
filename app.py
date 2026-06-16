from flask import Flask, request, jsonify, send_from_directory
import uuid
import os
import subprocess

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    images = data.get("images", [])
    voice = data.get("voice", "")

    job_id = str(uuid.uuid4())

    video_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")
    list_path = os.path.join(OUTPUT_DIR, f"{job_id}.txt")

    # نحول الصور إلى ملف ffmpeg list
    with open(list_path, "w") as f:
        for img in images:
            f.write(f"file '{img}'\n")
            f.write("duration 2\n")

    # تشغيل ffmpeg
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-vf", "scale=1280:720",
        "-pix_fmt", "yuv420p",
        video_path
    ]

    subprocess.run(cmd, check=True)

    return jsonify({
        "status": "done",
        "job_id": job_id,
        "video_url": f"/download/{job_id}.mp4"
    })


@app.route("/download/<file>")
def download(file):
    return send_from_directory(OUTPUT_DIR, file)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
