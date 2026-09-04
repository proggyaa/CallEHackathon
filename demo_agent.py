import os
from calle import CalleClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# Initialize the client (ensure CALLE_API_KEY is set in your environment variables)
client = CalleClient(api_key=os.environ["CALLE_API_KEY"])

# Replace with your actual phone number in E.164 format (e.g., "+14155552671" or "+919876543210")
MY_PHONE_NUMBER = "Demo"

# Create a call task and block until execution finishes
call = client.calls.create_and_wait(
    task=f"Call {MY_PHONE_NUMBER} and ask whether they can hear clearly.",
    result_schema={
        "type": "object",
        "required": ["can_hear_clearly"],
        "properties": {
            "can_hear_clearly": {
                "type": "string",
                "enum": ["yes", "no", "unknown"],
            }
        },
    },
)

# Print the output summary
print(f"Status: {call['status']}")
print(f"Task Completed: {call['task_completed']}")
print(f"Result: {call['structured_result']}")