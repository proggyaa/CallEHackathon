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


from datetime import datetime, timedelta, timezone

def get_available_slots(hours_ahead=48, slot_duration_minutes=30):
    service = get_calendar_service()
    
    # Query window starting from now
    now = datetime.now(timezone.utc)
    end_time = now + timedelta(hours=hours_ahead)
    
    # Fetch existing busy blocks
    body = {
        "timeMin": now.isoformat(),
        "timeMax": end_time.isoformat(),
        "timeZone": "UTC",
        "items": [{"id": "primary"}]
    }
    
    freebusy_result = service.freebusy().query(body=body).execute()
    busy_intervals = freebusy_result["calendars"]["primary"]["busy"]
    
    # Convert ISO strings to datetime objects
    busy_list = []
    for interval in busy_intervals:
        start = datetime.fromisoformat(interval["start"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(interval["end"].replace("Z", "+00:00"))
        busy_list.append((start, end))

    # Candidate slot search (checking working hours 9 AM - 6 PM local)
    available_slots = []
    candidate = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    while candidate < end_time and len(available_slots) < 2:
        candidate_end = candidate + timedelta(minutes=slot_duration_minutes)
        
        # Check for overlaps with existing busy blocks
        is_busy = False
        for busy_start, busy_end in busy_list:
            if max(candidate, busy_start) < min(candidate_end, busy_end):
                is_busy = True
                break
                
        # Only accept slots during normal hours (9:00 - 18:00)
        if not is_busy and 9 <= candidate.hour < 18:
            formatted_slot = candidate.strftime("%A at %I:%M %p")
            available_slots.append(formatted_slot)
            
        candidate += timedelta(minutes=30)
        
    return available_slots

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