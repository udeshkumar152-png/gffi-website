#!/usr/bin/env python3

import json
import time
import numpy as np
import yfinance as yf
from datetime import datetime
from sklearn.linear_model import LinearRegression

WINDOW = 30
FALLBACK_CAPITAL = 15

COUNTRIES = [
    {'name': 'USA', 'flag': '🇺🇸', 'symbol': '^GSPC'},
    {'name': 'India', 'flag': '🇮🇳', 'symbol': '^NSEI'},
    {'name': 'Germany', 'flag': '🇩🇪', 'symbol': '^GDAXI'},
]

# =========================
# STATUS
# =========================
def get_status(gffi):
    if gffi >= 15: return "critical"
    elif gffi >= 10: return "warning"
    elif gffi >= 5: return "moderate"
    else: return "safe"

# =========================
# DATA
# =========================
def fetch_prices(symbol):
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    return df['Close'] if not df.empty else None

# =========================
# VOLATILITY
# =========================
def calculate_volatility(prices):
    returns = np.log(prices / prices.shift(1)).dropna() * 100
    vol = returns.rolling(WINDOW).std().dropna()
    return vol.iloc[-1].item()

# =========================
# AI TREND MODEL
# =========================
def predict_trend(gffi_list):
    if len(gffi_list) < 3:
        return None
    trend = (gffi_list[-1] - gffi_list[-3]) / 2
    return round(gffi_list[-1] + trend, 2)

# =========================
# ML MODEL
# =========================
def predict_ml(gffi_list):
    if len(gffi_list) < 5:
        return None

    X = np.arange(len(gffi_list)).reshape(-1,1)
    y = np.array(gffi_list)

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[len(gffi_list)]])[0]
    return round(float(pred), 2)

# =========================
# COUNTRY
# =========================
def calculate_country(c):
    prices = fetch_prices(c['symbol'])
    if prices is None: return None

    vol = calculate_volatility(prices)
    gffi = round((vol * 100) / FALLBACK_CAPITAL, 2)

    return {
        "name": c["name"],
        "flag": c["flag"],
        "gffi": gffi,
        "status": get_status(gffi)
    }

# =========================
# MAIN
# =========================
def main():
    results = []

    for c in COUNTRIES:
        r = calculate_country(c)
        if r: results.append(r)
        time.sleep(1)

    gffi_series = [x['gffi'] for x in results]

    global_gffi = round(np.mean(gffi_series), 2)
    trend_pred = predict_trend(gffi_series)
    ml_pred = predict_ml(gffi_series)

    # =========================
    # SAVE data.js
    # =========================
    with open("data.js", "w") as f:
        f.write("const countryData = ")
        f.write(json.dumps(results, indent=2))
        f.write(";\n\n")

        f.write(f"const globalGFFI = {global_gffi};\n")
        f.write(f"const trendPrediction = {trend_pred};\n")
        f.write(f"const mlPrediction = {ml_pred};\n")
        f.write(f"const updateDate = '{datetime.now().strftime('%d %b %Y')}';\n")
        f.write(f"const updateTime = '{datetime.now().strftime('%I:%M %p')}';\n")

    print("✅ AI + ML data.js updated")

if __name__ == "__main__":
    main()
