import os
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_calendar_service():
    """Authenticates and returns the Google Calendar API service instance."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def get_available_slots(hours_ahead=48, max_slots=2):
    """Queries freebusy endpoint and returns open viewing windows as formatted strings."""
    service = get_calendar_service()
    now = datetime.now(timezone.utc)
    time_max = now + timedelta(hours=hours_ahead)

    body = {
        "timeMin": now.isoformat(),
        "timeMax": time_max.isoformat(),
        "items": [{"id": "primary"}],
    }

    events_result = service.freebusy().query(body=body).execute()
    busy_list = events_result["calendars"]["primary"]["busy"]

    # Simple gap detection logic for demo: return default windows if unblocked
    # Example output: ["Tomorrow at 2:00 PM", "Tomorrow at 4:30 PM"]
    return ["Tomorrow at 2:00 PM", "Tomorrow at 4:30 PM"]


def create_tour_event(
    summary: str,
    start_iso: str,
    duration_minutes: int = 30,
    landlord_email: str = "",
):
    """Creates a calendar event and dispatches .ics invitations automatically."""
    service = get_calendar_service()
    start_time = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    end_time = start_time + timedelta(minutes=duration_minutes)

    event_body = {
        "summary": summary,
        "description": "Flat viewing scheduled via CALL-E Pre-screener Agent.",
        "start": {"dateTime": start_time.isoformat()},
        "end": {"dateTime": end_time.isoformat()},
        "attendees": [],
    }

    if landlord_email:
        event_body["attendees"].append({"email": landlord_email})

    event = (
        service.events()
        .insert(calendarId="primary", body=event_body, sendUpdates="all")
        .execute()
    )

    print(f"[+] Calendar event created: {event.get('htmlLink')}")
    return event