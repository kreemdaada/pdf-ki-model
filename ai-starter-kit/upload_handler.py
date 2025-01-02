import os
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Verzeichnis für hochgeladene Dateien
UPLOAD_FOLDER = "./data_extraction/data/customers/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Keine Datei hochgeladen"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Dateiname ist leer"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Starte die Pipeline
    try:
        result = subprocess.run(["bash", "./run_complete_pipeline.sh"], check=True, text=True, capture_output=True)
        return jsonify({
            "message": "Datei verarbeitet",
            "details": result.stdout,
            "pdf_link": f"/data/output/{file.filename.replace('.csv', '.pdf').replace('.json', '.pdf')}"
        }), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Fehler in der Pipeline", "details": e.stderr}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
