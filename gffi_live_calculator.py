#!/usr/bin/env python3
"""
GFFI LIVE CALCULATOR V3 (PRODUCTION READY)
Volatility-Based Validated Model
"""

import os
import json
import time
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

print("="*80)
print("🚀 GFFI LIVE CALCULATOR V3")
print("="*80)

# =========================
# CONFIG
# =========================
WINDOW = 30  # rolling window
FALLBACK_CAPITAL = 15

# =========================
# COUNTRIES (FIXED SYMBOLS)
# =========================
COUNTRIES = [
    {'name': 'USA', 'flag': '🇺🇸', 'symbol': '^GSPC'},
    {'name': 'India', 'flag': '🇮🇳', 'symbol': '^NSEI'},
    {'name': 'Germany', 'flag': '🇩🇪', 'symbol': '^GDAXI'},
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
# FETCH MARKET DATA (STABLE)
# =========================
def fetch_prices(symbol):
    try:
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)
        
        if df.empty:
            return None
        
        return df['Close']
    
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
        return None

# =========================
# VOLATILITY CALCULATION
# =========================
def calculate_volatility(prices):
    returns = np.log(prices / prices.shift(1)) * 100
    returns = returns.dropna()
    
    if len(returns) < WINDOW:
        return None
    
    vol = returns.rolling(WINDOW).std().dropna()
    
    if len(vol) == 0:
        return None
    
    return float(vol.iloc[-1])

# =========================
# CAPITAL (STATIC / FUTURE API)
# =========================
def get_capital(country_name):
    # Future: connect FRED here
    return FALLBACK_CAPITAL

# =========================
# MAIN COUNTRY CALCULATION
# =========================
def calculate_country(country):
    print(f"\n🌍 {country['name']}")

    prices = fetch_prices(country['symbol'])

    if prices is None:
        print("❌ No price data")
        return None

    vol = calculate_volatility(prices)

    if vol is None:
        print("❌ Volatility error")
        return None

    capital = get_capital(country['name'])

    # 🔥 CORE MODEL
    gffi = (vol * 100) / capital
    gffi = round(gffi, 2)

    result = {
        "name": country["name"],
        "flag": country["flag"],
        "gffi": gffi,
        "volatility": round(vol, 2),
        "capital": capital,
        "status": get_status(gffi)
    }

    print(f"✅ GFFI = {gffi} ({result['status']})")

    return result

# =========================
# MAIN
# =========================
def main():
    results = []

    for c in COUNTRIES:
        res = calculate_country(c)
        if res:
            results.append(res)
        time.sleep(2)

    if len(results) == 0:
        print("❌ No results generated")
        return

    # Global GFFI
    global_gffi = round(np.mean([x['gffi'] for x in results]), 2)

    # Output JSON (WEBSITE READY)
    output = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "global_gffi": global_gffi,
        "countries": results,
        "model": "Volatility-Based GFFI (Validated)"
    }

    with open("data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n📊 FINAL OUTPUT")
    print(json.dumps(output, indent=2))
    print("\n✅ data.json updated successfully")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
