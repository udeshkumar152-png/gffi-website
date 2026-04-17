#!/usr/bin/env python3

import json
import time
import numpy as np
import yfinance as yf
from datetime import datetime
from sklearn.linear_model import LinearRegression

# =========================
# CONFIG
# =========================
WINDOW = 30
CAPITAL = 15

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
    return "safe"

# =========================
# DATA
# =========================
def fetch_prices(symbol):
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    return df['Close'] if not df.empty else None

# =========================
# VOLATILITY
# =========================
def calc_vol(prices):
    r = np.log(prices / prices.shift(1)).dropna() * 100
    v = r.rolling(WINDOW).std().dropna()
    return v.iloc[-1].item()

# =========================
# AI TREND
# =========================
def predict_trend(x):
    if len(x) < 3: return None
    return round(x[-1] + (x[-1] - x[-3]) / 2, 2)

# =========================
# ML MODEL
# =========================
def predict_ml(x):
    if len(x) < 5: return None
    X = np.arange(len(x)).reshape(-1,1)
    y = np.array(x)
    model = LinearRegression().fit(X, y)
    return round(float(model.predict([[len(x)]])[0]), 2)

# =========================
# SAFE LSTM (fallback)
# =========================
def predict_lstm_safe(x):
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
        from sklearn.preprocessing import MinMaxScaler

        if len(x) < 10:
            return None

        data = np.array(x).reshape(-1,1)
        scaler = MinMaxScaler()
        d = scaler.fit_transform(data)

        X, y = [], []
        for i in range(3, len(d)):
            X.append(d[i-3:i])
            y.append(d[i])

        X, y = np.array(X), np.array(y)

        model = Sequential()
        model.add(LSTM(20, input_shape=(3,1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        model.fit(X, y, epochs=5, verbose=0)

        pred = model.predict(d[-3:].reshape(1,3,1), verbose=0)
        return round(float(scaler.inverse_transform(pred)[0][0]), 2)

    except:
        return None

# =========================
# COUNTRY
# =========================
def calc_country(c):
    p = fetch_prices(c['symbol'])
    if p is None: return None

    vol = calc_vol(p)
    gffi = round((vol * 100) / CAPITAL, 2)

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
        r = calc_country(c)
        if r: results.append(r)
        time.sleep(1)

    if not results:
        print("❌ No data")
        return

    series = [x['gffi'] for x in results]

    global_gffi = round(np.mean(series), 2)
    trend = predict_trend(series)
    ml = predict_ml(series)
    lstm = predict_lstm_safe(series)
    # STOCK SIGNAL
signal = "BUY 📈" if ml > trend else "SELL 📉"
confidence = round(abs(ml - trend) * 10, 2)
    
    # =========================
    # SAVE JS (SAFE)
    # =========================
    with open("data.js", "w") as f:
        f.write("const countryData = ")
        f.write(json.dumps(results, indent=2))
        f.write(";\n\n")

        f.write(f"const globalGFFI = {global_gffi};\n")
        f.write(f"const trendPrediction = {trend if trend else 0};\n")
        f.write(f"const mlPrediction = {ml if ml else 0};\n")
        f.write(f"const lstmPrediction = {lstm if lstm else 0};\n")
        f.write(f"const updateDate = '{datetime.now().strftime('%d %b %Y')}';\n")
        f.write(f"const updateTime = '{datetime.now().strftime('%I:%M %p')}';\n")

    print("✅ AI + ML + LSTM data.js updated")

if __name__ == "__main__":
    main()
