import subprocess
from gtts import gTTS  # لتحويل النص إلى صوت

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    images = data.get("images", [])
    script_text = data.get("script", "")  # نص لتحويله لصوت
    voice_file = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.mp3")

    # تحويل النص إلى صوت
    if script_text:
        tts = gTTS(script_text)
        tts.save(voice_file)

    job_id = str(uuid.uuid4())
    video_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")
    list_file = os.path.join(OUTPUT_DIR, f"{job_id}.txt")

    # إعداد قائمة الصور مع مدة 2 ثانية لكل صورة
    with open(list_file, "w") as f:
        for img in images:
            f.write(f"file '{img}'\n")
            f.write("duration 2\n")
        f.write(f"file '{images[-1]}'\n")

    # دمج الصور + الصوت
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-i", voice_file if script_text else "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf", "scale=1920:1080",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        video_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    jobs[job_id] = {"status": "done", "video_url": f"/download/{job_id}.mp4"}
    save_jobs()

    return jsonify({"job_id": job_id, "status": "done", "video_url": f"/download/{job_id}.mp4"})
