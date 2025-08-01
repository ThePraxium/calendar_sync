# Path: /Users/cjbw/Documents/CODE/calendar_sync/main.py
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tzlocal import get_localzone
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

        # --- List all available calendars for the user ---
        print("--- Your Accessible Calendars ---")
        all_calendars = service.calendarList().list().execute()
        for calendar_entry in all_calendars.get('items', []):
            summary = calendar_entry.get('summary')
            cal_id = calendar_entry.get('id')
            print(f"  Name: {summary}\n  ID: {cal_id}\n")
        print("---------------------------------\n")

        # Read configuration from calendars.json
        with open('calendars.json') as f:
            config = json.load(f)
        
        source_calendars = config['source_calendars']
        target_calendar_name = config['target_calendar_name']

        # Handle target calendar
        calendar_list = service.calendarList().list().execute()
        target_calendar_id = None
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == target_calendar_name:
                target_calendar_id = calendar_list_entry['id']
                print(f"Found target calendar '{target_calendar_name}' with ID: {target_calendar_id}")
                break
        
        if not target_calendar_id:
            # Create the target calendar if it doesn't exist
            calendar = {
                'summary': target_calendar_name,
                'timeZone': str(get_localzone())
            }
            created_calendar = service.calendars().insert(body=calendar).execute()
            target_calendar_id = created_calendar['id']
            print(f"Created new target calendar '{target_calendar_name}' with ID: {target_calendar_id}")

        # Fetch and sync events
        now = datetime.datetime.utcnow()
        time_min = (now - datetime.timedelta(days=30)).isoformat() + "Z"   # 30 days back
        time_max = (now + datetime.timedelta(days=365)).isoformat() + "Z"  # 365 days forward
        
        print(f"Syncing events from {time_min[:10]} to {time_max[:10]} (395 days total)")
        print("=" * 60)
        
        # Color mapping for Google Calendar (updated with correct IDs)
        color_map = {
            "eucalyptus": "2",  # Green
            "cobalt": "1",      # Blue (was "9" - let's try "1")
            "grape": "3",       # Purple
            "tomato": "11",     # Red
            "tangerine": "6",   # Orange
            "banana": "5",      # Yellow
            "basil": "2",       # Green (alternative)
            "sage": "2",        # Green (alternative)
            "peacock": "7",     # Turquoise
            "blueberry": "1",   # Lavender
            "lavender": "1",    # Lavender
            "cherry": "11"      # Red (alternative)
        }
        
        total_events_synced = 0

        for i, source_calendar in enumerate(source_calendars, 1):
            calendar_id = source_calendar['calendar_id']
            display_name = source_calendar['display_name']
            color_name = source_calendar.get('color', 'eucalyptus').lower()
            color_id = color_map.get(color_name, "2")  # Default to green if color not found
            
            print(f"[{i}/{len(source_calendars)}] Processing: {display_name} ({calendar_id})")
            print(f"    Color: {color_name} -> Google Calendar Color ID: {color_id}")
            print(f"    Fetching events from {time_min[:10]} to {time_max[:10]}...")
            
            try:
                events_result = (
                    service.events()
                    .list(
                        calendarId=calendar_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])

                print(f"    Found {len(events)} total events in calendar")
                
                if not events:
                    print(f"    ✓ No events to sync from {display_name}")
                    print()
                    continue
                
                # Debug: Show a sample of event dates to verify time range
                if len(events) > 0:
                    first_event = events[0]
                    last_event = events[-1]
                    first_date = first_event.get('start', {}).get('dateTime', first_event.get('start', {}).get('date', 'Unknown'))
                    last_date = last_event.get('start', {}).get('dateTime', last_event.get('start', {}).get('date', 'Unknown'))
                    print(f"    Date range: {first_date[:10]} to {last_date[:10]}")
                
                events_synced_for_calendar = 0
                
                for j, event in enumerate(events, 1):
                    # Show progress every 10 events or for small batches
                    if j % 10 == 0 or len(events) <= 20:
                        print(f"    Processing event {j}/{len(events)}...")
                    
                    # Handle both timed events (dateTime) and all-day events (date)
                    start_info = event.get('start', {})
                    end_info = event.get('end', {})
                    
                    # Create event body with proper start/end format
                    event_body = {
                        'summary': f'{display_name} - Busy',
                        'start': start_info,
                        'end': end_info,
                        'colorId': color_id
                    }
                    
                    service.events().insert(calendarId=target_calendar_id, body=event_body).execute()
                    events_synced_for_calendar += 1
                
                print(f"    ✓ Synced {events_synced_for_calendar} events from {display_name}")
                print(f"    Color applied: {color_name}")
                print()
                total_events_synced += events_synced_for_calendar
                
            except HttpError as calendar_error:
                print(f"    ✗ Error accessing calendar {display_name} ({calendar_id}): {calendar_error}")
                print()
                continue

        print("=" * 60)
        print(f"🎉 Sync complete!")
        print(f"   Total events synced: {total_events_synced}")
        print(f"   Source calendars processed: {len(source_calendars)}")
        print(f"   Target calendar: '{target_calendar_name}'")
        print(f"   Time range: 30 days back to 365 days forward")


    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
