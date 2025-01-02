import json
from fpdf import FPDF
import os

# Pfade
input_json = "../data/dummy_data.json"
output_folder = "../data/generated_pdfs/"

def create_customer_pdf(customer, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Titel
    pdf.cell(200, 10, txt="Rechnung", ln=True, align="C")
    pdf.ln(10)

    # Kundendaten
    pdf.cell(200, 10, txt=f"Name: {customer['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Adresse: {customer['address']}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon: {customer['phone']}", ln=True)
    pdf.cell(200, 10, txt=f"E-Mail: {customer['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Rechnungsnummer: {customer['invoice_number']}", ln=True)
    pdf.cell(200, 10, txt=f"Rechnungsdatum: {customer['invoice_date']}", ln=True)
    pdf.ln(5)

    # Produkte
    pdf.cell(200, 10, txt="Produkte:", ln=True)
    for product in customer["products"]:
        pdf.cell(200, 10, txt=f"- {product['product_name']} "
                              f"(Menge: {product['quantity']}, "
                              f"Einzelpreis: {product['unit_price']} EUR, "
                              f"Gesamt: {product['total']} EUR)", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Gesamtbetrag: {customer['total_amount']}", ln=True)
    pdf.cell(200, 10, txt=f"Zahlungsziel: {customer['payment_due']}", ln=True)
    pdf.cell(200, 10, txt=f"Kommentare: {customer['comments']}", ln=True)

    pdf.output(output_path)
    print(f"PDF für {customer['name']} erstellt: {output_path}")

# Hauptlogik
if __name__ == "__main__":
    # Lade Kundendaten
    with open(input_json, "r", encoding="utf-8") as file:
        customers = json.load(file)

    # Sicherstellen, dass der Ausgabeordner existiert
    os.makedirs(output_folder, exist_ok=True)

    # PDFs für jeden Kunden erstellen
    for customer in customers:
        customer_pdf_path = os.path.join(output_folder, f"{customer['name'].replace(' ', '_')}_invoice.pdf")
        create_customer_pdf(customer, customer_pdf_path)
