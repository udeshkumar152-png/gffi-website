#!/usr/bin/env python3
"""
GFFI LIVE CALCULATOR V3 (FINAL - WEBSITE READY)
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
WINDOW = 30
FALLBACK_CAPITAL = 15

# =========================
# COUNTRIES
# =========================
COUNTRIES = [
    {'name': 'USA', 'flag': '🇺🇸', 'symbol': '^GSPC'},
    {'name': 'India', 'flag': '🇮🇳', 'symbol': '^NSEI'},
    {'name': 'Germany', 'flag': '🇩🇪', 'symbol': '^GDAXI'},
]

# =========================
# STATUS
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
# FETCH DATA
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
# VOLATILITY
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
# CAPITAL
# =========================
def get_capital():
    return FALLBACK_CAPITAL

# =========================
# COUNTRY CALC
# =========================
def calculate_country(country):
    print(f"\n🌍 {country['name']}")

    prices = fetch_prices(country['symbol'])
    if prices is None:
        return None

    vol = calculate_volatility(prices)
    if vol is None:
        return None

    capital = get_capital()

    gffi = round((vol * 100) / capital, 2)

    return {
        "name": country["name"],
        "flag": country["flag"],
        "gffi": gffi,
        "status": get_status(gffi)
    }

# =========================
# MAIN
# =========================
def main():
    results = []

    for c in COUNTRIES:
        res = calculate_country(c)
        if res:
            results.append(res)
        time.sleep(1)

    if not results:
        print("❌ No data")
        return

    global_gffi = round(np.mean([x['gffi'] for x in results]), 2)

    # =========================
    # SAVE AS data.js (IMPORTANT)
    # =========================
    with open("data.js", "w") as f:
        f.write("const countryData = ")
        f.write(json.dumps(results, indent=2))
        f.write(";\n\n")

        f.write(f"const globalGFFI = {global_gffi};\n")
        f.write(f"const updateDate = '{datetime.now().strftime('%d %b %Y')}';\n")
        f.write(f"const updateTime = '{datetime.now().strftime('%I:%M %p')}';\n")

    print("\n✅ data.js updated successfully")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
