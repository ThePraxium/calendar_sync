# Google Calendar Aggregator

This application aggregates multiple Google Calendars into a single "Consolidated View" calendar. It creates a master calendar and populates it with "Busy" events from your source calendars, with customizable colors and comprehensive sync capabilities.

## Features

- **Multi-Calendar Sync**: Aggregate events from multiple Google Calendars
- **Color-Coded Events**: Assign different colors to distinguish between source calendars  
- **Smart Date Range**: Syncs events from 30 days back to 365 days forward (395 days total)
- **Automatic Calendar Discovery**: Lists all accessible calendars to help with configuration
- **Flexible Event Handling**: Supports both timed events and all-day events
- **Progress Tracking**: Real-time sync progress with detailed logging
- **Cloud Deployment Ready**: Includes Google Cloud deployment scripts

## Project Structure

```
├── main.py              # Main synchronization script
├── calendars.json       # Calendar configuration file
├── requirements.txt     # Python dependencies
├── credentials.json     # Google API credentials (you provide)
├── token.json          # OAuth token (auto-generated)
├── gcloud_startup.sh   # Google Cloud deployment script
└── README.md           # This file
```

## Setup

### Prerequisites
- Python 3.7 or higher
- Google account with calendar access
- Google Cloud Project (for API access)

### Installation

1. **Enable the Google Calendar API:**
   - Follow the [Google Calendar API Python Quickstart](https://developers.google.com/calendar/api/quickstart/python)
   - Enable the Calendar API in your Google Cloud Console
   - Download your `credentials.json` file to the project root

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure calendars:**
   Edit `calendars.json` to specify your source calendars:
   ```json
   {
     "source_calendars": [
       {
         "calendar_id": "your.email@gmail.com",
         "display_name": "Personal",
         "color": "eucalyptus"
       },
       {
         "calendar_id": "work.email@company.com", 
         "display_name": "Work",
         "color": "cobalt"
       }
     ],
     "target_calendar_name": "Consolidated View"
   }
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## Configuration

### Calendar Colors
Available colors for visual distinction:
- `eucalyptus` (green)
- `cobalt` (blue) 
- `grape` (purple)
- `tomato` (red)
- `tangerine` (orange)
- `banana` (yellow)
- `peacock` (turquoise)
- `lavender` (light purple)

### First Run
On first execution, the script will:
1. Display all your accessible calendars with their IDs
2. Prompt for Google account authorization
3. Create the target "Consolidated View" calendar if it doesn't exist
4. Sync all events from configured source calendars

## Cloud Deployment

For automated scheduling, use the included Google Cloud deployment script:

```bash
chmod +x gcloud_startup.sh
./gcloud_startup.sh
```

This sets up the necessary cloud infrastructure for periodic synchronization.

## Output Example

```
--- Your Accessible Calendars ---
  Name: Personal
  ID: your.email@gmail.com

  Name: Work Calendar  
  ID: work.calendar@company.com
---------------------------------

Syncing events from 2024-07-01 to 2025-08-01 (395 days total)
============================================================
[1/2] Processing: Personal (your.email@gmail.com)
    Color: eucalyptus -> Google Calendar Color ID: 2
    Found 45 total events in calendar
    ✓ Synced 45 events from Personal

[2/2] Processing: Work (work.calendar@company.com)
    Color: cobalt -> Google Calendar Color ID: 1  
    Found 67 total events in calendar
    ✓ Synced 67 events from Work
============================================================
🎉 Sync complete!
   Total events synced: 112
   Source calendars processed: 2
   Target calendar: 'Consolidated View'
   Time range: 30 days back to 365 days forward
```

