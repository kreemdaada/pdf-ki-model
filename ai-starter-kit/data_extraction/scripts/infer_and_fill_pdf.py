from fpdf import FPDF
import json

MODEL_JSON = "../../yoda/output/trained_model/model.json"
OUTPUT_PDF = "../data/inference_filled.pdf"

def fill_pdf_with_model(model, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Beispieltext aus dem Modell
    example_data = model["example"]["label"]
    
    # Statische Felder
    pdf.cell(200, 10, txt="Rechnung", ln=True, align="C")
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Name: {example_data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Adresse: {example_data['address']}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon: {example_data['phone']}", ln=True)
    pdf.cell(200, 10, txt=f"E-Mail: {example_data['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Rechnungsnummer: {example_data['invoice_number']}", ln=True)
    pdf.cell(200, 10, txt=f"Rechnungsdatum: {example_data['invoice_date']}", ln=True)
    pdf.ln(5)
    
    # Produkte
    pdf.cell(200, 10, txt="Produkte:", ln=True)
    for product in example_data["products"]:
        pdf.cell(200, 10, txt=f"- {product['product_name']} "
                              f"(Menge: {product['quantity']}, "
                              f"Einzelpreis: {product['unit_price']}, "
                              f"Gesamt: {product['total']})", ln=True)
    
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Gesamtbetrag: {example_data['total_amount']}", ln=True)
    pdf.cell(200, 10, txt=f"Zahlungsziel: {example_data['payment_due']}", ln=True)
    pdf.cell(200, 10, txt=f"Kommentare: {example_data['comments']}", ln=True)

    pdf.output(output_pdf)
    print(f"PDF erfolgreich erstellt: {output_pdf}")

# Lade das Modell
with open(MODEL_JSON, "r") as model_file:
    model = json.load(model_file)

# Erstelle die ausgefüllte PDF
fill_pdf_with_model(model, OUTPUT_PDF)
