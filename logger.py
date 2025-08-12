#!/usr/bin/env python3
"""
KLARIQO CALL LOGGING MODULE
Handles structured logging of all call data to CSV
"""

import os
import csv
import time
from datetime import datetime
from config import Config

class CallLogger:
    """Manages structured logging of call data"""
    
    def __init__(self):
        self.logs_folder = Config.LOGS_FOLDER
        self.call_log_file = os.path.join(self.logs_folder, "call_logs.csv")
        self.conversation_log_file = os.path.join(self.logs_folder, "conversation_logs.csv")
        
        # Ensure logs folder exists
        os.makedirs(self.logs_folder, exist_ok=True)
        
        # Initialize CSV files with headers if they don't exist
        self._initialize_log_files()
    
    def _initialize_log_files(self):
        """Initialize CSV log files with proper headers"""
        
        # Call logs header
        call_headers = [
            'timestamp', 'call_sid', 'phone_number', 'call_direction', 
            'call_duration', 'total_audio_files_used', 'tts_responses_count',
            'session_flags', 'lead_data', 'final_status'
        ]
        
        if not os.path.exists(self.call_log_file):
            with open(self.call_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(call_headers)
            print(f"📊 Created call log file: {self.call_log_file}")
        
        # Conversation logs header  
        conversation_headers = [
            'timestamp', 'call_sid', 'speaker', 'message_type', 
            'content', 'audio_files_used', 'response_time_ms'
        ]
        
        if not os.path.exists(self.conversation_log_file):
            with open(self.conversation_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(conversation_headers)
            print(f"💬 Created conversation log file: {self.conversation_log_file}")
    
    def log_call_start(self, call_sid, phone_number, call_direction, lead_data=None):
        """Log the start of a new call"""
        timestamp = datetime.now().isoformat()
        
        # Store call start info (we'll update with end info later)
        call_data = {
            'call_sid': call_sid,
            'phone_number': phone_number,
            'call_direction': call_direction,
            'start_time': time.time(),
            'start_timestamp': timestamp,
            'lead_data': lead_data or {},
            'audio_files_used': [],
            'tts_responses': 0,
            'customer_details': {
                'name': None,
                'phone': phone_number,
                'location': None,
                'service_type': None,
                'urgency_level': None,
                'issue_description': None,
                'preferred_date': None,
                'preferred_time': None,
                'property_type': None,
                'previous_customer': None
            }
        }
        
        # Store in memory for this session
        if not hasattr(self, '_active_calls'):
            self._active_calls = {}
        self._active_calls[call_sid] = call_data
        
        print(f"📞 Call started - {call_direction}: {call_sid}")
    
    def update_customer_details(self, call_sid, session_variables):
        """Update customer details during the call"""
        if hasattr(self, '_active_calls') and call_sid in self._active_calls:
            call_data = self._active_calls[call_sid]
            customer_details = call_data['customer_details']
            
            # Update with any new information
            for key, value in session_variables.items():
                if value is not None and key in customer_details:
                    customer_details[key] = value
            
            print(f"📝 Updated customer details for {call_sid}: {customer_details}")
    
    def log_conversation_turn(self, call_sid, speaker, message_type, content, 
                            audio_files_used=None, response_time_ms=None):
        """
        Log a single conversation turn
        
        Args:
            call_sid: Twilio call SID
            speaker: 'Parent' or 'Nisha'  
            message_type: 'transcript', 'audio', 'tts'
            content: The actual message content
            audio_files_used: List of audio files played (if any)
            response_time_ms: Response generation time in milliseconds
        """
        timestamp = datetime.now().isoformat()
        
        # Format audio files as comma-separated string
        audio_files_str = ""
        if audio_files_used:
            if isinstance(audio_files_used, list):
                audio_files_str = ", ".join(audio_files_used)
            else:
                audio_files_str = str(audio_files_used)
        
        # Write to conversation log
        with open(self.conversation_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, call_sid, speaker, message_type,
                content, audio_files_str, response_time_ms or ""
            ])
        
        # Update active call tracking
        if hasattr(self, '_active_calls') and call_sid in self._active_calls:
            call_data = self._active_calls[call_sid]
            
            if audio_files_used:
                call_data['audio_files_used'].extend(
                    audio_files_used if isinstance(audio_files_used, list) else [audio_files_used]
                )
            
            if message_type == 'tts':
                call_data['tts_responses'] += 1
    
    def log_call_end(self, call_sid, final_status="completed", session_variables=None):
        """Log the end of a call with summary data"""
        if not hasattr(self, '_active_calls') or call_sid not in self._active_calls:
            print(f"⚠️ No call data found for {call_sid}")
            return
        
        call_data = self._active_calls[call_sid]
        timestamp = datetime.now().isoformat()
        
        # Update customer details if provided
        if session_variables:
            self.update_customer_details(call_sid, session_variables)
        
        # Calculate call duration
        call_duration = int(time.time() - call_data['start_time'])
        
        # Count unique audio files used
        unique_audio_files = len(set(call_data['audio_files_used']))
        
        # Get customer details
        customer_details = call_data['customer_details']
        
        # Format lead data as JSON string
        lead_data_str = str(call_data['lead_data']) if call_data['lead_data'] else ""
        
        # Create comprehensive call summary
        call_summary = {
            'call_sid': call_sid,
            'start_time': call_data['start_timestamp'],
            'end_time': timestamp,
            'duration_seconds': call_duration,
            'direction': call_data['call_direction'],
            'phone_number': call_data['phone_number'],
            'customer_name': customer_details['name'],
            'customer_location': customer_details['location'],
            'service_type': customer_details['service_type'],
            'urgency_level': customer_details['urgency_level'],
            'issue_description': customer_details['issue_description'],
            'preferred_date': customer_details['preferred_date'],
            'preferred_time': customer_details['preferred_time'],
            'property_type': customer_details['property_type'],
            'previous_customer': customer_details['previous_customer'],
            'audio_files_used': unique_audio_files,
            'tts_responses': call_data['tts_responses'],
            'final_status': final_status
        }
        
        # Write to call log
        with open(self.call_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, call_sid, call_data['phone_number'], 
                call_data['call_direction'], call_duration,
                unique_audio_files, call_data['tts_responses'],
                str(call_summary), lead_data_str, final_status
            ])
        
        # Also write to detailed customer data file
        self._write_customer_data(call_summary)
        
        # Clean up from memory
        del self._active_calls[call_sid]
        
        print(f"📋 Call logged - Duration: {call_duration}s, Customer: {customer_details['name']}, Service: {customer_details['service_type']}")
    
    def log_parent_input(self, call_sid, transcript, response_time_ms=None):
        """Log parent's speech input"""
        self.log_conversation_turn(
            call_sid, "Parent", "transcript", transcript, 
            response_time_ms=response_time_ms
        )
    
    def log_nisha_audio_response(self, call_sid, audio_files, response_time_ms=None):
        """Log Nisha's audio file response"""
        # Parse audio files (handle chaining with +)
        audio_list = [f.strip() for f in audio_files.split('+')]
        
        # Log the response
        self.log_conversation_turn(
            call_sid, "Nisha", "audio", f"<audio: {audio_files}>",
            audio_files_used=audio_list, response_time_ms=response_time_ms
        )
    
    def log_nisha_tts_response(self, call_sid, tts_text, response_time_ms=None):
        """Log Nisha's TTS response"""
        self.log_conversation_turn(
            call_sid, "Nisha", "tts", f"<TTS: {tts_text}>",
            response_time_ms=response_time_ms
        )
    
    def get_call_stats(self, days=7):
        """Get call statistics for the last N days"""
        if not os.path.exists(self.call_log_file):
            return {}
        
        stats = {
            'total_calls': 0,
            'inbound_calls': 0,
            'outbound_calls': 0,
            'avg_duration': 0,
            'total_audio_files_used': 0,
            'total_tts_responses': 0
        }
        
        cutoff_time = time.time() - (days * 24 * 3600)
        durations = []
        
        try:
            with open(self.call_log_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Parse timestamp
                    call_time = datetime.fromisoformat(row['timestamp']).timestamp()
                    
                    if call_time >= cutoff_time:
                        stats['total_calls'] += 1
                        
                        if row['call_direction'] == 'inbound':
                            stats['inbound_calls'] += 1
                        else:
                            stats['outbound_calls'] += 1
                        
                        # Add duration
                        duration = int(row['call_duration']) if row['call_duration'] else 0
                        durations.append(duration)
                        
                        # Add audio file count
                        audio_count = int(row['total_audio_files_used']) if row['total_audio_files_used'] else 0
                        stats['total_audio_files_used'] += audio_count
                        
                        # Add TTS count
                        tts_count = int(row['tts_responses_count']) if row['tts_responses_count'] else 0
                        stats['total_tts_responses'] += tts_count
        
            # Calculate average duration
            if durations:
                stats['avg_duration'] = sum(durations) // len(durations)
        
        except Exception as e:
            print(f"⚠️ Error reading call stats: {e}")
        
        return stats
    
    def export_logs_for_date(self, date_str):
        """Export logs for a specific date (YYYY-MM-DD format)"""
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Export call logs
            call_export_file = f"call_logs_{date_str}.csv"
            conversation_export_file = f"conversation_logs_{date_str}.csv" 
            
            # Filter and export call logs
            with open(self.call_log_file, 'r', encoding='utf-8') as infile:
                with open(call_export_file, 'w', newline='', encoding='utf-8') as outfile:
                    reader = csv.reader(infile)
                    writer = csv.writer(outfile)
                    
                    # Copy header
                    header = next(reader)
                    writer.writerow(header)
                    
                    # Filter rows by date
                    for row in reader:
                        if row[0]:  # timestamp column
                            row_date = datetime.fromisoformat(row[0]).date()
                            if row_date == target_date:
                                writer.writerow(row)
            
            print(f"📤 Exported logs for {date_str}")
            return call_export_file, conversation_export_file
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None, None

    def _write_customer_data(self, call_summary):
        """Write detailed customer data to separate file"""
        customer_data_file = os.path.join(self.logs_folder, "customer_data.csv")
        
        # Create customer data file with headers if it doesn't exist
        if not os.path.exists(customer_data_file):
            headers = [
                'call_date', 'call_time', 'call_sid', 'customer_name', 'customer_phone',
                'customer_location', 'service_type', 'urgency_level', 'issue_description',
                'preferred_date', 'preferred_time', 'property_type', 'previous_customer',
                'call_duration', 'call_status', 'audio_files_used', 'tts_responses'
            ]
            with open(customer_data_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        
        # Parse timestamp
        start_dt = datetime.fromisoformat(call_summary['start_time'].replace('Z', '+00:00'))
        
        # Write customer data
        with open(customer_data_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                start_dt.strftime('%Y-%m-%d'),  # call_date
                start_dt.strftime('%H:%M:%S'),  # call_time
                call_summary['call_sid'],
                call_summary['customer_name'] or '',
                call_summary['phone_number'],
                call_summary['customer_location'] or '',
                call_summary['service_type'] or '',
                call_summary['urgency_level'] or '',
                call_summary['issue_description'] or '',
                call_summary['preferred_date'] or '',
                call_summary['preferred_time'] or '',
                call_summary['property_type'] or '',
                call_summary['previous_customer'] or '',
                call_summary['duration_seconds'],
                call_summary['final_status'],
                call_summary['audio_files_used'],
                call_summary['tts_responses']
            ])

# Global call logger instance
call_logger = CallLogger()