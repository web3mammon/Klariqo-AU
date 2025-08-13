# 🏫 Klariqo AI Voice Assistant v3.0 - AU/NZ Edition

**Production-Ready Business Voice System** | Ultra-Fast μ-law Streaming | Patent-Pending Technology

Intelligent AI voice assistant that handles customer inquiries across multiple industries. Features **human-like conversation memory**, **contextual responses**, **call forwarding**, **agent transfer**, and **comprehensive customer data tracking** optimized for Australian and New Zealand telephony systems.

## 🆕 **Version 3.0 - Twilio AU/NZ Production**

### **🎵 μ-law Audio Revolution**
- **Direct μ-law Streaming** - No conversion overhead, direct audio serving
- **Twilio Media Streams** - Full bidirectional streaming with flexible chunking
- **Memory-Cached μ-law** - All audio files loaded into RAM for instant access
- **Excel-to-JSON Converter** - Manage all audio files via simple Excel spreadsheet
- **Hybrid Audio System** - Pre-recorded snippets + TTS fallback with μ-law conversion

### **⚡ Performance Optimizations**
- **0-50ms Response Time** - Pre-recorded snippets served directly from memory
- **μ-law Format Compliance** - 8-bit μ-law, 8kHz, mono for AU/NZ telephony
- **Flexible Chunking** - Optimized for Twilio Media Streams
- **TTS Fallback** - Dynamic MP3→μ-law conversion when snippets unavailable

### **🤖 Enhanced AI Engine**
- **Multi-Model Support** - Switch between Groq (Llama), OpenAI (GPT-3.5/4), or Gemini
- **Smart File Selection** - AI automatically chooses appropriate audio responses
- **Structured Prompting** - Rule-based responses with intelligent fallbacks
- **Session Memory** - Prevents repetitive responses, natural conversations
- **Configurable Australian Timezones** - GPT uses client-specific timezone (Sydney, Melbourne, Brisbane, Adelaide, Perth, etc.) for accurate "today"/"tomorrow" handling

### **📞 Call Management Features**
- **Call Forwarding** - Configurable boolean flag to forward calls to existing business numbers
- **Agent Transfer** - Mid-conversation transfer to human agents when requested
- **Emergency Handling** - Automatic transfer for urgent situations
- **Flexible Setup** - Support for both AI-first and direct-forwarding modes

### **📊 Enterprise Features** 
- **Comprehensive Logging** - Every call tracked in CSV format
- **Session Management** - Handles concurrent calls with isolated state
- **Hot Reloading** - Update audio library without system restart
- **Debug Endpoints** - System health monitoring and troubleshooting
- **Customer Data Export** - Automatic CSV export of customer information and booking details
- **Business Analytics Dashboard** - Real-time customer data visualization and download
- **Complete Customer Tracking** - Name, phone, location, service type, urgency, issue description
- **Configurable Australian Timezones** - All customer timing preferences properly understood in client's specific timezone

## 🎯 What This Does

- **AI Assistant** handles customer inquiries across multiple industries (hotels, real estate, schools, plumbing, etc.)
- Handles both **inbound** (customers calling business) and **outbound** (business calling customers) 
- Uses **pre-recorded μ-law audio snippets** for ultra-fast, human-like responses
- **Smart AI with conversation memory** remembers customer conversation context
- **Dynamic contextual responses** based on gathered information (industry-specific details)
- **Call forwarding capability** - Forward calls to existing business numbers
- **Agent transfer system** - Transfer to human agents when customers request
- **Complete customer data capture** - Name, phone, location, service, urgency, issue description
- **Configurable Australian timezone awareness** - Proper handling of "today", "tomorrow", scheduling in client's specific timezone
- Falls back to **real-time TTS** (with μ-law conversion) only when needed
- **Excel-driven content management** for easy updates by business staff
- **Automatic customer data collection** and CSV export for business reporting
- Logs every conversation for analysis and improvement
- **Twilio integration** optimized for Australian and New Zealand telephony systems

## 📞 **PRODUCTION DEPLOYMENT READY**

**This system is ready for immediate deployment at any business using Twilio AU/NZ.**

✅ **Production Features:**
- **Session Memory**: Remembers customer conversation context 
- **Dynamic Responses**: Gives specific information based on customer needs
- **17+ Professional Audio Responses**: Customizable for any industry
- **Twilio Integration**: Optimized for AU/NZ telephony with proper μ-law format
- **Comprehensive Logging**: Tracks all conversations for business analytics
- **Customer Data Export**: Automatic collection and CSV export of customer information
- **Business Dashboard**: Real-time customer data visualization and download
- **Call Forwarding**: Forward calls to existing business numbers
- **Agent Transfer**: Transfer to human agents when needed
- **Complete Customer Tracking**: All essential customer details captured and logged

## 📚 **Documentation & Guides**

### **Essential Reading for New Team Members:**

1. **[CLIENT_ADAPTATION_GUIDE.md](CLIENT_ADAPTATION_GUIDE.md)** - Complete step-by-step guide for adapting this system to different industries and clients
2. **[CALL_FORWARDING_GUIDE.md](CALL_FORWARDING_GUIDE.md)** - How to configure call forwarding to existing business numbers
3. **[AGENT_TRANSFER_GUIDE.md](AGENT_TRANSFER_GUIDE.md)** - How the agent transfer system works and configuration options
4. **[CUSTOMER_DATA_TRACKING_GUIDE.md](CUSTOMER_DATA_TRACKING_GUIDE.md)** - Complete guide to customer data capture, logging, and export
5. **[API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)** - Detailed API setup and configuration for all services
6. **[CALENDAR_INTEGRATION_GUIDE.md](CALENDAR_INTEGRATION_GUIDE.md)** - Complete Google Calendar integration for real-time appointment booking
7. **[CLIENT_CALENDAR_SETUP_GUIDE.md](CLIENT_CALENDAR_SETUP_GUIDE.md)** - Simple setup guide for clients to connect their existing Google Calendar
8. **[AUSTRALIAN_TIMEZONE_GUIDE.md](AUSTRALIAN_TIMEZONE_GUIDE.md)** - Configurable timezone system for different Australian cities

### **Quick Reference for Different Roles:**

**For VAs & Content Teams:**
- Start with `CLIENT_ADAPTATION_GUIDE.md` for industry customization
- Use `CUSTOMER_DATA_TRACKING_GUIDE.md` to understand what data is captured
- Reference `CALL_FORWARDING_GUIDE.md` for client setup options
- Share `CLIENT_CALENDAR_SETUP_GUIDE.md` with clients for Google Calendar integration

**For Python Developers:**
- Review `API_INTEGRATION_GUIDE.md` for technical setup
- Study `AGENT_TRANSFER_GUIDE.md` for transfer logic implementation
- Check `CUSTOMER_DATA_TRACKING_GUIDE.md` for data flow architecture
- Reference `AUSTRALIAN_TIMEZONE_GUIDE.md` for timezone configuration

**For Business Analysts:**
- Focus on `CUSTOMER_DATA_TRACKING_GUIDE.md` for analytics capabilities
- Review `CALL_FORWARDING_GUIDE.md` for business setup options
- Use `CLIENT_ADAPTATION_GUIDE.md` for client requirements gathering

## 🔐 **IMPORTANT: Git & Audio Files Management**

### **Why Audio Files Are Not in Git (This is CORRECT!)**
```bash
# Your .gitignore properly excludes:
audio_ulaw/             # μ-law audio files (1.8MB total)
audio_optimised/        # Converted audio files  
*.ulaw                  # All μ-law files
.env                    # API keys and secrets
logs/                   # Runtime logs
temp/                   # Temporary files
```

**This is PROFESSIONAL best practice because:**
- ✅ **Security**: Keeps API keys out of version control
- ✅ **Performance**: Prevents 1.8MB+ audio files from bloating git history
- ✅ **Scalability**: Separates code from assets (industry standard)
- ✅ **Deployment**: Allows independent code and asset updates

### **Current Production Status: 100% Ready** 
- ✅ **All code is in git and deployable**
- ✅ **17 μ-law audio files converted** (`audio_ulaw/` directory)
- ✅ **Environment configuration complete** (`.env` with all API keys)
- ✅ **Audio files deployment automated** (see deployment section below)

### **📋 For Freelancers & New Client Adaptation:**
👉 **See [CLIENT_ADAPTATION_GUIDE.md](CLIENT_ADAPTATION_GUIDE.md)** for complete step-by-step instructions on adapting this system for different industries.

**Perfect for AU/NZ businesses:**
- 🏨 **Hotels in Melbourne/Sydney** - Room bookings, amenities, concierge services
- 🏡 **Real Estate in Auckland/Brisbane** - Property inquiries, inspections, market info
- 🏥 **Medical practices** - Appointments, billing, patient services
- 🛒 **E-commerce** - Orders, returns, customer support
- 🏫 **Educational institutions** - Admissions, events, parent inquiries
- 🔧 **Plumbing/Service Businesses** - Emergency calls, appointment booking, service inquiries

The guide covers:
- ✅ **Content planning** for AU/NZ market requirements
- ✅ **Audio file creation** with Australian/NZ accents and terminology
- ✅ **Conversation logic** for local business practices
- ✅ **Twilio configuration** for AU/NZ deployment
- ✅ **Testing and validation** procedures
- ✅ **Industry-specific examples** with local context

## 📊 **Customer Data Export System**

### **🎯 Business Intelligence Built-In**
The system automatically collects and exports customer data for business reporting:

**📋 Data Collected Per Call:**
- **Customer Information**: Name, phone, location
- **Service Details**: Type of service, urgency level, property type
- **Booking Information**: Preferred dates/times, selected appointments
- **Conversation Analysis**: Booking status, follow-up requirements
- **Call Analytics**: Duration, conversation summary, business outcomes

**📊 Export Features:**
- **Automatic CSV Export**: Every call session saved to `customer_data/customer_sessions.csv`
- **Business Dashboard**: View recent customers at `/customer-data`
- **Download Reports**: Download full customer database anytime
- **Follow-up Tracking**: Identifies customers needing callbacks
- **Booking Analytics**: Track conversion rates and service preferences

**🔗 Dashboard Access:**
- **Health Check**: `http://localhost:5000/` - Shows export statistics
- **Customer Data**: `http://localhost:5000/customer-data` - Recent customer sessions
- **CSV Download**: `http://localhost:5000/download-customer-data` - Full customer database

**💼 Client Benefits:**
- **CRM Integration**: CSV files import into any CRM system
- **Business Analytics**: Track customer patterns and service demand
- **Follow-up Management**: Know who needs callbacks and why
- **Performance Metrics**: Measure booking conversion rates
- **Customer Database**: Build comprehensive customer profiles

### **📈 Example Customer Data Output:**
```csv
call_sid,call_date,call_time,customer_name,customer_phone,service_type,booking_status
CA123,2024-08-01,14:30:25,John Smith,0412345678,blocked_drain,Booked - Confirmed
CA124,2024-08-01,15:45:12,Sarah Jones,,leaking_tap,Interested - No Booking
CA125,2024-08-01,16:20:33,Mike Wilson,0498765432,emergency,Emergency - Immediate Service
```

## 🏗️ Architecture

```
├── main.py                 # Application runner & WebSocket handler with μ-law streaming
├── config.py              # Centralized configuration management (call forwarding, agent transfer)
├── session.py             # Call session state management with customer data tracking
├── router.py              # AI-powered response selection with date/time context
├── audio_manager.py       # μ-law audio file library management with memory caching
├── tts_engine.py          # ElevenLabs TTS fallback with MP3→μ-law conversion
├── logger.py              # Structured call logging to CSV with customer data export
├── session_data_exporter.py # Customer data export and business analytics
├── routes/
│   ├── inbound.py         # Inbound call handlers with forwarding/transfer support
│   ├── outbound.py        # Outbound call & campaign management
│   └── test.py            # Testing & debug endpoints (call forwarding, agent transfer)
├── audio_optimised/       # Original high-quality audio files (MP3)
├── audio_ulaw/            # μ-law audio files (8-bit, 8kHz, mono) - USED BY SYSTEM
├── logs/                  # Call logs, conversation transcripts, customer data
├── temp/                  # Temporary TTS generated files
├── audio_snippets.json    # Auto-generated from Excel (don't edit manually)
├── audio_files.xlsx       # YOUR MAIN AUDIO MANAGEMENT FILE
├── excel_to_json.py       # Excel to JSON converter script
├── audio-optimiser.py     # MP3→μ-law conversion utility
├── .env                   # Environment variables & API keys
└── requirements.txt       # Python dependencies

📚 Documentation:
├── CLIENT_ADAPTATION_GUIDE.md      # Industry adaptation guide
├── CALL_FORWARDING_GUIDE.md        # Call forwarding configuration
├── AGENT_TRANSFER_GUIDE.md         # Agent transfer system guide
├── CUSTOMER_DATA_TRACKING_GUIDE.md # Customer data capture & export
└── API_INTEGRATION_GUIDE.md        # API setup & configuration
```

## 📞 **Call Management Features**

### **Call Forwarding System**
- **Configurable Boolean Flag**: `CALL_FORWARDING["enabled"]` in `config.py`
- **Two Modes**: AI Assistant mode vs Direct Forwarding mode
- **Customizable Settings**: Forward-to number, message, timeout
- **Business Flexibility**: Easy adaptation for different client preferences

### **Agent Transfer System**
- **Mid-Conversation Transfer**: Transfer to human agents when requested
- **Automatic Detection**: Keywords like "speak to agent", "human", "emergency"
- **Context Preservation**: Customer details passed to human agent
- **Flexible Configuration**: Transfer keywords and conditions customizable

### **Customer Data Tracking**
- **Real-time Capture**: Name, phone, location, service type, urgency, issue description
- **Date/Time Context**: GPT always knows current date/time for accurate scheduling
- **CSV Export**: Business-ready data files for CRM integration
- **Session Persistence**: Data survives connection issues and technical problems

## 📋 Prerequisites

1. **Python 3.8+** 
2. **API Accounts:**
   - [Twilio](https://twilio.com) - Voice calling & streaming (AU/NZ regions supported)
   - [Deepgram](https://deepgram.com) - Speech-to-Text
   - [OpenAI](https://openai.com) or [Groq](https://groq.com) - LLM for response selection
   - [ElevenLabs](https://elevenlabs.io) - Text-to-Speech fallback
3. **ngrok** - For local development webhooks
4. **Audio Libraries** - `librosa` and `audioop` for TTS μ-law conversion

## 🚀 Quick Setup

### 1. Clone & Install
```bash
git clone https://github.com/web3mammon/Klariqo-AU.git
cd Klariqo-AU
pip install -r requirements.txt
# All dependencies including librosa & numpy are now included ✅
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
nano .env
```

**Production-Ready Environment Variables:**
```env
# Required for Production
DEEPGRAM_API_KEY=your_deepgram_key        # Speech recognition
ELEVENLABS_API_KEY=your_elevenlabs_key    # Voice synthesis fallback

# AI Model (choose one - OpenAI recommended for production)
OPENAI_API_KEY=your_openai_key            # Most reliable for production
# OR
GEMINI_API_KEY=your_gemini_key            # Cost-effective alternative

# Twilio (Primary for AU/NZ Deployment)
TWILIO_ACCOUNT_SID=your_twilio_sid        # From Twilio Console
TWILIO_AUTH_TOKEN=your_twilio_token       # From Twilio Console
TWILIO_PHONE=+61XXXXXXXXXX                # AU number (+64 for NZ)

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False                         # Set to False for production
```

### 3. Prepare Audio Files & μ-law Conversion

**CRITICAL: Audio files must be in μ-law format for Twilio Media Streams**

```bash
# 1. Create your audio management Excel file
# Columns: Filename | Transcript | Category | Alternate_Version

# 2. Convert Excel to JSON
py excel_to_json.py
# Choose option 1 to convert

# 3. Convert MP3 files to μ-law format (REQUIRED)
py audio-optimiser.py
# This converts audio_optimised/ → audio_ulaw/ (μ-law format)

# 4. Your directory structure:
mkdir audio_optimised         # Original MP3 files from recording
mkdir audio_ulaw             # μ-law files (system uses these)
mkdir temp                   # Temporary TTS files
mkdir logs                   # Call logs and analytics
```

**Excel Structure Example:**
| Filename | Transcript | Category | Alternate_Version |
|----------|------------|----------|-------------------|
| intro_klariqo.mp3 | नमस्ते! मैं निशा... | introductions | intro_klariqo2.mp3 |
| pricing_basic.mp3 | हमारी pricing... | pricing | pricing_detailed.mp3 |

### 4. Run the System
```bash
py main.py
```

The system will:
- ✅ Validate configuration and API keys
- 🎵 Load μ-law audio files into memory cache
- 🌐 Start ngrok tunnel (for webhooks)
- 📞 Display webhook URLs for Twilio AU/NZ
- 🧪 Provide test page URL

## 🎵 μ-law Audio System (NEW!)

### **Understanding the Audio Flow**

**For New Developers:** Our system uses a hybrid approach for optimal performance:

1. **Pre-recorded Responses (95% of calls)**: 
   - AI selects appropriate audio file
   - System serves μ-law data directly from memory
   - **Latency: 0-50ms** ⚡

2. **TTS Fallback (5% of calls)**:
   - AI generates text response
   - ElevenLabs creates MP3 audio
   - System converts MP3→μ-law in real-time
   - **Latency: 200-500ms** 🔄

### **Excel-Based Workflow (For Content Teams)**

**Step 1: Create/Update Audio Content**
```bash
# 1. Record new audio as MP3 files
# 2. Save to audio_optimised/ folder
# 3. Update audio_files.xlsx with new entries
# 4. Run converter: py excel_to_json.py
# 5. Convert to μ-law: py audio-optimiser.py
# 6. Restart system: py main.py
```

**Step 2: Excel File Structure**
- **Filename**: `intro_klariqo.mp3` (without path)
- **Transcript**: `नमस्ते! मैं निशा बोल रही हूं...` (what Nisha says)
- **Category**: `introductions` (auto-categorization)
- **Alternate_Version**: `intro_klariqo2.mp3` (optional variation)

### **μ-law Technical Details (For Developers)**

**Why μ-law Format?**
- **Twilio Media Streams Standard**: Required format for bidirectional streaming
- **No Conversion Overhead**: Direct streaming to callers
- **AU/NZ Telephony Compliance**: 8-bit μ-law, 8kHz, mono required
- **Flexible Chunking**: Twilio supports variable chunk sizes

**Audio Manager Implementation:**
```python
# System loads μ-law files but stores with MP3 keys for compatibility
audio_manager.memory_cache["intro_business.mp3"] = ulaw_bytes_data

# AI router uses MP3 references
router_response = "intro_business.mp3 + pricing_basic.mp3"

# System fetches μ-law data and streams to caller via WebSocket
```

## 🧪 Testing

### Browser Testing
1. Go to `http://your-ngrok-url/test`
2. Click "Call +61XXXXXXXXX" (update with your AU/NZ number)
3. Answer the call and test customer inquiry scenarios
4. Experience AI handling inquiries with ultra-low latency!

### **New Feature Testing**

**Call Forwarding Test:**
1. Visit `http://your-ngrok-url/debug/call_forwarding`
2. Check current configuration status
3. Test with `CALL_FORWARDING["enabled"] = True` in `config.py`
4. Verify calls are forwarded to specified number

**Agent Transfer Test:**
1. Visit `http://your-ngrok-url/debug/agent_transfer`
2. Check transfer keywords and configuration
3. During a call, say "I want to speak to a human"
4. Verify transfer to agent number

**Customer Data Tracking Test:**
1. Visit `http://your-ngrok-url/debug/call_logs`
2. Make a test call with customer details
3. Check `logs/customer_data.csv` for captured information
4. Verify date/time context works correctly

### API Testing
```bash
# Start outbound campaign
curl -X POST http://your-ngrok-url/outbound/start_campaign

# Check system health with μ-law cache status
curl http://your-ngrok-url/debug/system_health

# System health check
curl http://your-ngrok-url/

# Test call forwarding configuration
curl http://your-ngrok-url/debug/call_forwarding

# Test agent transfer configuration  
curl http://your-ngrok-url/debug/agent_transfer
```

## 📞 Telephony Integration

### **Twilio Setup (AU/NZ Production Ready)**
```bash
# Configure in Twilio Console:
# 1. Incoming Call URL: https://your-business-domain.com/twilio/voice
# 2. HTTP Method: POST
# 3. Enable Media Streams for bidirectional audio
# 4. Audio format: μ-law, 8-bit, 8kHz, mono (automatic)
# 5. Purchase Twilio phone number for AU (+61) or NZ (+64)
# 6. Set up TwiML webhook handlers
# 7. Configure WebSocket streaming endpoint
```

### **Twilio Media Streams Configuration**
```bash
# Required webhook endpoints:
# Incoming calls: /twilio/voice
# WebSocket handler: /media/<call_sid>
# Both support inbound and outbound call flows
```

## 🤖 AI Model Configuration

### **Switching AI Models (For Developers)**

**Current Default: OpenAI GPT-3.5-turbo**
```python
# In router.py
from openai import OpenAI
client = OpenAI(api_key=Config.OPENAI_API_KEY)
model = "gpt-3.5-turbo"  # Reliable, 200-500ms
```

**Ultra-Fast Option: Groq Llama**
```python
# In router.py
from groq import Groq
client = Groq(api_key=Config.GROQ_API_KEY)
model = "llama-3.1-8b-instant"  # 50-100ms
```

**Google Option: Gemini**
```python
# In router_gemini.py (alternative router)
import google.generativeai as genai
genai.configure(api_key=Config.GEMINI_API_KEY)
model = "gemini-1.5-flash"  # Fast and reliable
```

### **Model Performance Comparison**
| Model | Speed | Reliability | Cost/1M tokens | Best For |
|-------|-------|-------------|----------------|----------|
| Llama-3.1-8b | 🚀 50-100ms | ⭐⭐⭐ | $0.10 | Speed-critical calls |
| GPT-3.5-turbo | ⚡ 200-500ms | ⭐⭐⭐⭐⭐ | $0.50 | Production reliability |
| Gemini-1.5-flash | ⚡ 150-300ms | ⭐⭐⭐⭐ | $0.15 | Cost-effective option |

## 🔧 Advanced Configuration

### **For Content Teams (Non-Technical)**

**Adding New Responses:**
1. Record new MP3 file and save to `audio_optimised/` folder
2. Open `audio_files.xlsx` in Excel
3. Add new row with filename and transcript
4. Run: `py excel_to_json.py` (choose option 1)
5. Run: `py audio-optimiser.py` (converts to μ-law)
6. Restart system: `py main.py`

**Updating Existing Content:**
1. Replace MP3 file in `audio_optimised/` folder
2. Update transcript in Excel if needed
3. Re-run converter and optimizer
4. System will auto-reload new content

### **For Developers**

**Custom Response Logic:**
```python
# In router.py, add new matching rules:
User asks about scholarships → scholarship_info.mp3 + eligibility_criteria.mp3
```

**Session Memory Flags:**
```python
# In config.py, add new tracking flags:
SESSION_FLAGS_TEMPLATE = {
    "intro_played": False,
    "pricing_mentioned": False,
    "scholarship_discussed": False,  # New flag
}
```

**PCM Audio Validation:**
```python
# Test PCM cache loading
python -c "from audio_manager import audio_manager; print(f'Loaded: {len(audio_manager.memory_cache)} files')"
```

## 🐛 Troubleshooting

### **Common Issues for New Team Members**

**"No audio files found in cache"**
- ✅ Check `audio_ulaw/` folder exists and has `.ulaw` files
- ✅ Run `py excel_to_json.py` to update JSON
- ✅ Run `py audio-optimiser.py` to convert MP3→μ-law
- ✅ Verify filenames in Excel match actual files

**"μ-law audio file not in cache"**
- ✅ Check `audio_snippets.json` uses `.mp3` extensions (not `.ulaw`)
- ✅ Ensure μ-law files exist in `audio_ulaw/` folder
- ✅ Restart system to reload audio cache

**"TTS MP3 to μ-law conversion failed"**
- ✅ Install missing libraries: `pip install librosa audioop-lts`
- ✅ Check ElevenLabs API quota and voice ID
- ✅ Test TTS separately: `py -c "from tts_engine import tts_engine; print(tts_engine.generate_audio('test'))"`

**"Twilio audio not playing"**
- ✅ Verify μ-law format: 8-bit, 8kHz, mono
- ✅ Check WebSocket message format uses `streamSid` (camelCase)
- ✅ Test with single audio file first

### **New Feature Troubleshooting**

**"Call forwarding not working"**
- ✅ Check `CALL_FORWARDING["enabled"]` is set to `True` in `config.py`
- ✅ Verify `forward_to_number` is a valid phone number
- ✅ Test configuration at `/debug/call_forwarding`
- ✅ Ensure Twilio number is properly configured

**"Agent transfer not triggering"**
- ✅ Check `AGENT_TRANSFER["enabled"]` is set to `True` in `config.py`
- ✅ Verify transfer keywords in configuration
- ✅ Test configuration at `/debug/agent_transfer`
- ✅ Ensure agent number is valid and reachable

**"Customer data not being captured"**
- ✅ Check session variables are being updated in `router.py`
- ✅ Verify logger is receiving session variables
- ✅ Check `logs/customer_data.csv` for data export
- ✅ Test with explicit customer information in conversation

**"Date/time context not working"**
- ✅ Verify current Australian date/time (AEST/AEDT) is being passed to GPT
- ✅ Check router context prompt includes date information
- ✅ Test with "today" or "tomorrow" in conversation
- ✅ Ensure system clock is correct
- ✅ Verify pytz is installed for timezone handling

### **Debug Commands**
```bash
# Test audio cache loading
py -c "from audio_manager import audio_manager; print(f'Cache: {len(audio_manager.memory_cache)} files')"

# Test specific file
py -c "from audio_manager import audio_manager; print('intro_business.mp3' in audio_manager.memory_cache)"

# View memory usage
py -c "from audio_manager import audio_manager; stats = audio_manager.get_memory_stats(); print(f'Total: {stats[\"total_size_mb\"]:.1f}MB')"

# Test TTS conversion
py -c "from main import convert_mp3_to_ulaw_for_tts; print('TTS conversion available:', convert_mp3_to_ulaw_for_tts is not None)"

# Test call forwarding configuration
py -c "from config import Config; print('Call forwarding enabled:', Config.CALL_FORWARDING['enabled'])"

# Test agent transfer configuration
py -c "from config import Config; print('Agent transfer enabled:', Config.AGENT_TRANSFER['enabled'])"

# Test customer data tracking
py -c "from config import Config; print('Session variables:', len(Config.SESSION_VARIABLES_TEMPLATE))"

# View logs
tail -f logs/call_logs.csv
tail -f logs/conversation_logs.csv
tail -f logs/customer_data.csv
```

## 📈 Performance Metrics & Updates

### **Version 3.0 Benchmarks (Current)**
- **Pre-recorded Audio Response**: 0-50ms (μ-law direct from memory)
- **TTS Fallback Response**: 200-500ms (MP3→μ-law conversion)
- **Memory Usage**: ~8-12MB for 17 μ-law audio files (50% smaller than PCM)
- **File Loading**: Instant (all files pre-cached in RAM)
- **Telephony Compatibility**: 100% (proper μ-law format for Twilio)
- **AI Accuracy**: 95%+ with structured prompting

### **Performance Comparison**
| Metric | v2.5 (PCM) | v3.0 (μ-law) | Improvement |
|--------|-------------|-------------|-------------|
| Response Time | 0-50ms | 0-50ms | Same speed |
| Memory Usage | 15MB | 8MB | 🚀 50% smaller |
| Audio Quality | Telephony-optimized | Twilio-optimized | Superior for AU/NZ |
| File Size | Larger | 50% smaller | Better efficiency |

### **Recent Major Updates**

**v3.0 (Current) - Twilio AU/NZ Production**
- ✅ Direct μ-law audio streaming (0-50ms responses)
- ✅ Twilio Media Streams bidirectional integration
- ✅ Memory-cached audio files for instant access
- ✅ TTS fallback with real-time MP3→μ-law conversion
- ✅ WebSocket-based streaming architecture

**v2.5 (Previous) - PCM Revolution**
- ✅ Direct PCM audio streaming
- ✅ Exotel integration for Indian market
- ✅ Excel-to-JSON audio management system
- ✅ Multi-model AI support (Groq/OpenAI/Gemini)

## 🚀 **PRODUCTION DEPLOYMENT CHECKLIST**

### **✅ System Ready For Deployment (Yes!)**
This system is **immediately deployable** for any business. Here's what you get:

**Core Features Ready:**
- ✅ **17 μ-law Audio Files** optimized for Twilio AU/NZ
- ✅ **Dynamic Session Variables** tracking (context-aware)
- ✅ **Intelligent Conversation Flow** with memory
- ✅ **Professional Customer Interaction** handling
- ✅ **Comprehensive Logging** for business analytics
- ✅ **Excel-based Content Management**
- ✅ **Multi-industry Support** (customizable for any business)

**New Call Management Features:**
- ✅ **Call Forwarding System** - Forward calls to existing business numbers
- ✅ **Agent Transfer System** - Transfer to human agents when requested
- ✅ **Emergency Handling** - Automatic transfer for urgent situations
- ✅ **Flexible Configuration** - AI-first or direct-forwarding modes

**Customer Data & Analytics:**
- ✅ **Complete Customer Tracking** - Name, phone, location, service, urgency, issue description
- ✅ **Configurable Australian Timezones** - Accurate "today"/"tomorrow" handling in client's specific timezone
- ✅ **CSV Export System** - Business-ready data files for CRM integration
- ✅ **Session Data Exporter** - Automatic customer data collection and export
- ✅ **Business Intelligence** - Analytics on call patterns and customer behavior

**Infrastructure Ready:**
- ✅ **Twilio Integration** with proper TwiML format
- ✅ **μ-law Audio Streaming** for optimal call quality
- ✅ **WebSocket Handling** for real-time bidirectional conversation
- ✅ **Error Handling & Fallbacks** for production stability
- ✅ **Health Monitoring** endpoints
- ✅ **Debug Interfaces** for call forwarding, agent transfer, and customer data

### **🎯 Ready To Launch Tomorrow**
**Required Time:** ~2 hours to deploy for any AU/NZ business
**Required Skills:** Basic server setup + Twilio account
**Cost:** Twilio subscription + server hosting (~AUD $150/month total)

---

## 🏗️ **PRODUCTION DEPLOYMENT GUIDE**

### **Step 1: Code Deployment (15 minutes)**
```bash
# 1. Deploy code from git to production server
git clone https://github.com/web3mammon/Klariqo-AU.git
cd Klariqo-AU
pip install -r requirements.txt
# All dependencies including audio processing libraries are included ✅

# 2. Configure environment (copy from development)
# IMPORTANT: .env is not in git (security), so copy it manually
scp .env production-server:/path/to/klariqo-schools/
```

### **Step 1.5: Audio Files Deployment (15 minutes)**
```bash
# CRITICAL: Audio files are NOT in git (by design)
# You have 3 deployment options:

# Option A: Upload from development machine (Recommended)
scp -r audio_ulaw/ production-server:/path/to/Klariqo-AU/
scp -r audio_optimised/ production-server:/path/to/Klariqo-AU/

# Option B: Regenerate on production server
scp audio_files.xlsx production-server:/path/to/Klariqo-AU/
# Then on production server:
py excel_to_json.py
py audio-optimiser.py

# Option C: Force add to git (for simple deployment)
git add -f audio_ulaw/ audio_optimised/
git commit -m "Add audio assets for deployment"
git push
# Then normal git clone will include audio files
```

### **Step 1.6: System Startup (5 minutes)**
```bash
# 1. Verify all components
ls audio_ulaw/  # Should show 17 .ulaw files
cat .env | head -5  # Should show API keys (not empty)

# 2. Start system
py main.py
# Should see: "🎵 μ-law cache: 17 files loaded (1.7MB)"
```

### **Step 2: Twilio Configuration (15 minutes)**
```bash
# 1. Login to Twilio Console
# 2. Purchase a phone number for AU (+61) or NZ (+64)
# 3. Set up Voice App:
#    - Incoming Call URL: https://your-server.com/twilio/voice
#    - HTTP Method: POST
#    - Enable Media Streams for bidirectional audio
#    - WebSocket handler: https://your-server.com/media/<call_sid>

# 4. Test the number - customers can now call!
```

### **Step 3: Business Integration (15 minutes)**
```bash
# 1. Update business's published phone number to Twilio number
# 2. Train staff on system monitoring
# 3. Set up call log monitoring: /logs/call_logs.csv
# 4. Test customer inquiry scenarios

# 🎉 SYSTEM IS LIVE!
```

### **Step 4: Content Customization (Optional)**
```bash
# Update audio_files.xlsx with business-specific information
# Run: py excel_to_json.py
# Run: py audio-optimiser.py  
# Restart: py main.py
```

## 📚 Onboarding Guide for New Team Members

### **For Prompt Engineers**
1. **Understand the audio flow**: Pre-recorded snippets vs TTS fallback
2. **Study `router.py`**: Learn how AI matches user input to audio files
3. **Practice with Excel**: Update `audio_files.xlsx` and test changes
4. **Test different scenarios**: Ensure comprehensive coverage of user inputs
5. **Learn date/time context**: Understand how "today"/"tomorrow" are handled
6. **Review customer data extraction**: See how customer details are captured

### **For Python Developers**
1. **Study the architecture**: Main components and data flow
2. **Understand PCM format**: Why telephony systems need specific audio formats
3. **Learn WebSocket handling**: How real-time audio streaming works
4. **Practice debugging**: Use debug commands and log analysis
5. **Review call management**: Study call forwarding and agent transfer logic
6. **Understand customer data flow**: Session variables, logging, and export systems

### **For Content Teams**
1. **Master Excel workflow**: How to add/update audio content
2. **Understand categories**: How to organize audio files logically
3. **Learn quality standards**: Recording quality and transcript accuracy
4. **Test your changes**: Always verify updates work before deploying
5. **Review customer tracking**: Understand what data is captured from calls
6. **Study call management**: Know when calls are forwarded or transferred

### **For Operations Teams**
1. **Monitor system health**: Use debug endpoints and log analysis
2. **Understand metrics**: Response times, cache hit rates, error rates
3. **Learn troubleshooting**: Common issues and resolution steps
4. **Track performance**: Monitor call success rates and user satisfaction
5. **Review customer data**: Check CSV exports and business analytics
6. **Monitor call management**: Track forwarding and transfer patterns

### **For Business Analysts**
1. **Study customer data tracking**: Review `CUSTOMER_DATA_TRACKING_GUIDE.md`
2. **Understand call management**: Review `CALL_FORWARDING_GUIDE.md` and `AGENT_TRANSFER_GUIDE.md`
3. **Analyze business intelligence**: Use CSV exports for customer analytics
4. **Review client adaptation**: Study `CLIENT_ADAPTATION_GUIDE.md` for industry customization
5. **Monitor performance metrics**: Track call success rates and customer satisfaction
6. **Generate business reports**: Use exported data for client reporting

## 📄 Patent Information

This system implements our **"Modular Voice Response System with Dynamic Audio Assembly and Fallback AI Generation"** patent (pending). Key innovations:

- **Memory-cached PCM audio library** with instant AI selection
- **Hybrid audio system** with intelligent fallback to TTS
- **Session memory management** to prevent repetitive responses  
- **Ultra-low latency architecture** with direct audio streaming
- **Format-agnostic compatibility** with automatic conversion

## 🤝 Contributing

### **Hiring Checklist for New Team Members**

**Technical Roles:**
1. **Python/Flask Experience** - WebSocket, API integration, audio processing
2. **Telephony Knowledge** - Understanding of PCM, audio formats, streaming
3. **AI/ML Familiarity** - LLM integration, prompt engineering, model selection
4. **Audio Processing** - librosa, numpy, format conversion experience

**Non-Technical Roles:**
1. **Excel Proficiency** - Comfortable with spreadsheets and data entry
2. **Audio Production** - Recording quality, transcript accuracy
3. **Testing Mindset** - Systematic verification of changes
4. **Documentation Skills** - Clear communication of processes

## 📞 Support & Escalation

### **Self-Service Resources**
- **Debug Endpoints**: `/debug/system_health`, `/exotel/debug`
- **Log Files**: `logs/call_logs.csv`, `logs/conversation_logs.csv`
- **Test Interface**: `/test` (browser-based testing)

### **Escalation Path**
1. **Level 1**: Check logs and debug endpoints
2. **Level 2**: Run diagnostic commands from troubleshooting section
3. **Level 3**: Check API quotas and service status
4. **Level 4**: Contact technical lead with specific error messages

---

**Built with ❤️ by the Klariqo Team**

*Revolutionizing voice AI with patent-pending μ-law streaming technology for AU/NZ markets*