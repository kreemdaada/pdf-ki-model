import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory
import mimetypes
import csv
import json
import sys

# Füge das Verzeichnis mit `convert_csv_to_json` zu den Suchpfaden hinzu
sys.path.append(os.path.abspath("./data_extraction/scripts"))

# Importiere die Funktion
from convert_csv_to_json import convert_csv_to_json

app = Flask(__name__)


CUSTOMERS_DIR = "./data_extraction/data/customers"
PDFS_DIR = "./data_extraction/data/output/customer_pdfs"
PIPELINE_SCRIPT = os.path.abspath("./test_pipeline.sh")  # Absoluter Pfad zum Pipeline-Skript

# Verzeichnisse erstellen, falls sie nicht existieren
os.makedirs(CUSTOMERS_DIR, exist_ok=True)
os.makedirs(PDFS_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        # Prüfe, ob eine Datei hochgeladen wurde
        if "file" not in request.files:
            return jsonify({"error": "Keine Datei hochgeladen"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Leerer Dateiname"}), 400

        # Datei im Kundenverzeichnis speichern
        file_path = os.path.join(CUSTOMERS_DIR, file.filename)
        file.save(file_path)
        file_path = os.path.abspath(file_path)  # Absoluter Pfad zur Datei
        print(f"DEBUG: Datei gespeichert unter {file_path}")

        # Prüfen, ob die Datei CSV ist, und konvertieren
        if file.filename.endswith(".csv"):
            json_file_path = file_path.replace(".csv", ".json")
            convert_csv_to_json(file_path, json_file_path)
            print(f"DEBUG: CSV-Datei erfolgreich zu JSON konvertiert: {json_file_path}")
            file_path = json_file_path  # Weiterarbeiten mit der JSON-Datei

        # Starte die Pipeline
        result = subprocess.run(
            ["bash", PIPELINE_SCRIPT, file_path],
            capture_output=True,
            text=True
        )
        print(f"DEBUG: Übergebener Dateipfad: {file_path}")
        print(f"DEBUG: Pipeline stdout: {result.stdout}")
        print(f"DEBUG: Pipeline stderr: {result.stderr}")

        if result.returncode != 0:
            return jsonify({"error": "Pipeline-Fehler", "details": result.stderr}), 500

        # Liste der generierten PDFs erstellen
        pdf_files = [f"http://127.0.0.1:5000/pdfs/{pdf}" for pdf in os.listdir(PDFS_DIR) if pdf.endswith(".pdf")]

        return jsonify({
            "message": "Pipeline erfolgreich abgeschlossen",
            "pdf_links": pdf_files
        }), 200

    except Exception as e:
        print(f"DEBUG: Ein unerwarteter Fehler ist aufgetreten: {e}")
        return jsonify({"error": "Ein unerwarteter Fehler ist aufgetreten", "details": str(e)}), 500


@app.route("/pdfs/<filename>", methods=["GET"])
def download_pdf(filename):
    try:
        return send_from_directory(PDFS_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Datei nicht gefunden"}), 404


if __name__ == "__main__":
    app.run(debug=True)
