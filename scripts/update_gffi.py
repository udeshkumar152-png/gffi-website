import numpy as np
import pandas as pd
import yfinance as yf
import json

# =========================
# DOWNLOAD DATA
# =========================
sp500 = yf.download("^GSPC", start="2020-01-01")

sp500['returns'] = np.log(sp500['Close'] / sp500['Close'].shift(1)) * 100
returns = sp500['returns'].dropna()

# =========================
# VOLATILITY
# =========================
volatility = returns.rolling(30).std()

# =========================
# CAPITAL (STATIC OR CSV)
# =========================
capital = 12.5  # manually set OR load from CSV

# =========================
# GFFI CALCULATION
# =========================
gffi = (volatility * 100) / capital

# =========================
# CLEAN DATA
# =========================
df = pd.DataFrame({
    "date": volatility.index,
    "gffi": gffi
}).dropna()

# =========================
# SAVE JSON
# =========================
df['date'] = df['date'].astype(str)

data = df.tail(100).to_dict(orient="records")

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

print("✅ data.json updated")
