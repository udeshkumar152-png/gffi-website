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
    if gffi >= 15:
        return "critical"
    elif gffi >= 10:
        return "warning"
    elif gffi >= 5:
        return "moderate"
    return "safe"

# =========================
# FETCH DATA
# =========================
def fetch_prices(symbol):
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    if df.empty:
        return None
    return df['Close']

# =========================
# VOLATILITY
# =========================
def calc_vol(prices):
    returns = np.log(prices / prices.shift(1)).dropna() * 100
    vol = returns.rolling(WINDOW).std().dropna()
    return vol.iloc[-1].item()

# =========================
# AI TREND
# =========================
def predict_trend(series):
    if len(series) < 3:
        return 0
    return round(series[-1] + (series[-1] - series[-3]) / 2, 2)

# =========================
# ML MODEL
# =========================
def predict_ml(series):
    if len(series) < 5:
        return 0
    X = np.arange(len(series)).reshape(-1, 1)
    y = np.array(series)
    model = LinearRegression()
    model.fit(X, y)
    return round(float(model.predict([[len(series)]])[0]), 2)

# =========================
# SAFE LSTM (OPTIONAL)
# =========================
def predict_lstm_safe(series):
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
        from sklearn.preprocessing import MinMaxScaler

        if len(series) < 10:
            return 0

        data = np.array(series).reshape(-1, 1)
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(data)

        X, y = [], []
        for i in range(3, len(scaled)):
            X.append(scaled[i-3:i])
            y.append(scaled[i])

        X = np.array(X)
        y = np.array(y)

        model = Sequential()
        model.add(LSTM(20, input_shape=(3,1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        model.fit(X, y, epochs=5, verbose=0)

        pred = model.predict(scaled[-3:].reshape(1,3,1), verbose=0)
        return round(float(scaler.inverse_transform(pred)[0][0]), 2)

    except:
        return 0

# =========================
# COUNTRY CALCULATION
# =========================
def calc_country(c):
    prices = fetch_prices(c['symbol'])
    if prices is None:
        return None

    vol = calc_vol(prices)
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
        if r:
            results.append(r)
        time.sleep(1)

    if not results:
        print("❌ No data")
        return

    # =========================
    # CALCULATIONS
    # =========================
    series = [x['gffi'] for x in results]

    global_gffi = round(np.mean(series), 2)
    trend = predict_trend(series)
    ml = predict_ml(series)
    lstm = predict_lstm_safe(series)

    # =========================
    # STOCK SIGNAL
    # =========================
    signal = "BUY 📈" if ml > trend else "SELL 📉"
    confidence = round(abs(ml - trend) * 10, 2)

    # =========================
    # SAVE FILE (IMPORTANT)
    # =========================
    with open("data.js", "w") as f:
        f.write("const countryData = ")
        f.write(json.dumps(results, indent=2))
        f.write(";\n\n")

        f.write(f"const globalGFFI = {global_gffi};\n")
        f.write(f"const trendPrediction = {trend};\n")
        f.write(f"const mlPrediction = {ml};\n")
        f.write(f"const lstmPrediction = {lstm};\n")

        f.write(f"const stockSignal = '{signal}';\n")
        f.write(f"const confidence = {confidence};\n")

        f.write(f"const updateDate = '{datetime.now().strftime('%d %b %Y')}';\n")
        f.write(f"const updateTime = '{datetime.now().strftime('%I:%M %p')}';\n")

    print("✅ data.js updated successfully")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
