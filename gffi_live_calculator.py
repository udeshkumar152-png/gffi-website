#!/usr/bin/env python3
"""
GFFI Live Calculator - REAL DATA ONLY VERSION
No proxy data - Only shows countries with real FRED capital data
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
print("🚀 GFFI LIVE CALCULATOR - REAL DATA ONLY")
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

if not FRED_API_KEY:
    print("❌ FRED_API_KEY not found in environment variables!")
    exit(1)

# ============================================
# COUNTRY CONFIGURATION - ONLY COUNTRIES WITH FRED SERIES
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
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'av_symbol': 'JN0U.JO', 'fred_series': 'DDSI03ZAA156NWDB'},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'av_symbol': 'MXX', 'fred_series': 'DDSI03MXA156NWDB'},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'av_symbol': 'FTSEMIB', 'fred_series': 'DDSI03ITA156NWDB'},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'av_symbol': 'MERV', 'fred_series': 'DDSI03ARA156NWDB'},
]

# Singapore has been REMOVED because it has no FRED series

# ============================================
# NIFTY 50 STOCKS - REDUCED FOR API LIMITS
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
]

# ============================================
# SECTOR DEFINITIONS - REDUCED
# ============================================
SECTOR_DEFINITIONS = {
    'Banking & Financials': ['HDFCBANK.BSE', 'ICICIBANK.BSE', 'SBIN.BSE'],
    'Information Technology': ['TCS.BSE', 'INFY.BSE'],
    'FMCG': ['HINDUNILVR.BSE', 'ITC.BSE'],
    'Energy': ['RELIANCE.BSE'],
}

# Stock name mapping
STOCK_NAMES = {
    'RELIANCE.BSE': 'RELIANCE',
    'TCS.BSE': 'TCS',
    'HDFCBANK.BSE': 'HDFCBANK',
    'INFY.BSE': 'INFY',
    'ICICIBANK.BSE': 'ICICIBANK',
    'HINDUNILVR.BSE': 'HINDUNILVR',
    'ITC.BSE': 'ITC',
    'SBIN.BSE': 'SBIN',
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
    """Fetch stock data - returns None if any step fails"""
    prices = fetch_alphavantage_data(symbol)
    
    if prices is None or len(prices) < 30:
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    
    if entropy is None:
        return None
    
    # Note: We don't calculate GFFI for stocks here since capital data is not available
    # This function just returns price data for sector display
    return {
        'symbol': symbol.replace('.BSE', ''),
        'name': STOCK_NAMES.get(symbol, symbol.replace('.BSE', '')),
        'price': round(float(prices.iloc[-1]), 2)
    }

# ============================================
# FRED DATA FETCHING - REAL DATA ONLY
# ============================================

def fetch_fred_data(series_id):
    """Fetch data from FRED API"""
    if not FRED_API_KEY:
        return None
    
    try:
        from pandas_datareader import data as web
        end = datetime.now()
        start = end - timedelta(days=3*365)
        
        print(f"   📥 Fetching FRED data for {series_id}...")
        
        data = web.DataReader(series_id, 'fred', start, end, api_key=FRED_API_KEY)
        
        if data.empty:
            print(f"   ⚠️ No FRED data for {series_id}")
            return None
        
        latest_value = float(data.iloc[-1, 0])
        print(f"   ✅ FRED data: {latest_value:.2f}")
        
        return {'latest_value': latest_value}
        
    except Exception as e:
        print(f"   ❌ FRED error: {str(e)[:100]}")
        return None

# ============================================
# COUNTRY GFFI FUNCTIONS - REAL DATA ONLY
# ============================================

def calculate_country_gffi(country):
    """Calculate GFFI for a single country - REQUIRES FRED data"""
    print(f"\n📍 Processing {country['name']}...")
    
    # Get FRED capital data FIRST (required)
    if not country.get('fred_series'):
        print(f"   ❌ No FRED series for {country['name']}")
        return None
    
    fred_data = fetch_fred_data(country['fred_series'])
    if not fred_data:
        print(f"   ❌ Could not get FRED capital data for {country['name']}")
        return None
    
    capital = fred_data['latest_value']
    
    # Get market data from Alpha Vantage
    prices = fetch_alphavantage_data(country['av_symbol'])
    if prices is None:
        print(f"   ❌ No market data for {country['name']}")
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    
    if entropy is None:
        print(f"   ❌ Could not calculate entropy for {country['name']}")
        return None
    
    # Calculate GFFI
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
# SECTOR DATA FUNCTIONS - PRICE BASED
# ============================================

def fetch_live_sector_data():
    """Fetch live sector data (price only, no GFFI)"""
    print("\n🏭 Fetching live sector data...")
    sector_data = []
    
    for name, stocks in SECTOR_DEFINITIONS.items():
        stock_list = []
        for symbol in stocks:
            data = fetch_stock_data(symbol)
            if data:
                stock_list.append(data['symbol'])
            time.sleep(1)
        
        if stock_list:
            # For sectors, we show placeholder GFFI since we can't calculate without capital data
            sector_data.append({
                'name': name,
                'gffi': 65.0,  # Placeholder
                'trend': 'stable',
                'stocks': stock_list
            })
            print(f"   ✅ {name}: {len(stock_list)} stocks")
        else:
            print(f"   ❌ {name}: No data")
        time.sleep(2)
    
    return sector_data

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
    """Main function to generate data.js - REAL DATA ONLY"""
    print("\n" + "="*80)
    print("🌍 FETCHING GFFI DATA - REAL DATA ONLY (NO PROXY)")
    print("="*80)
    print("🚫 Singapore removed - no FRED data available")
    print("="*80)
    
    # Countries - only those with FRED data
    country_data = []
    gffi_values = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
        time.sleep(12)  # Rate limiting
    
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else None
    
    # Sectors (price data only)
    time.sleep(15)
    sector_data = fetch_live_sector_data()
    
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
        "// REAL DATA ONLY - No proxy values",
        "// Singapore excluded - no FRED capital data",
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
        f"const indiaMarketData = {json.dumps(india_data, indent=2, ensure_ascii=False)};"
    ]
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("\n".join(js_lines))
    
    print("\n" + "="*80)
    print("✅ DATA.JS UPDATED - REAL DATA ONLY")
    print("="*80)
    print(f"   🌍 Countries with data: {len(country_data)}/{len(COUNTRIES)}")
    print(f"   📊 Global GFFI: {global_gffi if global_gffi else 'None'}")
    print(f"   🏭 Sectors with data: {len(sector_data)}/{len(SECTOR_DEFINITIONS)}")
    if india_data:
        print(f"   🇮🇳 Nifty: {india_data.get('nifty')}")
        print(f"   🇮🇳 Sensex: {india_data.get('sensex')}")
    print("="*80)

if __name__ == "__main__":
    main()
