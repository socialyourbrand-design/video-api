from flask import Flask, request, jsonify, send_from_directory
import uuid
import os
import json

app = Flask(__name__)

OUTPUT_DIR = "outputs"
DATA_FILE = "jobs.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# تحميل البيانات
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        jobs = json.load(f)
else:
    jobs = {}

def save_jobs():
    with open(DATA_FILE, "w") as f:
        json.dump(jobs, f)

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    job_id = str(uuid.uuid4())

    jobs[job_id] = {"status": "processing"}
    save_jobs()

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
