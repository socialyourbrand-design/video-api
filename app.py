from flask import Flask, request, jsonify, send_from_directory
import uuid
import os
import subprocess

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/generate-video", methods=["POST"])
def generate_video():
    try:
        data = request.get_json()
        images = data.get("images", [])

        if len(images) == 0:
            return jsonify({"error": "no images"}), 400

        job_id = str(uuid.uuid4())

        video_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

        # 🔥 الطريقة الصحيحة: slideshow images
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", "1",
            "-pattern_type", "glob",
            "-i", "/app/outputs/*.png",
            "-vf", "scale=1280:720",
            "-pix_fmt", "yuv420p",
            video_path
        ]

        # نحفظ الصور أولاً محلياً
        local_images = []
        for i, img in enumerate(images):
            path = os.path.join(OUTPUT_DIR, f"{job_id}_{i}.png")
            subprocess.run(["curl", "-o", path, img])
            local_images.append(path)

        # نعيد تشغيل ffmpeg بطريقة صحيحة
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", "1",
            "-i", os.path.join(OUTPUT_DIR, f"{job_id}_%d.png"),
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/<file>")
def download(file):
    return send_from_directory(OUTPUT_DIR, file)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
