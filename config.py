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
    
    # API Keys - loaded from environment variables
    DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY') 
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE = os.getenv('TWILIO_PHONE')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # ElevenLabs Voice Settings
    VOICE_ID = "uA0L9FxeLpzlG615Ueay"  # Jason's voice - Pete's Plumbing representative
    
    # Deepgram Settings
    DEEPGRAM_MODEL = "nova-2"
    DEEPGRAM_LANGUAGE = "en"  # English for Australian plumbing business
    
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