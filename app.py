from flask import Flask, request, jsonify, send_from_directory
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os, uuid, requests

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_file(url, path):
    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    captions = data.get("caption", [])
    images = data.get("images", [])
    voice = data.get("voice", "")

    job_id = str(uuid.uuid4())
    video_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")

    clips = []
    duration = 3

    for i, img_url in enumerate(images):
        img_path = os.path.join(OUTPUT_DIR, f"{job_id}_{i}.jpg")
        download_file(img_url, img_path)

        clip = ImageClip(img_path).set_duration(duration)
        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose")

    if voice:
        audio_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp3")
        download_file(voice, audio_path)
        audio = AudioFileClip(audio_path)
        final_video = final_video.set_audio(audio)

    final_video.write_videofile(video_path, fps=24)

    return jsonify({
        "status": "ok",
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
