#!/bin/bash

# Environment Variablen
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="$ROOT_DIR/../data_extraction/data/training_data.jsonl"
OUTPUT_DIR="$ROOT_DIR/data/output/preprocessed"
TRAINING_SCRIPT="$ROOT_DIR/train.py"
DATA_PREP_SCRIPT="$ROOT_DIR/generative_data_prep.py"

echo "==== Schritt 1: JSON in JSONL umwandeln ===="
cd "$ROOT_DIR/../data_extraction/scripts"
python3 convert_json_to_jsonl.py
echo "✅ JSONL-Datei erfolgreich erstellt."

echo "==== Schritt 2: Datenvorbereitung für YoDA ===="
cd "$ROOT_DIR"
if [ -f "$DATA_PREP_SCRIPT" ]; then
    python3 "$DATA_PREP_SCRIPT"
    echo "✅ Datenvorbereitung abgeschlossen. Dateien gespeichert in: $OUTPUT_DIR"
else
    echo "❌ Datenvorbereitungs-Skript nicht gefunden: $DATA_PREP_SCRIPT"
    exit 1
fi

echo "==== Schritt 3: YoDA-Modell trainieren ===="
if [ -f "$TRAINING_SCRIPT" ]; then
    python3 "$TRAINING_SCRIPT"
    echo "✅ Training abgeschlossen. Modell gespeichert unter ./output/trained_model"
else
    echo "⚠️ Training-Skript ($TRAINING_SCRIPT) nicht gefunden. Bitte überprüfe den Pfad."
    exit 1
fi
