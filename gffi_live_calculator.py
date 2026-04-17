#!/usr/bin/env python3
"""
GFFI DAILY CALCULATOR (NEW MODEL)
Volatility-based (Validated Model)
"""

import os
import json
import time
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta

print("="*80)
print("🚀 GFFI CALCULATOR V2 (VOLATILITY MODEL)")
print("="*80)

# =========================
# CONFIG
# =========================
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY')
FRED_API_KEY = os.getenv('FRED_API_KEY')

# =========================
# COUNTRIES
# =========================
COUNTRIES = [
    {'name': 'USA', 'flag': '🇺🇸', 'symbol': 'SPX', 'fred': 'RCTRWAMXM163N'},
    {'name': 'India', 'flag': '🇮🇳', 'symbol': 'NSEI', 'fred': 'DDSI03INA156NWDB'},
    {'name': 'Germany', 'flag': '🇩🇪', 'symbol': 'GDAXI', 'fred': 'DDSI03DEA156NWDB'},
]

# =========================
# STATUS FUNCTION
# =========================
def get_status(gffi):
    if gffi >= 15:
        return "critical"
    elif gffi >= 10:
        return "warning"
    elif gffi >= 5:
        return "moderate"
    else:
        return "safe"

# =========================
# FETCH MARKET DATA
# =========================
def fetch_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    
    r = requests.get(url)
    data = r.json()
    
    if "Time Series (Daily)" not in data:
        return None
    
    ts = data["Time Series (Daily)"]
    
    dates = []
    prices = []
    
    for d in sorted(ts.keys())[-60:]:
        dates.append(pd.Timestamp(d))
        prices.append(float(ts[d]["4. close"]))
    
    return pd.Series(prices, index=dates)

# =========================
# VOLATILITY CALCULATION
# =========================
def calculate_volatility(prices):
    returns = prices.pct_change().dropna() * 100
    
    if len(returns) < 30:
        return None
    
    vol = returns.rolling(30).std().dropna()
    
    if len(vol) == 0:
        return None
    
    return float(vol.iloc[-1])

# =========================
# FETCH CAPITAL (FRED)
# =========================
def fetch_capital(series):
    if not FRED_API_KEY:
        return None
    
    try:
        from pandas_datareader import data as web
        
        end = datetime.now()
        start = end - timedelta(days=365*3)
        
        df = web.DataReader(series, "fred", start, end, api_key=FRED_API_KEY)
        
        return float(df.iloc[-1, 0])
    
    except:
        return None

# =========================
# MAIN CALCULATION
# =========================
def calculate_country(country):
    print(f"\n🌍 {country['name']}...")
    
    prices = fetch_data(country['symbol'])
    
    if prices is None:
        print("❌ No data")
        return None
    
    vol = calculate_volatility(prices)
    
    if vol is None:
        print("❌ No volatility")
        return None
    
    capital = fetch_capital(country['fred'])
    
    if capital is None:
        capital = 15  # fallback
    
    # 🔥 NEW MODEL
    gffi = (vol * 100) / capital
    gffi = round(gffi, 2)
    
    result = {
        "name": country["name"],
        "flag": country["flag"],
        "gffi": gffi,
        "volatility": round(vol, 2),
        "capital": round(capital, 2),
        "status": get_status(gffi)
    }
    
    print(f"✅ GFFI: {gffi} ({result['status']})")
    
    return result

# =========================
# MAIN
# =========================
def main():
    results = []
    
    for c in COUNTRIES:
        r = calculate_country(c)
        
        if r:
            results.append(r)
        
        time.sleep(15)  # API limit
    
    if not results:
        print("❌ No data generated")
        return
    
    # Global GFFI
    global_gffi = round(np.mean([x['gffi'] for x in results]), 2)
    
    # Save JSON
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "global_gffi": global_gffi,
        "countries": results
    }
    
    with open("data.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n✅ data.json updated")
    print(f"🌍 Global GFFI: {global_gffi}")

if __name__ == "__main__":
    main()
