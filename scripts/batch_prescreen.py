import argparse
import csv
import json
import os
from prescreen_runner import prescreen_landlord

def process_record(row: dict, slots: list[str] | None, index: int) -> dict | None:
    """Processes a single CSV row entry."""
    phone = row.get("phone")
    address = row.get("address", "Rental Unit")
    if not phone:
        return None

    print(f"\n--- Processing {address} ({phone}) ---")
    res = prescreen_landlord(
        phone=phone,
        address=address,
        user_slots=slots,
        offset_minutes=index * 30,
    )
    return {"phone": phone, "address": address, "result": res}

def run_batch(csv_file: str, output_file: str, slots: list[str] | None = None) -> None:
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    with open(csv_file, mode="r", encoding="utf-8") as f:
        listings = list(csv.DictReader(f))

    results = [
        res for idx, row in enumerate(listings)
        if (res := process_record(row, slots, idx)) is not None
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[+] Batch complete. Saved {len(results)} scorecards to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch flat pre-screening runner.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", default="batch_results.json", help="Path to output JSON file")
    parser.add_argument("--slots", nargs="*", default=None, help="Optional custom time slots")
    args = parser.parse_args()

    run_batch(csv_file=args.input, output_file=args.output, slots=args.slots)