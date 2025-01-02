import json
import os
import sys
from fpdf import FPDF

if len(sys.argv) < 3:
    print("❌ Fehler: Bitte den Pfad zur Eingabedatei und den Ausgabepfad angeben.")
    sys.exit(1)

CUSTOMER_DATA_JSON = os.path.abspath(sys.argv[1])  # Absoluter Pfad
OUTPUT_DIR = os.path.abspath(sys.argv[2])  # Absoluter Pfad
os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_get(data, key, default="Nicht angegeben"):
    return data.get(key, default)

def create_customer_pdfs():
    print(f"DEBUG: Eingabedatei ist {CUSTOMER_DATA_JSON}")
    print(f"DEBUG: PDF-Ausgabeordner ist {OUTPUT_DIR}")

    if not os.path.exists(CUSTOMER_DATA_JSON):
        print(f"❌ Fehler: Kundendaten nicht gefunden: {CUSTOMER_DATA_JSON}")
        sys.exit(1)

    try:
        with open(CUSTOMER_DATA_JSON, "r", encoding="utf-8") as file:
            customers = json.load(file)
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Kundendaten: {e}")
        sys.exit(1)

    if not isinstance(customers, list):
        print("❌ Fehler: JSON-Daten sind nicht im Listenformat.")
        sys.exit(1)

    for customer in customers:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Kundeninformationen hinzufügen
            pdf.cell(200, 10, txt=f"Name: {safe_get(customer, 'name')}", ln=True)
            pdf.cell(200, 10, txt=f"Adresse: {safe_get(customer, 'address')}", ln=True)
            pdf.cell(200, 10, txt=f"Telefon: {safe_get(customer, 'phone')}", ln=True)
            pdf.cell(200, 10, txt=f"E-Mail: {safe_get(customer, 'email')}", ln=True)
            pdf.cell(200, 10, txt=f"Rechnungsnummer: {safe_get(customer, 'invoice_number')}", ln=True)
            pdf.cell(200, 10, txt=f"Rechnungsdatum: {safe_get(customer, 'invoice_date')}", ln=True)

            # Produkte hinzufügen
            pdf.cell(200, 10, txt="Produkte:", ln=True)
            products = safe_get(customer, 'products', [])
            if isinstance(products, list) and products:
                for idx, product in enumerate(products, start=1):
                    product_name = safe_get(product, 'name', 'Unbekannt')
                    quantity = safe_get(product, 'quantity', 'N/A')
                    price = safe_get(product, 'price', 'N/A')
                    pdf.cell(200, 10, txt=f"{idx}. {product_name} - Menge: {quantity} - Preis: {price} EUR", ln=True)
            else:
                pdf.cell(200, 10, txt="Keine Produkte angegeben.", ln=True)

            # Gesamtbetrag
            pdf.cell(200, 10, txt=f"Gesamtbetrag: {safe_get(customer, 'total_amount', 'Nicht angegeben')} EUR", ln=True)

            # PDF speichern
            output_file = os.path.join(OUTPUT_DIR, f"{safe_get(customer, 'name').replace('/', '_')}_invoice.pdf")
            pdf.output(output_file)
            print(f"✅ PDF erstellt: {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"❌ Fehler beim Erstellen des PDFs für {safe_get(customer, 'name', 'Unbekannt')}: {e}")

if __name__ == "__main__":
    create_customer_pdfs()
