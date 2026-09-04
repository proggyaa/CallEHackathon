import argparse
import csv
import json
import os
from prescreen_runner import prescreen_landlord


def run_batch(csv_file: str, output_file: str):
    if not os.path.exists(csv_file):
        print(f"Error: CSV file {csv_file} not found.")
        return

    results = []
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            phone = row.get("phone")
            address = row.get("address", "Rental Unit")
            if phone:
                print(f"\n--- Processing {address} ({phone}) ---")
                res = prescreen_landlord(phone, address)
                results.append(
                    {"phone": phone, "address": address, "result": res}
                )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Batch complete. Scorecards saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch flat pre-screening runner"
    )
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument(
        "--output", default="batch_results.json", help="Path to output JSON file"
    )
    args = parser.parse_args()
    run_batch(args.input, args.output)