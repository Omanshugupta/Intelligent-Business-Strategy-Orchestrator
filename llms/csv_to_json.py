import pandas as pd
import json
import os

def convert_csv_to_json(csv_path, output_path="data/company_data.json"):
    df = pd.read_csv(csv_path)

    data = {}
    for _, row in df.iterrows():
        key = row["field"]
        value = row["value"]

        try:
            value = int(value)
        except:
            try:
                value = float(value)
            except:
                pass

        data[key] = value

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    return data
