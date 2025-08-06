# 🔌 Klariqo AI - API Integration & Dynamic Data Guide

**Complete Developer Guide for Implementing Dynamic Data Systems**

*For Freelance VAs, Python Developers, and Technical Teams*

---

## 📖 **Table of Contents**

1. [Understanding the Current Architecture](#understanding-the-current-architecture)
2. [API Integration Implementation](#api-integration-implementation)
3. [Non-API Systems (Manual Updates)](#non-api-systems-manual-updates)
4. [Implementation Examples](#implementation-examples)
5. [Best Practices](#best-practices)
6. [Testing & Deployment](#testing--deployment)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ **Understanding the Current Architecture**

### **How Klariqo Currently Works**

Klariqo is a sophisticated AI voice assistant that:
- Receives customer calls via Twilio
- Uses Deepgram for speech-to-text
- Routes responses through AI (GPT/Gemini/Groq)
- Serves pre-recorded μ-law audio files for fast responses
- Falls back to TTS for dynamic content

### **Key Components for Dynamic Data**

```
📁 Current System Flow:
├── main.py              # Handles Twilio WebSocket connections
├── router.py            # AI decision-making & response selection
├── session.py           # Session memory & variables storage
├── config.py            # Configuration & templates
├── audio_manager.py     # Pre-recorded audio serving
└── tts_engine.py        # Dynamic text-to-speech fallback
```

### **Session Variables System (Your Foundation)**

The system already tracks dynamic data through session variables:

```python
# In config.py - Current session variables
SESSION_VARIABLES_TEMPLATE = {
    "admission_type": None,      # "firsttime" or "transfer"
    "admission_class": None,     # "KG1", "Class 1", etc.
    "student_location": None,    # Location for bus route
    "student_age": None,         # Age for eligibility
    "parent_name": None,         # Parent's name
    "student_name": None,        # Student's name
    "inquiry_focus": None        # "fees", "admission", "transport"
}
```

**This same pattern can be extended for ANY business type!**

---

## 🔌 **API Integration Implementation**

### **Scenario: Doctor's Office with API Support**

**Goal**: Customer calls asking for appointment → System fetches real-time availability → AI responds with actual available slots.

### **Step 1: Extend Session Variables**

```python
# In config.py - Add new variables for medical practice
SESSION_VARIABLES_TEMPLATE = {
    # Existing school variables...
    
    # NEW: Medical Practice Variables
    "requested_service": None,        # "dental", "consultation", "checkup"
    "preferred_date": None,           # "thursday", "friday", "next week"
    "preferred_time": None,           # "morning", "afternoon", "11:30 AM"
    "appointment_type": None,         # "new patient", "follow-up", "emergency"
    "doctor_preference": None,        # "Dr. Smith", "any doctor"
    "insurance_type": None,           # "Medicare", "private", "bulk billing"
    
    # API Data Storage
    "available_slots": [],            # Fetched from doctor's system
    "selected_slot": None,            # Customer's choice
    "booking_reference": None         # Confirmation number
}

# API Configuration
DOCTOR_API_URL = os.getenv('DOCTOR_API_URL')
DOCTOR_API_KEY = os.getenv('DOCTOR_API_KEY')
DOCTOR_API_TIMEOUT = 5  # seconds
```

### **Step 2: Create API Integration Module**

Create new file: `api_integrations.py`

```python
#!/usr/bin/env python3
"""
KLARIQO API INTEGRATIONS MODULE
Handles external API calls for dynamic data
"""

import requests
import json
import time
from datetime import datetime, timedelta
from config import Config

class DoctorAPIClient:
    """Handles integration with doctor's appointment system"""
    
    def __init__(self):
        self.api_url = Config.DOCTOR_API_URL
        self.api_key = Config.DOCTOR_API_KEY
        self.timeout = Config.DOCTOR_API_TIMEOUT
        self.cache = {}  # Simple caching to avoid repeated calls
        self.cache_duration = 300  # 5 minutes
    
    def fetch_availability(self, service_type="general", days_ahead=7):
        """
        Fetch doctor availability from external API
        
        Args:
            service_type: "dental", "consultation", "checkup"
            days_ahead: How many days to look ahead
            
        Returns:
            dict: {"available_slots": ["Thu 11:30 AM", "Fri 2:00 PM"], "success": True}
        """
        try:
            # Check cache first
            cache_key = f"{service_type}_{days_ahead}"
            if self._is_cache_valid(cache_key):
                print(f"📋 Using cached availability for {service_type}")
                return self.cache[cache_key]["data"]
            
            # Make API call
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "service_type": service_type,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d"),
                "format": "human_readable"  # Request human-friendly format
            }
            
            print(f"🔍 Fetching availability for {service_type}...")
            response = requests.post(
                f"{self.api_url}/availability",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache the result
                self.cache[cache_key] = {
                    "data": data,
                    "timestamp": time.time()
                }
                
                print(f"✅ Fetched {len(data.get('available_slots', []))} available slots")
                return data
            else:
                print(f"❌ API Error: {response.status_code}")
                return {"available_slots": [], "success": False, "error": "API_ERROR"}
                
        except requests.RequestException as e:
            print(f"❌ API Request failed: {e}")
            return {"available_slots": [], "success": False, "error": "CONNECTION_ERROR"}
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {"available_slots": [], "success": False, "error": "UNKNOWN_ERROR"}
    
    def book_appointment(self, slot_id, patient_info):
        """
        Book an appointment via API
        
        Args:
            slot_id: Unique identifier for the time slot
            patient_info: dict with patient details
            
        Returns:
            dict: {"booking_reference": "ABC123", "success": True}
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "slot_id": slot_id,
                "patient_info": patient_info,
                "booking_type": "phone_call"
            }
            
            response = requests.post(
                f"{self.api_url}/book",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Appointment booked: {data.get('booking_reference')}")
                return data
            else:
                return {"success": False, "error": "BOOKING_FAILED"}
                
        except Exception as e:
            print(f"❌ Booking error: {e}")
            return {"success": False, "error": "BOOKING_ERROR"}
    
    def _is_cache_valid(self, cache_key):
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cache_age = time.time() - self.cache[cache_key]["timestamp"]
        return cache_age < self.cache_duration
    
    def format_availability_for_speech(self, slots_data):
        """
        Convert API slots to natural speech format
        
        Args:
            slots_data: API response with available_slots
            
        Returns:
            str: "11:30 AM on Thursday and 2 PM on Friday"
        """
        if not slots_data.get("available_slots"):
            return "no appointments available this week"
        
        slots = slots_data["available_slots"]
        
        if len(slots) == 1:
            return slots[0]
        elif len(slots) == 2:
            return f"{slots[0]} and {slots[1]}"
        else:
            # More than 2 slots - pick first 2 and mention more available
            return f"{slots[0]}, {slots[1]}, and {len(slots)-2} more times"

# Global API client instance
doctor_api = DoctorAPIClient()
```

### **Step 3: Enhance Router for API Integration**

Update `router.py`:

```python
# Add this import at the top
from api_integrations import doctor_api

# Add this method to ResponseRouter class
def _handle_appointment_booking(self, user_input, session):
    """Handle appointment booking requests with real-time API data"""
    user_lower = user_input.lower()
    
    # Detect appointment request
    if any(word in user_lower for word in ["appointment", "booking", "book", "schedule"]):
        
        # Extract service type
        service_type = "general"  # default
        if "dental" in user_lower:
            service_type = "dental"
            session.update_session_variable("requested_service", "dental")
        elif "checkup" in user_lower:
            service_type = "checkup"
            session.update_session_variable("requested_service", "checkup")
        
        # Fetch real-time availability
        print(f"🔍 Fetching {service_type} appointments...")
        availability_data = doctor_api.fetch_availability(service_type)
        
        if availability_data.get("success", True) and availability_data.get("available_slots"):
            # Store in session
            session.update_session_variable("available_slots", availability_data["available_slots"])
            
            # Format for speech
            slots_text = doctor_api.format_availability_for_speech(availability_data)
            
            # Generate natural response
            response = f"Sure! I can help you book a {service_type} appointment. I have slots available at {slots_text}. Which one works better for you?"
            
            return "TTS", response
        else:
            # Fallback when API fails or no slots
            return "TTS", "I'd be happy to help you book an appointment. Let me check with our receptionist and have them call you back within the hour. Can I get your phone number?"
    
    return None, None

# Update get_school_response method to include appointment handling
def get_school_response(self, user_input, session):
    """Enhanced response routing with API integration"""
    
    # PRIORITY 1: Check for appointment booking
    response_type, content = self._handle_appointment_booking(user_input, session)
    if response_type:
        return response_type, content
    
    # PRIORITY 2: Existing school response logic
    # ... rest of existing method ...
```

### **Step 4: Session Data Management**

Update `session.py` to handle API data:

```python
# Add this method to StreamingSession class
def store_api_data(self, api_name, data, expiry_minutes=30):
    """Store API response data in session with expiry"""
    if not hasattr(self, 'api_data'):
        self.api_data = {}
    
    self.api_data[api_name] = {
        "data": data,
        "timestamp": time.time(),
        "expiry": expiry_minutes * 60  # Convert to seconds
    }
    
    print(f"📋 Stored API data: {api_name}")

def get_api_data(self, api_name):
    """Retrieve API data if still valid"""
    if not hasattr(self, 'api_data') or api_name not in self.api_data:
        return None
    
    api_entry = self.api_data[api_name]
    age = time.time() - api_entry["timestamp"]
    
    if age > api_entry["expiry"]:
        print(f"⏰ API data expired: {api_name}")
        del self.api_data[api_name]
        return None
    
    return api_entry["data"]
```

---

## 📝 **Non-API Systems (Manual Updates)**

### **The Challenge**

Many businesses use systems that **DON'T** have API support:
- Small dental practices with basic scheduling software
- Restaurants using pen-and-paper reservations
- Local services with simple Excel-based booking

### **Solution: Manual Update System**

**Yes, you're absolutely right!** For non-API systems, we need a manual update workflow where client staff updates availability data.

### **Option 1: Separate Data File (Recommended)**

Create `dynamic_data.json`:

```json
{
  "doctor_availability": {
    "last_updated": "2024-01-15T10:30:00Z",
    "updated_by": "Sarah (Receptionist)",
    "available_slots": [
      {
        "datetime": "2024-01-18T11:30:00",
        "display": "Thursday 11:30 AM",
        "service": "dental",
        "doctor": "Dr. Smith"
      },
      {
        "datetime": "2024-01-19T14:00:00", 
        "display": "Friday 2:00 PM",
        "service": "general",
        "doctor": "Dr. Jones"
      }
    ],
    "blocked_dates": [
      "2024-01-16",  // Public holiday
      "2024-01-22"   // Doctor vacation
    ],
    "special_notes": "Emergency slots available after 5 PM"
  }
}
```

### **Manual Update Module**

Create `manual_data_manager.py`:

```python
#!/usr/bin/env python3
"""
MANUAL DATA MANAGEMENT MODULE
For businesses without API support - handles manual data updates
"""

import json
import os
import time
from datetime import datetime, timedelta

class ManualDataManager:
    """Manages manually updated business data"""
    
    def __init__(self, data_file="dynamic_data.json"):
        self.data_file = data_file
        self.data = self.load_data()
        self.last_check = 0
        self.check_interval = 60  # Check for updates every minute
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                print(f"📋 Loaded manual data from {self.data_file}")
                return data
            else:
                print(f"⚠️ Data file not found: {self.data_file}")
                return self.create_default_data()
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return self.create_default_data()
    
    def create_default_data(self):
        """Create default data structure"""
        default_data = {
            "doctor_availability": {
                "last_updated": datetime.now().isoformat(),
                "updated_by": "System",
                "available_slots": [],
                "blocked_dates": [],
                "special_notes": "Please update availability data"
            }
        }
        self.save_data(default_data)
        return default_data
    
    def save_data(self, data=None):
        """Save data to JSON file"""
        try:
            if data is None:
                data = self.data
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Saved data to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def check_for_updates(self):
        """Check if data file has been updated"""
        if time.time() - self.last_check < self.check_interval:
            return False
        
        try:
            file_modified = os.path.getmtime(self.data_file)
            data_timestamp = datetime.fromisoformat(
                self.data.get("doctor_availability", {}).get("last_updated", "1970-01-01T00:00:00")
            ).timestamp()
            
            if file_modified > data_timestamp:
                print("🔄 Data file updated, reloading...")
                self.data = self.load_data()
                self.last_check = time.time()
                return True
        except Exception as e:
            print(f"⚠️ Error checking for updates: {e}")
        
        self.last_check = time.time()
        return False
    
    def get_doctor_availability(self, service_type="general"):
        """Get current doctor availability"""
        self.check_for_updates()  # Check for manual updates
        
        doctor_data = self.data.get("doctor_availability", {})
        all_slots = doctor_data.get("available_slots", [])
        
        # Filter by service type if specified
        if service_type != "general":
            filtered_slots = [
                slot for slot in all_slots 
                if slot.get("service", "general") == service_type
            ]
        else:
            filtered_slots = all_slots
        
        # Remove past slots
        current_time = datetime.now()
        valid_slots = []
        
        for slot in filtered_slots:
            try:
                slot_time = datetime.fromisoformat(slot["datetime"])
                if slot_time > current_time:
                    valid_slots.append(slot["display"])
            except Exception as e:
                print(f"⚠️ Invalid slot datetime: {slot}")
        
        return {
            "available_slots": valid_slots,
            "success": True,
            "last_updated": doctor_data.get("last_updated"),
            "updated_by": doctor_data.get("updated_by")
        }
    
    def format_availability_for_speech(self, availability_data):
        """Format availability for natural speech"""
        slots = availability_data.get("available_slots", [])
        
        if not slots:
            return "no appointments available this week"
        elif len(slots) == 1:
            return slots[0]
        elif len(slots) == 2:
            return f"{slots[0]} and {slots[1]}"
        else:
            return f"{slots[0]}, {slots[1]}, and {len(slots)-2} more times"

# Global manual data manager instance
manual_data = ManualDataManager()
```

### **Option 2: Simple Variables in Config**

For very simple cases, update `config.py`:

```python
# In config.py - Simple manual data (updated by staff)
DOCTOR_AVAILABILITY = {
    "available_slots": [
        "Thursday 11:30 AM",
        "Friday 2:00 PM", 
        "Monday 10:00 AM"
    ],
    "last_updated": "2024-01-15 10:30 AM",
    "updated_by": "Sarah (Reception)",
    "special_notes": "Emergency slots available after 5 PM"
}

RESTAURANT_AVAILABILITY = {
    "dinner_slots": [
        "Tonight 7:00 PM",
        "Tomorrow 6:30 PM",
        "Friday 8:00 PM"
    ],
    "lunch_slots": [
        "Today 12:30 PM",
        "Tomorrow 1:15 PM"
    ],
    "last_updated": "2024-01-15 09:00 AM"
}
```

**Staff Update Process:**
```
1. Open config.py file
2. Find the DOCTOR_AVAILABILITY section
3. Update the "available_slots" array
4. Change "last_updated" timestamp
5. Save file and restart system: py main.py
```

### **Option 3: Excel + Auto-Converter System**

For businesses already comfortable with Excel:

Create `availability_data.xlsx`:

| Date | Time | Service | Doctor | Status | Notes |
|------|------|---------|---------|---------|-------|
| 2024-01-18 | 11:30 AM | Dental | Dr. Smith | Available | Regular checkup |
| 2024-01-19 | 2:00 PM | General | Dr. Jones | Available | New patients OK |
| 2024-01-22 | 10:00 AM | Consultation | Dr. Smith | Booked | Follow-up |

**Auto-converter script (`excel_to_availability.py`):**

```python
#!/usr/bin/env python3
"""
EXCEL TO AVAILABILITY CONVERTER
Converts Excel availability data to JSON for the AI system
"""

import pandas as pd
import json
from datetime import datetime
import os

class AvailabilityConverter:
    """Converts Excel availability data to system-readable JSON"""
    
    def __init__(self, excel_file="availability_data.xlsx"):
        self.excel_file = excel_file
        self.output_file = "dynamic_data.json"
    
    def convert_excel_to_json(self):
        """Convert Excel file to JSON availability data"""
        try:
            print(f"📊 Reading Excel file: {self.excel_file}")
            
            # Read Excel file
            df = pd.read_excel(self.excel_file)
            
            # Filter only available slots
            available_df = df[df['Status'].str.lower() == 'available']
            
            # Convert to our format
            available_slots = []
            for _, row in available_df.iterrows():
                slot = {
                    "datetime": f"{row['Date']}T{self._convert_time_format(row['Time'])}:00",
                    "display": f"{self._format_date_display(row['Date'])} {row['Time']}",
                    "service": row['Service'].lower(),
                    "doctor": row['Doctor'],
                    "notes": row.get('Notes', '')
                }
                available_slots.append(slot)
            
            # Create JSON structure
            json_data = {
                "doctor_availability": {
                    "last_updated": datetime.now().isoformat(),
                    "updated_by": "Excel Auto-Converter",
                    "source_file": self.excel_file,
                    "available_slots": available_slots,
                    "total_slots": len(available_slots)
                }
            }
            
            # Save to JSON
            with open(self.output_file, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            print(f"✅ Converted {len(available_slots)} slots to {self.output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False
    
    def _convert_time_format(self, time_str):
        """Convert '11:30 AM' to '11:30' 24-hour format"""
        try:
            time_obj = datetime.strptime(str(time_str), '%I:%M %p')
            return time_obj.strftime('%H:%M')
        except:
            return str(time_str)
    
    def _format_date_display(self, date_obj):
        """Convert date to display format like 'Thursday'"""
        try:
            if isinstance(date_obj, str):
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
            return date_obj.strftime('%A')  # Thursday, Friday, etc.
        except:
            return str(date_obj)
    
    def auto_watch_and_convert(self):
        """Watch Excel file for changes and auto-convert"""
        import time
        
        last_modified = 0
        print(f"👀 Watching {self.excel_file} for changes...")
        
        while True:
            try:
                if os.path.exists(self.excel_file):
                    current_modified = os.path.getmtime(self.excel_file)
                    
                    if current_modified > last_modified:
                        print("🔄 Excel file updated, converting...")
                        if self.convert_excel_to_json():
                            print("✅ Auto-conversion complete!")
                        last_modified = current_modified
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                print("👋 Stopping file watcher")
                break
            except Exception as e:
                print(f"⚠️ Watcher error: {e}")
                time.sleep(30)

# Usage
if __name__ == "__main__":
    converter = AvailabilityConverter()
    
    print("Choose option:")
    print("1. Convert Excel to JSON once")
    print("2. Watch Excel file and auto-convert on changes")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        converter.convert_excel_to_json()
    elif choice == "2":
        converter.auto_watch_and_convert()
    else:
        print("Invalid choice")
```

**Staff Workflow:**
```
1. Staff updates availability_data.xlsx (familiar Excel interface)
2. Saves Excel file
3. Auto-converter detects change and updates JSON
4. AI system automatically uses new data
5. No technical knowledge required!
```

### **Option 4: WhatsApp Bot Updates (Advanced)**

For real-time updates via WhatsApp messages:

```python
# whatsapp_updater.py (Advanced implementation)
"""
WHATSAPP AVAILABILITY UPDATER
Updates availability via WhatsApp messages from staff
"""

from twilio.rest import Client
import re
import json
from datetime import datetime

class WhatsAppUpdater:
    """Handle availability updates via WhatsApp"""
    
    def __init__(self):
        self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.authorized_numbers = ["+61XXXXXXXXX"]  # Staff phone numbers
    
    def process_whatsapp_message(self, from_number, message_body):
        """Process incoming WhatsApp message for availability updates"""
        
        if from_number not in self.authorized_numbers:
            return "Unauthorized number"
        
        # Parse commands like:
        # "ADD Thursday 2PM dental Dr Smith"
        # "REMOVE Friday 11AM" 
        # "BLOCK January 26 holiday"
        
        message = message_body.upper().strip()
        
        if message.startswith("ADD"):
            return self._handle_add_slot(message)
        elif message.startswith("REMOVE"):
            return self._handle_remove_slot(message)
        elif message.startswith("BLOCK"):
            return self._handle_block_date(message)
        elif message.startswith("STATUS"):
            return self._handle_status_request()
        else:
            return self._send_help_message()
    
    def _handle_add_slot(self, message):
        """Handle ADD commands"""
        # Parse: "ADD THURSDAY 2PM DENTAL DR SMITH"
        parts = message.split()
        if len(parts) >= 4:
            day = parts[1]
            time = parts[2]
            service = parts[3] if len(parts) > 3 else "GENERAL"
            
            # Add to availability data
            # Implementation details...
            return f"✅ Added {day} {time} {service} appointment"
        
        return "❌ Invalid ADD format. Use: ADD Thursday 2PM dental"
    
    def _send_help_message(self):
        """Send help message with available commands"""
        return """
🤖 AVAILABILITY BOT COMMANDS:

ADD Thursday 2PM dental - Add appointment slot
REMOVE Friday 11AM - Remove slot  
BLOCK Jan 26 holiday - Block entire day
STATUS - Show current availability

Example: ADD Monday 10AM general Dr Smith
        """

# WhatsApp webhook handler in main.py
@app.route("/whatsapp/webhook", methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages for availability updates"""
    from_number = request.form.get('From')
    message_body = request.form.get('Body')
    
    updater = WhatsAppUpdater()
    response = updater.process_whatsapp_message(from_number, message_body)
    
    # Send response back via WhatsApp
    updater.twilio_client.messages.create(
        body=response,
        from_='whatsapp:+14155238886',  # Twilio WhatsApp number
        to=from_number
    )
    
    return "OK"
```

**Staff Usage:**
```
Staff texts WhatsApp bot:
"ADD Thursday 2PM dental Dr Smith"

Bot responds:
"✅ Added Thursday 2PM dental appointment"

Next customer call immediately gets updated availability!
```

---

## 📊 **Comprehensive Method Comparison**

### **Manual Update Methods Overview**

| Method | Difficulty | Setup Time | Real-time Updates | Staff Training | Best For |
|--------|------------|------------|-------------------|----------------|----------|
| **JSON File** | Easy | 30 mins | Yes (auto-reload) | 15 mins | Most businesses |
| **Config Variables** | Very Easy | 15 mins | No (restart needed) | 5 mins | Simple cases |
| **Excel + Converter** | Medium | 2 hours | Yes (auto-watch) | None (familiar) | Excel-savvy staff |
| **WhatsApp Bot** | Advanced | 1 day | Yes (instant) | 10 mins | Tech-forward clients |

### **Detailed Method Analysis**

#### **🏆 Option 1: JSON File (RECOMMENDED)**
**Best for:** 80% of businesses

✅ **Pros:**
- No system restart required
- Real-time updates (auto-reload)
- Flexible data structure
- Version control friendly
- Easy backup and restore

❌ **Cons:**
- Staff needs basic JSON syntax knowledge
- Possible syntax errors if not careful

**Client Types:**
- Small to medium businesses
- Staff comfortable with basic tech
- Need frequent availability updates

**Sample JSON for different businesses:**
```json
{
  "doctor_availability": {...},
  "restaurant_reservations": {...}, 
  "salon_appointments": {...},
  "service_bookings": {...}
}
```

#### **⚡ Option 2: Config Variables**
**Best for:** Very simple, rarely changing data

✅ **Pros:**
- Extremely simple for staff
- No learning curve
- Direct Python variables
- Can't break JSON syntax

❌ **Cons:**
- Requires system restart
- Not suitable for frequent updates
- Limited flexibility

**Client Types:**
- Very small businesses
- Infrequent availability changes
- Non-technical staff
- Fixed schedule businesses

#### **📊 Option 3: Excel + Auto-Converter**
**Best for:** Businesses already using Excel

✅ **Pros:**
- Staff already know Excel
- Familiar interface
- Auto-conversion to JSON
- Can handle complex data
- Built-in data validation

❌ **Cons:**
- Requires pandas dependency
- More complex setup
- Excel file can get corrupted
- Conversion delays (30 seconds)

**Client Types:**
- Medical practices with patient management
- Restaurants with complex booking rules
- Services with detailed appointment data
- Businesses with existing Excel workflows

#### **💬 Option 4: WhatsApp Bot (ADVANCED)**
**Best for:** Tech-savvy, high-frequency update businesses

✅ **Pros:**
- Instant real-time updates
- Mobile-first approach
- Natural language commands
- Works from anywhere
- Audit trail of changes

❌ **Cons:**
- Complex development
- Requires WhatsApp Business API
- Command syntax to learn
- Potential for mistakes in messages

**Client Types:**
- Restaurants with daily menu changes
- Event venues with frequent bookings
- Emergency services
- High-volume appointment businesses

### **Implementation Decision Matrix**

Use this to choose the right method for each client:

| Client Characteristic | Recommended Method |
|----------------------|-------------------|
| **Small dental practice, basic updates** | JSON File |
| **Hair salon, Excel-comfortable staff** | Excel + Converter |
| **Restaurant, tech-savvy owner** | WhatsApp Bot |
| **Simple service, fixed schedule** | Config Variables |
| **Medical center, complex scheduling** | Excel + Converter or API |
| **Event venue, frequent changes** | WhatsApp Bot or API |

### **Mixed Approach Strategy**

You can also combine methods for different clients:

```python
# config.py - Support multiple update methods
UPDATE_METHOD = os.getenv('UPDATE_METHOD', 'json')  # json, config, excel, whatsapp

if UPDATE_METHOD == 'json':
    from manual_data_manager import manual_data as data_source
elif UPDATE_METHOD == 'excel':
    from excel_converter import excel_data as data_source
elif UPDATE_METHOD == 'whatsapp':
    from whatsapp_updater import whatsapp_data as data_source
else:  # config
    data_source = MANUAL_AVAILABILITY_DATA
```

This allows you to choose the best method per client without changing the core system!

### **Client Communication Strategy**

**For Non-API Clients, you'll need regular communication with staff:**

#### **Daily/Weekly Check-ins:**
```
1. 📞 WhatsApp/Call client: "Hi Sarah, any schedule changes this week?"
2. 📝 Staff updates: "Dr. Smith off Friday, added Saturday morning slots"
3. 🔄 You update data (JSON/Excel/Config): Remove Friday, add Saturday
4. ✅ System automatically uses new data for customer calls
5. 📊 Send weekly report: "Updated 12 slots, 45 calls handled"
```

#### **Emergency Updates:**
```
1. 🚨 Staff texts: "URGENT - Dr. canceled all afternoon appointments"  
2. ⚡ You immediately update data file
3. 📞 System stops offering those slots within 1 minute
4. 💬 Confirm: "Updated! No more afternoon bookings offered"
```

#### **Client Training Materials:**

**For JSON Method:**
```
STAFF INSTRUCTIONS - UPDATING APPOINTMENTS:

1. Open dynamic_data.json on computer
2. Find "available_slots" section  
3. Add/remove appointment times
4. Update "last_updated" with current date/time
5. Update "updated_by" with your name
6. Save file - system updates automatically!

EXAMPLE:
"available_slots": [
  "Thursday 11:30 AM",    ← Add new slot
  "Friday 2:00 PM"        ← Remove canceled slot
]
```

**For Excel Method:**
```
STAFF INSTRUCTIONS - EXCEL UPDATES:

1. Open availability_data.xlsx
2. Update Status column: "Available" or "Booked"
3. Add new rows for new time slots
4. Save Excel file
5. System auto-converts to AI format!

NO TECHNICAL KNOWLEDGE NEEDED!
```

**For Config Method:**
```
STAFF INSTRUCTIONS - SIMPLE UPDATES:

1. Open config.py file
2. Find DOCTOR_AVAILABILITY section
3. Update the appointment times in quotes
4. Save file
5. Text me to restart system

EXAMPLE:
DOCTOR_AVAILABLE_TIMES = ["11:30 AM", "2:00 PM", "Monday 10 AM"]
```

### **Staff Update Workflow**

1. **Staff receives new booking/cancellation**
2. **Updates data using their assigned method** (JSON/Excel/Config/WhatsApp)
3. **System automatically detects changes** (or restart for config method)
4. **Next customer call gets updated availability**
5. **Weekly reporting to ensure data freshness**

---

## 💡 **Implementation Examples**

### **Example 1: Doctor's Office**

**Customer Call Flow:**
```
Customer: "I'd like to book a dental appointment"
AI: Detects "dental appointment" → Fetches availability
AI: "Sure! I have dental appointments at Thursday 11:30 AM and Friday 2 PM. Which works for you?"
Customer: "Thursday sounds good"
AI: "Perfect! I'll book you for Thursday 11:30 AM. Can I get your name and phone number?"
```

### **Example 2: Restaurant Reservations**

**Customer Call Flow:**
```
Customer: "Do you have a table for tonight?"
AI: Checks dinner availability → "Yes, I have tables at 7 PM and 8:30 PM for tonight. How many people?"
Customer: "Four people, 7 PM would be perfect"
AI: "Excellent! Table for 4 at 7 PM tonight. Can I get a name for the reservation?"
```

### **Example 3: Service Appointment**

**Customer Call Flow:**
```
Customer: "I need my air conditioner serviced"
AI: Checks technician schedule → "I can schedule a technician for Tuesday 2 PM or Wednesday 10 AM. Which works better?"
Customer: "Tuesday afternoon is perfect"
AI: "Great! Technician visit scheduled for Tuesday 2 PM. I'll send you a confirmation text."
```

---

## 🛠️ **Best Practices**

### **For API Systems:**
- ✅ **Cache API responses** (5-10 minutes) to avoid repeated calls
- ✅ **Handle API failures gracefully** with fallback responses
- ✅ **Set reasonable timeouts** (5 seconds max)
- ✅ **Log API calls** for debugging
- ✅ **Validate API data** before using

### **For Manual Systems:**
- ✅ **Use JSON files** for easy staff updates
- ✅ **Check for updates regularly** (every minute)
- ✅ **Provide clear staff instructions** for updating data
- ✅ **Include metadata** (last_updated, updated_by)
- ✅ **Validate data format** to prevent errors

### **General Guidelines:**
- ✅ **Always have fallback responses** when data is unavailable
- ✅ **Use natural language** for availability ("Thursday 2 PM" not "2024-01-18T14:00")
- ✅ **Limit options** (2-3 slots max) to avoid overwhelming customers
- ✅ **Store session data** for multi-step booking conversations

---

## 🧪 **Testing & Deployment**

### **Testing API Integration:**

```python
# Test script: test_api_integration.py
from api_integrations import doctor_api

def test_api_connection():
    """Test API connectivity"""
    print("🧪 Testing API connection...")
    
    # Test availability fetch
    result = doctor_api.fetch_availability("dental")
    print(f"API Response: {result}")
    
    # Test response formatting
    formatted = doctor_api.format_availability_for_speech(result)
    print(f"Speech Format: {formatted}")

if __name__ == "__main__":
    test_api_connection()
```

### **Testing Manual Data:**

```python
# Test script: test_manual_data.py
from manual_data_manager import manual_data

def test_manual_data():
    """Test manual data system"""
    print("🧪 Testing manual data...")
    
    # Test data loading
    availability = manual_data.get_doctor_availability("dental")
    print(f"Availability: {availability}")
    
    # Test speech formatting
    formatted = manual_data.format_availability_for_speech(availability)
    print(f"Speech Format: {formatted}")

if __name__ == "__main__":
    test_manual_data()
```

---

## 🐛 **Troubleshooting**

### **Common API Issues:**

**❌ "API timeout error"**
- Check internet connection
- Verify API endpoint URL
- Increase timeout value
- Check API service status

**❌ "Invalid API key"**
- Verify API key in .env file
- Check API key permissions
- Confirm API key hasn't expired

**❌ "No slots returned"**
- Check API response format
- Verify date range parameters
- Check if API returns empty data

### **Common Manual Data Issues:**

**❌ "Data file not found"**
- Create dynamic_data.json file
- Check file path and permissions
- Verify file format is valid JSON

**❌ "Data not updating"**
- Check file modification timestamp
- Verify JSON format is valid
- Restart application if needed

**❌ "Invalid slot format"**
- Check datetime format in JSON
- Ensure all required fields present
- Validate slot data structure

---

## 🚀 **Deployment Checklist**

### **For API Systems:**
- [ ] API credentials configured in .env
- [ ] API endpoints tested and working
- [ ] Error handling implemented
- [ ] Caching system working
- [ ] Fallback responses ready

### **For Manual Systems:**
- [ ] dynamic_data.json file created
- [ ] Staff trained on update process
- [ ] File permissions set correctly
- [ ] Update documentation provided
- [ ] Backup process established

### **General:**
- [ ] Session variables configured
- [ ] Router logic updated
- [ ] TTS responses tested
- [ ] Conversation flow validated
- [ ] Error scenarios handled

---

## 📞 **Support & Updates**

This guide covers the foundation for implementing dynamic data systems in Klariqo. For specific business implementations:

1. **Identify data source** (API vs Manual)
2. **Define session variables** for that business type
3. **Implement data fetching logic** (API client or manual data manager)
4. **Update router logic** to handle new conversation flows
5. **Test thoroughly** with various scenarios
6. **Train staff** on any manual update processes

**Remember:** The Klariqo architecture is designed to be flexible. You can mix and match approaches - some data from APIs, some manually updated, some static pre-recorded responses.

---

**Built with ❤️ for the Klariqo Development Team**

*Complete Developer Documentation for Dynamic Data Integration*