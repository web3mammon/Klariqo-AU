# Google Calendar Credentials Setup

This directory contains Google Calendar API credentials for the Klariqo AI assistant.

## Setup Instructions

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable the Google Calendar API

### 2. Create Service Account
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details
4. Download the JSON credentials file

### 3. Configure Calendar Access
1. Rename the downloaded file to `google-calendar-credentials.json`
2. Place it in this directory
3. Share your Google Calendar with the service account email

### 4. Environment Variables
Add these to your `.env` file:
```
GOOGLE_CALENDAR_ENABLED=true
GOOGLE_CALENDAR_ID=primary
GOOGLE_CREDENTIALS_FILE=credentials/google-calendar-credentials.json
```

## File Structure
```
credentials/
├── README.md                           # This file
├── google-calendar-credentials.json    # Your credentials (not in git)
└── .gitkeep                           # Keep directory in git
```

## Security Notes
- Never commit credentials to git
- The credentials file is in `.gitignore`
- Keep credentials secure and rotate regularly
