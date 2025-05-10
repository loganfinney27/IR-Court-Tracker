# scraper/pipeline.py
import csv
import os


def write_to_csv(new_rows, filename="output.csv"):
    if not new_rows:
        print("No data to write.")
        return

    fieldnames = ["Court", "Case", "Topic", "Original", "Latest", "Tag"]

    # Step 1: Load existing rows into a dict
    existing_data = {}
    if os.path.exists(filename):
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_data[row["Case"]] = row

    # Step 2: Update existing data only if the new value is not "N/A"
    for new_row in new_rows:
        case_key = new_row["Case"]
        old_row = existing_data.get(case_key, {})
        merged_row = {}

        for field in fieldnames:
            new_val = new_row.get(field, "N/A")
            old_val = old_row.get(field, "N/A")
            # Keep old if new is "N/A"
            merged_row[field] = new_val if new_val != "N/A" else old_val

        existing_data[case_key] = merged_row

    # Step 3: Write final rows
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data.values())

    print(f"Saved {len(existing_data)} rows to {filename}")
