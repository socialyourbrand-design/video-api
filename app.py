from flask import Flask, request, jsonify, send_from_directory
import uuid
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    images = data.get("images", [])
    voice = data.get("voice", "")

    job_id = str(uuid.uuid4())
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

    # 🎬 تحويل الصور لفيديو
    clips = []
    for img in images:
        clip = ImageClip(img).set_duration(2)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    # 🎧 إضافة صوت إذا موجود
    if voice:
        audio = AudioFileClip(voice)
        video = video.set_audio(audio)

    video.write_videofile(output_path, fps=24)

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
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
