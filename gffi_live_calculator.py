#!/usr/bin/env python3
"""
GFFI Live Calculator - ALPHA VANTAGE ONLY VERSION
No Yahoo Finance - Works reliably on GitHub Actions
"""

import os
import json
import time
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🚀 GFFI LIVE CALCULATOR - ALPHA VANTAGE ONLY")
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
# COUNTRY CONFIGURATION - 5 countries for now
# ============================================
COUNTRIES = [
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'av_symbol': 'STI', 'fred_series': None}, 
]

# Nifty 50 stocks (using Alpha Vantage symbols)
NIFTY_50_STOCKS = [
    {'symbol': 'RELIANCE.BSE', 'name': 'Reliance Industries'},
    {'symbol': 'TCS.BSE', 'name': 'Tata Consultancy Services'},
    {'symbol': 'HDFCBANK.BSE', 'name': 'HDFC Bank'},
    {'symbol': 'INFY.BSE', 'name': 'Infosys'},
    {'symbol': 'ICICIBANK.BSE', 'name': 'ICICI Bank'},
    {'symbol': 'HINDUNILVR.BSE', 'name': 'Hindustan Unilever'},
    {'symbol': 'ITC.BSE', 'name': 'ITC Ltd'},
    {'symbol': 'SBIN.BSE', 'name': 'State Bank of India'},
    {'symbol': 'BHARTIARTL.BSE', 'name': 'Bharti Airtel'},
    {'symbol': 'KOTAKBANK.BSE', 'name': 'Kotak Mahindra Bank'},
]

# Sector definitions with Alpha Vantage symbols
SECTOR_DEFINITIONS = {
    'Banking & Financials': ['HDFCBANK.BSE', 'ICICIBANK.BSE', 'SBIN.BSE'],
    'Information Technology': ['TCS.BSE', 'INFY.BSE', 'HCLTECH.BSE'],
    'Pharmaceuticals': ['SUNPHARMA.BSE', 'CIPLA.BSE', 'DRREDDY.BSE'],
    'Energy': ['RELIANCE.BSE', 'ONGC.BSE', 'BPCL.BSE'],
    'FMCG': ['HINDUNILVR.BSE', 'ITC.BSE', 'BRITANNIA.BSE'],
    'Metals': ['TATASTEEL.BSE', 'JSWSTEEL.BSE', 'HINDALCO.BSE'],
}

# Stock name mapping
STOCK_NAMES = {
    'TCS.BSE': 'TCS',
    'HDFCBANK.BSE': 'HDFC Bank',
    'INFY.BSE': 'Infosys',
    'ICICIBANK.BSE': 'ICICI Bank',
    'HINDUNILVR.BSE': 'HUL',
    'ITC.BSE': 'ITC',
    'SBIN.BSE': 'SBI',
    'SUNPHARMA.BSE': 'Sun Pharma',
    'CIPLA.BSE': 'Cipla',
    'DRREDDY.BSE': 'Dr Reddy',
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
# ALPHA VANTAGE DATA FETCHING (ONLY SOURCE)
# ============================================

def fetch_alphavantage_data(symbol, max_retries=3):
    """Fetch data from Alpha Vantage with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"   📥 Fetching {symbol} (attempt {attempt+1}/{max_retries})...")
            
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}&outputsize=compact"
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                dates = []
                prices = []
                
                sorted_dates = sorted(time_series.keys())[-60:]
                for date_str in sorted_dates:
                    dates.append(pd.Timestamp(date_str))
                    prices.append(float(time_series[date_str]['4. close']))
                
                prices_series = pd.Series(prices, index=dates)
                print(f"   ✅ Got {len(prices_series)} days of data")
                return prices_series
            
            elif 'Note' in data:
                print(f"   ⚠️ API Note: {data['Note'][:100]}")
                if attempt < max_retries - 1:
                    wait_time = 15 * (attempt + 1)
                    print(f"   ⏳ Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
            else:
                print(f"   ⚠️ Unexpected response format")
                return None
                
        except Exception as e:
            print(f"   ⚠️ Attempt {attempt+1} failed: {str(e)[:50]}")
            if attempt < max_retries - 1:
                time.sleep(10)
    
    return None

def fetch_market_data(av_symbol):
    """Fetch market data - Alpha Vantage only"""
    return fetch_alphavantage_data(av_symbol)

def fetch_stock_data(symbol):
    """Fetch stock data and calculate GFFI"""
    prices = fetch_alphavantage_data(symbol)
    
    if prices is None or len(prices) < 30:
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    capital = calculate_capital_proxy(returns)
    
    if entropy is None or capital is None:
        return None
    
    gffi = (entropy / capital) * 1000
    
    return {
        'symbol': symbol.replace('.BSE', ''),
        'name': STOCK_NAMES.get(symbol, symbol.replace('.BSE', '')),
        'gffi': round(gffi, 1),
        'price': round(float(prices.iloc[-1]), 2)
    }

def fetch_index_data(symbol):
    """Fetch index data (Nifty, Sensex)"""
    prices = fetch_alphavantage_data(symbol)
    
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
    """Fetch data from FRED API"""
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
    """Calculate GFFI for a single country"""
    print(f"\n📍 Processing {country['name']}...")
    
    prices = fetch_market_data(country['av_symbol'])
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
    """Calculate live GFFI for a sector"""
    values = []
    for symbol in stocks[:3]:
        data = fetch_stock_data(symbol)
        if data:
            values.append(data['gffi'])
        time.sleep(2)  # Rate limiting
    
    if len(values) < 2:
        return None, None
    
    avg = sum(values) / len(values)
    trend = 'up' if avg > 62 else 'down' if avg < 58 else 'stable'
    return round(avg, 1), trend

def get_sector_stocks(stocks):
    """Get display names for sector stocks"""
    names = []
    for symbol in stocks[:4]:
        names.append(STOCK_NAMES.get(symbol, symbol.replace('.BSE', '')))
    return names

def fetch_live_sector_data():
    """Fetch live data for all sectors"""
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
    """Generate live stock picks based on GFFI values"""
    print("\n📈 Generating live stock picks...")
    stocks = []
    
    for s in NIFTY_50_STOCKS:
        data = fetch_stock_data(s['symbol'])
        if data:
            stocks.append(data)
        time.sleep(2)
    
    if len(stocks) < 5:
        print("   ❌ Insufficient stock data")
        return {}
    
    stocks.sort(key=lambda x: x['gffi'])
    
    return {
        'safe': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'BUY', 'reason': f'Low GFFI at ₹{s["price"]}'} for s in stocks[:3]],
        'risky': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'SELL', 'reason': f'High GFFI at ₹{s["price"]}'} for s in stocks[-3:][::-1]],
        'watch': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'WATCH', 'reason': f'Moderate GFFI at ₹{s["price"]}'} for s in stocks[3:6]]
    }

# ============================================
# INDIA MARKET DATA FUNCTIONS
# ============================================

def fetch_live_india_market_data():
    """Fetch live India market data"""
    print("\n🇮🇳 Fetching live India market data...")
    
    nifty = fetch_index_data('NSEI')
    sensex = fetch_index_data('BSESN')
    
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
# GIT CONFLICT RESOLUTION
# ============================================

def resolve_git_conflict():
    """Helper function to resolve git conflicts in data.js"""
    if os.path.exists('data.js'):
        with open('data.js', 'r') as f:
            content = f.read()
        
        # Check for conflict markers
        if '<<<<<<<' in content or '=======' in content or '>>>>>>>' in content:
            print("⚠️ Git conflict detected in data.js, creating fresh file...")
            return True  # Will create new file
    return False

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js"""
    print("\n" + "="*70)
    print("🌍 FETCHING GFFI DATA FROM ALPHA VANTAGE")
    print("="*70)
    
    # Check for git conflict
    create_new = resolve_git_conflict()
    
    # Fetch country GFFI data
    country_data = []
    gffi_values = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
        time.sleep(12)  # Rate limiting
    
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else None
    
    # Fetch other data
    time.sleep(15)
    sector_data = fetch_live_sector_data()
    
    time.sleep(15)
    stock_picks = generate_stock_picks()
    
    time.sleep(10)
    india_data = fetch_live_india_market_data()
    
    # Generate data.js content
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
