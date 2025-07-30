# Google Calendar Aggregator

This script aggregates multiple Google Calendars into a single "master" view. It creates a new calendar and populates it with "Busy" events corresponding to the events in your source calendars.

## Setup

1.  **Enable the Google Calendar API:** Follow the instructions in the [Google Calendar API Python Quickstart](https://developers.google.com/calendar/api/quickstart/python) to enable the API and download your `credentials.json` file.
2.  **Install dependencies:** `pip install -r requirements.txt`
3.  **Configure calendars:** Edit `calendars.json` to include the calendar IDs you want to aggregate.
4.  **Run the script:** `python main.py`

