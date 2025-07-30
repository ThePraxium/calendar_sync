# Path: /Users/cjbw/Documents/CODE/calendar_sync/main.py
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Read configuration from calendars.json
        with open('calendars.json') as f:
            config = json.load(f)
        
        source_calendar_ids = config['source_calendar_ids']
        target_calendar_name = config['target_calendar_name']

        # Handle target calendar
        calendar_list = service.calendarList().list().execute()
        target_calendar_id = None
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == target_calendar_name:
                target_calendar_id = calendar_list_entry['id']
                # Clear existing events from the target calendar
                events_to_delete = service.events().list(calendarId=target_calendar_id).execute()
                for event in events_to_delete.get('items', []):
                    service.events().delete(calendarId=target_calendar_id, eventId=event['id']).execute()
                break
        
        if not target_calendar_id:
            # Create the target calendar if it doesn't exist
            calendar = {
                'summary': target_calendar_name,
                'timeZone': 'America/Los_Angeles' # Replace with your timezone
            }
            created_calendar = service.calendars().insert(body=calendar).execute()
            target_calendar_id = created_calendar['id']

        # Fetch and sync events
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat() + "Z"

        for source_id in source_calendar_ids:
            events_result = (
                service.events()
                .list(
                    calendarId=source_id,
                    timeMin=now,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print(f"No upcoming events found in calendar {source_id}.")
                continue
            
            for event in events:
                event_body = {
                    'summary': 'Busy',
                    'start': event['start'],
                    'end': event['end'],
                }
                service.events().insert(calendarId=target_calendar_id, body=event_body).execute()

        print(f"Sync complete. Synced events from {len(source_calendar_ids)} calendars to '{target_calendar_name}'.")


    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
