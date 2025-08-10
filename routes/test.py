#!/usr/bin/env python3
"""
KLARIQO TESTING ROUTES
Browser-friendly test endpoints for development and demos
"""

import os
import sys

# Fix import path for parent directory modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request
from routes.outbound import make_outbound_call
from session import session_manager
from logger import call_logger
from audio_manager import audio_manager
from tts_engine import tts_engine

# Create blueprint for test routes
test_bp = Blueprint('test', __name__)

@test_bp.route("/call_test/<phone_number>", methods=['GET'])
def call_test(phone_number):
    """Browser-friendly test endpoint - call any number"""
    try:
        # Add + if not present
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            
        lead_data = {
            'id': 'test_123',
            'customer_name': 'Test Customer Demo',
            'type': 'test'
        }
        
        # Get base URL for callback
        base_url = request.url_root.rstrip('/')
        
        call_sid = make_outbound_call(phone_number, lead_data, base_url)
        
        if call_sid:
            return f"""
            <h2>✅ Test Call Initiated!</h2>
            <p><strong>Call SID:</strong> {call_sid}</p>
            <p><strong>Phone:</strong> {phone_number}</p>
            <p><strong>Customer:</strong> {lead_data['customer_name']}</p>
            <p>Your phone should ring in 5-10 seconds!</p>
            <p><a href="/test">← Back to Test Menu</a></p>
            """
        else:
            return f"""
            <h2>❌ Call Failed</h2>
            <p>Could not initiate call to {phone_number}</p>
            <p><a href="/test">← Back to Test Menu</a></p>
            """
            
    except Exception as e:
        return f"""
        <h2>❌ Error</h2>
        <p>Error: {str(e)}</p>
        <p><a href="/test">← Back to Test Menu</a></p>
        """

@test_bp.route("/test")
def test_page():
    """Main test page with all testing options"""
    return """
    <h1>🧪 Klariqo Testing Dashboard</h1>
    
    <h3>📞 Test Outbound Calls:</h3>
    <p>Test the outbound calling system:</p>
    <ul>
        <li><a href="/call_test/61412345678">Call +61-412-345-678 (Update with your number)</a></li>
        <li><a href="/call_test/61487654321">Call +61-487-654-321</a></li>
    </ul>
    
    <h3>🎯 Campaign Management:</h3>
    <ul>
        <li><a href="/outbound/start_campaign" onclick="return confirm('Start campaign?')">Start Plumbing Campaign (POST)</a></li>
        <li><a href="/outbound/start_csv_campaign" onclick="return confirm('Start CSV campaign?')">Start CSV Campaign (POST)</a></li>
        <li><a href="/outbound/campaign_status">View Campaign Status</a></li>
    </ul>
    
    <h3>📋 System Information:</h3>
    <ul>
        <li><a href="/debug/audio_files">View Audio Files</a></li>
        <li><a href="/debug/call_logs">Download Call Logs</a></li>
        <li><a href="/debug/system_health">System Health Check</a></li>
    </ul>
    
    <br>
    <p><strong>Instructions:</strong></p>
    <ol>
        <li>Click a test link above (update phone number first)</li>
        <li>Your phone should ring in 5-10 seconds</li>
        <li>Answer the call and pretend to be a customer asking about plumbing</li>
        <li>Jason will handle your inquiry with personalized responses!</li>
        <li>Ask about services, pricing, booking, etc!</li>
    </ol>
    
    <p><strong>👤 Customer Name Personalization:</strong></p>
    <ul>
        <li>When using CSV campaigns, Jason will know the customer's name</li>
        <li>He'll use it for personalization (e.g., "Thanks John!")</li>
        <li>Check the CSV file in <code>customer_data/leads.csv</code></li>
    </ul>
    
    <p><strong>🔧 Experience professional plumbing service - with personalization!</strong></p>
    
    <hr>
    <p><small>Klariqo v3.0 - Twilio μ-law Streaming | Patent Pending</small></p>
    """

@test_bp.route("/debug/audio_files")
def debug_audio_files():
    """Debug page showing all audio files"""
    audio_files = audio_manager.list_all_files()
    
    html = "<h2>🎵 Audio Files Status</h2>\n<table border='1' style='border-collapse: collapse;'>\n"
    html += "<tr><th>Filename</th><th>Category</th><th>Transcript</th><th>Status</th></tr>\n"
    
    for file_info in audio_files:
        status = "✅ Available" if file_info['exists'] else "❌ Missing"
        status_color = "green" if file_info['exists'] else "red"
        
        html += f"""<tr>
            <td>{file_info['filename']}</td>
            <td>{file_info['category']}</td>
            <td style='max-width: 300px;'>{file_info['transcript']}</td>
            <td style='color: {status_color};'>{status}</td>
        </tr>\n"""
    
    html += "</table>\n"
    html += f"<p><a href='/test'>← Back to Test Page</a></p>"
    
    return html

@test_bp.route("/debug/call_logs")
def debug_call_logs():
    """Download recent call logs"""
    stats = call_logger.get_call_stats(days=7)
    
    html = f"""
    <h2>📋 Call Logs Summary (Last 7 Days)</h2>
    <ul>
        <li><strong>Total Calls:</strong> {stats['total_calls']}</li>
        <li><strong>Inbound:</strong> {stats['inbound_calls']}</li>
        <li><strong>Outbound:</strong> {stats['outbound_calls']}</li>
        <li><strong>Avg Duration:</strong> {stats['avg_duration']}s</li>
        <li><strong>Audio Files Used:</strong> {stats['total_audio_files_used']}</li>
        <li><strong>TTS Responses:</strong> {stats['total_tts_responses']}</li>
    </ul>
    
    <h3>📁 Log Files:</h3>
    <ul>
        <li><a href="/logs/call_logs.csv">call_logs.csv</a></li>
        <li><a href="/logs/conversation_logs.csv">conversation_logs.csv</a></li>
    </ul>
    
    <p><a href="/test">← Back to Test Page</a></p>
    """
    
    return html

@test_bp.route("/debug/system_health")
def debug_system_health():
    """System health check"""
    
    # Test all components
    health_checks = {
        "Audio Manager": "✅ OK" if len(audio_manager.cached_files) > 0 else "❌ No audio files",
        "TTS Engine": "✅ OK" if tts_engine.test_voice() else "❌ Failed",
        "Session Manager": f"✅ OK ({session_manager.get_active_count()} active)",
        "Call Logger": "✅ OK",  # Always OK if we got here
    }
    
    # Check API keys
    from config import Config
    api_checks = {
        "Deepgram API": "✅ Set" if Config.DEEPGRAM_API_KEY else "❌ Missing",
        "Groq API": "✅ Set" if Config.GROQ_API_KEY else "❌ Missing", 
        "ElevenLabs API": "✅ Set" if Config.ELEVENLABS_API_KEY else "❌ Missing",
        "Twilio Account": "✅ Set" if Config.TWILIO_ACCOUNT_SID else "❌ Missing",
    }
    
    html = "<h2>🏥 System Health Check</h2>\n"
    
    html += "<h3>📡 Components:</h3>\n<ul>\n"
    for component, status in health_checks.items():
        html += f"<li><strong>{component}:</strong> {status}</li>\n"
    html += "</ul>\n"
    
    html += "<h3>🔑 API Keys:</h3>\n<ul>\n"
    for api, status in api_checks.items():
        html += f"<li><strong>{api}:</strong> {status}</li>\n"
    html += "</ul>\n"
    
    html += "<p><a href='/test'>← Back to Test Page</a></p>"
    
    return html