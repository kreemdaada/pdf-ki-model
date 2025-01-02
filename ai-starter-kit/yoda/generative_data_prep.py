import os
import json

def preprocess_data(input_file, output_path, max_seq_length=4096, shuffle=True):
    os.makedirs(output_path, exist_ok=True)
    processed_file = os.path.join(output_path, "preprocessed_data.jsonl")
    
    with open(input_file, "r") as infile, open(processed_file, "w") as outfile:
        for line in infile:
            data = json.loads(line)
            text = data.get("text", "")
            # Truncate text to max sequence length
            truncated_text = text[:max_seq_length]
            processed_entry = {
                "text": truncated_text,
                "label": data.get("label", {})
            }
            json.dump(processed_entry, outfile)
            outfile.write("\n")
    
    print(f"Preprocessing abgeschlossen: {processed_file}")

if __name__ == "__main__":
    input_path = "../data_extraction/data/training_data.jsonl"
    output_dir = "./data/output/preprocessed"
    preprocess_data(input_path, output_dir)
