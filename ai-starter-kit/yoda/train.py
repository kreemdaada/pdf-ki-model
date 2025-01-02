import json
import os

def train_model(input_data, output_model):
    with open(input_data, "r", encoding="utf-8") as infile:
        data = [json.loads(line) for line in infile]
    
    print("Trainingsdaten geladen:", len(data), "Einträge")

    # Simuliere das Training
    model = {
        "model_name": "dummy_yoda_model",
        "status": "training_complete",
        "fields": ["name", "address", "phone", "email", "products", "total_amount", "payment_due"],
        "example": data[0] if data else {}  # Beispiel aus den Trainingsdaten
    }

    # Verzeichnis erstellen, falls nicht vorhanden
    os.makedirs(os.path.dirname(output_model), exist_ok=True)

    # Modell speichern
    with open(output_model, "w", encoding="utf-8") as outfile:
        json.dump(model, outfile, indent=4, ensure_ascii=False)
        print(f"Modell gespeichert unter: {output_model}")

# Pfade anpassen
input_data_path = "./data/output/preprocessed/preprocessed_data.jsonl"
output_model_path = "./output/trained_model/model.json"

if os.path.exists(input_data_path):
    train_model(input_data_path, output_model_path)
else:
    print(f"Fehler: Eingabedatei {input_data_path} nicht gefunden.")
