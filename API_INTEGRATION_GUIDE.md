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

### **Staff Update Workflow**

1. **Staff receives new booking/cancellation**
2. **Updates `dynamic_data.json` file**
3. **System automatically detects changes**
4. **Next customer call gets updated availability**

**Example staff instructions:**
```
TO UPDATE DOCTOR AVAILABILITY:
1. Open dynamic_data.json file
2. Update the "available_slots" section
3. Change "last_updated" to current date/time
4. Change "updated_by" to your name
5. Save the file
6. System will automatically use new data
```

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