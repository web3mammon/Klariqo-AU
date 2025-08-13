#!/usr/bin/env python3
"""
KLARIQO CONFIGURATION MODULE
Centralized configuration management for all API keys, constants, and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration class for Klariqo"""
    
    # ============================================================================
    # 🏢 CLIENT CONFIGURATION - EASY ADAPTATION FOR DIFFERENT CLIENTS
    # ============================================================================
    # To adapt this system for a new client, update these variables:
    CLIENT_CONFIG = {
        "business_name": "Pete's Plumbing",           # Your client's business name
        "ai_assistant_name": "Jason",                 # Name of the AI assistant
        "industry": "plumbing",                       # Industry type (plumbing, hotel, real_estate, etc.)
        "location": "Australia",                      # Country/region
        "city": "Melbourne",                          # Primary city
        "phone_number": "+61XXXXXXXXX",               # Client's phone number
        "website": "https://petesplumbing.com.au",    # Client's website
        "business_hours": "Mon-Fri 8AM-6PM, Sat 9AM-4PM",
        "emergency_available": True,                  # 24/7 emergency service
        "service_area": "Greater Melbourne",          # Service coverage area
        "currency": "AUD",                            # Currency for pricing
        "timezone": "Australia/Melbourne"             # Timezone for scheduling
    }
    
    # ============================================================================
    # 🌏 AUSTRALIAN TIMEZONE MAPPING - SUPPORT FOR ALL AUSTRALIAN CITIES
    # ============================================================================
    # Comprehensive mapping of Australian cities to their timezones
    # This allows the system to automatically use the correct timezone based on client location
    AUSTRALIAN_TIMEZONES = {
        # New South Wales (AEST/AEDT - UTC+10/+11)
        "Sydney": "Australia/Sydney",
        "Melbourne": "Australia/Melbourne", 
        "Canberra": "Australia/Sydney",
        "Newcastle": "Australia/Sydney",
        "Wollongong": "Australia/Sydney",
        "Central Coast": "Australia/Sydney",
        "Gold Coast": "Australia/Sydney",
        "Coffs Harbour": "Australia/Sydney",
        "Port Macquarie": "Australia/Sydney",
        "Tweed Heads": "Australia/Sydney",
        
        # Victoria (AEST/AEDT - UTC+10/+11)
        "Geelong": "Australia/Melbourne",
        "Ballarat": "Australia/Melbourne",
        "Bendigo": "Australia/Melbourne",
        "Shepparton": "Australia/Melbourne",
        "Mildura": "Australia/Melbourne",
        "Warrnambool": "Australia/Melbourne",
        "Albury": "Australia/Melbourne",
        "Wodonga": "Australia/Melbourne",
        
        # Queensland (AEST - UTC+10, NO daylight saving)
        "Brisbane": "Australia/Brisbane",
        "Gold Coast": "Australia/Brisbane",  # Note: Gold Coast is in QLD, not NSW
        "Townsville": "Australia/Brisbane",
        "Cairns": "Australia/Brisbane",
        "Toowoomba": "Australia/Brisbane",
        "Mackay": "Australia/Brisbane",
        "Rockhampton": "Australia/Brisbane",
        "Bundaberg": "Australia/Brisbane",
        "Hervey Bay": "Australia/Brisbane",
        "Sunshine Coast": "Australia/Brisbane",
        "Ipswich": "Australia/Brisbane",
        "Logan": "Australia/Brisbane",
        
        # South Australia (ACST/ACDT - UTC+9:30/+10:30)
        "Adelaide": "Australia/Adelaide",
        "Mount Gambier": "Australia/Adelaide",
        "Whyalla": "Australia/Adelaide",
        "Murray Bridge": "Australia/Adelaide",
        "Port Augusta": "Australia/Adelaide",
        "Port Pirie": "Australia/Adelaide",
        
        # Western Australia (AWST - UTC+8, NO daylight saving)
        "Perth": "Australia/Perth",
        "Fremantle": "Australia/Perth",
        "Rockingham": "Australia/Perth",
        "Mandurah": "Australia/Perth",
        "Albany": "Australia/Perth",
        "Bunbury": "Australia/Perth",
        "Geraldton": "Australia/Perth",
        "Kalgoorlie": "Australia/Perth",
        
        # Tasmania (AEST/AEDT - UTC+10/+11)
        "Hobart": "Australia/Hobart",
        "Launceston": "Australia/Hobart",
        "Devonport": "Australia/Hobart",
        "Burnie": "Australia/Hobart",
        
        # Northern Territory (ACST - UTC+9:30, NO daylight saving)
        "Darwin": "Australia/Darwin",
        "Alice Springs": "Australia/Darwin",
        "Palmerston": "Australia/Darwin",
        
        # Australian Capital Territory (AEST/AEDT - UTC+10/+11)
        "Canberra": "Australia/Sydney",  # ACT uses same timezone as NSW
        
        # Default fallback
        "default": "Australia/Sydney"
    }
    
    # Helper function to get timezone for any Australian city
    @staticmethod
    def get_australian_timezone(city_name):
        """
        Get the correct timezone for an Australian city
        
        Args:
            city_name (str): Name of the Australian city
            
        Returns:
            str: pytz timezone string (e.g., 'Australia/Sydney')
        """
        # Normalize city name (remove spaces, convert to title case)
        normalized_city = city_name.strip().title()
        
        # Check if city exists in our mapping
        if normalized_city in Config.AUSTRALIAN_TIMEZONES:
            return Config.AUSTRALIAN_TIMEZONES[normalized_city]
        
        # If not found, try partial matches
        for city, timezone in Config.AUSTRALIAN_TIMEZONES.items():
            if city_name.lower() in city.lower() or city.lower() in city_name.lower():
                return timezone
        
        # Fallback to default (Sydney timezone)
        print(f"⚠️  City '{city_name}' not found in timezone mapping. Using default: Australia/Sydney")
        return Config.AUSTRALIAN_TIMEZONES["default"]
    
    # ============================================================================
    # 📞 CALL FORWARDING CONFIGURATION
    # ============================================================================
    # Call forwarding settings for incoming calls
    CALL_FORWARDING = {
        "enabled": False,                             # Set to True to enable call forwarding
        "forward_to_number": "+61412345678",          # Number to forward calls to (client's existing number)
        "forward_message": "Please hold while I transfer you to our team.",  # Message before forwarding
        "timeout": 30                                 # Timeout in seconds for forwarded call
    }

    # ============================================================================
    # 👥 AGENT TRANSFER CONFIGURATION
    # ============================================================================
    # Agent transfer settings for "speak to agent" functionality
    AGENT_TRANSFER = {
        "enabled": True,                              # Set to True to enable agent transfer
        "agent_number": "+61412345678",               # Number to transfer to (same as forward_to_number usually)
        "transfer_message": "I'll transfer you to our team now. Please hold.",  # Message before transfer
        "transfer_timeout": 30,                       # Timeout in seconds for transfer
        "transfer_keywords": [                        # Keywords that trigger transfer
            "speak to agent", "human", "real person", "transfer", 
            "speak to someone", "talk to someone", "agent", "representative"
        ],
        "auto_transfer_conditions": [                 # Conditions for automatic transfer
            "emergency", "urgent", "complaint", "escalate"
        ]
    }
    
    # ============================================================================
    # 🎙️ VOICE & TTS CONFIGURATION
    # ============================================================================
    # ElevenLabs Voice Settings
    VOICE_ID = "uA0L9FxeLpzlG615Ueay"  # Jason's voice - Pete's Plumbing representative
    
    # Deepgram Settings
    DEEPGRAM_MODEL = "nova-2"
    DEEPGRAM_LANGUAGE = "en"  # English for Australian plumbing business
    
    # ============================================================================
    # 🔧 API KEYS - Loaded from environment variables
    # ============================================================================
    DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY') 
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE = os.getenv('TWILIO_PHONE')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Google Calendar Integration Configuration
    GOOGLE_CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')  # Default to primary calendar
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials/google-calendar-credentials.json')
    GOOGLE_CALENDAR_ENABLED = os.getenv('GOOGLE_CALENDAR_ENABLED', 'false').lower() == 'true'
    GOOGLE_CALENDAR_CACHE_DURATION = int(os.getenv('GOOGLE_CALENDAR_CACHE_DURATION', '300'))  # 5 minutes default
    
    # Business hours for calendar integration (in client's timezone)
    BUSINESS_HOURS = {
        "monday": {"start": "08:00", "end": "17:00"},
        "tuesday": {"start": "08:00", "end": "17:00"},
        "wednesday": {"start": "08:00", "end": "17:00"},
        "thursday": {"start": "08:00", "end": "17:00"},
        "friday": {"start": "08:00", "end": "17:00"},
        "saturday": {"start": "09:00", "end": "15:00"},
        "sunday": {"start": "00:00", "end": "00:00"}  # Closed
    }
    
    # Appointment duration settings
    APPOINTMENT_DURATION_MINUTES = int(os.getenv('APPOINTMENT_DURATION_MINUTES', '120'))  # 2 hours default
    APPOINTMENT_BUFFER_MINUTES = int(os.getenv('APPOINTMENT_BUFFER_MINUTES', '30'))  # 30 min buffer between appointments
    
    # Session Settings
    SILENCE_THRESHOLD = 0.4  # seconds before considering speech complete
    
    # Flask Settings
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = False
    
    # File Paths
    AUDIO_FOLDER = "audio_ulaw/"
    LOGS_FOLDER = "logs/"
    TEMP_FOLDER = "temp/"
    
    # Call Campaign Settings
    MAX_CONCURRENT_CALLS = 50
    CALL_INTERVAL = 10  # seconds between outbound calls
    
    # Session Memory Flags Template for Plumbing Business Context
    SESSION_FLAGS_TEMPLATE = {
        "intro_played": False,
        "services_explained": False, 
        "pricing_discussed": False,
        "availability_mentioned": False,
        "location_confirmed": False,
        "urgency_assessed": False,
        "contact_details_collected": False,
        "booking_confirmed": False,
        "experience_mentioned": False
    }
    
    # Dynamic Session Variables Template for Plumbing Business
    SESSION_VARIABLES_TEMPLATE = {
        "service_type": None,  # "blocked_drain", "leaking_tap", "toilet_repair", "hot_water", "emergency", "gas_fitting"
        "urgency_level": None,  # "emergency", "urgent", "routine", "flexible"
        "property_type": None,  # "residential", "commercial", "unit", "house"
        "customer_location": None,  # Suburb/area for scheduling
        "customer_name": None,  # Customer's name
        "customer_phone": None,  # Phone number for booking
        "preferred_date": None,  # "today", "tomorrow", "this_week", specific date
        "preferred_time": None,  # "morning", "afternoon", "evening", specific time
        "issue_description": None,  # Brief description of the plumbing issue
        "previous_customer": None,  # "yes", "no" - for repeat customer handling
        "selected_appointment": None  # Final booked appointment slot
    }
    
    # Manual Availability Data for August 2024 (Pete's Plumbing Schedule)
    AVAILABLE_DATES = [
        "Monday, August 5th",
        "Tuesday, August 6th", 
        "Wednesday, August 7th",
        "Thursday, August 8th",
        "Friday, August 9th",
        "Monday, August 12th",
        "Tuesday, August 13th",
        "Wednesday, August 14th",
        "Thursday, August 15th",
        "Friday, August 16th",
        "Monday, August 19th",
        "Tuesday, August 20th",
        "Wednesday, August 21st",
        "Thursday, August 22nd",
        "Friday, August 23rd",
        "Monday, August 26th",
        "Tuesday, August 27th",
        "Wednesday, August 28th",
        "Thursday, August 29th",
        "Friday, August 30th"
    ]
    
    AVAILABLE_TIMES = [
        "8:00 AM - 10:00 AM",
        "10:30 AM - 12:30 PM", 
        "1:00 PM - 3:00 PM",
        "3:30 PM - 5:30 PM"
    ]
    
    # Combined availability slots for easy booking
    PLUMBING_AVAILABILITY = {
        "available_slots": [
            {"date": "Monday, August 5th", "time": "8:00 AM - 10:00 AM", "slot_id": "MON05_0800"},
            {"date": "Monday, August 5th", "time": "10:30 AM - 12:30 PM", "slot_id": "MON05_1030"},
            {"date": "Monday, August 5th", "time": "1:00 PM - 3:00 PM", "slot_id": "MON05_1300"},
            {"date": "Tuesday, August 6th", "time": "8:00 AM - 10:00 AM", "slot_id": "TUE06_0800"},
            {"date": "Tuesday, August 6th", "time": "3:30 PM - 5:30 PM", "slot_id": "TUE06_1530"},
            {"date": "Wednesday, August 7th", "time": "10:30 AM - 12:30 PM", "slot_id": "WED07_1030"},
            {"date": "Wednesday, August 7th", "time": "1:00 PM - 3:00 PM", "slot_id": "WED07_1300"},
            {"date": "Thursday, August 8th", "time": "8:00 AM - 10:00 AM", "slot_id": "THU08_0800"},
            {"date": "Thursday, August 8th", "time": "3:30 PM - 5:30 PM", "slot_id": "THU08_1530"},
            {"date": "Friday, August 9th", "time": "10:30 AM - 12:30 PM", "slot_id": "FRI09_1030"},
            {"date": "Monday, August 12th", "time": "8:00 AM - 10:00 AM", "slot_id": "MON12_0800"},
            {"date": "Monday, August 12th", "time": "1:00 PM - 3:00 PM", "slot_id": "MON12_1300"},
            {"date": "Tuesday, August 13th", "time": "10:30 AM - 12:30 PM", "slot_id": "TUE13_1030"},
            {"date": "Tuesday, August 13th", "time": "3:30 PM - 5:30 PM", "slot_id": "TUE13_1530"},
            {"date": "Wednesday, August 14th", "time": "8:00 AM - 10:00 AM", "slot_id": "WED14_0800"},
            {"date": "Friday, August 16th", "time": "1:00 PM - 3:00 PM", "slot_id": "FRI16_1300"},
            {"date": "Friday, August 16th", "time": "3:30 PM - 5:30 PM", "slot_id": "FRI16_1530"}
        ],
        "last_updated": "2024-08-01 09:00 AM",
        "updated_by": "Jason (Pete's Plumbing)"
    }
    
    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            'DEEPGRAM_API_KEY',
            'ELEVENLABS_API_KEY'
        ]
        
        # Optional: Either OpenAI, Groq, or Gemini for AI (at least one required)
        ai_apis = ['OPENAI_API_KEY', 'GROQ_API_KEY', 'GEMINI_API_KEY']
        if not any(getattr(cls, api) for api in ai_apis):
            raise ValueError("At least one AI API key required: OPENAI_API_KEY, GROQ_API_KEY, or GEMINI_API_KEY")
        
        # Twilio for telephony (required)
        if not all([cls.TWILIO_ACCOUNT_SID, cls.TWILIO_AUTH_TOKEN]):
            raise ValueError("Twilio configuration required: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN")
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

# Validate configuration on import
Config.validate_config()