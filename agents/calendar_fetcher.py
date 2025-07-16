from googleapiclient.discovery import build
from datetime import datetime

def fetch_today_events(creds):
    service = build("calendar", "v3", credentials=creds)
    now = datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return [event['summary'] for event in events]
