from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

output_folder = "../data/templates/"

# Templates-Definitionen
def create_invoice_template(c):
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Rechnung")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Name:")
    c.drawString(150, height - 100, "_________________________")

    c.drawString(50, height - 120, "Adresse:")
    c.drawString(150, height - 120, "_________________________")

    c.drawString(50, height - 140, "Telefon:")
    c.drawString(150, height - 140, "_________________________")

    c.drawString(50, height - 160, "E-Mail:")
    c.drawString(150, height - 160, "_________________________")

    c.drawString(50, height - 180, "Rechnungsnummer:")
    c.drawString(200, height - 180, "_________________________")

    c.drawString(50, height - 200, "Rechnungsdatum:")
    c.drawString(200, height - 200, "_________________________")

    c.drawString(50, height - 220, "Produkte:")
    y = height - 240
    for i in range(1, 6):  # Bis zu 5 Produkte
        c.drawString(50, y, f"{i}. _____________________ Menge: ____ Preis: ____ EUR")
        y -= 20

    c.drawString(50, y, "Gesamtbetrag:")
    c.drawString(200, y, "_________________________")
    y -= 20

    c.drawString(50, y, "Zahlungsziel:")
    c.drawString(200, y, "_________________________")




def create_contract_template(c):
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Vertrag")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Vertragspartner:")
    c.drawString(200, height - 100, "_________________________")

    c.drawString(50, height - 120, "Vertragsnummer:")
    c.drawString(200, height - 120, "_________________________")

    c.drawString(50, height - 140, "Vertragsdatum:")
    c.drawString(200, height - 140, "_________________________")

    c.drawString(50, height - 160, "Bedingungen:")
    c.drawString(50, height - 180, "1. ____________________________")
    c.drawString(50, height - 200, "2. ____________________________")
    c.drawString(50, height - 220, "3. ____________________________")

    c.drawString(50, height - 260, "Unterschrift:")
    c.drawString(200, height - 260, "_________________________")

# Hauptlogik
def create_pdf_template(template_type, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)

    if template_type == "invoice":
        create_invoice_template(c)
    elif template_type == "contract":
        create_contract_template(c)
    else:
        print(f"Unbekannter Template-Typ: {template_type}")
        return

    c.save()
    print(f"PDF-Template '{template_type}' erstellt: {output_path}")

# Generiere Templates
if __name__ == "__main__":
    os.makedirs(output_folder, exist_ok=True)
    create_pdf_template("invoice", os.path.join(output_folder, "invoice_template.pdf"))
    create_pdf_template("contract", os.path.join(output_folder, "contract_template.pdf"))
