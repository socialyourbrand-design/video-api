from flask import Flask, request, jsonify, send_from_directory
import uuid
import os
import threading
import subprocess

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# نخزن حالات الشغل
jobs = {}


def generate_video(job_id, images):
    try:
        video_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")
        list_file = os.path.join(OUTPUT_DIR, f"{job_id}.txt")

        with open(list_file, "w") as f:
            for img in images:
                f.write(f"file '{img}'\n")
                f.write("duration 2\n")
            f.write(f"file '{images[-1]}'\n")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-vf", "scale=1280:720",
            "-pix_fmt", "yuv420p",
            video_path
        ]

        subprocess.run(cmd, check=True)

        jobs[job_id]["status"] = "done"
        jobs[job_id]["video_url"] = f"/download/{job_id}.mp4"

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.route("/generate-video", methods=["POST"])
def generate_video_api():
    data = request.get_json()
    images = data.get("images", [])

    if not images:
        return jsonify({"error": "no images"}), 400

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "processing"
    }

    # تشغيل بالخلفية (هذا الاحترافي)
    threading.Thread(target=generate_video, args=(job_id, images)).start()

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })


@app.route("/status/<job_id>")
def status(job_id):
    return jsonify(jobs.get(job_id, {"error": "not found"}))


@app.route("/download/<file>")
def download(file):
    return send_from_directory(OUTPUT_DIR, file)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
