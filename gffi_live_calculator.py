#!/usr/bin/env python3
"""
GFFI Live Calculator - COMPLETE VERSION
Fetches live data from Alpha Vantage - NO DEFAULTS, only real data
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

print("="*80)
print("🚀 GFFI LIVE CALCULATOR - PURE REAL DATA")
print("="*80)
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
# COUNTRY CONFIGURATION - ALL 17 COUNTRIES
# ============================================
COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'av_symbol': 'SPX', 'fred_series': 'DDSI03USA156NWDB'},
    {'code': 'Germany', 'name': 'Germany', 'flag': '🇩🇪', 'av_symbol': 'GDAXI', 'fred_series': 'DDSI03DEA156NWDB'},
    {'code': 'France', 'name': 'France', 'flag': '🇫🇷', 'av_symbol': 'FCHI', 'fred_series': 'DDSI03FRA156NWDB'},
    {'code': 'Japan', 'name': 'Japan', 'flag': '🇯🇵', 'av_symbol': 'NIKKEI225', 'fred_series': 'DDSI03JPA156NWDB'},
    {'code': 'UK', 'name': 'UK', 'flag': '🇬🇧', 'av_symbol': 'FTSE', 'fred_series': 'DDSI03GBA156NWDB'},
    {'code': 'China', 'name': 'China', 'flag': '🇨🇳', 'av_symbol': 'SSEC', 'fred_series': 'DDSI03CNA156NWDB'},
    {'code': 'India', 'name': 'India', 'flag': '🇮🇳', 'av_symbol': 'NSEI', 'fred_series': 'DDSI03INA156NWDB'},
    {'code': 'Brazil', 'name': 'Brazil', 'flag': '🇧🇷', 'av_symbol': 'BVSP', 'fred_series': 'DDSI03BRA156NWDB'},
    {'code': 'Canada', 'name': 'Canada', 'flag': '🇨🇦', 'av_symbol': 'GSPTSE', 'fred_series': 'DDSI03CAA156NWDB'},
    {'code': 'Australia', 'name': 'Australia', 'flag': '🇦🇺', 'av_symbol': 'AXJO', 'fred_series': 'DDSI03AUA156NWDB'},
    {'code': 'SouthKorea', 'name': 'S. Korea', 'flag': '🇰🇷', 'av_symbol': 'KS11', 'fred_series': 'DDSI03KRA156NWDB'},
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'av_symbol': 'STI', 'fred_series': None},
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'av_symbol': 'JN0U.JO', 'fred_series': 'DDSI03ZAA156NWDB'},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'av_symbol': 'MXX', 'fred_series': 'DDSI03MXA156NWDB'},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'av_symbol': 'FTSEMIB', 'fred_series': 'DDSI03ITA156NWDB'},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'av_symbol': 'MERV', 'fred_series': 'DDSI03ARA156NWDB'},
]

# ============================================
# NIFTY 50 STOCKS - FOR LIVE STOCK PICKS
# ============================================
NIFTY_50_STOCKS = [
    {'symbol': 'RELIANCE.BSE', 'name': 'RELIANCE'},
    {'symbol': 'TCS.BSE', 'name': 'TCS'},
    {'symbol': 'HDFCBANK.BSE', 'name': 'HDFCBANK'},
    {'symbol': 'INFY.BSE', 'name': 'INFY'},
    {'symbol': 'ICICIBANK.BSE', 'name': 'ICICIBANK'},
    {'symbol': 'HINDUNILVR.BSE', 'name': 'HINDUNILVR'},
    {'symbol': 'ITC.BSE', 'name': 'ITC'},
    {'symbol': 'SBIN.BSE', 'name': 'SBIN'},
    {'symbol': 'BHARTIARTL.BSE', 'name': 'BHARTIARTL'},
    {'symbol': 'KOTAKBANK.BSE', 'name': 'KOTAKBANK'},
    {'symbol': 'LT.BSE', 'name': 'LT'},
    {'symbol': 'ASIANPAINT.BSE', 'name': 'ASIANPAINT'},
    {'symbol': 'MARUTI.BSE', 'name': 'MARUTI'},
    {'symbol': 'SUNPHARMA.BSE', 'name': 'SUNPHARMA'},
    {'symbol': 'TATAMOTORS.BSE', 'name': 'TATAMOTORS'},
    {'symbol': 'AXISBANK.BSE', 'name': 'AXISBANK'},
    {'symbol': 'NTPC.BSE', 'name': 'NTPC'},
    {'symbol': 'ONGC.BSE', 'name': 'ONGC'},
    {'symbol': 'POWERGRID.BSE', 'name': 'POWERGRID'},
    {'symbol': 'TITAN.BSE', 'name': 'TITAN'},
]

# ============================================
# SECTOR DEFINITIONS
# ============================================
SECTOR_DEFINITIONS = {
    'Banking & Financials': ['HDFCBANK.BSE', 'ICICIBANK.BSE', 'SBIN.BSE', 'KOTAKBANK.BSE', 'AXISBANK.BSE'],
    'Information Technology': ['TCS.BSE', 'INFY.BSE', 'HCLTECH.BSE', 'WIPRO.BSE'],
    'Pharmaceuticals': ['SUNPHARMA.BSE', 'CIPLA.BSE', 'DRREDDY.BSE', 'DIVISLAB.BSE'],
    'Automobile': ['MARUTI.BSE', 'TATAMOTORS.BSE', 'M&M.BSE', 'BAJAJ-AUTO.BSE'],
    'Energy': ['RELIANCE.BSE', 'ONGC.BSE', 'BPCL.BSE', 'IOC.BSE'],
    'FMCG': ['HINDUNILVR.BSE', 'ITC.BSE', 'BRITANNIA.BSE', 'NESTLEIND.BSE'],
    'Metals': ['TATASTEEL.BSE', 'JSWSTEEL.BSE', 'HINDALCO.BSE', 'COALINDIA.BSE'],
    'Telecom': ['BHARTIARTL.BSE'],
}

# ============================================
# STOCK NAME MAPPING
# ============================================
STOCK_NAMES = {
    'RELIANCE.BSE': 'RELIANCE',
    'TCS.BSE': 'TCS',
    'HDFCBANK.BSE': 'HDFCBANK',
    'INFY.BSE': 'INFY',
    'ICICIBANK.BSE': 'ICICIBANK',
    'HINDUNILVR.BSE': 'HINDUNILVR',
    'ITC.BSE': 'ITC',
    'SBIN.BSE': 'SBIN',
    'BHARTIARTL.BSE': 'BHARTIARTL',
    'KOTAKBANK.BSE': 'KOTAKBANK',
    'LT.BSE': 'LT',
    'ASIANPAINT.BSE': 'ASIANPAINT',
    'MARUTI.BSE': 'MARUTI',
    'SUNPHARMA.BSE': 'SUNPHARMA',
    'TATAMOTORS.BSE': 'TATAMOTORS',
    'AXISBANK.BSE': 'AXISBANK',
    'NTPC.BSE': 'NTPC',
    'ONGC.BSE': 'ONGC',
    'POWERGRID.BSE': 'POWERGRID',
    'TITAN.BSE': 'TITAN',
    'HCLTECH.BSE': 'HCLTECH',
    'WIPRO.BSE': 'WIPRO',
    'CIPLA.BSE': 'CIPLA',
    'DRREDDY.BSE': 'DRREDDY',
    'DIVISLAB.BSE': 'DIVISLAB',
    'M&M.BSE': 'M&M',
    'BAJAJ-AUTO.BSE': 'BAJAJAUTO',
    'BPCL.BSE': 'BPCL',
    'IOC.BSE': 'IOC',
    'TATASTEEL.BSE': 'TATASTEEL',
    'JSWSTEEL.BSE': 'JSWSTEEL',
    'HINDALCO.BSE': 'HINDALCO',
    'COALINDIA.BSE': 'COALINDIA',
}

# ============================================
# CORE UTILITY FUNCTIONS
# ============================================

def get_status(gffi):
    """Get status based on GFFI value"""
    if gffi >= 70:
        return 'critical'
    elif gffi >= 65:
        return 'warning'
    else:
        return 'success'

def calculate_entropy(returns_series):
    """Calculate Shannon entropy from returns"""
    returns = returns_series.dropna().values
    returns = returns[~np.isinf(returns)]
    returns = returns[~np.isnan(returns)]
    
    if len(returns) < 20:
        return None
    
    bins = min(10, len(returns)//2)
    hist, _ = np.histogram(returns, bins=bins, density=True)
    probs = hist / hist.sum()
    probs = probs[probs > 0]
    
    if len(probs) == 0:
        return None
    
    entropy = -np.sum(probs * np.log(probs))
    max_entropy = np.log(bins)
    if max_entropy > 0:
        entropy = entropy / max_entropy
    
    return entropy

def calculate_capital_proxy(returns_series):
    """Calculate capital proxy from volatility"""
    if len(returns_series) < 30:
        return None
    
    rolling_vol = returns_series.rolling(30).std().dropna()
    if len(rolling_vol) == 0:
        return None
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 20 / (1 + latest_vol)
    return capital_proxy

# ============================================
# ALPHA VANTAGE DATA FETCHING
# ============================================

def fetch_alphavantage_data(symbol, max_retries=2):
    """Fetch data from Alpha Vantage"""
    for attempt in range(max_retries):
        try:
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
                
                return pd.Series(prices, index=dates)
            
            elif 'Note' in data:
                if attempt < max_retries - 1:
                    time.sleep(10)
            else:
                return None
                
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(10)
    
    return None

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
    
    gffi_value = (entropy / capital) * 1000
    gffi_value = round(gffi_value, 1)
    
    # Sanity check
    if gffi_value > 100 or gffi_value < 20:
        return None
    
    return {
        'symbol': symbol.replace('.BSE', ''),
        'name': STOCK_NAMES.get(symbol, symbol.replace('.BSE', '')),
        'gffi': gffi_value,
        'price': round(float(prices.iloc[-1]), 2)
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
    except Exception:
        return None

# ============================================
# COUNTRY GFFI FUNCTIONS
# ============================================

def calculate_country_gffi(country):
    """Calculate GFFI for a single country"""
    print(f"\n📍 Processing {country['name']}...")
    
    prices = fetch_alphavantage_data(country['av_symbol'])
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
    
    gffi_value = (entropy / capital) * 1000
    gffi_value = round(gffi_value, 1)
    
    # Sanity check
    if gffi_value > 100 or gffi_value < 20:
        print(f"   ⚠️ GFFI value {gffi_value} seems abnormal, skipping")
        return None
    
    result = {
        'flag': country['flag'],
        'name': country['name'],
        'gffi': gffi_value,
        'status': get_status(gffi_value)
    }
    
    print(f"   ✅ GFFI: {gffi_value} ({result['status']})")
    return result

# ============================================
# SECTOR DATA FUNCTIONS
# ============================================

def calculate_sector_gffi(sector_name, stocks):
    """Calculate GFFI for a sector"""
    values = []
    valid_stocks = []
    
    for symbol in stocks:
        data = fetch_stock_data(symbol)
        if data:
            values.append(data['gffi'])
            valid_stocks.append(data['symbol'])
        time.sleep(1)
    
    if len(values) < 2:
        return None, None, []
    
    avg_gffi = sum(values) / len(values)
    trend = 'up' if avg_gffi > 62 else 'down' if avg_gffi < 58 else 'stable'
    
    return round(avg_gffi, 1), trend, valid_stocks[:4]

def fetch_live_sector_data():
    """Fetch live data for all sectors"""
    print("\n🏭 Fetching live sector data...")
    sector_data = []
    
    for name, stocks in SECTOR_DEFINITIONS.items():
        gffi, trend, stock_list = calculate_sector_gffi(name, stocks)
        if gffi:
            sector_data.append({
                'name': name,
                'gffi': gffi,
                'trend': trend,
                'stocks': stock_list
            })
            print(f"   ✅ {name}: GFFI={gffi}")
        else:
            print(f"   ❌ {name}: Insufficient data")
        time.sleep(2)
    
    return sector_data

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
        time.sleep(1)
    
    if len(stocks) < 10:
        print("   ❌ Insufficient stock data for reliable picks")
        return {}
    
    stocks.sort(key=lambda x: x['gffi'])
    
    safe_count = min(3, len(stocks) // 3)
    risky_count = min(3, len(stocks) // 3)
    watch_count = min(3, len(stocks) - safe_count - risky_count)
    
    return {
        'safe': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'BUY', 'reason': f'Low GFFI at ₹{s["price"]}'} for s in stocks[:safe_count]],
        'risky': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'SELL', 'reason': f'High GFFI at ₹{s["price"]}'} for s in stocks[-risky_count:][::-1]],
        'watch': [{'symbol': s['symbol'], 'name': s['name'], 'gffi': s['gffi'], 'action': 'WATCH', 'reason': f'Mid GFFI at ₹{s["price"]}'} for s in stocks[safe_count:safe_count+watch_count]]
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
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js"""
    print("\n" + "="*80)
    print("🌍 FETCHING GFFI DATA - ONLY REAL DATA")
    print("="*80)
    
    # Countries
    country_data = []
    gffi_values = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
        time.sleep(12)
    
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else None
    
    # Sectors
    time.sleep(15)
    sector_data = fetch_live_sector_data()
    
    # Stock picks
    time.sleep(15)
    stock_picks = generate_stock_picks()
    
    # India market
    time.sleep(10)
    india_data = fetch_live_india_market_data()
    
    # Generate data.js
    now = datetime.now()
    
    js_lines = [
        "// ============================================",
        "// DATA.JS - Auto-generated by GFFI Live Calculator",
        f"// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "// ============================================",
        "// ONLY REAL DATA - No defaults",
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
    
    print("\n" + "="*80)
    print("✅ DATA.JS UPDATED - ONLY REAL DATA")
    print("="*80)
    print(f"   🌍 Countries with data: {len(country_data)}/{len(COUNTRIES)}")
    print(f"   📊 Global GFFI: {global_gffi if global_gffi else 'None'}")
    print(f"   🏭 Sectors with data: {len(sector_data)}/{len(SECTOR_DEFINITIONS)}")
    print(f"   📈 Stock picks: {'Yes' if stock_picks else 'No'}")
    if india_data:
        print(f"   🇮🇳 Nifty: {india_data.get('nifty')}")
        print(f"   🇮🇳 Sensex: {india_data.get('sensex')}")
    print("="*80)

if __name__ == "__main__":
    main()
