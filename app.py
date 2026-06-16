@app.route("/status/<job_id>", methods=["GET"])
def status(job_id):
    file_path = os.path.join("outputs", f"{job_id}.mp4")

    if os.path.exists(file_path):
        return jsonify({
            "status": "done",
            "video_url": f"/download/{job_id}.mp4"
        })

    return jsonify({
        "status": "processing"
    })
