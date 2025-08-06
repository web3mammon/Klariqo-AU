# 🔄 CLIENT ADAPTATION GUIDE - AU/NZ Edition
## Complete Guide for Freelancers & VAs to Deploy Klariqo Voice AI for AU/NZ Clients

---

### 🎯 **Overview: What This Guide Covers**

This guide helps freelancers/VAs clone and adapt the Klariqo AI Voice Assistant for **AU/NZ clients** across different industries using **Twilio μ-law streaming**:

**🇦🇺 Perfect for Australian Businesses:**
- 🏨 **Hotels in Melbourne/Sydney** → 🏡 **Real Estate in Brisbane/Perth** → 🏥 **Medical Centers** → 🛒 **E-commerce**

**🇳🇿 Perfect for New Zealand Businesses:**
- 🏨 **Hotels in Auckland/Wellington** → 🏡 **Real Estate in Christchurch** → 🏫 **Education** → 🏢 **Professional Services**

**Time Required:** 3-4 hours for complete adaptation  
**Skills Needed:** Basic Git, Excel, Audio editing, Twilio account  
**Result:** Production-ready AI voice system with Twilio integration for AU/NZ

---

## 📋 **PHASE 1: Repository Setup (30 minutes)**

### **Step 1: Create New Repository for Client**
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

### **Step 2: Rename Project Files**
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

**For AU/NZ Hotels (Melbourne Grand, Auckland City Hotel, etc.):**
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

**For AU/NZ Real Estate (Brisbane Property Group, Auckland Realty, etc.):**
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
# - buyer_type (first_home, investor, upgrader)
# - inspection_availability, contact_method
# - financing_status, timeline
# - specific_requirements (bedrooms, garage, etc.)
```

**For AU/NZ Medical Centers:**
```bash
# Common inquiries to cover:
# - Doctor availability & bulk billing
# - Appointment bookings & cancellations
# - Medicare & health fund billing
# - Prescription renewals
# - Test results & pathology
# - Specialist referrals
# - Practice locations & parking
# - After-hours & emergency contacts

# Session variables to track:
# - patient_name, medicare_number
# - doctor_preference, appointment_type
# - health_fund, urgency_level
# - preferred_time, contact_method
```

### **Step 2: Create New Audio Content**

#### **Update Excel Management File**
```bash
# 1. Open audio_files.xlsx
# 2. Replace ALL content with new industry-specific responses
# 3. Structure by categories relevant to AU/NZ client:

# Example for Melbourne Hotel:
Category | Filename | Transcript | Alternate_Version
---------|----------|------------|------------------
introductions | melbourne_hotel_intro.mp3 | "G'day! Welcome to [HOTEL NAME] Melbourne..." | hotel_intro_formal.mp3
room_inquiries | room_availability_au.mp3 | "I can check our availability for you..." | room_check_alt.mp3
amenities | amenities_melbourne.mp3 | "Our hotel features a rooftop pool, gym..." | amenities_detailed.mp3
booking | booking_process_au.mp3 | "I can help you book directly..." | booking_simple.mp3
local_info | melbourne_attractions.mp3 | "Melbourne's famous for its laneways..." | cbd_info.mp3
```

#### **Record New Audio Files**
```bash
# 1. Script writing for AU/NZ market:
#    - Use Australian/NZ accent and terminology
#    - Professional, friendly, helpful tone
#    - Include local references (CBD, suburbs, etc.)
#    - Use familiar terms (lift vs elevator, car park vs parking lot)

# 2. Recording requirements:
#    - Professional voice actor with AU/NZ accent
#    - Clear recording quality (no background noise)
#    - Format: MP3, high quality (44.1kHz recommended)
#    - Length: 10-45 seconds per response
#    - Natural speech pace, easy to understand

# 3. File naming convention:
#    - location_industry_topic.mp3 (e.g., melbourne_hotel_checkin.mp3)
#    - Keep filenames descriptive but concise
#    - No spaces, use underscores
#    - Include city/region if relevant
```

### **Step 3: Audio File Processing**
```bash
# 1. Place new MP3 files in audio_optimised/ directory
# 2. Update Excel file with all new content
# 3. Convert Excel to JSON:
py excel_to_json.py
# Select option 1 to convert

# 4. Convert MP3 to μ-law format for Twilio:
py audio-optimiser.py
# This creates audio_ulaw/ directory with Twilio-ready files

# 5. Verify conversion:
ls audio_ulaw/  # Should show all your new .ulaw files
# Each .ulaw file is ~50% smaller than equivalent PCM
```

### **⚠️ CRITICAL STEP: Update Route Files (OFTEN MISSED!)**
```bash
# 🚨 IMPORTANT: After changing audio files, you MUST update the intro files in routes

# 6. Update inbound call intro:
# File: routes/inbound.py
# Find line: selected_intro = "old_intro_file.mp3"
# Change to: selected_intro = "your_new_intro_file.mp3"

# Example for Pete's Plumbing:
# OLD: selected_intro = "school_intro.mp3"
# NEW: selected_intro = "plumbing_intro.mp3"

# Example for Melbourne Hotel:
# OLD: selected_intro = "school_intro.mp3"  
# NEW: selected_intro = "melbourne_hotel_intro.mp3"

# 7. Update outbound call intro (if using outbound calls):
# File: routes/outbound.py
# Find line: selected_intro = "old_outbound_intro.mp3"
# Change to: selected_intro = "your_new_intro_file.mp3"

# 🔧 Why this matters:
# - The route files tell the system which audio file to play first
# - If you don't update these, you'll get "audio not in cache" errors
# - This is the most commonly missed step when adapting for new clients
```

---

## ⚙️ **PHASE 3: Configuration Updates (30 minutes)**

### **Step 1: Update Session Management**
```python
# In config.py, update SESSION_FLAGS_TEMPLATE:

# For AU/NZ Hotel:
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

### **Step 2: Update AI Response Logic**
```python
# In router.py, update the base prompt:

# Replace generic prompts with AU/NZ industry-specific ones
# Update file selection rules for local context
# Modify conversation flow for Australian/NZ customer expectations

# Example for Melbourne hotel:
prompt = f"""You are [AI_NAME], a helpful voice assistant at [HOTEL_NAME] in Melbourne. 
Your job is to respond to guest inquiries with appropriate audio responses.

🏨 MELBOURNE HOTEL RESPONSE RULES:
Guest asks about rooms → melbourne_room_availability.mp3
Guest mentions dates → Check season: summer_rates.mp3 or winter_rates.mp3
Guest asks amenities → melbourne_amenities.mp3
Guest asks location → melbourne_location_cbd.mp3
Guest wants to book → booking_process_au.mp3
Guest asks attractions → melbourne_attractions.mp3
..."""
```

### **Step 3: Update Voice & TTS Settings**
```python
# In config.py, update voice settings for AU/NZ:
VOICE_ID = "AU_VOICE_ID"   # ElevenLabs Australian/NZ accent voice
DEEPGRAM_LANGUAGE = "en-AU"  # Australian English (or en-NZ for New Zealand)

# In tts_engine.py, adjust voice settings for local market:
voice_settings = VoiceSettings(
    stability=0.7,           # Higher stability for professional tone
    similarity_boost=0.8,    # Good accent consistency
    style=0.2,              # Slight Australian/NZ warmth
    use_speaker_boost=True   # Essential for clear phone audio
)
```

---

## 🧪 **PHASE 4: Testing & Validation (45 minutes)**

### **Step 1: Audio Testing**
```bash
# 1. Test audio file loading:
py main.py
# Should see: "🎵 μ-law cache: [N] files loaded (X.XMB)"

# 2. Test individual audio files:
# Use /test endpoint to play specific files
# Verify all audio is clear with AU/NZ accent
# Check for proper pronunciation of local terms

# 3. Test audio chains:
# Ensure multiple files can play together smoothly
# Test transitions between different file types
```

### **Step 2: Conversation Flow Testing**
```bash
# Create test scenarios for AU/NZ industry:

# Melbourne Hotel Test Scenarios:
# 1. "I'm looking for a room in Melbourne CBD for next weekend"
# 2. "What facilities do you have?"  
# 3. "What are your rates for a standard room?"
# 4. "I need to change my booking"
# 5. "How do I get to your hotel from the airport?"
# 6. "What's nearby for entertainment?"

# Expected AI responses:
# - Should use Australian terminology and accent
# - Should mention Melbourne-specific amenities/locations
# - Should provide local context (CBD, transport, etc.)
# - Should guide through booking process clearly
```

### **Step 3: Twilio Integration Testing**
```bash
# Test Twilio Media Streams functionality:
# 1. Verify WebSocket connection establishes
# 2. Test μ-law audio streaming works correctly
# 3. Check session variables are tracked correctly:
#    - Mention dates → system should remember
#    - Ask about location → should use remembered city
# 4. Verify no repetitive responses
# 5. Check conversation history logging
# 6. Test both inbound and outbound call flows
```

---

## 🚀 **PHASE 5: Client Delivery (30 minutes)**

### **Step 1: Documentation Update**
```bash
# 1. Update README.md:
#    - Change title to client business
#    - Update AU/NZ specific examples
#    - Modify deployment instructions for Twilio AU/NZ
#    - Include local phone number formats (+61/+64)

# 2. Create CLIENT_SETUP_AU.md:
#    - Client-specific Twilio configuration
#    - AU/NZ phone number setup
#    - Business-specific webhook URLs
#    - Go-live checklist for Australian/NZ deployment
```

### **Step 2: Environment Configuration**
```bash
# 1. Create client-specific .env.example:
# Copy your .env but replace actual keys with placeholders
cp .env .env.example
# Edit .env.example to remove real API keys

# 2. Document API accounts needed for AU/NZ:
#    - Deepgram (same for all, supports en-AU/en-NZ)
#    - OpenAI/Gemini (same for all)  
#    - ElevenLabs (with Australian/NZ voice)
#    - Twilio (client's account with AU/NZ phone number)
```

### **Step 3: Deployment Package**
```bash
# Create deployment package for AU/NZ client:
# 1. Clean repository (remove logs, temp files)
# 2. Test fresh clone and setup
# 3. Create AU/NZ specific deployment checklist
# 4. Record demonstration video with local scenarios

# Final deliverables:
# ✅ GitHub repository with new client code
# ✅ All audio files (MP3 + μ-law)
# ✅ Updated configuration for Twilio AU/NZ
# ✅ Testing documentation with local test cases
# ✅ Deployment guide for AU/NZ
# ✅ Demo video showing Melbourne/Auckland scenarios
```

---

## 📊 **AU/NZ Industry-Specific Quick Guides**

### **🏨 AU/NZ Hotel Adaptation Checklist**
- [ ] Room types & availability (twin, queen, king)
- [ ] Amenities & services (pool, gym, wifi, car park)
- [ ] Booking & reservation process (direct booking, OTAs)
- [ ] Rate information by season (peak/off-peak)
- [ ] Location & directions (CBD, airport transfers)
- [ ] Special services (concierge, room service, laundry)
- [ ] Local attractions & tours (city-specific)
- [ ] Business facilities (meeting rooms, conference)

### **🏡 AU/NZ Real Estate Adaptation Checklist**  
- [ ] Property listings & availability
- [ ] Inspection bookings & open homes
- [ ] Price guides & market reports
- [ ] Suburb information & school zones
- [ ] Financing & mortgage assistance
- [ ] Property management services
- [ ] Investment property advice
- [ ] Settlement & conveyancing

### **🏥 AU/NZ Medical Adaptation Checklist**
- [ ] Doctor availability & bulk billing
- [ ] Appointment booking & Medicare
- [ ] Health fund & insurance billing
- [ ] Prescription renewals & repeats
- [ ] Pathology & test results
- [ ] Specialist referrals
- [ ] Practice locations & accessibility
- [ ] After-hours & emergency contacts

---

## ⚠️ **Common Pitfalls & Solutions**

### **Audio File Issues**
```bash
# 🚨 Problem: "❌ Intro audio not in cache: [filename].mp3" (MOST COMMON!)
# Solution: Update route files! This is the #1 missed step
#   - Edit routes/inbound.py: Change selected_intro = "your_new_intro.mp3"
#   - Edit routes/outbound.py: Change selected_intro = "your_new_intro.mp3"
#   - Make sure the filename matches what's in your audio_snippets.json

# Problem: μ-law conversion fails
# Solution: Check MP3 file quality, ensure librosa and audioop are installed

# Problem: Audio sounds robotic or accent is wrong
# Solution: Use professional Australian/NZ voice actor, natural speech patterns

# Problem: Twilio audio not playing
# Solution: Verify WebSocket message format uses 'streamSid' (camelCase)

# Problem: Files too large for git
# Solution: Use deployment options in main README, keep audio separate

# Problem: Cache shows files loaded but none play
# Solution: Check audio_snippets.json format, ensure MP3 filenames match .ulaw files
```

### **Configuration Issues**
```bash
# Problem: AI gives wrong responses for AU/NZ context
# Solution: Update prompts with local examples, terminology, and city references

# Problem: Session variables not tracking
# Solution: Verify variable names match in config.py and router.py

# Problem: TTS fallback not working with AU/NZ voice
# Solution: Check ElevenLabs API key and voice ID for Australian/NZ accent
```

### **Deployment Issues**
```bash
# Problem: Audio files missing on production
# Solution: Use audio deployment options from main README

# Problem: Environment variables not loading
# Solution: Verify .env file is copied to production server

# Problem: Twilio integration fails
# Solution: Check webhook URLs match client's domain and Twilio account region
```

---

## 💰 **Pricing Guide for AU/NZ Clients**

### **Development Cost Breakdown (AUD)**
- **Repository Setup & Customization:** $400-600
- **Audio Content Creation (AU/NZ accent):** $1,200-2,000 (depends on # of responses)
- **Configuration & Testing:** $600-800
- **Deployment & Training:** $400-600
- **Total Project:** $2,600-4,000 AUD

### **Ongoing Costs (Monthly - AUD)**
- **Server Hosting (AWS AU/NZ):** $80-150
- **Twilio AU/NZ:** $150-400 (based on call volume)
- **API Costs:** $80-200 (Deepgram, OpenAI, ElevenLabs)
- **Maintenance & Support:** $300-500
- **Total Monthly:** $610-1,250 AUD

---

## 📞 **Support & Next Steps**

### **For Freelancers/VAs working with AU/NZ clients:**
1. **Follow this guide step-by-step**
2. **Test thoroughly with local scenarios before delivery**
3. **Keep original repository as template for future AU/NZ clients**
4. **Document any client-specific customizations**
5. **Understand local business practices and terminology**

### **For AU/NZ Clients:**
1. **Review adapted system thoroughly with local test scenarios**
2. **Test with real business scenarios (Melbourne hotel, Auckland real estate, etc.)**
3. **Provide feedback on local accuracy and pronunciation**
4. **Schedule training for staff on system monitoring**
5. **Plan go-live strategy with backup support**

### **Quality Assurance Checklist for AU/NZ:**
- [ ] All audio files play correctly with proper AU/NZ accent
- [ ] Session memory works as expected with local context
- [ ] Industry-specific responses are accurate for AU/NZ market
- [ ] Local terminology and references are correct
- [ ] Twilio integration works with AU/NZ phone numbers
- [ ] Configuration matches client business and local practices
- [ ] Deployment documentation includes AU/NZ specific instructions

---

**🎉 Congratulations!** You've successfully adapted the Klariqo AI Voice Assistant for an AU/NZ client. The system is now ready for production deployment with Twilio integration.

**Next Steps:**
1. **Follow the deployment guide in the main README.md**
2. **Configure Twilio with AU (+61) or NZ (+64) phone number**
3. **Test with client's target audience**
4. **Go live with confidence!**