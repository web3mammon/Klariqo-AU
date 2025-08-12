#!/usr/bin/env python3
"""
KLARIQO RESPONSE ROUTER MODULE  
Clean GPT-based response selection with reliable TTS handling
"""

from openai import OpenAI
from config import Config
from audio_manager import audio_manager

# Initialize OpenAI client
openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

class ResponseRouter:
    """Handles AI-powered response selection with reliable GPT processing"""
    
    def __init__(self):
        self.base_prompt = self._build_base_prompt()
        print("🤖 Response Router initialized: GPT-only mode (reliable & fast)")
    
    def _extract_session_variables(self, user_input, session):
        """Extract and update session variables from user input for plumbing business"""
        user_lower = user_input.lower()
        
        # Extract service type
        service_mappings = {
            "blocked drain": "blocked_drain", "drain blocked": "blocked_drain", "clogged drain": "blocked_drain",
            "leaking tap": "leaking_tap", "tap leak": "leaking_tap", "dripping tap": "leaking_tap", "faucet leak": "leaking_tap",
            "toilet": "toilet_repair", "loo": "toilet_repair", "dunny": "toilet_repair",
            "hot water": "hot_water_issues", "water heater": "hot_water_issues", "no hot water": "hot_water_issues", "cold water": "hot_water_issues",
            "emergency": "emergency", "urgent": "emergency", "flooding": "emergency", "burst pipe": "emergency",
            "gas": "gas_fitting", "gas fitting": "gas_fitting", "gas leak": "emergency",
            "shower": "bath_kitchen_plumbing", "bath": "bath_kitchen_plumbing", "bathroom": "bath_kitchen_plumbing",
            "kitchen": "bath_kitchen_plumbing", "sink": "bath_kitchen_plumbing", "dishwasher": "bath_kitchen_plumbing",
            "pipe relining": "pipe_relining", "relining": "pipe_relining", "pipe lining": "pipe_relining",
            "general problem": "general_problems", "plumbing issue": "general_problems", "problem": "general_problems"
        }
        
        for keyword, service_type in service_mappings.items():
            if keyword in user_lower:
                session.update_session_variable("service_type", service_type)
                break
        
        # Extract urgency level
        if any(word in user_lower for word in ["emergency", "urgent", "asap", "flooding", "burst", "now", "immediately", "straight away"]):
            session.update_session_variable("urgency_level", "emergency")
        elif any(word in user_lower for word in ["soon", "today", "this week", "quickly", "fast"]):
            session.update_session_variable("urgency_level", "urgent")
        elif any(word in user_lower for word in ["whenever", "flexible", "no rush", "no hurry", "take your time"]):
            session.update_session_variable("urgency_level", "flexible")
        else:
            session.update_session_variable("urgency_level", "routine")
        
        # Extract property type
        if any(word in user_lower for word in ["unit", "apartment", "flat"]):
            session.update_session_variable("property_type", "unit")
        elif any(word in user_lower for word in ["house", "home"]):
            session.update_session_variable("property_type", "house")
        elif any(word in user_lower for word in ["business", "office", "shop", "commercial"]):
            session.update_session_variable("property_type", "commercial")
        else:
            session.update_session_variable("property_type", "residential")
        
        # Extract location/suburb with improved logic
        location_indicators = ["in", "at", "from", "located", "address", "suburb", "area"]
        words = user_input.split()
        for i, word in enumerate(words):
            if any(indicator in word.lower() for indicator in location_indicators):
                if i < len(words) - 1:
                    potential_location = words[i + 1]
                    # Common Australian suburbs/areas - check for longer location names
                    if len(potential_location) > 2:  # Allow shorter suburb names
                        # Try to get multi-word locations
                        location_parts = []
                        for j in range(i + 1, min(i + 4, len(words))):  # Check next 3 words
                            if words[j].lower() not in ["and", "the", "a", "an", "to", "for", "with"]:
                                location_parts.append(words[j])
                        if location_parts:
                            full_location = " ".join(location_parts).title()
                            session.update_session_variable("customer_location", full_location)
                break
        
        # Extract customer name with improved patterns
        import re
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"this is (\w+)",
            r"(\w+) speaking",
            r"call me (\w+)",
            r"i am (\w+)",
            r"name's (\w+)"
        ]
        for pattern in name_patterns:
            name_match = re.search(pattern, user_lower)
            if name_match:
                name = name_match.group(1).title()
                session.update_session_variable("customer_name", name)
                break
        
        # Extract phone number with improved patterns
        phone_patterns = [
            r'(\d{4}\s?\d{3}\s?\d{3})',  # 0412 345 678
            r'(\d{10})',  # 0412345678
            r'(\d{2}\s?\d{4}\s?\d{4})',  # 04 1234 5678
            r'\+61\s?(\d{1}\s?\d{4}\s?\d{4})'  # +61 4 1234 5678
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, user_input)
            if phone_match:
                phone = phone_match.group(1).replace(" ", "")
                session.update_session_variable("customer_phone", phone)
                break
        
        # Extract time preferences
        if any(word in user_lower for word in ["morning", "am", "early", "9", "10", "11"]):
            session.update_session_variable("preferred_time", "morning")
        elif any(word in user_lower for word in ["afternoon", "pm", "lunch", "12", "1", "2", "3"]):
            session.update_session_variable("preferred_time", "afternoon")
        elif any(word in user_lower for word in ["evening", "after work", "late", "4", "5", "6", "7", "8"]):
            session.update_session_variable("preferred_time", "evening")
        
        # Extract date preferences with current date context in client's timezone
        from datetime import datetime, timedelta
        import pytz
        
        # Use client's specific timezone from config
        client_timezone = Config.get_australian_timezone(Config.CLIENT_CONFIG["city"])
        australia_tz = pytz.timezone(client_timezone)
        current_date = datetime.now(australia_tz)
        tomorrow = current_date + timedelta(days=1)
        
        if any(word in user_lower for word in ["today", "now", "asap", "straight away"]):
            session.update_session_variable("preferred_date", "today")
        elif any(word in user_lower for word in ["tomorrow"]):
            session.update_session_variable("preferred_date", "tomorrow")
        elif any(word in user_lower for word in ["this week", "week", "sometime this week"]):
            session.update_session_variable("preferred_date", "this_week")
        elif any(word in user_lower for word in ["next week"]):
            session.update_session_variable("preferred_date", "next_week")
        
        # Extract issue description - capture the main problem description
        issue_keywords = ["problem", "issue", "broken", "not working", "leaking", "blocked", "clogged", "burst", "flooding"]
        if any(keyword in user_lower for keyword in issue_keywords):
            # Try to extract a meaningful description
            words = user_input.split()
            issue_start = -1
            for i, word in enumerate(words):
                if any(keyword in word.lower() for keyword in issue_keywords):
                    issue_start = i
                    break
            
            if issue_start != -1:
                # Get the issue description (next 5-10 words)
                issue_words = words[issue_start:issue_start + 8]
                issue_description = " ".join(issue_words)
                if len(issue_description) > 10:  # Only store if meaningful
                    session.update_session_variable("issue_description", issue_description)
        
        # Track if this is a repeat customer
        if any(word in user_lower for word in ["before", "last time", "previous", "again", "repeat"]):
            session.update_session_variable("previous_customer", "yes")
        elif any(word in user_lower for word in ["first time", "new customer", "never used"]):
            session.update_session_variable("previous_customer", "no")
    
    def _handle_appointment_booking(self, user_input, session):
        """Handle appointment booking requests with available slots"""
        user_lower = user_input.lower()
        
        # Check if this is a booking request
        booking_keywords = ["book", "appointment", "schedule", "visit", "come out", "arrange", "slot", "time"]
        is_booking_request = any(keyword in user_lower for keyword in booking_keywords)
        
        if not is_booking_request:
            return None, None
        
        # Get available slots from config
        from config import Config
        available_slots = Config.PLUMBING_AVAILABILITY["available_slots"]
        
        # Get current date context for relative dates in client's timezone
        from datetime import datetime, timedelta
        import pytz
        
        # Use client's specific timezone from config
        client_timezone = Config.get_australian_timezone(Config.CLIENT_CONFIG["city"])
        australia_tz = pytz.timezone(client_timezone)
        current_date = datetime.now(australia_tz)
        today_str = current_date.strftime("%A, %B %d")
        tomorrow_str = (current_date + timedelta(days=1)).strftime("%A, %B %d")
        
        # Check if customer already has a preferred date/time
        preferred_date = session.get_session_variable("preferred_date")
        preferred_time = session.get_session_variable("preferred_time")
        service_type = session.get_session_variable("service_type") or "plumbing service"
        urgency_level = session.get_session_variable("urgency_level")
        customer_name = session.get_session_variable("customer_name")
        
        # Handle emergency bookings
        if urgency_level == "emergency":
            return "TTS", "That sounds urgent! I can have someone out to you within the hour. What's your address and what's the specific problem?"
        
        # If customer is confirming a specific time slot
        confirmation_words = ["yes", "sounds good", "perfect", "that works", "confirm", "book that"]
        if any(word in user_lower for word in confirmation_words):
            if customer_name:
                return "TTS", f"Excellent {customer_name}! You're all booked. I'll give you a call 30 minutes before we arrive. Thanks for choosing {Config.CLIENT_CONFIG['business_name']}!"
            else:
                return "TTS", "Perfect! Can I grab your name and phone number to confirm the booking?"
        
        # Filter available slots based on preferences
        suitable_slots = []
        
        # If they specified a date preference
        if preferred_date == "today":
            suitable_slots = [slot for slot in available_slots if today_str.lower() in slot["date"].lower()]
        elif preferred_date == "tomorrow":
            suitable_slots = [slot for slot in available_slots if tomorrow_str.lower() in slot["date"].lower()]
        else:
            # Show next few available slots
            suitable_slots = available_slots[:6]  # First 6 available slots
        
        # If they specified time preference, filter further
        if preferred_time == "morning":
            suitable_slots = [slot for slot in suitable_slots if "8:00 AM" in slot["time"] or "10:30 AM" in slot["time"]]
        elif preferred_time == "afternoon":
            suitable_slots = [slot for slot in suitable_slots if "1:00 PM" in slot["time"] or "3:30 PM" in slot["time"]]
        
        # Generate response with available slots
        if suitable_slots:
            if len(suitable_slots) == 1:
                slot = suitable_slots[0]
                response = f"I can fit you in for {service_type} on {slot['date']} from {slot['time']}. Does that work for you?"
            elif len(suitable_slots) == 2:
                slot1, slot2 = suitable_slots[:2]
                response = f"I have availability for {service_type} on {slot1['date']} from {slot1['time']} or {slot2['date']} from {slot2['time']}. Which time works better for you?"
            else:
                slot1, slot2, slot3 = suitable_slots[:3]
                response = f"I can fit you in for {service_type} on {slot1['date']} from {slot1['time']}, {slot2['date']} from {slot2['time']}, or {slot3['date']} from {slot3['time']}. What works best for you?"
            
            return "TTS", response
        else:
            return "TTS", "Let me check my schedule. I have several openings this week. Would morning or afternoon work better for you?"
    
    def _handle_agent_transfer(self, user_input, session):
        """Handle agent transfer requests"""
        from config import Config
        
        # Check if agent transfer is enabled
        if not Config.AGENT_TRANSFER["enabled"]:
            return None, None
        
        user_lower = user_input.lower()
        
        # Check for transfer keywords
        transfer_keywords = Config.AGENT_TRANSFER["transfer_keywords"]
        auto_transfer_conditions = Config.AGENT_TRANSFER["auto_transfer_conditions"]
        
        # Check if user wants to speak to agent
        wants_agent = any(keyword in user_lower for keyword in transfer_keywords)
        
        # Check for automatic transfer conditions
        auto_transfer = any(condition in user_lower for condition in auto_transfer_conditions)
        
        if wants_agent or auto_transfer:
            # Mark session for transfer
            session.update_session_variable("transfer_requested", "yes")
            session.update_session_variable("transfer_reason", "customer_request" if wants_agent else "auto_transfer")
            
            # Get customer context for transfer
            customer_name = session.get_session_variable("customer_name")
            service_type = session.get_session_variable("service_type")
            urgency_level = session.get_session_variable("urgency_level")
            
            # Log transfer request
            print(f"🔄 AGENT TRANSFER REQUESTED: {user_input}")
            print(f"   Customer: {customer_name}")
            print(f"   Service: {service_type}")
            print(f"   Urgency: {urgency_level}")
            
            # Return transfer response
            if customer_name:
                return "TTS", f"Of course {customer_name}! I'll transfer you to our team now. Please hold while I connect you."
            else:
                return "TTS", "I'll transfer you to our team now. Please hold while I connect you."
        
        return None, None
    
    def _build_base_prompt(self):
        """Build the base prompt for GPT response selection"""
        
        # Get available files for dynamic selection
        available_files = self._get_available_files_by_category()
        
        # Get current date/time context for booking
        from datetime import datetime
        current_date = datetime.now()
        current_date_str = current_date.strftime("%A, %B %d, %Y")
        current_time_str = current_date.strftime("%I:%M %p")
        
        prompt = f"""You are {Config.CLIENT_CONFIG['ai_assistant_name']} from {Config.CLIENT_CONFIG['business_name']} — a friendly, professional voice assistant helping customers with {Config.CLIENT_CONFIG['industry']} services in {Config.CLIENT_CONFIG['location']}.
        Your job is to respond to customer queries with the right audio file snippet(s) from our library OR generate appropriate booking responses.

🚨 CRITICAL RULES:
Always reply using only the correct filenames (e.g., plumbing_intro.mp3 + services_offered.mp3) OR use GENERATE for dynamic responses

Never repeat a file that was recently played during this session

If you're unsure what to play, use exactly this format:
GENERATE: Could you tell me a bit more about the plumbing issue you're having?

For appointment booking requests, ALWAYS use GENERATE: followed by your response

IMPORTANT: When using GENERATE, always include the colon (:) after GENERATE

🎙️ Tone & Format Instructions:
Speak in Australian English with a friendly, professional tradesman tone

Keep the tone natural, helpful, and reassuring — like an experienced plumber speaking to a customer

Avoid all special characters, formatting, or symbols, including:

🚫 No colons (:), dashes (–), slashes (/), arrows (>)
🚫 No numbered lists (1., 2.)
🚫 No hashtags, emojis, or technical jargon

Use Australian terms: "G'day", "mate", "no worries", "fair dinkum"

Prioritize helping the customer feel confident about the service

📅 CURRENT DATE/TIME CONTEXT:
Today is: {current_date_str}
Current time: {current_time_str}
Month: August 2024

📋 DYNAMIC SESSION VARIABLES YOU TRACK:
Variable	Purpose	Example Values
service_type	Type of plumbing service	"blocked_drain", "leaking_tap", "toilet_repair", "hot_water", "emergency"
urgency_level	How urgent the job is	"emergency", "urgent", "routine", "flexible" 
property_type	Type of property	"house", "unit", "commercial", "residential"
customer_location	Suburb/area	Melbourne suburbs, Sydney areas, etc.
customer_name	Customer's name	First name extracted from conversation
customer_phone	Contact number	Phone number for booking
preferred_date	When they want service	"today", "tomorrow", "this_week", specific date
preferred_time	Time preference	"morning", "afternoon", "evening"
selected_appointment	Booked slot	Final confirmed appointment time

📋 INTELLIGENT AUDIO SELECTION RULES:
Customer Input	Response Strategy

General inquiry/greeting	plumbing_intro.mp3 OR intro_greeting.mp3

Asks about services	services_offered.mp3

Asks about pricing	pricing.mp3 OR cost_estimate_enquiry.mp3

Asks about experience/reputation	in_business_how_long.mp3

Asks about availability (general)	available_hours.mp3

Asks about timing/scheduling	ask_time_day.mp3 OR when_can_come.mp3

Specific service inquiries:
- Blocked drain	blocked_drain.mp3
- Leaking tap	leaking_tap.mp3
- Toilet repair	toilet_repair.mp3
- Hot water issues	hot_water_issues.mp3
- Gas fitting	gas_fitting.mp3
- Pipe relining	pipe_relining.mp3
- Bath/kitchen plumbing	bath_kitchen_plumbing.mp3
- General problems	general_problems.mp3

After hours calls	after_hours_greeting.mp3

Urgent/emergency situations	urgent_callout.mp3

Booking confirmation	confirmed_bye.mp3

Need to check availability	need_to_check.mp3

APPOINTMENT BOOKING (Use GENERATE:):
Customer asks to book appointment	
→ Check available slots and offer 2-3 options
→ Use current date context for "tomorrow", "today" etc.
→ GENERATE: I can fit you in for [service_type] on [available slots]. Which time works better for you?

Customer confirms time slot	
→ Collect name and phone if not already obtained
→ GENERATE: Perfect! I've got you down for [selected_time]. Can I grab your name and phone number to confirm?

Customer provides contact details	
→ Confirm the booking
→ GENERATE: Excellent [customer_name]! You're all booked for [service] on [date] at [time]. I'll give you a call 30 minutes before we arrive. Is [phone] the best number to reach you on?

Emergency situations	
→ If urgency_level="emergency": Prioritize immediate response
→ GENERATE: That sounds urgent! I can have someone out to you within the hour. What's your address?

📅 AVAILABLE APPOINTMENT SLOTS (August 2024):
Monday Aug 5: 8AM-10AM, 10:30AM-12:30PM, 1PM-3PM
Tuesday Aug 6: 8AM-10AM, 3:30PM-5:30PM  
Wednesday Aug 7: 10:30AM-12:30PM, 1PM-3PM
Thursday Aug 8: 8AM-10AM, 3:30PM-5:30PM
Friday Aug 9: 10:30AM-12:30PM
Monday Aug 12: 8AM-10AM, 1PM-3PM
Tuesday Aug 13: 10:30AM-12:30PM, 3:30PM-5:30PM
Wednesday Aug 14: 8AM-10AM
Friday Aug 16: 1PM-3PM, 3:30PM-5:30PM
(Plus more dates through August)

📋 AVAILABLE AUDIO FILES:
{available_files}

🔧 PLUMBING SERVICE EXAMPLES:
"blocked drain" → blocked_drain.mp3
"leaking tap" → leaking_tap.mp3
"toilet repair" → toilet_repair.mp3
"hot water" → hot_water_issues.mp3
"gas fitting" → gas_fitting.mp3
"pipe relining" → pipe_relining.mp3
"bathroom/kitchen" → bath_kitchen_plumbing.mp3
"emergency" → urgent_callout.mp3

Remember: Always be helpful, professional, and ready to book appointments with available time slots!"""
        
        return prompt
    
    def _get_available_files_by_category(self):
        """Get formatted list of available files by category (excluding intro files)"""
        categories = []
        for category, files in audio_manager.audio_snippets.items():
            if category != "quick_responses" and files:
                # Filter out intro files from the available files list
                filtered_files = {k: v for k, v in files.items() if not k.startswith('intro_klariqo')}
                if filtered_files:
                    file_list = ", ".join(filtered_files.keys())
                    categories.append(f"{category}: {file_list}")
        return "\n".join(categories)
    
    # Remove the _get_alternatives method completely since no more alternate files
    
    def _get_recent_files(self, session, limit=3):
        """Get recently played audio files to avoid repetition"""
        recent_files = []
        
        # Look through recent conversation history for audio responses
        if hasattr(session, 'conversation_history'):
            for entry in session.conversation_history[-6:]:  # Last 6 entries
                if "Nisha:" in entry and "<audio:" in entry:
                    # Extract filenames from "<audio: file1.mp3 + file2.mp3>"
                    import re
                    files = re.findall(r'<audio: ([^>]+)>', entry)
                    if files:
                        audio_chain = files[0]
                        file_list = [f.strip() for f in audio_chain.split('+')]
                        recent_files.extend(file_list)
        
        # Return last N unique files
        seen = set()
        unique_recent = []
        for f in reversed(recent_files):
            if f not in seen and len(unique_recent) < limit:
                unique_recent.append(f)
                seen.add(f)
        
        return unique_recent[:limit]
    
    def _get_recent_conversation(self, session, limit=2):
        """Get recent conversation context"""
        if not hasattr(session, 'conversation_history'):
            return "None"
        
        recent = session.conversation_history[-(limit*2):]  # Last N exchanges
        return " | ".join(recent) if recent else "None"
    
    def _build_context_prompt(self, session, user_input):
        """Build context prompt with dynamic session variables"""
        
        # Get current date and time for context in client's timezone
        from datetime import datetime, timedelta
        import pytz
        
        # Use client's specific timezone from config
        client_timezone = Config.get_australian_timezone(Config.CLIENT_CONFIG["city"])
        australia_tz = pytz.timezone(client_timezone)
        current_datetime = datetime.now(australia_tz)
        current_date = current_datetime.strftime("%A, %B %d, %Y")
        current_time = current_datetime.strftime("%I:%M %p")
        tomorrow_date = (current_datetime + timedelta(days=1)).strftime("%A, %B %d, %Y")
        
        # Extract and update session variables from user input
        self._extract_session_variables(user_input, session)
        
        # Get recent conversation history
        recent_files = self._get_recent_files(session, limit=3)
        recent_conversation = self._get_recent_conversation(session, limit=2)
        
        # Get current session context
        session_context = session.get_session_context()
        
        # Check if customer name is available for personalization
        customer_name = session.get_session_variable("customer_name")
        personalization_note = ""
        if customer_name and customer_name != "Customer":
            personalization_note = f"\n👤 CUSTOMER NAME: {customer_name} - Use their name for personalization when appropriate"
        
        context_prompt = f"""
📅 CURRENT DATE & TIME CONTEXT:
Today is {current_date} at {current_time}
Tomorrow is {tomorrow_date}
When customer says "today" they mean {current_date}
When customer says "tomorrow" they mean {tomorrow_date}

🧠 CONVERSATION MEMORY:
Recently played files (DON'T repeat): {', '.join(recent_files)}
Recent conversation: {recent_conversation}

📋 CURRENT SESSION VARIABLES:
{session_context}{personalization_note}

📝 CURRENT USER INPUT: "{user_input}"

🎯 PLUMBING SERVICE RULES:
- If service_type is known, tailor the response to that specific service
- If urgency_level is "emergency", prioritize immediate response
- If customer asks about booking/appointment, use GENERATE with available time slots
- If customer_name and customer_phone are collected, proceed with booking confirmation
- If customer confirms a time slot, finalize the booking
- If customer_name is available, use it for personalization (e.g., "Thanks {customer_name}")
- ALWAYS extract and store customer details: name, phone, location, issue description
- When customer mentions timing, use the current date context above

🎙️ AUDIO FILE SELECTION GUIDANCE:
- For general greetings: plumbing_intro.mp3 OR intro_greeting.mp3
- For service inquiries: services_offered.mp3
- For pricing questions: pricing.mp3 OR cost_estimate_enquiry.mp3
- For timing/scheduling: ask_time_day.mp3 OR when_can_come.mp3
- For specific services: Use the corresponding service file (blocked_drain.mp3, leaking_tap.mp3, etc.)
- For urgent situations: urgent_callout.mp3
- For after hours: after_hours_greeting.mp3
- For booking confirmations: confirmed_bye.mp3
- For availability checks: need_to_check.mp3

Apply the rules from your system prompt. Choose appropriate files or GENERATE response for dynamic booking."""
        
        return context_prompt
    
    def get_school_response(self, user_input, session):
        """Get appropriate response for plumbing business conversation with booking capability"""
        
        try:
            import time
            start = time.time()
            
            # PRIORITY 1: Check for agent transfer request
            response_type, content = self._handle_agent_transfer(user_input, session)
            if response_type:
                return response_type, content
            
            # PRIORITY 2: Check for appointment booking
            response_type, content = self._handle_appointment_booking(user_input, session)
            if response_type:
                return response_type, content
            
            # PRIORITY 3: Standard GPT response for other queries
            # Build messages with cached system prompt + lightweight context
            messages = [
                {"role": "system", "content": self.base_prompt},
                {"role": "user", "content": self._build_context_prompt(session, user_input)}
            ]
            
            # Call OpenAI GPT-4.1-mini for response
            response = openai_client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.1,  # Very low for consistency
                max_tokens=100,   # Allow longer responses for chaining
                timeout=10        # 10 second timeout
            )
            
            openai_response = response.choices[0].message.content.strip()
            openai_response = openai_response.replace('"', '').replace("'", "")
            
            response_time = int((time.time() - start) * 1000)
            
            # Check if it's a custom generation request (flexible detection)
            if openai_response.startswith("GENERATE:") or openai_response.startswith("GENERATE "):
                # Handle both "GENERATE:" and "GENERATE " formats
                if openai_response.startswith("GENERATE:"):
                    text_to_generate = openai_response.replace("GENERATE:", "").strip()
                else:
                    text_to_generate = openai_response.replace("GENERATE", "", 1).strip()
                
                print(f"🎯 GPT → TTS: {text_to_generate} ({response_time}ms)")
                return "TTS", text_to_generate
            else:
                print(f"🎯 GPT → Audio: {openai_response} ({response_time}ms)")
                return "AUDIO", openai_response
                
        except Exception as e:
            # Fallback to safe response
            print(f"❌ GPT error: {e}")
            return "TTS", "I want to make sure I give you the right information. Could you tell me what specific aspect you'd like to know more about?"
    
    def validate_response(self, response_content):
        """Validate that the response contains valid audio files"""
        if not response_content or response_content.startswith("GENERATE:"):
            return True
        
        # Validate audio chain
        return audio_manager.validate_audio_chain(response_content)

# Global response router instance
response_router = ResponseRouter()