#!/usr/bin/env python3
"""
PETE'S PLUMBING INBOUND CALL ROUTES
Handles incoming calls from customers inquiring about plumbing services
"""

import os
import sys
import random

# Fix import path for parent directory modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream, Dial

from session import session_manager
from logger import call_logger
from audio_manager import audio_manager
from config import Config

# Create blueprint for inbound routes
inbound_bp = Blueprint('inbound', __name__)

@inbound_bp.route("/twilio/voice", methods=['POST'])
def handle_incoming_call():
    """Handle INBOUND calls from prospects"""
    
    # Extract call information
    caller = request.form.get('From', 'Unknown')
    call_sid = request.form.get('CallSid', 'unknown')
    
    print(f"📞 INBOUND call from customer: {caller}")
    
    # Log call start
    call_logger.log_call_start(call_sid, caller, "inbound")
    
    # Build TwiML response
    response = VoiceResponse()
    
    # Check if call forwarding is enabled
    if Config.CALL_FORWARDING["enabled"]:
        print(f"🔄 CALL FORWARDING ENABLED - Forwarding to: {Config.CALL_FORWARDING['forward_to_number']}")
        
        # Play forwarding message if specified
        if Config.CALL_FORWARDING["forward_message"]:
            response.say(Config.CALL_FORWARDING["forward_message"])
        
        # Forward the call to the specified number
        dial = Dial(
            timeout=Config.CALL_FORWARDING["timeout"],
            caller_id=Config.TWILIO_PHONE
        )
        dial.number(Config.CALL_FORWARDING["forward_to_number"])
        response.append(dial)
        
        # Log forwarding action
        call_logger.log_call_end(call_sid, "forwarded")
        
    else:
        print(f"🤖 AI ASSISTANT MODE - Processing with Jason")
        
        # Create INBOUND session for customer inquiry
        session = session_manager.create_session(call_sid, call_direction="inbound")
        
        # Use plumbing intro for customer calls
        selected_intro = "plumbing_intro.mp3"
        
        # Mark intro as played in session memory
        session.session_memory["intro_played"] = True
        
        # Store selected intro for WebSocket streaming
        session.selected_intro = selected_intro
        
        # Connect directly to WebSocket for bidirectional streaming
        # Intro will be sent via WebSocket stream
        connect = Connect()
        stream = Stream(url=f'wss://{request.host}/media/{call_sid}')
        connect.append(stream)
        response.append(connect)
    
    return str(response)

@inbound_bp.route("/twilio/continue/<call_sid>", methods=['POST'])
def continue_inbound_conversation(call_sid):
    """Continue inbound conversation after processing user input"""
    
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
        session.add_to_history("Parent", transcript)
        session.add_to_history("Nisha", content)
        
        # Build TwiML response
        twiml_response = VoiceResponse()
        
        if response_type == "AUDIO":
            # Handle audio file response
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
            print(f"🔄 EXECUTING AGENT TRANSFER for call {call_sid}")
            
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
            
            # Log transfer
            call_logger.log_call_end(call_sid, "transferred_to_agent")
            session_manager.remove_session(call_sid)
            
            return str(twiml_response)
        
        # Check if conversation should end
        if any(word in content.lower() for word in ["goodbye", "goodbye1.mp3"]):
            twiml_response.hangup()
            
            # Clean up session
            call_logger.log_call_end(call_sid, "completed")
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
        print(f"❌ Error in inbound continue: {e}")
        
        # Log error and cleanup
        call_logger.log_call_end(call_sid, "error")
        session_manager.remove_session(call_sid)
        
        response = VoiceResponse()
        response.say("I'm having technical difficulties.")
        response.hangup()
        return str(response)