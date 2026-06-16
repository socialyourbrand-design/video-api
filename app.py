from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    job_id = str(uuid.uuid4())

    return jsonify({
        "status": "ok",
        "job_id": job_id,
        "video_url": f"/download/{job_id}.mp4"
    })


@app.route("/health")
def health():
    return {"status": "ok"}
