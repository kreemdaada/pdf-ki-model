import json
import os
import sys
import csv

def convert_csv_to_json(csv_file, json_file):
    """Konvertiere CSV-Datei in eine JSON-Datei."""
    try:
        with open(csv_file, "r", encoding="utf-8") as csvfile, open(json_file, "w", encoding="utf-8") as jsonfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            json.dump(rows, jsonfile, indent=4)
        print(f"✅ CSV erfolgreich in JSON konvertiert: {json_file}")
        return True
    except Exception as e:
        print(f"❌ Fehler bei der CSV-Konvertierung: {e}")
        return False

def convert_to_jsonl(input_file, output_jsonl):
    """Konvertiere JSON-Datei zu JSONL."""
    if not os.path.exists(input_file):
        print(f"❌ Eingabedatei nicht gefunden: {input_file}")
        return False

    try:
        with open(input_file, "r", encoding="utf-8") as infile, open(output_jsonl, "w", encoding="utf-8") as outfile:
            data_list = json.load(infile)
            if not isinstance(data_list, list):
                print("❌ Ungültiges JSON-Format. Erwartet wird eine Liste von Objekten.")
                return False

            for i, data in enumerate(data_list):
                if isinstance(data, dict):
                    text = (
                        f"Name: {data.get('name', 'Unbekannt')}, "
                        f"Adresse: {data.get('address', 'Unbekannt')}, "
                        f"Telefon: {data.get('phone', 'Unbekannt')}, "
                        f"E-Mail: {data.get('email', 'Unbekannt')}, "
                        f"Rechnungsnummer: {data.get('invoice_number', 'Unbekannt')}, "
                        f"Rechnungsdatum: {data.get('invoice_date', 'Unbekannt')}, "
                        f"Produkte: {', '.join([p.get('product_name', 'Unbekannt') for p in data.get('products', [])])}, "
                        f"Gesamtbetrag: {data.get('total_amount', 'Unbekannt')}, "
                        f"Zahlungsziel: {data.get('payment_due', 'Unbekannt')}, "
                        f"Kommentare: {data.get('comments', 'Keine Kommentare')}"
                    )
                    jsonl_entry = {"text": text, "label": data}
                    outfile.write(json.dumps(jsonl_entry) + "\n")
        print(f"✅ JSONL-Datei erfolgreich erstellt: {output_jsonl}")
        return True
    except Exception as e:
        print(f"❌ Fehler bei der Verarbeitung: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Nutzung: python convert_to_jsonl.py <input_file> <output_jsonl>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_jsonl = sys.argv[2]

    # Wenn die Eingabedatei CSV ist, konvertiere sie zuerst nach JSON
    if input_file.endswith(".csv"):
        json_file = input_file.replace(".csv", ".json")
        if not convert_csv_to_json(input_file, json_file):
            sys.exit(1)
        input_file = json_file  # JSON-Datei als neue Eingabe setzen

    if convert_to_jsonl(input_file, output_jsonl):
        sys.exit(0)
    else:
        sys.exit(1)
