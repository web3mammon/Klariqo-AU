#!/usr/bin/env python3
"""
KLARIQO GOOGLE CALENDAR INTEGRATION MODULE
Handles real-time calendar availability and booking for AI assistant
Works with existing Google Calendar setups - no calendar changes needed!
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pytz

# Google Calendar API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.exceptions import RefreshError
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False
    print("⚠️ Google Calendar API not available. Install with: pip install google-auth google-auth-oauthlib google-api-python-client")

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleCalendarClient:
    """Handles Google Calendar API integration for appointment booking with existing calendars"""
    
    def __init__(self):
        self.calendar_id = Config.GOOGLE_CALENDAR_ID
        self.credentials_file = Config.GOOGLE_CREDENTIALS_FILE
        self.service = None
        self.cache = {}
        self.cache_duration = Config.GOOGLE_CALENDAR_CACHE_DURATION
        self.business_hours = Config.BUSINESS_HOURS
        self.appointment_duration = Config.APPOINTMENT_DURATION_MINUTES
        self.buffer_minutes = Config.APPOINTMENT_BUFFER_MINUTES
        self.setup_status = "not_configured"
        
        # Initialize service if credentials are available
        if Config.GOOGLE_CALENDAR_ENABLED and GOOGLE_CALENDAR_AVAILABLE:
            self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Calendar service with credentials"""
        try:
            if not os.path.exists(self.credentials_file):
                logger.warning(f"⚠️ Google Calendar credentials file not found: {self.credentials_file}")
                logger.info("📋 Please set up Google Calendar credentials (see CLIENT_CALENDAR_SETUP_GUIDE.md)")
                self.setup_status = "credentials_missing"
                return False
            
            # Load credentials
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', Config.GOOGLE_CALENDAR_SCOPES)
            
            # If no valid credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except RefreshError:
                        logger.error("❌ Failed to refresh Google Calendar credentials")
                        self.setup_status = "credentials_expired"
                        return False
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, Config.GOOGLE_CALENDAR_SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            
            # Build the service
            self.service = build('calendar', 'v3', credentials=creds)
            
            # Test calendar access
            try:
                calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
                logger.info(f"✅ Connected to Google Calendar: {calendar.get('summary', 'Unknown')}")
                self.setup_status = "connected"
                return True
            except HttpError as e:
                if e.resp.status == 404:
                    logger.error(f"❌ Calendar not found: {self.calendar_id}")
                    logger.info("💡 Please check the calendar ID and ensure it's shared with the service account")
                    self.setup_status = "calendar_not_found"
                else:
                    logger.error(f"❌ Calendar access error: {e}")
                    self.setup_status = "access_denied"
                return False
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google Calendar service: {e}")
            self.setup_status = "initialization_failed"
            return False
    
    def get_available_slots(self, days_ahead: int = 7, service_type: str = "general") -> Dict:
        """
        Get available appointment slots from Google Calendar
        
        Args:
            days_ahead: Number of days to look ahead
            service_type: Type of service (for filtering if needed)
            
        Returns:
            Dict with available slots and metadata
        """
        try:
            # Check cache first
            cache_key = f"availability_{days_ahead}_{service_type}"
            if self._is_cache_valid(cache_key):
                logger.info(f"📋 Using cached availability for {service_type}")
                return self.cache[cache_key]["data"]
            
            if not self.service:
                logger.warning("⚠️ Google Calendar service not available, using fallback data")
                return self._get_fallback_availability()
            
            # Get current time in client's timezone
            client_timezone = Config.get_australian_timezone(Config.CLIENT_CONFIG["city"])
            tz = pytz.timezone(client_timezone)
            now = datetime.now(tz)
            
            # Calculate time range
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(days=days_ahead)
            
            # Get busy times from calendar
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Generate available slots
            available_slots = self._generate_available_slots(
                start_time, end_time, events, tz
            )
            
            # Format response
            response_data = {
                "available_slots": available_slots,
                "total_slots": len(available_slots),
                "date_range": {
                    "start": start_time.strftime("%Y-%m-%d"),
                    "end": end_time.strftime("%Y-%m-%d")
                },
                "timezone": client_timezone,
                "last_updated": datetime.now().isoformat(),
                "source": "google_calendar",
                "success": True
            }
            
            # Cache the result
            self.cache[cache_key] = {
                "data": response_data,
                "timestamp": time.time()
            }
            
            logger.info(f"✅ Fetched {len(available_slots)} available slots from Google Calendar")
            return response_data
            
        except HttpError as e:
            logger.error(f"❌ Google Calendar API error: {e}")
            return self._get_fallback_availability()
        except Exception as e:
            logger.error(f"❌ Unexpected error fetching calendar availability: {e}")
            return self._get_fallback_availability()
    
    def _generate_available_slots(self, start_time: datetime, end_time: datetime, 
                                 events: List, timezone: pytz.timezone) -> List[Dict]:
        """Generate available time slots based on business hours and existing events"""
        available_slots = []
        
        # Create busy time ranges from events
        busy_times = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            if 'T' in start:  # DateTime event
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                busy_times.append((start_dt, end_dt))
        
        # Generate slots for each day
        current_date = start_time
        while current_date < end_time:
            day_name = current_date.strftime("%A").lower()
            
            # Check if business is open on this day
            if day_name in self.business_hours:
                day_hours = self.business_hours[day_name]
                
                if day_hours["start"] != "00:00":  # Not closed
                    # Parse business hours
                    start_hour, start_minute = map(int, day_hours["start"].split(":"))
                    end_hour, end_minute = map(int, day_hours["end"].split(":"))
                    
                    # Create day start and end times
                    day_start = current_date.replace(hour=start_hour, minute=start_minute)
                    day_end = current_date.replace(hour=end_hour, minute=end_minute)
                    
                    # Generate time slots within business hours
                    slot_start = day_start
                    while slot_start + timedelta(minutes=self.appointment_duration) <= day_end:
                        slot_end = slot_start + timedelta(minutes=self.appointment_duration)
                        
                        # Check if slot conflicts with existing events
                        slot_available = True
                        for busy_start, busy_end in busy_times:
                            # Check for overlap
                            if (slot_start < busy_end and slot_end > busy_start):
                                slot_available = False
                                break
                        
                        if slot_available:
                            # Add buffer time check
                            buffer_start = slot_start - timedelta(minutes=self.buffer_minutes)
                            buffer_end = slot_end + timedelta(minutes=self.buffer_minutes)
                            
                            buffer_conflict = False
                            for busy_start, busy_end in busy_times:
                                if (buffer_start < busy_end and buffer_end > busy_start):
                                    buffer_conflict = True
                                    break
                            
                            if not buffer_conflict:
                                # Format slot for display
                                slot_display = slot_start.strftime("%A, %B %d") + " at " + slot_start.strftime("%I:%M %p")
                                
                                available_slots.append({
                                    "datetime": slot_start.isoformat(),
                                    "display": slot_display,
                                    "slot_id": f"{slot_start.strftime('%Y%m%d_%H%M')}",
                                    "duration_minutes": self.appointment_duration,
                                    "service_type": "general"
                                })
                        
                        # Move to next slot (with buffer)
                        slot_start += timedelta(minutes=self.appointment_duration + self.buffer_minutes)
            
            # Move to next day
            current_date += timedelta(days=1)
        
        return available_slots
    
    def book_appointment(self, slot_datetime: str, customer_info: Dict) -> Dict:
        """
        Book an appointment by creating a calendar event
        
        Args:
            slot_datetime: ISO format datetime string
            customer_info: Dictionary with customer details
            
        Returns:
            Dict with booking result
        """
        try:
            if not self.service:
                logger.error("❌ Google Calendar service not available")
                return {"success": False, "error": "Calendar service not available"}
            
            # Parse datetime
            start_time = datetime.fromisoformat(slot_datetime.replace('Z', '+00:00'))
            end_time = start_time + timedelta(minutes=self.appointment_duration)
            
            # Convert to client's timezone
            client_timezone = Config.get_australian_timezone(Config.CLIENT_CONFIG["city"])
            tz = pytz.timezone(client_timezone)
            start_time = start_time.astimezone(tz)
            end_time = end_time.astimezone(tz)
            
            # Create event description
            description = f"""
Customer: {customer_info.get('customer_name', 'N/A')}
Phone: {customer_info.get('customer_phone', 'N/A')}
Service: {customer_info.get('service_type', 'General')}
Location: {customer_info.get('customer_location', 'N/A')}
Issue: {customer_info.get('issue_description', 'N/A')}

Booked via: Klariqo AI Assistant
            """.strip()
            
            # Create calendar event
            event = {
                'summary': f"Appointment - {customer_info.get('service_type', 'Service')}",
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': client_timezone
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': client_timezone
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},       # 1 hour before
                    ],
                },
            }
            
            # Insert event
            event_result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                sendUpdates='all'  # Send notifications to attendees
            ).execute()
            
            # Clear cache to force refresh
            self.cache.clear()
            
            logger.info(f"✅ Appointment booked successfully: {event_result.get('id')}")
            
            return {
                "success": True,
                "booking_reference": event_result.get('id'),
                "event_link": event_result.get('htmlLink'),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "customer_name": customer_info.get('customer_name'),
                "service_type": customer_info.get('service_type')
            }
            
        except HttpError as e:
            logger.error(f"❌ Google Calendar API error during booking: {e}")
            return {"success": False, "error": f"Calendar API error: {e}"}
        except Exception as e:
            logger.error(f"❌ Unexpected error during booking: {e}")
            return {"success": False, "error": f"Booking error: {e}"}
    
    def _get_fallback_availability(self) -> Dict:
        """Get fallback availability data when Google Calendar is not available"""
        logger.info("📋 Using fallback availability data")
        
        # Use manual availability data from config
        available_slots = []
        for slot in Config.PLUMBING_AVAILABILITY.get("available_slots", []):
            available_slots.append({
                "datetime": f"2024-08-{slot['slot_id'].split('_')[0][-2:]}:00:00",
                "display": f"{slot['date']} at {slot['time']}",
                "slot_id": slot['slot_id'],
                "duration_minutes": self.appointment_duration,
                "service_type": "general"
            })
        
        return {
            "available_slots": available_slots,
            "total_slots": len(available_slots),
            "date_range": {"start": "2024-08-01", "end": "2024-08-31"},
            "timezone": Config.get_australian_timezone(Config.CLIENT_CONFIG["city"]),
            "last_updated": datetime.now().isoformat(),
            "source": "fallback_data",
            "success": True
        }
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cache_age = time.time() - self.cache[cache_key]["timestamp"]
        return cache_age < self.cache_duration
    
    def format_availability_for_speech(self, available_slots: List[Dict]) -> str:
        """Format available slots for speech output"""
        if not available_slots:
            return "I don't have any available appointments at the moment."
        
        # Take first 5 slots for speech
        speech_slots = available_slots[:5]
        slot_texts = []
        
        for slot in speech_slots:
            slot_texts.append(slot["display"])
        
        if len(available_slots) > 5:
            return f"I have appointments available at {', '.join(slot_texts)}, and a few more times. Which works best for you?"
        else:
            return f"I have appointments available at {', '.join(slot_texts)}. Which works best for you?"
    
    def get_calendar_status(self) -> Dict:
        """Get current status of calendar integration"""
        return {
            "enabled": Config.GOOGLE_CALENDAR_ENABLED,
            "service_available": GOOGLE_CALENDAR_AVAILABLE,
            "setup_status": self.setup_status,
            "calendar_id": self.calendar_id,
            "credentials_file": self.credentials_file,
            "service_initialized": self.service is not None,
            "cache_size": len(self.cache),
            "business_hours": self.business_hours,
            "appointment_duration": self.appointment_duration,
            "buffer_minutes": self.buffer_minutes
        }

# Initialize the calendar client
calendar_client = GoogleCalendarClient()

# Set up Google Calendar scopes
Config.GOOGLE_CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
