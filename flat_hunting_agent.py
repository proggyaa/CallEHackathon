import json
import os
from calle import CalleClient

# 1. Initialize CALL-E Client
client = CalleClient(api_key=os.environ["CALLE_API_KEY"])

# Target landlord's phone number in strict E.164 format
LANDLORD_PHONE = ""  # Replace with actual E.164 number

# 2. Define the pre-screening task instruction
task_prompt = (
    f"Call {LANDLORD_PHONE} regarding the apartment listing. "
    "Act as a friendly buyer's agent and ask the following 4 questions: "
    "1. Is the apartment still available for rent? "
    "2. What is the security deposit amount and monthly rent? "
    "3. Are pets allowed (specifically cats/dogs)? "
    "4. Can we schedule a viewing tour for tomorrow?"
)

# 3. Define the strict JSON Schema for output extraction
result_schema = {
    "type": "object",
    "required": [
        "is_available",
        "monthly_rent",
        "security_deposit",
        "pets_allowed",
        "tour_available",
        "landlord_notes",
    ],
    "properties": {
        "is_available": {"type": "boolean"},
        "monthly_rent": {"type": "string"},
        "security_deposit": {"type": "string"},
        "pets_allowed": {"type": "string", "enum": ["yes", "no", "conditional", "unknown"]},
        "tour_available": {"type": "boolean"},
        "landlord_notes": {"type": "string"},
    },
}

print(f"Initiating tenant pre-screening call to {LANDLORD_PHONE}...")

# 4. Trigger the call and await schema-valid structured results
call = client.calls.create_and_wait(
    task=task_prompt,
    result_schema=result_schema,
)

# 5. Output Tenant Scorecard
print("\n--- TENANT PRE-SCREENING SCORECARD ---")
print(f"Status: {call.get('status')}")
print(f"Task Completed: {call.get('task_completed')}")

if call.get("structured_result"):
    result = call["structured_result"]
    print("\nStructured Data Captured:")
    print(json.dumps(result, indent=2))
else:
    print("\nStructured result was null or could not be verified.")
    print(f"Evidence: {call.get('evidence')}")