#!/bin/bash

# Überprüfen, ob der Dateiname übergeben wurde
if [ -z "$1" ]; then
    echo "❌ Kein Dateiname angegeben! Skript wird beendet."
    exit 1
fi

FILE_PATH="$1"
OUTPUT_DIR="./data_extraction/data/output"
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "=== Running Complete Pipeline ==="
echo "Eingabedatei: $FILE_PATH"

# 1. PDF-Testpipeline
echo "=== Running Test Pipeline (PDF Generation) ==="
cd "$SCRIPT_DIR" || exit
./test_pipeline.sh "$FILE_PATH" > pipeline_log.txt 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Fehler in der Testpipeline. Siehe pipeline_log.txt."
    exit 1
fi
echo "✅ Testpipeline erfolgreich abgeschlossen."

# 2. YoDA-Pipeline
echo "=== Running YoDA Pipeline ==="
cd "$SCRIPT_DIR/yoda" || exit
./run_yoda_pipeline.sh >> pipeline_log.txt 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Fehler in der YoDA-Pipeline. Siehe pipeline_log.txt."
    exit 1
fi
echo "✅ YoDA-Pipeline erfolgreich abgeschlossen."

# 3. Ergebnisse prüfen
PDF_NAME=$(basename "${FILE_PATH%.*}.pdf")
if [[ -f "$OUTPUT_DIR/$PDF_NAME" ]]; then
    echo "✅ PDF erfolgreich erstellt: $OUTPUT_DIR/$PDF_NAME"
else
    echo "❌ PDF konnte nicht erstellt werden. Siehe pipeline_log.txt."
    exit 1
fi
