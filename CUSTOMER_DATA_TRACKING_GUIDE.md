# 📊 Customer Data Tracking & Logging Guide

## ✅ IMPLEMENTATION COMPLETE

The system now comprehensively tracks and logs all essential customer information for business use, ensuring no customer details are lost.

## 🎯 **Critical Customer Data Captured**

### **Essential Information Tracked:**
1. **Customer Name** - Extracted from conversation
2. **Phone Number** - Caller's number + any mentioned numbers
3. **Location/Suburb** - Where customer is located
4. **Service Type** - What plumbing service they need
5. **Urgency Level** - Emergency, urgent, routine, flexible
6. **Issue Description** - Detailed problem description
7. **Preferred Date** - When they want service (today, tomorrow, etc.)
8. **Preferred Time** - Morning, afternoon, evening
9. **Property Type** - House, unit, commercial, residential
10. **Previous Customer** - Whether they've used service before
11. **Call Date/Time** - When the call occurred
12. **Call Duration** - How long the conversation lasted

## 📅 **Australian Date/Time Context System**

### **Current Date/Time Always Available:**
- **Today's Date**: Always provided to GPT (e.g., "Monday, August 5, 2024")
- **Current Time**: Real-time clock (e.g., "2:30 PM")
- **Tomorrow's Date**: Calculated automatically
- **Context Understanding**: GPT knows what "today" and "tomorrow" mean

### **Example Context:**
```
📅 CURRENT DATE & TIME CONTEXT:
Today is Monday, August 5, 2024 at 2:30 PM
Tomorrow is Tuesday, August 6, 2024
When customer says "today" they mean Monday, August 5, 2024
When customer says "tomorrow" they mean Tuesday, August 6, 2024
```

## 🔍 **Data Extraction Intelligence**

### **Customer Name Detection:**
- "My name is John"
- "I'm Sarah"
- "This is Mike"
- "Call me David"
- "Name's Lisa"

### **Phone Number Detection:**
- 0412 345 678 (Australian format)
- 0412345678 (no spaces)
- +61 4 1234 5678 (international)
- 04 1234 5678 (alternative format)

### **Location Detection:**
- "I'm in Melbourne"
- "Located in North Sydney"
- "From Brisbane"
- "Address in Perth"

### **Service Type Detection:**
- **Blocked Drain**: "drain blocked", "clogged drain"
- **Leaking Tap**: "tap leak", "dripping tap"
- **Toilet Repair**: "toilet", "loo", "dunny"
- **Hot Water Issues**: "no hot water", "water heater"
- **Emergency**: "emergency", "urgent", "flooding"
- **Gas Fitting**: "gas", "gas leak"

### **Urgency Level Detection:**
- **Emergency**: "emergency", "urgent", "asap", "flooding", "burst"
- **Urgent**: "soon", "today", "this week", "quickly"
- **Flexible**: "whenever", "no rush", "take your time"

## 📊 **Data Storage & Export**

### **Multiple Log Files:**
1. **`logs/call_logs.csv`** - General call statistics
2. **`logs/customer_data.csv`** - Detailed customer information
3. **`logs/conversation_logs.csv`** - Full conversation transcripts

### **Customer Data CSV Structure:**
```csv
call_date,call_time,call_sid,customer_name,customer_phone,customer_location,service_type,urgency_level,issue_description,preferred_date,preferred_time,property_type,previous_customer,call_duration,call_status,audio_files_used,tts_responses
2024-08-05,14:30:15,CA123456,John Smith,0412345678,Melbourne,blocked_drain,urgent,kitchen sink blocked,2024-08-05,afternoon,house,no,180,completed,5,3
```

## 🎯 **Real-World Example**

### **Customer Call Scenario:**
```
Customer: "Hi, my name is Sarah and I'm in North Sydney. I have a blocked drain in my kitchen sink. It's quite urgent and I need someone to come today if possible."

AI Response: "Hi Sarah! I understand you have an urgent blocked drain issue in North Sydney. Let me help you get someone out today."
```

### **Data Captured:**
- **Name**: Sarah
- **Location**: North Sydney
- **Service**: blocked_drain
- **Urgency**: urgent
- **Issue**: blocked drain in kitchen sink
- **Preferred Date**: today
- **Property Type**: residential (inferred)

## 🔧 **Configuration & Customization**

### **Session Variables Template** (`config.py`):
```python
SESSION_VARIABLES_TEMPLATE = {
    "service_type": None,        # Type of plumbing service
    "urgency_level": None,       # Emergency, urgent, routine, flexible
    "property_type": None,       # Residential, commercial, unit, house
    "customer_location": None,   # Suburb/area for scheduling
    "customer_name": None,       # Customer's name
    "customer_phone": None,      # Phone number for booking
    "preferred_date": None,      # When they want service
    "preferred_time": None,      # Time preference
    "issue_description": None,   # Brief description of the issue
    "previous_customer": None,   # Repeat customer handling
    "selected_appointment": None # Final booked appointment slot
}
```

## 📈 **Business Intelligence**

### **What Clients Get:**
1. **Immediate Access**: All customer data available in CSV files
2. **Call History**: Complete conversation logs
3. **Customer Profiles**: Name, contact, location, preferences
4. **Service Analytics**: Most common issues, urgency patterns
5. **Booking Data**: Preferred times, dates, appointment confirmations
6. **Performance Metrics**: Call duration, success rates

### **Sample Client Report:**
```
📊 DAILY CALL SUMMARY - August 5, 2024
Total Calls: 12
New Customers: 8
Repeat Customers: 4
Most Common Issue: Blocked Drains (5 calls)
Average Call Duration: 3 minutes
Bookings Made: 7
Emergency Calls: 2
```

## 🚨 **Critical Business Protection**

### **No Data Loss:**
- **Real-time Logging**: Every conversation turn is logged
- **Session Persistence**: Data survives connection issues
- **Multiple Backups**: CSV files + session memory
- **Error Recovery**: Graceful handling of technical issues

### **Data Quality:**
- **Validation**: Phone numbers, dates, times validated
- **Context Awareness**: Current date/time always available
- **Intelligent Extraction**: Multiple patterns for each data type
- **Fallback Handling**: Graceful degradation if extraction fails

## 🧪 **Testing & Verification**

### **Test Customer Data Extraction:**
```bash
# Test the system
py main.py

# Visit test page
http://localhost:5000/test

# Check customer data
http://localhost:5000/debug/call_logs
```

### **Sample Test Call:**
```
Customer: "Hi, I'm Mike from Brisbane. My toilet is blocked and it's an emergency. Can you come today? My number is 0412 345 678."

Expected Data Captured:
- Name: Mike
- Location: Brisbane  
- Service: toilet_repair
- Urgency: emergency
- Preferred Date: today
- Phone: 0412345678
```

## ✅ **Implementation Status**

- ✅ **Australian Date/Time Context** - GPT always knows current Australian date/time (AEST/AEDT)
- ✅ **Customer Name Extraction** - Multiple pattern detection
- ✅ **Phone Number Detection** - Australian format support
- ✅ **Location Tracking** - Suburb/area extraction
- ✅ **Service Classification** - Plumbing-specific categories
- ✅ **Urgency Assessment** - Emergency/urgent/routine classification
- ✅ **Issue Description** - Problem detail capture
- ✅ **Booking Preferences** - Date/time preference tracking
- ✅ **CSV Export** - Business-ready data files
- ✅ **Real-time Logging** - No data loss protection
- ✅ **Error Handling** - Graceful failure recovery

## 🎯 **Client Benefits**

1. **Complete Customer Records**: Every call fully documented
2. **Immediate Access**: Data available in CSV format
3. **Business Intelligence**: Analytics on call patterns
4. **Customer History**: Track repeat customers
5. **Booking Management**: All appointment preferences captured
6. **Emergency Handling**: Urgent issues properly flagged
7. **Location Intelligence**: Service area optimization
8. **Performance Tracking**: Call success rates and duration

## 🔄 **Integration with Existing Systems**

### **CSV Export Compatibility:**
- **CRM Systems**: Import customer data directly
- **Booking Systems**: Appointment data ready for integration
- **Analytics Tools**: Business intelligence ready
- **Reporting Software**: Standard CSV format

### **Real-time Access:**
- **Web Interface**: View data at `/debug/call_logs`
- **API Endpoints**: Programmatic access to data
- **File Downloads**: Direct CSV file access
- **Email Reports**: Automated daily summaries

---

**Implementation Date**: December 2024  
**Status**: ✅ Production Ready  
**Data Protection**: ✅ Complete Customer Data Tracking
