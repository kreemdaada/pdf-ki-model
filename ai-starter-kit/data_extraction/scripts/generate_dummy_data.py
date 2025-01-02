import json
import os

# Pfade anpassen
input_json = "../data/customers/customers.json"
output_jsonl = "../data/customers/customers_data.jsonl"
dummy_data_output = "../data/dummy_data.json"

# Ordner erstellen, falls nicht vorhanden
os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)

def process_customers_to_jsonl(input_path, output_path, dummy_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        customers = json.load(infile)  # Lädt eine Liste von Kunden

    # Erstelle die JSONL-Datei
    with open(output_path, "w", encoding="utf-8") as outfile:
        for customer in customers:
            # Struktur für JSONL-Eintrag
            product_details = ", ".join(
                [
                    f"{p['product_name']} (Menge: {p['quantity']}, Einzelpreis: {p['unit_price']}, Gesamt: {p['total']})"
                    for p in customer["products"]
                ]
            )
            jsonl_entry = {
                "text": (
                    f"Name: {customer['name']}, "
                    f"Adresse: {customer['address']}, "
                    f"Telefon: {customer['phone']}, "
                    f"E-Mail: {customer['email']}, "
                    f"Rechnungsnummer: {customer['invoice_number']}, "
                    f"Rechnungsdatum: {customer['invoice_date']}, "
                    f"Produkte: {product_details}, "
                    f"Gesamtbetrag: {customer['total_amount']}, "
                    f"Zahlungsziel: {customer['payment_due']}, "
                    f"Kommentare: {customer['comments']}"
                ),
                "label": customer,
            }
            # In JSONL-Datei schreiben
            outfile.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")

    print(f"✅ Kundendaten in JSONL-Datei gespeichert: {output_path}")

    # Speichere die erste Kundenstruktur als Dummy-Daten
    with open(dummy_path, "w", encoding="utf-8") as dummy_outfile:
        json.dump(customers[0], dummy_outfile, indent=4, ensure_ascii=False)
    print(f"✅ Dummy-Daten gespeichert: {dummy_path}")

# Verarbeite die Kundendaten
process_customers_to_jsonl(input_json, output_jsonl, dummy_data_output)
