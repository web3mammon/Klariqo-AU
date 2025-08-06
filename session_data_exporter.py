#!/usr/bin/env python3
"""
SESSION DATA EXPORTER MODULE
Exports collected customer session data to CSV/Excel files for client reporting
"""

import os
import csv
import json
from datetime import datetime
from config import Config

class SessionDataExporter:
    """Handles exporting session data to CSV files for client reporting"""
    
    def __init__(self):
        self.export_folder = "customer_data"
        self.csv_file = "customer_sessions.csv"
        self.ensure_export_directory()
        self.ensure_csv_headers()
    
    def ensure_export_directory(self):
        """Create export directory if it doesn't exist"""
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder, exist_ok=True)
            print(f"📁 Created customer data folder: {self.export_folder}")
    
    def ensure_csv_headers(self):
        """Ensure CSV file exists with proper headers"""
        csv_path = os.path.join(self.export_folder, self.csv_file)
        
        # Define CSV headers based on plumbing business session variables
        headers = [
            "call_sid",
            "call_date",
            "call_time", 
            "call_direction",
            "customer_name",
            "customer_phone",
            "customer_location",
            "service_type",
            "urgency_level",
            "property_type",
            "preferred_date",
            "preferred_time",
            "selected_appointment",
            "issue_description",
            "previous_customer",
            "call_duration_seconds",
            "conversation_summary",
            "booking_status",
            "follow_up_required"
        ]
        
        # Create CSV with headers if it doesn't exist
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
            print(f"📊 Created customer data CSV: {csv_path}")
    
    def export_session_data(self, session, call_duration=None):
        """Export session data to CSV file"""
        try:
            csv_path = os.path.join(self.export_folder, self.csv_file)
            
            # Extract session variables
            variables = session.session_variables
            
            # Calculate call duration if not provided
            if call_duration is None:
                call_duration = self._calculate_call_duration(session)
            
            # Generate conversation summary
            conversation_summary = self._generate_conversation_summary(session)
            
            # Determine booking status
            booking_status = self._determine_booking_status(session)
            
            # Check if follow-up is required
            follow_up_required = self._needs_follow_up(session)
            
            # Prepare row data
            row_data = [
                session.call_sid,
                datetime.now().strftime("%Y-%m-%d"),  # call_date
                datetime.now().strftime("%H:%M:%S"),  # call_time
                session.call_direction,  # inbound/outbound
                variables.get("customer_name", ""),
                variables.get("customer_phone", ""),
                variables.get("customer_location", ""),
                variables.get("service_type", ""),
                variables.get("urgency_level", ""),
                variables.get("property_type", ""),
                variables.get("preferred_date", ""),
                variables.get("preferred_time", ""),
                variables.get("selected_appointment", ""),
                variables.get("issue_description", ""),
                variables.get("previous_customer", ""),
                call_duration,
                conversation_summary,
                booking_status,
                follow_up_required
            ]
            
            # Append to CSV file
            with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row_data)
            
            # Log successful export
            customer_info = variables.get("customer_name", "Unknown")
            service_info = variables.get("service_type", "general inquiry")
            print(f"📊 Exported session data: {customer_info} - {service_info}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting session data: {e}")
            return False
    
    def _calculate_call_duration(self, session):
        """Calculate call duration from conversation history"""
        try:
            # Simple estimation based on conversation length
            # In a real implementation, you'd track start time
            conversation_length = len(session.conversation_history)
            estimated_duration = conversation_length * 10  # ~10 seconds per exchange
            return max(estimated_duration, 30)  # Minimum 30 seconds
        except:
            return 60  # Default 1 minute
    
    def _generate_conversation_summary(self, session):
        """Generate a brief summary of the conversation"""
        try:
            if not hasattr(session, 'conversation_history') or not session.conversation_history:
                return "No conversation recorded"
            
            # Get key conversation elements
            history = session.conversation_history
            summary_parts = []
            
            # Check what was discussed
            variables = session.session_variables
            if variables.get("service_type"):
                summary_parts.append(f"Service: {variables['service_type']}")
            if variables.get("urgency_level"):
                summary_parts.append(f"Urgency: {variables['urgency_level']}")
            if variables.get("selected_appointment"):
                summary_parts.append(f"Booked: {variables['selected_appointment']}")
            
            # Add conversation length info
            summary_parts.append(f"Exchanges: {len(history)}")
            
            return " | ".join(summary_parts) if summary_parts else "Brief conversation"
            
        except Exception as e:
            return f"Summary error: {str(e)[:50]}"
    
    def _determine_booking_status(self, session):
        """Determine if a booking was made"""
        try:
            variables = session.session_variables
            
            if variables.get("selected_appointment"):
                if variables.get("customer_name") and variables.get("customer_phone"):
                    return "Booked - Confirmed"
                else:
                    return "Booked - Pending Details"
            elif variables.get("preferred_date") or variables.get("preferred_time"):
                return "Interested - No Booking"
            elif variables.get("urgency_level") == "emergency":
                return "Emergency - Immediate Service"
            else:
                return "Inquiry Only"
                
        except:
            return "Unknown"
    
    def _needs_follow_up(self, session):
        """Determine if follow-up is required"""
        try:
            variables = session.session_variables
            
            # Follow-up needed if:
            # 1. Booking started but not completed
            # 2. Emergency without immediate resolution
            # 3. Customer provided partial contact info
            
            if variables.get("selected_appointment") and not variables.get("customer_phone"):
                return "Yes - Missing Contact Info"
            elif variables.get("urgency_level") == "emergency":
                return "Yes - Emergency Service"
            elif variables.get("service_type") and not variables.get("selected_appointment"):
                return "Yes - Service Interest"
            else:
                return "No"
                
        except:
            return "Unknown"
    
    def get_export_stats(self):
        """Get statistics about exported data"""
        try:
            csv_path = os.path.join(self.export_folder, self.csv_file)
            
            if not os.path.exists(csv_path):
                return {"total_sessions": 0, "file_size": 0}
            
            # Count rows (minus header)
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                row_count = sum(1 for row in csv.reader(csvfile)) - 1  # Subtract header
            
            # Get file size
            file_size = os.path.getsize(csv_path)
            
            return {
                "total_sessions": max(0, row_count),
                "file_size_kb": round(file_size / 1024, 2),
                "csv_file": csv_path
            }
            
        except Exception as e:
            print(f"❌ Error getting export stats: {e}")
            return {"total_sessions": 0, "file_size": 0, "error": str(e)}

# Global session data exporter instance
session_exporter = SessionDataExporter()