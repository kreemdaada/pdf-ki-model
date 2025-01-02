import csv
import json
from collections import defaultdict

def convert_csv_to_json(csv_file, json_file):
    """
    Konvertiert eine CSV-Datei in eine JSON-Datei und gruppiert Einträge basierend auf der Rechnungsnummer.
    """
    try:
        grouped_data = defaultdict(lambda: {
            "name": "",
            "address": "",
            "phone": "",
            "email": "",
            "invoice_number": "",
            "invoice_date": "",
            "products": [],
            "total_amount": "",
            "payment_due": "",
            "comments": ""
        })

        with open(csv_file, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                invoice_number = row["Invoice Number"]
                grouped_data[invoice_number]["name"] = row["Name"]
                grouped_data[invoice_number]["address"] = row["Address"]
                grouped_data[invoice_number]["phone"] = row["Phone"]
                grouped_data[invoice_number]["email"] = row["Email"]
                grouped_data[invoice_number]["invoice_number"] = row["Invoice Number"]
                grouped_data[invoice_number]["invoice_date"] = row["Invoice Date"]
                grouped_data[invoice_number]["total_amount"] = row["Total Amount"]
                grouped_data[invoice_number]["payment_due"] = row["Payment Due"]
                grouped_data[invoice_number]["comments"] = row["Comments"]
                grouped_data[invoice_number]["products"].append({
                    "product_name": row["Product Name"],
                    "quantity": int(row["Quantity"]),
                    "unit_price": float(row["Unit Price"]),
                    "total": float(row["Product Total"])
                })

        # Konvertiere defaultdict zu einer Liste
        data = list(grouped_data.values())

        with open(json_file, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"✅ JSON-Datei erfolgreich erstellt: {json_file}")
        return json_file

    except Exception as e:
        raise ValueError(f"Fehler beim Konvertieren von CSV nach JSON: {e}")


# Beispielaufruf (nur für Tests)
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("❌ Fehler: Bitte Eingabe-CSV und Ausgabe-JSON angeben.")
        sys.exit(1)
    csv_file = sys.argv[1]
    json_file = sys.argv[2]
    convert_csv_to_json(csv_file, json_file)
