# 🚀 CLIENT ADAPTATION - QUICK START GUIDE

## Overview
This system now has **centralized client configuration** making it easy to adapt for different clients without extensive code changes.

## 🎯 What's New

### ✅ **Centralized Client Configuration**
- All client-specific information is now in `Config.CLIENT_CONFIG` in `config.py`
- No more hardcoded business names throughout the codebase
- Easy to change business name, AI assistant name, industry, location, etc.

### ✅ **Automated Adaptation Tool**
- Run `py client_adaptation.py` for guided client setup
- Pre-built templates for common industries (hotel, real estate, plumbing)
- Automatic file updates and directory creation

## 🚀 Quick Adaptation (5 minutes)

### Option 1: Automated Tool (Recommended)
```bash
# Run the adaptation tool
py client_adaptation.py

# Choose from pre-built templates or create custom
# Follow the prompts to configure your client
```

### Option 2: Manual Configuration
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

## 📋 What Gets Updated Automatically

### ✅ **Core Files**
- `config.py` - Client configuration
- `router.py` - AI prompts and responses
- `main.py` - Dashboard and web interface
- `README.md` - Project documentation

### ✅ **Directories Created**
- `customer_data/your_business_name/` - Client-specific data
- `logs/your_business_name/` - Client-specific logs

### ✅ **Files Generated**
- `your_business_name_adaptation_summary.md` - Adaptation report

## 🔄 Manual Steps Required

After running the adaptation tool, you'll need to:

1. **Update Audio Files** (`audio_ulaw/` directory)
   - Replace audio files with client-specific content
   - Update file names to match your business

2. **Update Audio Transcripts** (`audio_snippets.json`)
   - Update all transcripts with client-specific messaging
   - Ensure file names match your audio files

3. **Update Route Files**
   - `routes/inbound.py` - Update intro file reference
   - `routes/outbound.py` - Update intro file reference

4. **Test the System**
   - Run `py main.py` to test with new configuration
   - Verify all client-specific information displays correctly

## 🏢 Example Client Configurations

### Hotel Business
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

### Real Estate Business
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

### Plumbing Business (Current)
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

## 🔧 Advanced Customization

### Custom Session Variables
Update `SESSION_VARIABLES_TEMPLATE` in `config.py` for industry-specific data collection:

```python
# For Hotel Business
SESSION_VARIABLES_TEMPLATE = {
    "check_in_date": None,
    "check_out_date": None,
    "room_type": None,
    "guest_count": None,
    "budget_range": None,
    "special_requests": None,
    "customer_name": None,
    "inquiry_focus": None
}

# For Real Estate Business  
SESSION_VARIABLES_TEMPLATE = {
    "property_type": None,
    "location_preference": None,
    "budget_range": None,
    "inspection_date": None,
    "customer_name": None,
    "contact_method": None
}
```

### Custom Availability Data
Update availability slots in `config.py` for your business schedule:

```python
YOUR_BUSINESS_AVAILABILITY = {
    "available_slots": [
        {"date": "Monday, August 5th", "time": "9:00 AM - 11:00 AM", "slot_id": "MON05_0900"},
        {"date": "Tuesday, August 6th", "time": "2:00 PM - 4:00 PM", "slot_id": "TUE06_1400"},
        # Add your business-specific availability
    ]
}
```

## 🎯 Benefits of This Approach

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

## 🚨 Important Notes

1. **Backup First**: Always backup your current configuration before adapting
2. **Test Thoroughly**: Test all functionality after adaptation
3. **Update Audio Files**: Don't forget to replace audio content
4. **Check Routes**: Verify intro files are correctly referenced
5. **Environment Variables**: Ensure API keys are set for new client

## 📞 Support

If you encounter issues during adaptation:
1. Check the `CLIENT_ADAPTATION_GUIDE.md` for detailed instructions
2. Review the generated adaptation summary file
3. Verify all file paths and references are correct
4. Test with a simple configuration first

---

**🎉 You're now ready to easily adapt this system for any client!**
