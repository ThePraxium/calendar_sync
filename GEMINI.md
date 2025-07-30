Project Goal: Modular Google Calendar Aggregator
The objective is to create a Python script that aggregates multiple Google Calendars into a single, consolidated "master" view. This script should be designed for local execution, run manually, and prioritize user privacy by only displaying minimal event information.

Core Principles & Strategy
Consolidation Strategy: The script will create a new, dedicated Google Calendar (e.g., named "Consolidated View") to serve as the aggregation target. It will not sync events across existing calendars. This approach prevents cluttering primary calendars, avoids complex two-way sync logic, and makes it easy to clear and re-sync events without affecting the source calendars.

Modularity: The script must be modular. The user will specify the source calendars to be aggregated via a simple configuration file (calendars.json). This allows the user to easily add or remove calendars from the aggregation process without modifying the script's code.

Privacy First: When an event is copied from a source calendar to the consolidated calendar, the new event's title must be set to "Busy". No other details (like description, attendees, location, or original title) should be included. The only data that should be preserved are the event's start and end times.

Manual Sync: The script must only run when the user explicitly executes it from the command line. It should perform a one-time sync for the upcoming 365 days and then terminate. There will be no background processes or automated scheduling.

Local Environment: The entire setup is intended to run on a local machine. It will use Python and require the standard Google API client libraries.

Technical Implementation Details
1. Setup & Configuration
calendars.json file: The script should read its configuration from a file named calendars.json. This file will contain the IDs of the source calendars.

Example calendars.json:

{
  "source_calendar_ids": [
    "primary",
    "work.email@example.com",
    "abcdef123456@group.calendar.google.com"
  ],
  "target_calendar_name": "Consolidated View"
}

Authentication: Use the Google Calendar API v3 with OAuth 2.0.

The script should look for a credentials.json file (downloaded from the Google Cloud Console).

On the first run, it must guide the user through the browser-based OAuth consent flow and then save the resulting token in a token.json file for future runs.

These sensitive files (credentials.json, token.json) should be included in a .gitignore file.

2. Script Execution Flow
Initialize: Start the script.

Authenticate: Authenticate with the Google Calendar API using the credentials.json and token.json files.

Read Config: Load the source_calendar_ids and target_calendar_name from calendars.json.

Handle Target Calendar:

Check if a calendar with the target_calendar_name already exists in the user's account.

If it exists: Get its ID and proceed to delete all events currently in it. This ensures a fresh sync and prevents duplicates from previous runs.

If it does not exist: Create the new calendar with the specified name and get its ID.

Fetch & Sync Events:

Define a time range for the sync: from the current time (now) to 365 days in the future.

Iterate through each calendar_id in the source_calendar_ids list.

For each source calendar, fetch all events within the defined time range.

For each event fetched from a source calendar:

Create a new event object for the target calendar.

Set the summary (title) to "Busy".

Set the start and end times to match the original event's times.

Insert this new "Busy" event into the target calendar.

Report & Exit: Once all source calendars have been processed, print a summary message to the console (e.g., "Sync complete. Synced events from 3 calendars to 'Consolidated View'.") and exit the script.

3. Required Libraries
The Python script will require the following libraries. Please include a requirements.txt file.

google-api-python-client

google-auth-httplib2

google-auth-oauthlib

4. File Structure
Please generate the project with the following file structure:

/calendar-aggregator
|-- main.py
|-- calendars.json
|-- requirements.txt
|-- .gitignore
|-- README.md
