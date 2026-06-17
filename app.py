from flask import Flask, request, jsonify
import uuid
import os

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

jobs = {}

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    images = data.get("images", [])

    job_id = str(uuid.uuid4())

    jobs[job_id] = {"status": "processing"}

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })


@app.route("/status/<job_id>", methods=["GET"])
def status(job_id):
    job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "not found"})

    return jsonify(job)


@app.route("/health")
def health():
    return {"status": "ok"}
