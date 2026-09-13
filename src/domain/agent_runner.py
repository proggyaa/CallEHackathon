import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from calle import CalleClient
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parents[2]
sys.path.append(str(PROJECT_ROOT))
from src.database.db_manager import save_call_result
from src.config.schemas.prescreen_schema import PRESCREEN_RESULT_SCHEMA
from src.utils.calendar_helper import create_tour_event, get_available_slots
from src.utils.mock_loader import load_mock_call_response
from src.utils.prompt_loader import build_prescreen_prompt

load_dotenv()

MOCK_CALL = False

def load_renter_prefs() -> dict:
    """Loads saved preferences from the frontend Streamlit dashboard."""
    prefs_path = PROJECT_ROOT / "data" / "user" / "renter_prefs.json"
    if prefs_path.exists():
        with open(prefs_path, "r") as f:
            return json.load(f)
    return {"must_haves": [], "negotiables": []}

def prescreen_landlord(
    phone: str,
    address: str,
    max_budget: str = "$2,400",
    max_deposit: str = "$2,400",
    user_slots: list[str] | None = None,
    offset_minutes: int = 0,
):
    api_key = os.environ.get("CALLE_API_KEY")

    if not MOCK_CALL:
        if not api_key:
            print(
                "Error: CALLE_API_KEY environment variable missing.",
                file=sys.stderr,
            )
            sys.exit(1)
        assert api_key is not None

    # Resolve slots: use user input if provided, otherwise fetch from calendar
    if user_slots and len(user_slots) >= 2:
        slot_1, slot_2 = user_slots[0], user_slots[1]
    else:
        print("[*] Fetching open slots from Google Calendar...")
        open_slots = get_available_slots(hours_ahead=48)
        slot_1 = open_slots[0] if len(open_slots) > 0 else "Tomorrow at 2:00 PM"
        slot_2 = open_slots[1] if len(open_slots) > 1 else "Tomorrow at 4:30 PM"

    # After resolving slots...
    prefs = load_renter_prefs()
    must_haves_str = ", ".join(prefs.get("must_haves", [])) or "None strictly required"
    negotiables_str = ", ".join(prefs.get("negotiables", [])) or "None specified"

    task_prompt = build_prescreen_prompt(
        phone=phone,
        address=address,
        max_budget=max_budget,
        max_deposit=max_deposit,
        slot_1=slot_1,
        slot_2=slot_2,
        must_haves=must_haves_str,      # New parameter
        negotiables=negotiables_str     # New parameter
    )
    
    if MOCK_CALL:
        print(
            "\n--- [MOCK MODE ENABLED] Loading mock response from tests/fixtures/mock_response.json ---"
        )
        call = load_mock_call_response()
        if call.get("structured_result"):
            staggered_time = datetime.now(timezone.utc) + timedelta(days=1, minutes=offset_minutes)
            call["structured_result"]["agreed_tour_iso"] = staggered_time.isoformat()
    else:
        client = CalleClient(api_key=api_key or "")
        print(f"[*] Initiating CALL-E agent for target: {phone} ({address})...")
        call = client.calls.create_and_wait(
            task=task_prompt, result_schema=PRESCREEN_RESULT_SCHEMA
        )

    print("\n[+] Call Execution Complete.")

    result = call.get("structured_result")
    if result:
        save_call_result(phone=phone, address=address, result=result)

        if result.get("tour_confirmed") and result.get("agreed_tour_iso"):
            print("\n[+] Tour confirmed! Creating Google Calendar event...")
            create_tour_event(
                summary=f"Flat Viewing: {address}",
                start_iso=result["agreed_tour_iso"],
            )

        print("\n[+] Structured Scorecard Saved:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    # Sample call to run the prescreen_landlord function directly for testing
    prescreen_landlord(
        phone="+15550001004",
        address="101 Example Street, Apt 4B",
        max_budget="$2,400",
        max_deposit="$2,400",
    )