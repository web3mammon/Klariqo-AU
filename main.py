#!/usr/bin/env python3
"""
KLARIQO MAIN APPLICATION - AUDIO FILE SERVING
Serves audio files directly without conversion
"""

import os
import json
import time 
import base64
import audioop
import threading
import io
import struct
import wave
import tempfile
import subprocess
import csv
from flask import Flask, request, send_file
from flask_sock import Sock
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents, 
    LiveOptions
)

# Import our modular components
from config import Config
from session import session_manager
from router import response_router
from tts_engine import tts_engine
from audio_manager import audio_manager
from logger import call_logger
from session_data_exporter import session_exporter

# Import route blueprints
from routes.inbound import inbound_bp
from routes.outbound import outbound_bp
from routes.test import test_bp

# Initialize Flask app with WebSocket support
app = Flask(__name__)
sock = Sock(app)

# Configure Flask logging to be less verbose
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

audio_manager.reload_library()

# Register route blueprints
app.register_blueprint(inbound_bp)
app.register_blueprint(outbound_bp, url_prefix='/outbound')
app.register_blueprint(test_bp)

# Initialize Deepgram client
config = DeepgramClientOptions(options={"keepalive": "true"})
deepgram_client = DeepgramClient(Config.DEEPGRAM_API_KEY, config)

# Global variable for ngrok URL
current_ngrok_url = None

@app.route("/", methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Get session export statistics
    export_stats = session_exporter.get_export_stats()
    
    return f"""
    <h1>🔧 Pete's Plumbing - AI Voice Assistant (Jason)</h1>
    <p><strong>Status:</strong> ✅ Running</p>
    <p><strong>Active Sessions:</strong> {session_manager.get_active_count()}</p>
    <p><strong>Audio Files Cached:</strong> {len(audio_manager.memory_cache)}</p>
    <p><strong>Available Appointments:</strong> August 2024 slots active</p>
    <p><strong>Customer Data Exported:</strong> {export_stats['total_sessions']} sessions ({export_stats.get('file_size_kb', 0)} KB)</p>
    <br>    
    <p><a href="/test">🧪 Test Page</a> | <a href="/customer-data">📊 Customer Data</a></p>
    """



# ===== AUDIO FILE SERVING FUNCTIONS =====

def send_audio_twilio_media_stream(ws, ulaw_data, stream_sid):
    """
    Send μ-law data to Twilio Media Streams with proper formatting
    
    Twilio Media Streams:
    - Format: 8-bit μ-law, 8kHz, mono, base64 encoded
    - Flexible chunk sizes (no 320-byte requirement like Exotel)
    - Send via WebSocket as media events
    """
    try:
        if not stream_sid:
            print("❌ No stream_sid available")
            return
        
        if not ulaw_data:
            print("❌ No μ-law data provided")
            return
        
        print(f"🎵 Sending {len(ulaw_data)} bytes of μ-law data...")
        
        # Send μ-law data in reasonable chunks (Twilio is flexible)
        CHUNK_SIZE = 8000  # ~1 second of 8kHz μ-law audio
        total_chunks = len(ulaw_data) // CHUNK_SIZE
        
        print(f"🎵 Sending {total_chunks} chunks of {CHUNK_SIZE} bytes each")
        
        # Send chunks with minimal delay
        for i in range(total_chunks):
            start_pos = i * CHUNK_SIZE
            end_pos = start_pos + CHUNK_SIZE
            chunk = ulaw_data[start_pos:end_pos]
            
            # Send chunk to Twilio
            message = json.dumps({
                'event': 'media',
                'streamSid': stream_sid,
                'media': {
                    'payload': base64.b64encode(chunk).decode("ascii")
                }
            })
            
            ws.send(message)
            time.sleep(0.01)  # 10ms delay between chunks
            
            if (i + 1) % 100 == 0:
                print(f"📡 Sent {i + 1}/{total_chunks} chunks...")
        
        # Send remaining bytes (no padding needed for μ-law)
        remaining_bytes = len(ulaw_data) % CHUNK_SIZE
        if remaining_bytes > 0:
            last_chunk_start = total_chunks * CHUNK_SIZE
            last_chunk = ulaw_data[last_chunk_start:]
            
            message = json.dumps({
                'event': 'media',
                'streamSid': stream_sid,
                'media': {
                    'payload': base64.b64encode(last_chunk).decode("ascii")
                }
            })
            
            ws.send(message)
            print(f"📡 Sent final chunk")
        
        print(f"✅ μ-law audio sent successfully: {total_chunks} chunks")
        
    except Exception as e:
        print(f"❌ Send error: {e}")
        import traceback
        traceback.print_exc()

def convert_mp3_to_ulaw_for_tts(mp3_data):
    """
    Convert MP3 from TTS to μ-law format for Twilio
    Only used for TTS fallback - pre-recorded audio is already μ-law
    """
    try:
        # Try using librosa for MP3 to μ-law conversion
        import librosa
        import numpy as np
        
        # Load MP3 using librosa and convert to Twilio format
        audio_data, sr = librosa.load(io.BytesIO(mp3_data), sr=8000, mono=True)
        
        print(f"📊 TTS Audio: Converted to 8000Hz mono, {len(audio_data)} samples")
        
        # Convert to 16-bit PCM first (required for audioop.lin2ulaw)
        audio_data = np.clip(audio_data, -1.0, 1.0)
        pcm_16bit = (audio_data * 32767).astype(np.int16)
        
        # Convert 16-bit PCM to μ-law format (8-bit)
        ulaw_data = audioop.lin2ulaw(pcm_16bit.tobytes(), 2)  # 2 = 16-bit samples
        
        print(f"✅ TTS converted to μ-law: {len(ulaw_data)} bytes")
        return ulaw_data
        
    except ImportError:
        print("❌ librosa not available for TTS conversion")
        return None
    except Exception as e:
        print(f"❌ TTS MP3 to μ-law conversion failed: {e}")
        return None





# ===== TWILIO WEBSOCKET HANDLER =====

@sock.route('/media/<call_sid>')
def media_stream(ws, call_sid):
    """Handle Twilio streaming audio"""
    session = session_manager.get_session(call_sid)
    if not session:
        return
    
    session.twilio_ws = ws
    session.stream_sid = None
    
    def start_deepgram():
        """Initialize Deepgram connection for this session"""
        try:
            options = LiveOptions(
                model=Config.DEEPGRAM_MODEL,
                language=Config.DEEPGRAM_LANGUAGE,
                punctuate=True,
                smart_format=True,
                sample_rate=8000,
                encoding="linear16",
                channels=1,
                interim_results=True,
            )
            
            session.dg_connection = deepgram_client.listen.websocket.v("1")
            session.dg_connection.on(LiveTranscriptionEvents.Transcript, session.on_deepgram_message)
            session.dg_connection.on(LiveTranscriptionEvents.Error, session.on_deepgram_error)
            session.dg_connection.on(LiveTranscriptionEvents.Open, session.on_deepgram_open)
            session.dg_connection.start(options)
            
        except Exception as e:
            print(f"❌ Deepgram setup error: {e}")
    
    # Start Deepgram in separate thread
    deepgram_thread = threading.Thread(target=start_deepgram)
    deepgram_thread.daemon = True
    deepgram_thread.start()
    time.sleep(0.5)
    
    def transcript_checker():
        """Monitor for completed transcripts"""
        while True:
            time.sleep(0.05)
            if session.check_for_completion():
                process_and_respond_twilio_stream(session.completed_transcript, call_sid, ws, session.stream_sid)
                session.reset_for_next_input()
    
    # Start transcript checker
    checker_thread = threading.Thread(target=transcript_checker)
    checker_thread.daemon = True
    checker_thread.start()
    
    try:
        # Handle WebSocket messages from Twilio
        while True:
            message = ws.receive()
            if message is None:
                break
                
            data = json.loads(message)
            
            if data.get('event') == 'connected':
                print(f"🔌 Twilio connected: {call_sid}")
                
            elif data.get('event') == 'start':
                session.stream_sid = data.get('streamSid')
                print(f"🎤 Stream started: {session.stream_sid}")
                
                # Send intro audio immediately after stream starts
                if hasattr(session, 'selected_intro') and session.selected_intro:
                    intro_file = session.selected_intro
                    cache_key = intro_file.replace('.ulaw', '.mp3') if intro_file.endswith('.ulaw') else intro_file
                    
                    if cache_key in audio_manager.memory_cache:
                        ulaw_data = audio_manager.memory_cache[cache_key]
                        send_audio_twilio_media_stream(ws, ulaw_data, session.stream_sid)
                        call_logger.log_nisha_audio_response(call_sid, intro_file)
                        print(f"🎵 Sent intro via WebSocket: {intro_file}")
                    else:
                        print(f"❌ Intro audio not in cache: {cache_key}")
                
            elif data.get('event') == 'media':
                # Forward audio to Deepgram
                if session.dg_connection:
                    media_payload = data.get('media', {}).get('payload', '')
                    if media_payload:
                        try:
                            # Convert μ-law to linear PCM for Deepgram
                            mulaw_data = base64.b64decode(media_payload)
                            linear_data = audioop.ulaw2lin(mulaw_data, 2)
                            session.dg_connection.send(linear_data)
                        except Exception as e:
                            print(f"⚠️ Audio processing error: {e}")
                            
            elif data.get('event') == 'stop':
                print(f"🛑 Stream stopped: {call_sid}")
                break
                
    except Exception as e:
        print(f"❌ WebSocket error for {call_sid}: {e}")
        
    finally:
        # Export session data before cleanup
        try:
            if session:
                session_exporter.export_session_data(session)
        except Exception as e:
            print(f"⚠️ Error exporting session data: {e}")
        
        # Cleanup session
        if session.dg_connection:
            session.dg_connection.finish()
            session.dg_connection = None
        
        # Remove session from manager
        session_manager.remove_session(call_sid)

def process_and_respond_twilio_stream(transcript, call_sid, ws, stream_sid):
    """Process input and respond with bidirectional μ-law streaming"""
    try:
        session = session_manager.get_session(call_sid)
        if not session:
            return
        
        start_time = time.time()
        
        # Log parent's input
        call_logger.log_parent_input(call_sid, transcript)
        
        # Get AI response
        response_type, content = response_router.get_school_response(transcript, session)
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Add to history
        session.add_to_history("Parent", transcript)
        session.add_to_history("Nisha", f"<{response_type}: {content}>")
        
        # Clean logging
        print(f"📞 User: {transcript}")
        print(f"🤖 AI: {content} ({response_time_ms}ms)")
        
        if response_type == "AUDIO":
            # Send μ-law audio files directly via WebSocket
            audio_files = [f.strip() for f in content.split('+')]
            
            for audio_file in audio_files:
                # Ensure we use .mp3 extension for cache lookup (audio manager uses .mp3 keys)
                cache_key = audio_file.replace('.ulaw', '.mp3') if audio_file.endswith('.ulaw') else audio_file
                
                if cache_key in audio_manager.memory_cache:
                    ulaw_data = audio_manager.memory_cache[cache_key]
                    
                    # Send μ-law data directly to Twilio via WebSocket
                    send_audio_twilio_media_stream(ws, ulaw_data, stream_sid)
                    time.sleep(1.0)
                else:
                    print(f"❌ μ-law audio file not in cache: {cache_key} (original: {audio_file})")
                    
            call_logger.log_nisha_audio_response(call_sid, content)
            
        elif response_type == "TTS":
            # Generate TTS and convert MP3 to μ-law for Twilio
            tts_audio_data = tts_engine.generate_audio(content, save_temp=False)
            if tts_audio_data:
                # Convert MP3 from ElevenLabs to μ-law for Twilio
                ulaw_data = convert_mp3_to_ulaw_for_tts(tts_audio_data)
                if ulaw_data:
                    send_audio_twilio_media_stream(ws, ulaw_data, stream_sid)
                else:
                    print("❌ TTS MP3 to μ-law conversion failed")
                    
            call_logger.log_nisha_tts_response(call_sid, content)
        
        print(f"✅ Response sent")
        
    except Exception as e:
        print(f"❌ Processing error: {e}")
        import traceback
        traceback.print_exc()

@app.route("/audio_ulaw/<filename>")
def serve_audio(filename):
    """Serve μ-law audio files from memory cache"""
    return audio_manager.serve_audio_file(filename)

@app.route("/temp/<filename>")
def serve_temp_audio(filename):
    """Serve temporary TTS audio files"""
    try:
        if filename.startswith("temp_tts_"):
            file_path = os.path.join(Config.TEMP_FOLDER, filename)
            if os.path.exists(file_path):
                return send_file(file_path, mimetype='audio/mpeg')
            else:
                return "TTS file not found", 404
        else:
            return "Invalid file type", 404
            
    except Exception as e:
        print(f"❌ Error serving TTS audio {filename}: {e}")
        return "Error serving TTS audio", 500

@app.route("/logs/<filename>")
def serve_logs(filename):
    """Serve log files for download"""
    try:
        file_path = os.path.join(Config.LOGS_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return "Log file not found", 404
    except Exception as e:
        return f"Error serving log: {e}", 500

@app.route("/customer-data")
def customer_data_dashboard():
    """Customer data dashboard and download"""
    try:
        export_stats = session_exporter.get_export_stats()
        csv_path = export_stats.get('csv_file', '')
        
        if os.path.exists(csv_path):
            # Read recent entries for preview
            recent_entries = []
            try:
                with open(csv_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    rows = list(reader)
                    recent_entries = rows[-10:] if rows else []  # Last 10 entries
            except Exception as e:
                recent_entries = []
            
            # Generate HTML dashboard
            html = f"""
            <h1>📊 Pete's Plumbing - Customer Data Dashboard</h1>
            <p><strong>Total Sessions:</strong> {export_stats['total_sessions']}</p>
            <p><strong>File Size:</strong> {export_stats.get('file_size_kb', 0)} KB</p>
            <p><a href="/download-customer-data">📥 Download CSV File</a></p>
            <br>
            <h3>Recent Customer Sessions (Last 10):</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f0f0f0;">
                    <th>Date</th><th>Customer</th><th>Service</th><th>Phone</th><th>Booking Status</th>
                </tr>
            """
            
            for entry in reversed(recent_entries):  # Show newest first
                html += f"""
                <tr>
                    <td>{entry.get('call_date', '')}</td>
                    <td>{entry.get('customer_name', 'Unknown')}</td>
                    <td>{entry.get('service_type', 'General')}</td>
                    <td>{entry.get('customer_phone', '')}</td>
                    <td>{entry.get('booking_status', '')}</td>
                </tr>
                """
            
            html += """
            </table>
            <br>
            <p><a href="/">← Back to Dashboard</a></p>
            """
            
            return html
        else:
            return """
            <h1>📊 Customer Data Dashboard</h1>
            <p>No customer data available yet. Make some test calls to generate data!</p>
            <p><a href="/">← Back to Dashboard</a></p>
            """
            
    except Exception as e:
        return f"Error loading customer data: {e}", 500

@app.route("/download-customer-data")
def download_customer_data():
    """Download customer data CSV file"""
    try:
        export_stats = session_exporter.get_export_stats()
        csv_path = export_stats.get('csv_file', '')
        
        if os.path.exists(csv_path):
            return send_file(csv_path, as_attachment=True, download_name="pete_plumbing_customer_data.csv")
        else:
            return "Customer data file not found", 404
            
    except Exception as e:
        return f"Error downloading customer data: {e}", 500

def test_audio_cache():
    """Test audio cache availability"""
    try:
        if audio_manager.memory_cache:
            test_file = list(audio_manager.memory_cache.keys())[0]
            audio_data = audio_manager.memory_cache[test_file]
            
            print(f"🧪 Testing audio cache with {test_file}")
            
            if audio_data and len(audio_data) > 0:
                print(f"✅ Audio file loaded: {len(audio_data)} bytes")
                return True
            else:
                print("❌ Audio file empty or invalid")
                return False
        else:
            print("⚠️ No audio files in cache to test")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def start_ngrok():
    """Start ngrok tunnel for local development"""
    import subprocess
    import urllib.request
    
    try:
        # First check if ngrok is already running
        try:
            with urllib.request.urlopen('http://localhost:4040/api/tunnels') as response:
                data = json.loads(response.read())
                if 'tunnels' in data and len(data['tunnels']) > 0:
                    for tunnel in data['tunnels']:
                        if tunnel.get('proto') == 'https':
                            return tunnel['public_url']
        except:
            pass
        
        print("🚀 Starting ngrok...")
        process = subprocess.Popen([
            'ngrok', 'http', str(Config.FLASK_PORT)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        
        # Try to get tunnel info
        for attempt in range(10):
            try:
                with urllib.request.urlopen('http://localhost:4040/api/tunnels') as response:
                    data = json.loads(response.read())
                    
                    if 'tunnels' not in data:
                        time.sleep(1)
                        continue
                        
                    tunnels = data['tunnels']
                    if len(tunnels) == 0:
                        time.sleep(1)
                        continue
                    
                    # Find HTTPS tunnel
                    for tunnel in tunnels:
                        if tunnel.get('proto') == 'https':
                            return tunnel['public_url']
                    
                    # Fallback to first tunnel
                    if tunnels:
                        return tunnels[0]['public_url']
                        
            except Exception as e:
                time.sleep(1)
        
        print("❌ Could not get ngrok URL")
        return None
            
    except FileNotFoundError:
        print("⚠️ ngrok not found")
        return None
    except Exception as e:
        print(f"⚠️ ngrok error: {e}")
        return None

def cleanup_temp_files():
    """Periodic cleanup of temporary files"""
    while True:
        time.sleep(3600)
        tts_engine.cleanup_temp_files()

if __name__ == "__main__":
    print("🚀 KLARIQO - AI Voice Agent (Direct Audio Serving)")
    print("=" * 40)
    
    # Validate configuration
    try:
        Config.validate_config()
        print("✅ Config OK")
    except ValueError as e:
        print(f"❌ Config error: {e}")
        exit(1)
    
    # Test audio cache during startup
    print("🧪 Testing audio cache...")
    if test_audio_cache():
        print("✅ Audio cache working!")
    else:
        print("⚠️ Audio cache issues detected")
    
    # Start ngrok
    public_url = start_ngrok()
    current_ngrok_url = public_url
    
    if public_url:
        print(f"🌐 Public URL: {public_url}")
        print()
        print("📞 TWILIO SETUP:")
        print(f"   Incoming Call URL: {public_url}/twilio/voice")
        print(f"   WebSocket Handler: {public_url}/media/<call_sid>")
        print()
        print("🔧 TWILIO FLOW:")
        print("   TwiML → Bidirectional Media Streams")
        print("   ✅ μ-law audio streaming (WebSocket)")
        print("   ✅ Real-time audio processing")
        print()
    else:
        print("⚠️ Running without ngrok")
    
    print("✅ READY!")
    print("=" * 40)
    
    # Start background cleanup
    cleanup_thread = threading.Thread(target=cleanup_temp_files)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    # Run Flask app
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG,
        threaded=True
    )