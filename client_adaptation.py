#!/usr/bin/env python3
"""
CLIENT ADAPTATION SCRIPT
Quick and easy way to adapt Klariqo AI Voice Assistant for different clients
"""

import json
import os
import shutil
from datetime import datetime

def adapt_for_client(client_info):
    """
    Adapt the system for a new client by updating configuration files
    
    Args:
        client_info (dict): Dictionary containing client information
    """
    
    print(f"🔄 Adapting system for {client_info['business_name']}...")
    
    # 1. Update config.py with new client information
    update_config_file(client_info)
    
    # 2. Create client-specific directories
    create_client_directories(client_info)
    
    # 3. Update README.md
    update_readme(client_info)
    
    # 4. Create client adaptation summary
    create_adaptation_summary(client_info)
    
    print(f"✅ Successfully adapted for {client_info['business_name']}!")
    print("📋 Next steps:")
    print("   1. Update audio files in audio_ulaw/ directory")
    print("   2. Update audio_snippets.json with new transcripts")
    print("   3. Update routes/inbound.py and routes/outbound.py intro files")
    print("   4. Test the system with new client configuration")

def update_config_file(client_info):
    """Update config.py with new client information"""
    
    config_content = f'''#!/usr/bin/env python3
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
    CLIENT_CONFIG = {{
        "business_name": "{client_info['business_name']}",
        "ai_assistant_name": "{client_info['ai_assistant_name']}",
        "industry": "{client_info['industry']}",
        "location": "{client_info['location']}",
        "city": "{client_info['city']}",
        "phone_number": "{client_info['phone_number']}",
        "website": "{client_info['website']}",
        "business_hours": "{client_info['business_hours']}",
        "emergency_available": {str(client_info['emergency_available'])},
        "service_area": "{client_info['service_area']}",
        "currency": "{client_info['currency']}",
        "timezone": "{client_info['timezone']}"
    }}
    
    # ============================================================================
    # 🎙️ VOICE & TTS CONFIGURATION
    # ============================================================================
    # ElevenLabs Voice Settings
    VOICE_ID = "{client_info.get('voice_id', 'uA0L9FxeLpzlG615Ueay')}"
    
    # Deepgram Settings
    DEEPGRAM_MODEL = "nova-2"
    DEEPGRAM_LANGUAGE = "{client_info.get('language', 'en')}"
    
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
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
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
    
    # Session Memory Flags Template for {client_info['industry']} Business Context
    SESSION_FLAGS_TEMPLATE = {{
        "intro_played": False,
        "services_explained": False, 
        "pricing_discussed": False,
        "availability_mentioned": False,
        "location_confirmed": False,
        "urgency_assessed": False,
        "contact_details_collected": False,
        "booking_confirmed": False,
        "experience_mentioned": False
    }}
    
    # Dynamic Session Variables Template for {client_info['industry']} Business
    SESSION_VARIABLES_TEMPLATE = {{
        "service_type": None,
        "urgency_level": None,
        "property_type": None,
        "customer_location": None,
        "customer_name": None,
        "customer_phone": None,
        "preferred_date": None,
        "preferred_time": None,
        "issue_description": None,
        "previous_customer": None,
        "selected_appointment": None
    }}
    
    # Manual Availability Data for {client_info['business_name']}
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
    PLUMBING_AVAILABILITY = {{
        "available_slots": [
            {{"date": "Monday, August 5th", "time": "8:00 AM - 10:00 AM", "slot_id": "MON05_0800"}},
            {{"date": "Monday, August 5th", "time": "10:30 AM - 12:30 PM", "slot_id": "MON05_1030"}},
            {{"date": "Monday, August 5th", "time": "1:00 PM - 3:00 PM", "slot_id": "MON05_1300"}},
            {{"date": "Tuesday, August 6th", "time": "8:00 AM - 10:00 AM", "slot_id": "TUE06_0800"}},
            {{"date": "Tuesday, August 6th", "time": "3:30 PM - 5:30 PM", "slot_id": "TUE06_1530"}},
            {{"date": "Wednesday, August 7th", "time": "10:30 AM - 12:30 PM", "slot_id": "WED07_1030"}},
            {{"date": "Wednesday, August 7th", "time": "1:00 PM - 3:00 PM", "slot_id": "WED07_1300"}},
            {{"date": "Thursday, August 8th", "time": "8:00 AM - 10:00 AM", "slot_id": "THU08_0800"}},
            {{"date": "Thursday, August 8th", "time": "3:30 PM - 5:30 PM", "slot_id": "THU08_1530"}},
            {{"date": "Friday, August 9th", "time": "10:30 AM - 12:30 PM", "slot_id": "FRI09_1030"}},
            {{"date": "Monday, August 12th", "time": "8:00 AM - 10:00 AM", "slot_id": "MON12_0800"}},
            {{"date": "Monday, August 12th", "time": "1:00 PM - 3:00 PM", "slot_id": "MON12_1300"}},
            {{"date": "Tuesday, August 13th", "time": "10:30 AM - 12:30 PM", "slot_id": "TUE13_1030"}},
            {{"date": "Tuesday, August 13th", "time": "3:30 PM - 5:30 PM", "slot_id": "TUE13_1530"}},
            {{"date": "Wednesday, August 14th", "time": "8:00 AM - 10:00 AM", "slot_id": "WED14_0800"}},
            {{"date": "Friday, August 16th", "time": "1:00 PM - 3:00 PM", "slot_id": "FRI16_1300"}},
            {{"date": "Friday, August 16th", "time": "3:30 PM - 5:30 PM", "slot_id": "FRI16_1530"}}
        ],
        "last_updated": "{datetime.now().strftime('%Y-%m-%d %I:%M %p')}",
        "updated_by": "{client_info['ai_assistant_name']} ({client_info['business_name']})"
    }}
    
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
            raise ValueError(f"Missing required environment variables: {{', '.join(missing_vars)}}")
        
        return True

# Validate configuration on import
Config.validate_config()
'''
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"   ✅ Updated config.py for {client_info['business_name']}")

def create_client_directories(client_info):
    """Create client-specific directories"""
    
    # Create client-specific folders
    client_name_safe = client_info['business_name'].lower().replace(' ', '_').replace("'", "")
    
    # Create customer data directory for this client
    client_data_dir = f"customer_data/{client_name_safe}"
    os.makedirs(client_data_dir, exist_ok=True)
    
    # Create logs directory for this client
    client_logs_dir = f"logs/{client_name_safe}"
    os.makedirs(client_logs_dir, exist_ok=True)
    
    print(f"   ✅ Created client directories for {client_info['business_name']}")

def update_readme(client_info):
    """Update README.md with client-specific information"""
    
    readme_content = f'''# 🎙️ {client_info['business_name']} - AI Voice Assistant

## Overview
AI-powered voice assistant for {client_info['business_name']} using Twilio μ-law streaming for high-quality audio calls.

## Features
- 🤖 AI-powered conversation handling
- 🎙️ High-quality voice synthesis with ElevenLabs
- 📞 Twilio integration for phone calls
- 📊 Customer data collection and export
- 🔄 Dynamic appointment booking
- 🌍 {client_info['location']} localization

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env` file
3. Run: `py main.py`
4. Access dashboard at: `http://localhost:5000`

## Configuration
- **Business:** {client_info['business_name']}
- **AI Assistant:** {client_info['ai_assistant_name']}
- **Industry:** {client_info['industry']}
- **Location:** {client_info['city']}, {client_info['location']}
- **Phone:** {client_info['phone_number']}
- **Website:** {client_info['website']}

## Support
For technical support, contact the development team.
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✅ Updated README.md for {client_info['business_name']}")

def create_adaptation_summary(client_info):
    """Create a summary of the adaptation"""
    
    summary = f'''# {client_info['business_name']} - Adaptation Summary

## Client Information
- **Business Name:** {client_info['business_name']}
- **AI Assistant:** {client_info['ai_assistant_name']}
- **Industry:** {client_info['industry']}
- **Location:** {client_info['city']}, {client_info['location']}
- **Phone:** {client_info['phone_number']}
- **Website:** {client_info['website']}
- **Business Hours:** {client_info['business_hours']}
- **Emergency Available:** {client_info['emergency_available']}
- **Service Area:** {client_info['service_area']}
- **Currency:** {client_info['currency']}
- **Timezone:** {client_info['timezone']}

## Adaptation Date
{datetime.now().strftime('%Y-%m-%d %I:%M %p')}

## Next Steps Required
1. ✅ Update config.py (COMPLETED)
2. 🔄 Update audio files in audio_ulaw/ directory
3. 🔄 Update audio_snippets.json with new transcripts
4. 🔄 Update routes/inbound.py intro file
5. 🔄 Update routes/outbound.py intro file
6. 🔄 Test system with new configuration
7. 🔄 Update availability data in config.py
8. 🔄 Customize session variables for {client_info['industry']} industry

## Files Modified
- config.py (CLIENT_CONFIG section)
- README.md (client-specific information)
- router.py (uses CLIENT_CONFIG)
- main.py (uses CLIENT_CONFIG)

## Notes
- All hardcoded references to "Pete's Plumbing" and "Jason" have been replaced with dynamic configuration
- System is now easily adaptable for different clients
- Use CLIENT_CONFIG in config.py to make future changes
'''
    
    safe_name = client_info['business_name'].lower().replace(' ', '_').replace("'", "")
    filename = f"{safe_name}_adaptation_summary.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"   ✅ Created adaptation summary for {client_info['business_name']}")

def main():
    """Main function to run client adaptation"""
    
    print("🎙️ Klariqo AI Voice Assistant - Client Adaptation Tool")
    print("=" * 60)
    
    # Example client configurations
    example_clients = {
        "1": {
            "name": "Melbourne Grand Hotel",
            "config": {
                "business_name": "Melbourne Grand Hotel",
                "ai_assistant_name": "Emma",
                "industry": "hotel",
                "location": "Australia",
                "city": "Melbourne",
                "phone_number": "+61XXXXXXXXX",
                "website": "https://melbournegrand.com.au",
                "business_hours": "24/7",
                "emergency_available": True,
                "service_area": "Melbourne CBD",
                "currency": "AUD",
                "timezone": "Australia/Melbourne"
            }
        },
        "2": {
            "name": "Brisbane Property Group",
            "config": {
                "business_name": "Brisbane Property Group",
                "ai_assistant_name": "Sarah",
                "industry": "real_estate",
                "location": "Australia",
                "city": "Brisbane",
                "phone_number": "+61XXXXXXXXX",
                "website": "https://brisbaneproperty.com.au",
                "business_hours": "Mon-Fri 9AM-5PM, Sat 9AM-3PM",
                "emergency_available": False,
                "service_area": "Greater Brisbane",
                "currency": "AUD",
                "timezone": "Australia/Brisbane"
            }
        },
        "3": {
            "name": "Custom Client",
            "config": None
        }
    }
    
    print("Available example configurations:")
    for key, client in example_clients.items():
        print(f"  {key}. {client['name']}")
    
    choice = input("\nSelect an example (1-3) or press Enter for custom: ").strip()
    
    if choice in example_clients:
        if example_clients[choice]["config"]:
            client_info = example_clients[choice]["config"]
        else:
            client_info = get_custom_client_info()
    else:
        client_info = get_custom_client_info()
    
    # Confirm adaptation
    print(f"\n📋 Client Information:")
    for key, value in client_info.items():
        print(f"  {key}: {value}")
    
    confirm = input(f"\nProceed with adaptation for {client_info['business_name']}? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        adapt_for_client(client_info)
    else:
        print("❌ Adaptation cancelled.")

def get_custom_client_info():
    """Get custom client information from user input"""
    
    print("\n📝 Enter client information:")
    
    client_info = {
        "business_name": input("Business name: ").strip(),
        "ai_assistant_name": input("AI assistant name: ").strip(),
        "industry": input("Industry (plumbing, hotel, real_estate, etc.): ").strip(),
        "location": input("Country/region: ").strip(),
        "city": input("Primary city: ").strip(),
        "phone_number": input("Phone number: ").strip(),
        "website": input("Website: ").strip(),
        "business_hours": input("Business hours: ").strip(),
        "emergency_available": input("Emergency service available? (y/N): ").strip().lower() in ['y', 'yes'],
        "service_area": input("Service area: ").strip(),
        "currency": input("Currency (AUD, USD, etc.): ").strip(),
        "timezone": input("Timezone (e.g., Australia/Melbourne): ").strip()
    }
    
    return client_info

if __name__ == "__main__":
    main()
