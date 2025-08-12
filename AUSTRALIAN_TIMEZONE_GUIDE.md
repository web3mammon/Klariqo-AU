# 🌏 Australian Timezone Configuration Guide

## Overview

This guide explains the new configurable timezone system that allows the AI assistant to use the correct timezone based on the client's specific Australian city. This ensures that when customers say "today" or "tomorrow", the AI understands the correct date and time for their location.

## 🎯 Why This Matters

Australia has **multiple timezones**:
- **AEST/AEDT (UTC+10/+11)**: NSW, VIC, TAS, ACT, QLD
- **ACST/ACDT (UTC+9:30/+10:30)**: SA, NT  
- **AWST (UTC+8)**: WA

Without proper timezone handling, a customer in Perth saying "come tomorrow at 2 PM" would be interpreted incorrectly by an AI using Sydney time.

## 🚀 How It Works

### 1. Client Configuration
In `config.py`, set your client's city:

```python
CLIENT_CONFIG = {
    "business_name": "Pete's Plumbing",
    "city": "Melbourne",  # ← Change this to your client's city
    # ... other settings
}
```

### 2. Automatic Timezone Mapping
The system automatically maps the city to the correct timezone:

```python
# Examples:
"Melbourne" → "Australia/Melbourne" (AEST/AEDT)
"Adelaide"  → "Australia/Adelaide"  (ACST/ACDT)
"Perth"     → "Australia/Perth"     (AWST)
"Brisbane"  → "Australia/Brisbane"  (AEST, no DST)
```

### 3. AI Context Enhancement
The AI now receives real-time date/time context in the client's timezone:

```
📅 CURRENT DATE & TIME CONTEXT:
Today is Tuesday, August 12, 2025 at 08:50 PM
Tomorrow is Wednesday, August 13, 2025
When customer says "today" they mean Tuesday, August 12, 2025
When customer says "tomorrow" they mean Wednesday, August 13, 2025
```

## 📍 Supported Australian Cities

### New South Wales (AEST/AEDT - UTC+10/+11)
- Sydney, Canberra, Newcastle, Wollongong
- Central Coast, Gold Coast, Coffs Harbour
- Port Macquarie, Tweed Heads

### Victoria (AEST/AEDT - UTC+10/+11)
- Melbourne, Geelong, Ballarat, Bendigo
- Shepparton, Mildura, Warrnambool
- Albury, Wodonga

### Queensland (AEST - UTC+10, NO daylight saving)
- Brisbane, Gold Coast, Townsville, Cairns
- Toowoomba, Mackay, Rockhampton
- Bundaberg, Hervey Bay, Sunshine Coast
- Ipswich, Logan

### South Australia (ACST/ACDT - UTC+9:30/+10:30)
- Adelaide, Mount Gambier, Whyalla
- Murray Bridge, Port Augusta, Port Pirie

### Western Australia (AWST - UTC+8, NO daylight saving)
- Perth, Fremantle, Rockingham, Mandurah
- Albany, Bunbury, Geraldton, Kalgoorlie

### Tasmania (AEST/AEDT - UTC+10/+11)
- Hobart, Launceston, Devonport, Burnie

### Northern Territory (ACST - UTC+9:30, NO daylight saving)
- Darwin, Alice Springs, Palmerston

## 🔧 Configuration

### Quick Setup
1. **Find your client's city** in the supported cities list above
2. **Update `config.py`**:
   ```python
   CLIENT_CONFIG = {
       "city": "Adelaide",  # Change this line
       # ... rest of config
   }
   ```
3. **Test the timezone**:
   ```bash
   python test_timezones.py
   ```

### Advanced Configuration
If your client's city isn't in the list, you can add it to `AUSTRALIAN_TIMEZONES` in `config.py`:

```python
AUSTRALIAN_TIMEZONES = {
    # ... existing cities
    "Your City": "Australia/YourTimezone",
    # ... rest of mapping
}
```

## 🧪 Testing

### Run the Timezone Test
```bash
python test_timezones.py
```

This will show:
- ✅ Timezone mapping for all major cities
- ✅ Current time in each timezone
- ✅ Your client's configured timezone
- ✅ Timezone differences between cities

### Expected Output Example
```
🏢 TESTING CLIENT CONFIGURATION
==================================================
Current client city: Adelaide
Mapped timezone: Australia/Adelaide
Current time in Adelaide: Tuesday, August 12, 2025 at 08:20 PM
Timezone offset: UTC+09:30
```

## ⏰ Timezone Differences

Here are the typical time differences between major cities:

| City | Timezone | Offset | Example Time |
|------|----------|--------|--------------|
| Sydney | AEST/AEDT | UTC+10/+11 | 8:50 PM |
| Melbourne | AEST/AEDT | UTC+10/+11 | 8:50 PM |
| Brisbane | AEST | UTC+10 | 8:50 PM |
| Adelaide | ACST/ACDT | UTC+9:30/+10:30 | 8:20 PM |
| Perth | AWST | UTC+8 | 6:50 PM |
| Darwin | ACST | UTC+9:30 | 8:20 PM |

## 🎯 Real-World Impact

### Before (Hardcoded Sydney Time)
- Customer in Perth: "Can you come tomorrow at 2 PM?"
- AI thinks: "Tomorrow at 2 PM Sydney time"
- **Problem**: That's 4 PM Perth time - wrong!

### After (Client-Specific Timezone)
- Customer in Perth: "Can you come tomorrow at 2 PM?"
- AI thinks: "Tomorrow at 2 PM Perth time"
- **Result**: Correct interpretation and scheduling

## 🔄 Daylight Saving Time (DST)

The system automatically handles DST transitions:

- **NSW, VIC, TAS, ACT**: Use DST (AEST → AEDT)
- **QLD, WA, NT**: No DST (always AEST/AWST/ACST)
- **SA**: Uses DST (ACST → ACDT)

## 🚨 Troubleshooting

### Issue: Wrong timezone being used
**Solution**: Check `CLIENT_CONFIG["city"]` in `config.py`

### Issue: City not found in mapping
**Solution**: 
1. Check spelling (case-insensitive)
2. Add city to `AUSTRALIAN_TIMEZONES` mapping
3. System will fallback to Sydney timezone

### Issue: Time seems wrong
**Solution**: Run `python test_timezones.py` to verify current timezone

## 📋 Implementation Details

### Files Modified
- `config.py`: Added `AUSTRALIAN_TIMEZONES` mapping and `get_australian_timezone()` function
- `router.py`: Updated all datetime calls to use client's timezone

### Key Functions
```python
Config.get_australian_timezone(city_name)
# Returns: pytz timezone string (e.g., 'Australia/Sydney')
```

### Dependencies
- `pytz==2023.3` (already in requirements.txt)

## 🎉 Benefits

1. **Accurate Scheduling**: AI understands "tomorrow" correctly for each client
2. **Professional Service**: No timezone confusion in customer interactions
3. **Scalable**: Easy to adapt for new clients in different cities
4. **Automatic**: No manual timezone calculations needed
5. **DST Aware**: Handles daylight saving transitions automatically

## 💡 Best Practices

1. **Always test** timezone changes with `python test_timezones.py`
2. **Use exact city names** from the supported list
3. **Consider DST** when scheduling appointments across timezone boundaries
4. **Document the timezone** in client onboarding materials

---

**Next Steps**: 
- Update your client's city in `config.py`
- Run the timezone test to verify
- Deploy and test with real customer calls
