import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LogisticRegression

# =========================
# DATA FETCH
# =========================
symbol = "^GSPC"  # S&P 500

df = yf.download(symbol, period="1y", interval="1d")

# =========================
# FEATURES
# =========================
df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
df['volatility'] = df['returns'].rolling(20).std()

# Momentum
df['momentum'] = df['Close'].pct_change(5)

# GFFI proxy
df['gffi'] = (df['volatility'] * 100) / 15

# =========================
# TARGET (UP / DOWN)
# =========================
df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

df = df.dropna()

# =========================
# ML MODEL
# =========================
X = df[['momentum', 'gffi', 'volatility']]
y = df['target']

model = LogisticRegression()
model.fit(X, y)

# =========================
# PREDICTION
# =========================
latest = X.iloc[-1].values.reshape(1, -1)
prediction = model.predict(latest)[0]
prob = model.predict_proba(latest)[0][1]

# =========================
# RESULT
# =========================
signal = "BUY 📈" if prediction == 1 else "SELL 📉"

print("\n🔥 STOCK SIGNAL")
print("Signal:", signal)
print("Confidence:", round(prob * 100, 2), "%")
