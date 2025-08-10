# 🚀 CLIENT ADAPTATION GUIDE - AU/NZ Edition
## Complete Guide for Freelancers & VAs to Deploy Klariqo Voice AI for AU/NZ Clients

---

### 🎯 **Overview: What This Guide Covers**

This guide helps freelancers/VAs clone and adapt the Klariqo AI Voice Assistant for **AU/NZ clients** across different industries using **Twilio μ-law streaming**:

**🇦🇺 Perfect for Australian Businesses:**
- 🏨 **Hotels in Melbourne/Sydney** → 🏡 **Real Estate in Brisbane/Perth** → 🏥 **Medical Centers** → 🛒 **E-commerce** → 🔧 **Plumbing/Service Businesses**

**🇳🇿 Perfect for New Zealand Businesses:**
- 🏨 **Hotels in Auckland/Wellington** → 🏡 **Real Estate in Christchurch** → 🏫 **Education** → 🏢 **Professional Services** → 🔧 **Plumbing/Service Businesses**

**Time Required:** 5 minutes (automated) or 3-4 hours (manual)  
**Skills Needed:** Basic Git, Excel, Audio editing, Twilio account  
**Result:** Production-ready AI voice system with Twilio integration for AU/NZ

---

## 🚀 **QUICK START: Automated Adaptation (5 minutes)**

### **Option 1: Automated Tool (Recommended)**
```bash
# Run the adaptation tool
py client_adaptation.py

# Choose from pre-built templates or create custom
# Follow the prompts to configure your client
```

### **Option 2: Manual Configuration**
```python
# Edit config.py - Update CLIENT_CONFIG section:
CLIENT_CONFIG = {
    "business_name": "Your Business Name",
    "ai_assistant_name": "Your AI Name", 
    "industry": "your_industry",
    "location": "Your Country",
    "city": "Your City",
    "phone_number": "Your Phone",
    "website": "Your Website",
    "business_hours": "Your Hours",
    "emergency_available": True/False,
    "service_area": "Your Service Area",
    "currency": "Your Currency",
    "timezone": "Your Timezone"
}
```

### **✅ What Gets Updated Automatically**
- `config.py` - Client configuration
- `router.py` - AI prompts and responses  
- `main.py` - Dashboard and web interface
- `README.md` - Project documentation
- `customer_data/your_business_name/` - Client-specific data
- `logs/your_business_name/` - Client-specific logs
- `your_business_name_adaptation_summary.md` - Adaptation report

---

## 📋 **DETAILED MANUAL PROCESS (3-4 hours)**

### **PHASE 1: Repository Setup (30 minutes)**

#### **Step 1: Create New Repository for Client**
```bash
# 1. Clone the original as a NEW repository (don't fork!)
git clone https://github.com/web3mammon/Klariqo-AU.git
cd Klariqo-AU

# 2. Remove original git history (create fresh repo)
rm -rf .git
git init
git add .
git commit -m "Initial commit: AI Voice Assistant for [CLIENT_NAME] - AU/NZ"

# 3. Create new GitHub repository and push
# Go to GitHub.com → Create New Repository → "client-name-voice-ai-au"
git remote add origin https://github.com/your-username/CLIENT-NAME-voice-ai-au.git
git branch -M main
git push -u origin main
```

#### **Step 2: Rename Project Files**
```bash
# Update project name throughout codebase
# Find & Replace in ALL files:
# "Klariqo AI Voice Assistant" → "[CLIENT BUSINESS NAME] Voice AI"
# "AI Assistant" → "[CLIENT PREFERRED AI NAME]"
# "business" → "[CLIENT INDUSTRY]"
# "customer" → "[CLIENT TARGET AUDIENCE]"
# "+61XXXXXXXXX" → "[CLIENT TWILIO NUMBER]"

# Key files to update:
# - README.md (title, descriptions, examples)
# - main.py (header comments, health check messages)
# - config.py (SESSION_FLAGS_TEMPLATE, SESSION_VARIABLES_TEMPLATE)
# - router.py (prompts, industry-specific logic)
# - audio_snippets.json (all transcripts and file references)
```

---

## 🎵 **PHASE 2: Audio Content Adaptation (2-3 hours)**

### **Step 1: Industry Analysis & Content Planning**

#### **For AU/NZ Hotels (Melbourne Grand, Auckland City Hotel, etc.):**
```bash
# Common inquiries to cover:
# - Room availability & seasonal rates
# - Check-in/check-out times (local time zones)
# - Amenities (pool, gym, restaurant, wifi)
# - Location & directions (CBD, airport transfers)
# - Booking modifications & cancellations
# - Special services (concierge, room service, laundry)
# - Event hosting & conference facilities
# - Local attractions & tours

# Session variables to track:
# - check_in_date, check_out_date, duration
# - room_type, guest_count, bed_preference
# - special_requests, budget_range
# - arrival_method (flight, car, train)
# - purpose (business, leisure, event)
```

#### **For AU/NZ Real Estate (Brisbane Property Group, Auckland Realty, etc.):**
```bash
# Common inquiries to cover:
# - Property availability & listings
# - Inspection bookings & open homes
# - Price guides & market reports
# - Suburb information & schools
# - Financing & mortgage pre-approval
# - Property management services
# - Investment opportunities
# - Settlement & legal processes

# Session variables to track:
# - property_type, location_preference, budget_range
# - inspection_date, contact_method, urgency_level
# - investment_type, financing_status
```

#### **For AU/NZ Plumbing/Service Businesses (Current Setup):**
```bash
# Common inquiries to cover:
# - Service types (drain cleaning, hot water, gas fitting)
# - Emergency vs routine services
# - Pricing and quotes
# - Availability and booking
# - Service areas and coverage
# - Experience and reputation
# - Warranty and guarantees

# Session variables to track:
# - service_type, urgency_level, property_type
# - customer_location, preferred_date, preferred_time
# - customer_name, customer_phone, issue_description
```

### **Step 2: Audio File Recording & Production**

#### **Recording Requirements:**
```bash
# 1. Recording environment:
#    - Quiet room with minimal echo
#    - Professional microphone (USB condenser recommended)
#    - Recording software (Audacity, GarageBand, etc.)

# 2. Recording requirements:
#    - Clear recording quality (no background noise)
#    - Consistent volume levels
#    - Natural speaking pace (not too fast/slow)
#    - Australian/NZ accent appropriate for target market
#    - Professional but friendly tone

# 3. File format requirements:
#    - Save as MP3 files
#    - 44.1kHz sample rate
#    - 128kbps bitrate minimum
#    - Mono or stereo (system converts to mono)
```

#### **Audio File Organization:**
```bash
# Create these folders:
mkdir audio_optimised         # Original MP3 files from recording
mkdir audio_ulaw             # μ-law converted files (auto-generated)

# File naming convention:
# - Use descriptive names: "room_availability.mp3"
# - Avoid spaces: use underscores or hyphens
# - Keep names short but clear
# - Group related files: "hotel_intro.mp3", "hotel_amenities.mp3"
```

### **Step 3: Audio Content Creation**

#### **Essential Audio Files to Create:**

**For Hotels:**
```bash
# Core response files:
hotel_intro.mp3              # "Welcome to [Hotel Name], how can I help you today?"
room_availability.mp3        # "We have several room types available..."
room_rates.mp3              # "Our rates start from $XXX per night..."
check_in_times.mp3          # "Check-in is from 2 PM, check-out by 11 AM..."
amenities.mp3               # "We offer free WiFi, pool, gym, restaurant..."
location_directions.mp3     # "We're located in the CBD, 10 minutes from airport..."
booking_process.mp3         # "I can help you book a room. What dates do you need?"
local_attractions.mp3       # "Popular attractions include..."
goodbye.mp3                 # "Thank you for calling [Hotel Name]..."
```

**For Real Estate:**
```bash
# Core response files:
real_estate_intro.mp3       # "Welcome to [Agency Name], how can I help you?"
property_availability.mp3   # "We have several properties available..."
inspection_booking.mp3      # "I can help you book an inspection..."
price_guide.mp3            # "Properties in this area typically range from..."
suburb_info.mp3            # "This suburb is known for..."
financing_info.mp3         # "We can help with mortgage pre-approval..."
goodbye.mp3                # "Thank you for calling [Agency Name]..."
```

**For Plumbing (Current):**
```bash
# Core response files:
plumbing_intro.mp3          # "G'day! You've reached Pete's Plumbing..."
services_offered.mp3        # "We handle blocked drains, leaking taps..."
pricing.mp3                # "Our pricing usually starts at $98..."
available_hours.mp3        # "We're available Monday through Saturday..."
in_business_how_long.mp3   # "We've been doing this for 7 years..."
ask_time_day.mp3          # "We've got a few open slots this week..."
goodbye.mp3               # "Thanks for choosing Pete's Plumbing..."
```

### **Step 4: Audio File Processing**

#### **Convert to μ-law Format:**
```bash
# 1. Place MP3 files in audio_optimised/ folder
# 2. Run the audio optimizer:
py audio-optimiser.py

# This will:
# - Convert MP3 to μ-law format for telephony
# - Optimize for 8kHz, 8-bit μ-law encoding
# - Create files in audio_ulaw/ folder
# - Load files into memory cache for fast access
```

#### **Update Audio Transcripts:**
```bash
# Edit audio_snippets.json to match your new audio files:
{
  "introductions": {
    "your_intro.mp3": "Your actual transcript here..."
  },
  "pricing": {
    "your_pricing.mp3": "Your actual transcript here..."
  },
  "miscellaneous": {
    "your_service.mp3": "Your actual transcript here..."
  }
}
```

---

## ⚙️ **PHASE 3: Configuration Updates (30 minutes)**

### **Step 1: Update Session Management**

#### **For AU/NZ Hotel:**
```python
# In config.py, update SESSION_FLAGS_TEMPLATE:
SESSION_FLAGS_TEMPLATE = {
    "intro_played": False,
    "room_inquiry_made": False,
    "amenities_discussed": False,
    "rates_mentioned": False,
    "booking_attempted": False,
    "location_discussed": False,
    "local_attractions_mentioned": False,
    "special_services_mentioned": False
}

SESSION_VARIABLES_TEMPLATE = {
    "check_in_date": None,
    "check_out_date": None,
    "room_type": None,
    "guest_count": None,
    "budget_range": None,
    "special_requests": None,
    "customer_name": None,
    "inquiry_focus": None,  # "rooms", "dining", "events", "location"
    "city_location": None,  # "melbourne", "sydney", "auckland", etc.
    "arrival_method": None  # "flight", "car", "train"
}
```

#### **For AU/NZ Real Estate:**
```python
SESSION_FLAGS_TEMPLATE = {
    "intro_played": False,
    "property_inquiry_made": False,
    "inspection_discussed": False,
    "pricing_mentioned": False,
    "financing_discussed": False,
    "location_discussed": False,
    "market_info_shared": False,
    "contact_collected": False
}

SESSION_VARIABLES_TEMPLATE = {
    "property_type": None,
    "location_preference": None,
    "budget_range": None,
    "inspection_date": None,
    "customer_name": None,
    "contact_method": None,
    "urgency_level": None,
    "investment_type": None,
    "financing_status": None
}
```

#### **For AU/NZ Plumbing (Current):**
```python
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
```

### **Step 2: Update AI Response Logic**

#### **Update Base Prompt in router.py:**
```python
# Replace the base prompt with industry-specific content
prompt = f"""You are {Config.CLIENT_CONFIG['ai_assistant_name']}, a helpful voice assistant at {Config.CLIENT_CONFIG['business_name']} in {Config.CLIENT_CONFIG['city']}. 
Your job is to respond to customer inquiries with appropriate audio responses.

🏨 {Config.CLIENT_CONFIG['industry'].upper()} RESPONSE RULES:
# Add industry-specific rules here

📋 AVAILABLE AUDIO FILES:
{available_files}

Remember: Always be helpful, professional, and ready to assist customers!"""
```

### **Step 3: Update Availability Data**

#### **Custom Availability Slots:**
```python
# Update availability slots in config.py for your business schedule:
YOUR_BUSINESS_AVAILABILITY = {
    "available_slots": [
        {"date": "Monday, August 5th", "time": "9:00 AM - 11:00 AM", "slot_id": "MON05_0900"},
        {"date": "Tuesday, August 6th", "time": "2:00 PM - 4:00 PM", "slot_id": "TUE06_1400"},
        # Add your business-specific availability
    ]
}
```

---

## 🏢 **EXAMPLE CLIENT CONFIGURATIONS**

### **Hotel Business**
```python
CLIENT_CONFIG = {
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
```

### **Real Estate Business**
```python
CLIENT_CONFIG = {
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
```

### **Plumbing Business (Current)**
```python
CLIENT_CONFIG = {
    "business_name": "Pete's Plumbing",
    "ai_assistant_name": "Jason",
    "industry": "plumbing",
    "location": "Australia",
    "city": "Melbourne",
    "phone_number": "+61XXXXXXXXX",
    "website": "https://petesplumbing.com.au",
    "business_hours": "Mon-Fri 8AM-6PM, Sat 9AM-4PM",
    "emergency_available": True,
    "service_area": "Greater Melbourne",
    "currency": "AUD",
    "timezone": "Australia/Melbourne"
}
```

---

## 🔧 **PHASE 4: Route File Updates (15 minutes)**

### **Update Route Files:**

#### **File: routes/inbound.py**
```python
# Find line: selected_intro = "plumbing_intro.mp3"
# Change to: selected_intro = "your_new_intro_file.mp3"

# 🔧 Why this matters:
# - The route files tell the system which audio file to play first
# - If you don't update these, you'll get "audio not in cache" errors
# - This is the most commonly missed step when adapting for new clients
```

#### **File: routes/outbound.py**
```python
# Find line: selected_intro = "plumbing_intro.mp3"
# Change to: selected_intro = "your_new_intro_file.mp3"

# Same importance as inbound.py - must match your audio files
```

---

## 🧪 **PHASE 5: Testing & Validation (30 minutes)**

### **Step 1: System Testing**
```bash
# 1. Start the system:
py main.py

# 2. Check system health:
# Visit: http://localhost:5000/debug/system_health

# 3. Verify audio files:
# Visit: http://localhost:5000/debug/audio_files

# 4. Test TTS generation:
# Visit: http://localhost:5000/test
```

### **Step 2: Call Testing**
```bash
# 1. Set up Twilio webhook:
# - Point to your server: https://your-domain.com/twilio/voice
# - Enable Media Streams for bidirectional audio

# 2. Test inbound calls:
# - Call your Twilio number
# - Verify intro plays correctly
# - Test conversation flow

# 3. Test outbound calls:
# - Use test endpoint: /call_test/your_number
# - Verify customer name personalization works
# - Test CSV campaign functionality
```

### **Step 3: Content Validation**
```bash
# 1. Verify all audio files play correctly
# 2. Check transcripts match audio content
# 3. Test booking functionality
# 4. Verify customer data collection
# 5. Check call logging and exports
```

---

## 🎯 **BENEFITS OF THIS APPROACH**

### ✅ **Easy Replication**
- Clone repository → Run adaptation tool → Ready for new client
- No manual file editing required
- Consistent configuration across all files

### ✅ **Maintainable**
- Single source of truth for client information
- Easy to update business details
- Version control friendly

### ✅ **Scalable**
- Support multiple clients from same codebase
- Industry-specific templates
- Automated setup process

### ✅ **Production Ready**
- Twilio μ-law streaming for AU/NZ telephony
- Real-time conversation memory
- Comprehensive logging and analytics
- Customer name personalization
- CSV-based outbound campaigns

---

## 🚨 **IMPORTANT NOTES**

1. **Backup First**: Always backup your current configuration before adapting
2. **Test Thoroughly**: Test all functionality after adaptation
3. **Update Audio Files**: Don't forget to replace audio content
4. **Check Routes**: Verify intro files are correctly referenced
5. **Environment Variables**: Ensure API keys are set for new client
6. **Twilio Configuration**: Update webhook URLs for new domain
7. **Audio Quality**: Ensure all audio files meet telephony standards
8. **Content Accuracy**: Verify all transcripts match actual audio

---

## 📞 **SUPPORT & TROUBLESHOOTING**

### **Common Issues:**
1. **Audio not in cache**: Check file names in routes match audio_ulaw/ folder
2. **TTS not working**: Verify ElevenLabs API key in .env file
3. **Calls not connecting**: Check Twilio webhook URLs and Media Streams
4. **Customer name not working**: Verify CSV format and session variable updates

### **Getting Help:**
1. Check the generated adaptation summary file
2. Review logs in `logs/` directory
3. Test with simple configuration first
4. Verify all file paths and references are correct

---

## 🎉 **DEPLOYMENT CHECKLIST**

### **Pre-Deployment:**
- [ ] All audio files recorded and converted
- [ ] Audio transcripts updated in audio_snippets.json
- [ ] Route files updated with correct intro files
- [ ] Client configuration updated in config.py
- [ ] Session variables customized for industry
- [ ] Availability data updated for business schedule
- [ ] Twilio webhook URLs configured
- [ ] Environment variables set (.env file)

### **Post-Deployment:**
- [ ] System health check passed
- [ ] Audio files loading correctly
- [ ] TTS generation working
- [ ] Inbound calls functioning
- [ ] Outbound calls working
- [ ] Customer name personalization active
- [ ] CSV campaigns operational
- [ ] Call logging and exports working
- [ ] Client testing completed

---

**🎉 You're now ready to deploy a production-ready AI voice system for your AU/NZ client!**

The system includes:
- ✅ **Twilio μ-law streaming** for AU/NZ telephony
- ✅ **Customer name personalization** from CSV campaigns
- ✅ **Real-time conversation memory** and context
- ✅ **Comprehensive logging** and analytics
- ✅ **Industry-specific templates** and configurations
- ✅ **Automated adaptation tools** for quick setup