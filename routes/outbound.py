#!/usr/bin/env python3
"""
PETE'S PLUMBING OUTBOUND CALL ROUTES  
Handles outbound calls to potential customers for plumbing services
"""

import os
import sys
import threading
import time

# Fix import path for parent directory modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream, Dial
from twilio.rest import Client

from config import Config
from session import session_manager
from logger import call_logger

# Create blueprint for outbound routes
outbound_bp = Blueprint('outbound', __name__)

# Initialize Twilio client
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

@outbound_bp.route("/twilio/outbound/<lead_id>", methods=['GET', 'POST'])
def handle_outbound_call(lead_id):
    """Handle OUTBOUND calls to potential customers"""
    
    # Extract call information (handle both GET and POST)
    call_sid = request.form.get('CallSid') or request.args.get('CallSid', 'unknown')
    to_number = request.form.get('To') or request.args.get('To', 'Unknown')
    from_number = request.form.get('From') or request.args.get('From', 'Unknown')
    
    print(f"🔍 DEBUG: Method={request.method}")
    print(f"🔍 DEBUG: CallSid={call_sid}")
    print(f"🔍 DEBUG: To={to_number}, From={from_number}")
    
    # Get customer data from session manager's tracked outbound calls
    lead_data = session_manager.active_outbound_calls.get(call_sid, {})
    
    # If no lead data found, create default customer data
    if not lead_data:
        customer_data = {
            'id': lead_id, 
            'customer_name': 'Customer', 
            'type': 'lead',
            'phone': to_number,
            'call_purpose': 'service_inquiry'
        }
    else:
        # Use the actual customer data from CSV
        customer_data = {
            'id': lead_data.get('id', lead_id),
            'customer_name': lead_data.get('customer_name', 'Customer'),
            'type': lead_data.get('type', 'lead'),
            'phone': to_number,
            'address': lead_data.get('address', ''),
            'service_needed': lead_data.get('service_needed', ''),
            'notes': lead_data.get('notes', ''),
            'call_purpose': 'service_inquiry'
        }
    
    print(f"📞 OUTBOUND call to customer: {customer_data['customer_name']}")
    
    # Log call start
    call_logger.log_call_start(call_sid, customer_data['phone'], "outbound", customer_data)
    
    # Create OUTBOUND session
    session = session_manager.create_session(
        call_sid, 
        call_direction="outbound", 
        lead_data=customer_data
    )
    
    # Set the customer name in session variables for GPT to use
    if customer_data.get('customer_name') and customer_data['customer_name'] != 'Customer':
        session.update_session_variable("customer_name", customer_data['customer_name'])
        print(f"👤 Customer name set in session: {customer_data['customer_name']}")
    
    # Build TwiML response
    response = VoiceResponse()
    
    # Use plumbing intro for outbound calls
    selected_intro = "plumbing_intro.mp3"
    session.session_memory["intro_played"] = True
    
    # Store selected intro for WebSocket streaming
    session.selected_intro = selected_intro
    
    # Connect directly to WebSocket for bidirectional streaming  
    # Intro will be sent via WebSocket stream
    connect = Connect()
    stream = Stream(url=f'wss://{request.host}/media/{call_sid}')
    connect.append(stream)
    response.append(connect)
    
    print(f"📞 TwiML Response: {str(response)}")
    return str(response)

@outbound_bp.route("/twilio/continue/<call_sid>", methods=['POST'])
def continue_outbound_conversation(call_sid):
    """Continue outbound conversation after processing user input"""
    
    try:
        session = session_manager.get_session(call_sid)
        if not session or not hasattr(session, 'ready_for_twiml'):
            print(f"❌ No session or not ready: {call_sid}")
            response = VoiceResponse()
            response.say("Processing error")
            response.hangup()
            return str(response)
        
        # Get prepared response
        response_type = session.next_response_type
        content = session.next_response_content
        transcript = session.next_transcript
        
        # Add to conversation history
        session.add_to_history("Customer", transcript)
        session.add_to_history("Jason", content)
        
        # Build TwiML response
        twiml_response = VoiceResponse()
        
        if response_type == "AUDIO":
            # Handle audio file response
            from audio_manager import audio_manager
            
            audio_files = [f.strip() for f in content.split('+')]
            
            # Validate all files exist
            if audio_manager.validate_audio_chain(content):
                for audio_file in audio_files:
                    audio_url = f"{request.url_root}audio_ulaw/{audio_file}"
                    twiml_response.play(audio_url)
                
                # Log audio response
                call_logger.log_nisha_audio_response(call_sid, content)
            else:
                # Fallback if files don't exist
                twiml_response.say("I'm having trouble with my audio files.")
                call_logger.log_nisha_tts_response(call_sid, "Audio file error - fallback")
        
        elif response_type == "TTS":
            # Handle TTS response
            from tts_engine import tts_engine
            
            tts_url = tts_engine.generate_audio_url(content, request.url_root)
            if tts_url:
                twiml_response.play(tts_url)
                call_logger.log_nisha_tts_response(call_sid, content)
            else:
                twiml_response.say("Sorry, I'm having trouble generating audio.")
                call_logger.log_nisha_tts_response(call_sid, "TTS generation failed")
        
        # Check for agent transfer request
        transfer_requested = session.get_session_variable("transfer_requested")
        if transfer_requested == "yes":
            print(f"🔄 EXECUTING AGENT TRANSFER for outbound call {call_sid}")
            
            # Play transfer message
            if Config.AGENT_TRANSFER["transfer_message"]:
                twiml_response.say(Config.AGENT_TRANSFER["transfer_message"])
            
            # Transfer the call
            dial = Dial(
                timeout=Config.AGENT_TRANSFER["transfer_timeout"],
                caller_id=Config.TWILIO_PHONE
            )
            dial.number(Config.AGENT_TRANSFER["agent_number"])
            twiml_response.append(dial)
            
            # Log transfer with session variables
            call_logger.log_call_end(call_sid, "transferred_to_agent", session.session_variables)
            session_manager.remove_session(call_sid)
            
            return str(twiml_response)
        
        # Check if conversation should end
        if any(word in content.lower() for word in ["goodbye", "goodbye1.mp3"]):
            twiml_response.hangup()
            
            # Clean up session with session variables
            call_logger.log_call_end(call_sid, "completed", session.session_variables)
            session_manager.remove_session(call_sid)
            
        else:
            # Reset session for next input
            session.reset_for_next_input()
            
            # Continue streaming
            connect = Connect()
            stream = Stream(url=f'wss://{request.host}/media/{call_sid}')
            connect.append(stream)
            twiml_response.append(connect)
        
        return str(twiml_response)
        
    except Exception as e:
        print(f"❌ Error in outbound continue: {e}")
        
        # Log error and cleanup
        call_logger.log_call_end(call_sid, "error")
        session_manager.remove_session(call_sid)
        
        response = VoiceResponse()
        response.say("I'm having technical difficulties.")
        response.hangup()
        return str(response)

def make_outbound_call(target_number, lead_data, base_url):
    """Make an outbound call to a customer/prospect"""
    try:
        # Ensure phone number has + prefix
        if not target_number.startswith('+'):
            target_number = '+' + target_number
            
        print(f"📞 Calling {lead_data.get('customer_name')} at {target_number}")
        
        call = twilio_client.calls.create(
            to=target_number,
            from_=Config.TWILIO_PHONE,
            url=f"{base_url}/outbound/twilio/outbound/{lead_data['id']}",
            method='POST'
        )
        
        # Track call info
        session_manager.track_outbound_call(call.sid, lead_data)
        
        print(f"✅ Outbound call initiated: {call.sid}")
        print(f"📋 Webhook URL: {base_url}/outbound/twilio/outbound/{lead_data['id']}")
        return call.sid
        
    except Exception as e:
        print(f"❌ Failed to make outbound call: {e}")
        return None

def start_plumbing_calling_campaign(target_list, max_calls=50, base_url=""):
    """Start mass outbound calling campaign to potential customers"""
    
    call_count = 0
    successful_calls = 0
    
    for customer in target_list:
        if call_count >= max_calls:
            break
            
        # Check if already called today (in real implementation)
        if not customer.get('called_today', False):
            call_sid = make_outbound_call(customer['phone'], customer, base_url)
            
            if call_sid:
                successful_calls += 1
                # Wait between calls (be respectful!)
                time.sleep(Config.CALL_INTERVAL)
                
            call_count += 1
                
        if call_count >= max_calls:
            break
    
    print(f"🚀 Plumbing campaign complete: {successful_calls}/{call_count} calls successful")
    return successful_calls

@outbound_bp.route("/start_campaign", methods=['POST'])
def start_campaign():
    """API endpoint to start plumbing calling campaign"""
    try:
        # Sample customer data (in real implementation, load from database/CSV)
        sample_customers = [
            {
                'id': '1', 
                'customer_name': 'John Smith', 
                'phone': '+61412345678', 
                'type': 'lead',
                'address': '123 Main St, Melbourne',
                'service_needed': 'drain_cleaning'
            },
            {
                'id': '2', 
                'customer_name': 'Sarah Johnson', 
                'phone': '+61487654321', 
                'type': 'lead',
                'address': '456 Oak Ave, Melbourne',
                'service_needed': 'hot_water_repair'
            },
            # Add more customers from your database...
        ]
        
        # Get base URL for callbacks
        base_url = request.url_root.rstrip('/')
        
        # Start campaign in background thread
        campaign_thread = threading.Thread(
            target=start_plumbing_calling_campaign, 
            args=(sample_customers, 10, base_url)  # Start with 10 calls
        )
        campaign_thread.daemon = True
        campaign_thread.start()
        
        return {
            "status": "success", 
            "message": "Plumbing campaign started",
            "max_calls": 10
        }
        
    except Exception as e:
        print(f"❌ Campaign start error: {e}")
        return {
            "status": "error", 
            "message": str(e)
        }

@outbound_bp.route("/campaign_status", methods=['GET'])
def get_campaign_status():
    """Get current campaign status"""
    active_count = session_manager.get_active_count()
    
    # Get recent call stats
    stats = call_logger.get_call_stats(days=1)
    
    return {
        "active_calls": active_count,
        "today_stats": stats,
        "message": f"Currently {active_count} active calls"
    }

def load_customers_from_csv(csv_file_path):
    """Load customer data from CSV file for outbound campaigns"""
    import csv
    
    customers = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ensure required fields exist
                if 'phone' in row and row['phone'].strip():
                    customer = {
                        'id': row.get('id', str(len(customers) + 1)),
                        'customer_name': row.get('customer_name', 'Customer'),
                        'phone': row['phone'].strip(),
                        'type': row.get('type', 'lead'),
                        'address': row.get('address', ''),
                        'service_needed': row.get('service_needed', ''),
                        'notes': row.get('notes', ''),
                        'called_today': False
                    }
                    customers.append(customer)
        
        print(f"📋 Loaded {len(customers)} customers from CSV: {csv_file_path}")
        return customers
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return []

@outbound_bp.route("/start_csv_campaign", methods=['POST'])
def start_csv_campaign():
    """Start campaign using customer data from CSV file"""
    try:
        # CSV file path (you can make this configurable)
        csv_file = "customer_data/leads.csv"
        
        if not os.path.exists(csv_file):
            return {
                "status": "error",
                "message": f"CSV file not found: {csv_file}"
            }
        
        # Load customers from CSV
        customers = load_customers_from_csv(csv_file)
        
        if not customers:
            return {
                "status": "error",
                "message": "No valid customers found in CSV"
            }
        
        # Get base URL for callbacks
        base_url = request.url_root.rstrip('/')
        
        # Get max calls from request (default 10)
        max_calls = request.json.get('max_calls', 10) if request.json else 10
        
        # Start campaign in background thread
        campaign_thread = threading.Thread(
            target=start_plumbing_calling_campaign, 
            args=(customers, max_calls, base_url)
        )
        campaign_thread.daemon = True
        campaign_thread.start()
        
        return {
            "status": "success", 
            "message": f"CSV campaign started with {len(customers)} customers",
            "total_customers": len(customers),
            "max_calls": max_calls
        }
        
    except Exception as e:
        print(f"❌ CSV campaign start error: {e}")
        return {
            "status": "error", 
            "message": str(e)
        }