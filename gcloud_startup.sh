#!/bin/bash

# --- Helper Functions ---

# Function to log actions to a JSON file
log_resource() {
    local resource_type=$1
    local resource_name=$2
    local inventory_file="cloud_inventory.json"

    # Use a temporary file for safer JSON updates
    local temp_file=$(mktemp)

    # Add the resource to the corresponding array in the JSON file
    jq ".${resource_type} += [\"$resource_name\"]" "$inventory_file" > "$temp_file" && mv "$temp_file" "$inventory_file"
}

# --- Main Script ---

# 1. Check for gcloud installation
if ! command -v gcloud &> /dev/null; then
    echo "gcloud command could not be found. Please install the Google Cloud SDK and try again."
    exit 1
fi

# 2. Check for a configured project and log in if necessary
PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT" ]; then
    echo "No active Google Cloud project found."
    read -p "Would you like to log in and set a project? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gcloud auth login
        echo "Available projects:"
        gcloud projects list
        read -p "Please enter the PROJECT_ID you want to use: " PROJECT_ID
        gcloud config set project "$PROJECT_ID"
        PROJECT=$PROJECT_ID
    else
        echo "Please configure a project using 'gcloud config set project PROJECT_ID' and rerun this script."
        exit 1
    fi
fi
echo "Using Google Cloud project: $PROJECT"

# 3. Enable the Google Calendar API
API="calendar-json.googleapis.com"
echo "Enabling the Google Calendar API ($API)..."
gcloud services enable $API
if [ $? -eq 0 ]; then
    echo "API enabled successfully."
    log_resource "enabled_apis" "$API"
else
    echo "Failed to enable the Google Calendar API. Please check your permissions."
    exit 1
fi

# 4. Check for credentials.json and guide the user if it's missing
if [ -f "credentials.json" ]; then
    echo "'credentials.json' already exists. Setup complete."
else
    echo
    echo "--- Action Required: Create OAuth 2.0 Credentials ---"
    echo "This script cannot create 'credentials.json' for you automatically."
    echo "Please follow these steps in the Google Cloud Console:"
    echo
    echo "1. Go to the APIs & Services > Credentials page:"
    echo "   https://console.cloud.google.com/apis/credentials?project=$PROJECT"
    echo "2. Click '+ CREATE CREDENTIALS' and select 'OAuth client ID'."
    echo "3. If prompted, configure the consent screen. For 'User Type', select 'External' and create the screen with basic app info."
    echo "4. For 'Application type', select 'Desktop app'."
    echo "5. Give it a name (e.g., 'Calendar Sync Script')."
    echo "6. Click 'CREATE'. A window will appear with your client ID and secret."
    echo "7. Click the 'DOWNLOAD JSON' button on that screen (or from the credentials list)."
    echo "8. Save the downloaded file as 'credentials.json' in this directory:"
    echo "   /Users/cjbw/Documents/CODE/calendar_sync/"
    echo
    echo "After you have downloaded the file, you can run 'python main.py' to start the application."
    log_resource "oauth_clients" "Desktop client (manual creation required)"
fi