#!/usr/bin/env python3
import yfinance as yf
import numpy as np
from datetime import datetime
import json

print("🚀 GFFI Update Script Started")

# Sample data (for testing)
country_data = [
    {'flag': '🇺🇸', 'name': 'USA', 'gffi': 62.1, 'status': 'warning'},
    {'flag': '🇮🇳', 'name': 'India', 'gffi': 64.7, 'status': 'success'},
]

# Update script.js
js_content = f"""// Auto-generated on {datetime.now()}
const countryData = {json.dumps(country_data)};
const globalGFFI = 63.5;
const updateDate = '{datetime.now().strftime("%d %b %Y")}';
"""

with open('script.js', 'w') as f:
    f.write(js_content)

print("✅ script.js updated successfully")
