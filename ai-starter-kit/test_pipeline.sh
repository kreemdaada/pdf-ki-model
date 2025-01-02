#!/bin/bash

# Verzeichnis des Skripts ermitteln
ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
CUSTOMERS_DIR="$ROOT_DIR/data_extraction/data/customers"
PDFS_DIR="$ROOT_DIR/data_extraction/data/output/customer_pdfs"

# 0. Bereinigung alter PDF-Dateien
echo "=== 0. Bereinigung alter PDF-Dateien ==="
if [ -d "$PDFS_DIR" ]; then
    echo "⚠️  Alter PDF-Ordner gefunden. Lösche den Inhalt..."
    rm -rf "$PDFS_DIR"/*
else
    echo "ℹ️  Kein alter PDF-Ordner gefunden. Erstelle neuen Ordner..."
    mkdir -p "$PDFS_DIR"
fi
echo "✅ PDF-Verzeichnis bereinigt."

# 1. Virtuelle Umgebung erstellen
echo "=== 1. Virtuelle Umgebung erstellen ==="
cd "$ROOT_DIR/data_extraction"
if [ ! -d "venv" ]; then
    echo "ℹ️  Virtuelle Umgebung wird erstellt..."
    python3 -m venv venv
else
    echo "✅ Virtuelle Umgebung bereits vorhanden."
fi
source venv/bin/activate
pip install --upgrade pip
pip install fpdf reportlab pandas > /dev/null 2>&1
echo "✅ Abhängigkeiten installiert."

# 2. Kundendaten prüfen
CUSTOMER_DATA=$1
echo "DEBUG: Überprüfe Datei unter $CUSTOMER_DATA"

if [ -z "$CUSTOMER_DATA" ]; then
    echo "❌ Fehler: Kein Dateipfad angegeben!"
    exit 1
fi

if [ ! -f "$CUSTOMER_DATA" ]; then
    echo "❌ Fehler: Datei nicht gefunden: $CUSTOMER_DATA"
    ls -l "$(dirname "$CUSTOMER_DATA")"
    exit 1
fi
echo "✅ Datei gefunden: $CUSTOMER_DATA"

# 3. PDF mit Kundendaten generieren
echo "=== 3. PDFs generieren ==="
cd "$ROOT_DIR/data_extraction/scripts" || { echo "❌ Verzeichnis nicht gefunden: $ROOT_DIR/data_extraction/scripts"; exit 1; }
echo "DEBUG: Verzeichnisinhalt:"
ls -l

if python fill_pdf_with_customers.py "$CUSTOMER_DATA" "$PDFS_DIR"; then
    echo "✅ PDFs erfolgreich erstellt."
else
    echo "❌ Fehler beim Erstellen der PDFs."
    exit 1
fi

echo "🚀 Pipeline erfolgreich abgeschlossen!"
