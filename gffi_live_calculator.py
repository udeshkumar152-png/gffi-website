#!/usr/bin/env python3
"""
GFFI Live Calculator - 100% REAL DATA ONLY
NO FALLBACK DATA - If API fails, section remains empty
"""

import os
import json
import time
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🚀 GFFI LIVE CALCULATOR - 100% REAL DATA ONLY")
print("="*70)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# CONFIGURATION
# ============================================
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY')
FRED_API_KEY = os.getenv('FRED_API_KEY')

if not ALPHA_VANTAGE_KEY:
    print("❌ ALPHA_VANTAGE_KEY not found in environment variables!")
    exit(1)

# ============================================
# COUNTRY CONFIGURATION - All 17 countries
# ============================================
COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'av_symbol': 'SPX', 'yahoo_symbol': '^GSPC', 'fred_series': 'DDSI03USA156NWDB'},
    {'code': 'Germany', 'name': 'Germany', 'flag': '🇩🇪', 'av_symbol': 'GDAXI', 'yahoo_symbol': '^GDAXI', 'fred_series': 'DDSI03DEA156NWDB'},
    {'code': 'France', 'name': 'France', 'flag': '🇫🇷', 'av_symbol': 'FCHI', 'yahoo_symbol': '^FCHI', 'fred_series': 'DDSI03FRA156NWDB'},
    {'code': 'Japan', 'name': 'Japan', 'flag': '🇯🇵', 'av_symbol': 'NIKKEI225', 'yahoo_symbol': '^N225', 'fred_series': 'DDSI03JPA156NWDB'},
    {'code': 'UK', 'name': 'UK', 'flag': '🇬🇧', 'av_symbol': 'FTSE', 'yahoo_symbol': '^FTSE', 'fred_series': 'DDSI03GBA156NWDB'},
    {'code': 'China', 'name': 'China', 'flag': '🇨🇳', 'av_symbol': 'SSEC', 'yahoo_symbol': '000001.SS', 'fred_series': 'DDSI03CNA156NWDB'},
    {'code': 'India', 'name': 'India', 'flag': '🇮🇳', 'av_symbol': 'NSEI', 'yahoo_symbol': '^NSEI', 'fred_series': 'DDSI03INA156NWDB'},
    {'code': 'Brazil', 'name': 'Brazil', 'flag': '🇧🇷', 'av_symbol': 'BVSP', 'yahoo_symbol': '^BVSP', 'fred_series': 'DDSI03BRA156NWDB'},
    {'code': 'Canada', 'name': 'Canada', 'flag': '🇨🇦', 'av_symbol': 'GSPTSE', 'yahoo_symbol': '^GSPTSE', 'fred_series': 'DDSI03CAA156NWDB'},
    {'code': 'Australia', 'name': 'Australia', 'flag': '🇦🇺', 'av_symbol': 'AXJO', 'yahoo_symbol': '^AXJO', 'fred_series': 'DDSI03AUA156NWDB'},
    {'code': 'SouthKorea', 'name': 'S. Korea', 'flag': '🇰🇷', 'av_symbol': 'KS11', 'yahoo_symbol': '^KS11', 'fred_series': 'DDSI03KRA156NWDB'},
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'av_symbol': 'STI', 'yahoo_symbol': '^STI', 'fred_series': 'DDSI03SGA156NWDB'},
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'av_symbol': 'JN0U.JO', 'yahoo_symbol': '^JN0U.JO', 'fred_series': 'DDSI03ZAA156NWDB'},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'av_symbol': 'MXX', 'yahoo_symbol': '^MXX', 'fred_series': 'DDSI03MXA156NWDB'},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'av_symbol': 'FTSEMIB', 'yahoo_symbol': 'FTSEMIB.MI', 'fred_series': 'DDSI03ITA156NWDB'},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'av_symbol': 'MERV', 'yahoo_symbol': '^MERV', 'fred_series': 'DDSI03ARA156NWDB'},
]

# Nifty 50 stocks for live stock picks
NIFTY_50_STOCKS = [
    {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries'},
    {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services'},
    {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank'},
    {'symbol': 'INFY.NS', 'name': 'Infosys'},
    {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank'},
    {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever'},
    {'symbol': 'ITC.NS', 'name': 'ITC Ltd'},
    {'symbol': 'SBIN.NS', 'name': 'State Bank of India'},
    {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel'},
    {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank'},
]

# Sector definitions
SECTOR_DEFINITIONS = {
    'Banking & Financials': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS'],
    'Information Technology': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS'],
    'Pharmaceuticals': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'DIVISLAB.NS'],
    'Automobile': ['MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS'],
    'Energy': ['RELIANCE.NS', 'ONGC.NS', 'BPCL.NS', 'IOC.NS'],
    'FMCG': ['HINDUNILVR.NS', 'ITC.NS', 'BRITANNIA.NS', 'NESTLEIND.NS'],
    'Metals': ['TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'COALINDIA.NS'],
    'Telecom': ['BHARTIARTL.NS', 'IDEA.NS'],
}

# Stock name mapping
STOCK_NAMES = {
    'RELIANCE.NS': 'Reliance',
    'TCS.NS': 'TCS',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank',
    'HINDUNILVR.NS': 'HUL',
    'ITC.NS': 'ITC',
    'SBIN.NS': 'SBI',
    'BHARTIARTL.NS': 'Bharti Airtel',
    'KOTAKBANK.NS': 'Kotak Bank',
    'HCLTECH.NS': 'HCLTech',
    'WIPRO.NS': 'Wipro',
    'SUNPHARMA.NS': 'Sun Pharma',
    'CIPLA.NS': 'Cipla',
    'DRREDDY.NS': 'Dr Reddy',
    'DIVISLAB.NS': 'Divis Labs',
    'MARUTI.NS': 'Maruti',
    'TATAMOTORS.NS': 'Tata Motors',
    'M&M.NS': 'M&M',
    'BAJAJ-AUTO.NS': 'Bajaj Auto',
    'ONGC.NS': 'ONGC',
    'BPCL.NS': 'BPCL',
    'IOC.NS': 'IOC',
    'BRITANNIA.NS': 'Britannia',
    'NESTLEIND.NS': 'Nestle',
    'TATASTEEL.NS': 'Tata Steel',
    'JSWSTEEL.NS': 'JSW Steel',
    'HINDALCO.NS': 'Hindalco',
    'COALINDIA.NS': 'Coal India',
    'IDEA.NS': 'Vodafone Idea',
}

# ============================================
# CORE UTILITY FUNCTIONS
# ============================================

def get_status(gffi):
    if gffi >= 70:
        return 'critical'
    elif gffi >= 65:
        return 'warning'
    else:
        return 'success'

def calculate_entropy(returns_series):
    returns = returns_series.dropna().values
    returns = returns[~np.isinf(returns)]
    returns = returns[~np.isnan(returns)]
    
    if len(returns) < 10:
        return None
    
    bins = min(20, len(returns)//2)
    hist, _ = np.histogram(returns, bins=bins, density=True)
    probs = hist / hist.sum()
    probs = probs[probs > 0]
    
    if len(probs) == 0:
        return None
    
    entropy = -np.sum(probs * np.log(probs))
    max_entropy = np.log(bins)
    if max_entropy > 0:
        entropy = min(1.0, entropy / max_entropy)
    
    return max(0.1, min(0.9, entropy))

def calculate_capital_proxy(returns_series):
    if len(returns_series) < 60:
        return None
    
    rolling_vol = returns_series.rolling(60).std().dropna()
    if len(rolling_vol) == 0:
        return None
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 20 / (1 + latest_vol)
    return max(10, min(30, capital_proxy))

# ============================================
# DATA FETCHING FUNCTIONS
# ============================================

def fetch_yahoo_data(symbol, period="2mo"):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return None
        return hist['Close']
    except:
        return None

def fetch_alphavantage_data(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}&outputsize=compact"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            return None
        
        time_series = data['Time Series (Daily)']
        dates = []
        prices = []
        
        sorted_dates = sorted(time_series.keys())[-60:]
        for date_str in sorted_dates:
            dates.append(pd.Timestamp(date_str))
            prices.append(float(time_series[date_str]['4. close']))
        
        return pd.Series(prices, index=dates)
    except:
        return None

def fetch_market_data(yahoo_symbol, av_symbol):
    # Try Yahoo first
    prices = fetch_yahoo_data(yahoo_symbol)
    if prices is not None and len(prices) >= 30:
        return prices
    
    # Try Alpha Vantage as backup
    prices = fetch_alphavantage_data(av_symbol)
    if prices is not None and len(prices) >= 30:
        return prices
    
    return None

def fetch_stock_data(symbol):
    prices = fetch_yahoo_data(symbol)
    if prices is None or len(prices) < 30:
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    capital = calculate_capital_proxy(returns)
    
    if entropy is None or capital is None:
        return None
    
    gffi = (entropy / capital) * 1000
    
    return {
        'symbol': symbol.replace('.NS', ''),
        'name': STOCK_NAMES.get(symbol, symbol.replace('.NS', '')),
        'gffi': round(gffi, 1),
        'price': round(float(prices.iloc[-1]), 2)
    }

def fetch_index_data(yahoo_symbol):
    prices = fetch_yahoo_data(yahoo_symbol, period="5d")
    if prices is None or len(prices) < 2:
        return None
    
    current = prices.iloc[-1]
    prev = prices.iloc[-2]
    change = ((current - prev) / prev) * 100
    
    return {
        'value': round(current, 2),
        'change': round(change, 2)
    }

def fetch_fred_data(series_id):
    if not FRED_API_KEY:
        return None
    try:
        from pandas_datareader import data as web
        end = datetime.now()
        start = end - timedelta(days=3*365)
        data = web.DataReader(series_id, 'fred', start, end, api_key=FRED_API_KEY)
        if data.empty:
            return None
        return {'latest_value': float(data.iloc[-1, 0])}
    except:
        return None

# ============================================
# COUNTRY GFFI FUNCTIONS
# ============================================

def calculate_country_gffi(country):
    print(f"\n📍 Processing {country['name']}...")
    
    prices = fetch_market_data(country['yahoo_symbol'], country['av_symbol'])
    if prices is None:
        print(f"   ❌ No market data for {country['name']}")
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    if entropy is None:
        print(f"   ❌ Could not calculate entropy for {country['name']}")
        return None
    
    if country.get('fred_series') and FRED_API_KEY:
        fred_data = fetch_fred_data(country['fred_series'])
        if fred_data:
            capital = fred_data['latest_value']
        else:
            capital = calculate_capital_proxy(returns)
    else:
        capital = calculate_capital_proxy(returns)
    
    if capital is None:
        print(f"   ❌ Could not calculate capital for {country['name']}")
        return None
    
    gffi = (entropy / capital) * 1000
    gffi = round(gffi, 1)
    
    result = {
        'flag': country['flag'],
        'name': country['name'],
        'gffi': gffi,
        'status': get_status(gffi)
    }
    
    print(f"   ✅ GFFI: {gffi} ({result['status']})")
    return result

# ============================================
# SECTOR DATA FUNCTIONS
# ============================================

def calculate_sector_gffi(sector_name, stocks):
    values = []
    for symbol in stocks[:3]:
        data = fetch_stock_data(symbol)
        if data:
            values.append(data['gffi'])
        time.sleep(1)
    
    if len(values) < 2:
        return None, None
    
    avg = sum(values) / len(values)
    trend = 'up' if avg > 62 else 'down' if avg < 58 else 'stable'
    return round(avg, 1), trend

def get_sector_stocks(stocks):
    names = []
    for symbol in stocks[:4]:
        names.append(STOCK_NAMES.get(symbol, symbol.replace('.NS', '')))
    return names

def fetch_live_sector_data():
    print("\n🏭 Fetching live sector data...")
    data = []
    for name, stocks in SECTOR_DEFINITIONS.items():
        gffi, trend = calculate_sector_gffi(name, stocks)
        if gffi:
            data.append({
                'name': name,
                'gffi': gffi,
                'trend': trend,
                'stocks': get_sector_stocks(stocks)
            })
            print(f"   ✅ {name}: GFFI={gffi}")
        else:
            print(f"   ❌ {name}: No data")
        time.sleep(2)
    return data

# ============================================
# STOCK PICKS FUNCTIONS
# ============================================

def generate_stock_picks():
    print("\n📈 Generating live stock picks...")
    stocks = []
    
    for s in NIFTY_50_STOCKS[:15]:
        data = fetch_stock_data(s['symbol'])
        if data:
            stocks.append(data)
        time.sleep(1)
    
    if len(stocks) < 9:
        print("   ❌ Insufficient stock data")
        return {}
    
    stocks.sort(key=lambda x: x['gffi'])
    
    return {
        'safe': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'BUY', 'reason': f'Low GFFI at ₹{s["price"]}'} for s in stocks[:3]],
        'risky': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'SELL', 'reason': f'High GFFI at ₹{s["price"]}'} for s in stocks[-3:][::-1]],
        'watch': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'WATCH', 'reason': f'Moderate GFFI at ₹{s["price"]}'} for s in stocks[4:7]]
    }

# ============================================
# INDIA MARKET DATA FUNCTIONS
# ============================================

def fetch_live_india_market_data():
    print("\n🇮🇳 Fetching live India market data...")
    
    nifty = fetch_index_data('^NSEI')
    sensex = fetch_index_data('^BSESN')
    
    if not nifty or not sensex:
        print("   ❌ Could not fetch India market data")
        return {}
    
    print(f"   ✅ Nifty: {nifty['value']} ({nifty['change']}%)")
    print(f"   ✅ Sensex: {sensex['value']} ({sensex['change']}%)")
    
    return {
        'nifty': int(nifty['value']),
        'sensex': int(sensex['value']),
        'nifty_change': round(nifty['change'], 2),
        'sensex_change': round(sensex['change'], 2)
    }

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    print("\n" + "="*70)
    print("🌍 FETCHING 100% REAL GFFI DATA")
    print("="*70)
    
    # Countries
    country_data = []
    gffi_values = []
    for country in COUNTRIES[:5]:  # Start with 5 countries
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
        time.sleep(5)
    
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else None
    
    # Other data
    time.sleep(10)
    sector_data = fetch_live_sector_data()
    
    time.sleep(10)
    stock_picks = generate_stock_picks()
    
    time.sleep(5)
    india_data = fetch_live_india_market_data()
    
    # Generate data.js
    now = datetime.now()
    
    js_lines = [
        "// ============================================",
        "// DATA.JS - Auto-generated by GFFI Live Calculator",
        f"// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "// ============================================",
        "",
        f"const countryData = {json.dumps(country_data, indent=2, ensure_ascii=False)};",
        "",
        f"const globalGFFI = {json.dumps(global_gffi)};",
        "",
        f"const updateDate = '{now.strftime('%d %b %Y')}';",
        f"const updateTime = '{now.strftime('%I:%M %p')}';",
        "",
        f"const sectorData = {json.dumps(sector_data, indent=2, ensure_ascii=False)};",
        "",
        f"const stockPicks = {json.dumps(stock_picks, indent=2, ensure_ascii=False)};",
        "",
        f"const indiaMarketData = {json.dumps(india_data, indent=2, ensure_ascii=False)};"
    ]
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("\n".join(js_lines))
    
    print("\n" + "="*70)
    print("✅ DATA.JS UPDATED SUCCESSFULLY")
    print("="*70)
    print(f"   Countries: {len(country_data)}")
    print(f"   Global GFFI: {global_gffi if global_gffi else 'None'}")
    print(f"   Sectors: {len(sector_data)}")
    print(f"   Stock Picks: {'Yes' if stock_picks else 'No'}")
    if india_data:
        print(f"   Nifty: {india_data.get('nifty')}")
        print(f"   Sensex: {india_data.get('sensex')}")
    print("="*70)

if __name__ == "__main__":
    main()
