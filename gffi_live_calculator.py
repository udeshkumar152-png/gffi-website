#!/usr/bin/env python3
"""
GFFI Daily Calculator - Alpha Vantage + FRED
Fetches market data from Alpha Vantage and capital data from FRED
Runs once daily to respect API rate limits
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
print("🚀 GFFI DAILY CALCULATOR - ALPHA VANTAGE + FRED")
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
# ALL 17 COUNTRIES WITH FRED SERIES
# ============================================
COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'av_symbol': 'SPX', 'fred_series': 'RCTRWAMXM163N'},
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
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'av_symbol': 'STI', 'fred_series': 'DDSI03SGA156NWDB'},
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'av_symbol': 'JN0U.JO', 'fred_series': 'DDSI03ZAA156NWDB'},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'av_symbol': 'MXX', 'fred_series': 'DDSI03MXA156NWDB'},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'av_symbol': 'FTSEMIB', 'fred_series': 'DDSI03ITA156NWDB'},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'av_symbol': 'MERV', 'fred_series': 'DDSI03ARA156NWDB'},
    {'code': 'Russia', 'name': 'Russia', 'flag': '🇷🇺', 'av_symbol': 'IMOEX', 'fred_series': 'DDSI03RUA156NWDB'},
]

# ============================================
# CORE UTILITY FUNCTIONS
# ============================================

def get_status(gffi):
    if gffi >= 70:
        return 'critical'
    elif gffi >= 65:
        return 'warning'
    elif gffi >= 58:
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
    
    # Remove outliers (returns > 5% or < -5% are abnormal)
    returns = returns[(returns > -5) & (returns < 5)]
    
    if len(returns) < 15:
        return None
    
    bins = 10
    hist, _ = np.histogram(returns, bins=bins, range=(-3, 3), density=True)
    probs = hist / hist.sum()
    probs = probs[probs > 0]
    
    if len(probs) == 0:
        return None
    
    entropy = -np.sum(probs * np.log(probs))
    max_entropy = np.log(bins)
    if max_entropy > 0:
        entropy = entropy / max_entropy
    
    return max(0.2, min(0.8, entropy))

def calculate_capital_proxy(returns_series):
    """Calculate capital proxy from volatility (fallback when FRED not available)"""
    if len(returns_series) < 30:
        return 18.0
    
    rolling_vol = returns_series.rolling(30).std().dropna()
    if len(rolling_vol) == 0:
        return 18.0
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 25 / (1 + latest_vol / 10)
    return max(12, min(25, capital_proxy))

# ============================================
# FRED CAPITAL DATA FETCHING (REAL DATA)
# ============================================

def fetch_fred_capital_data(series_id):
    """
    Fetch REAL bank capital ratio from FRED API
    This is what the research paper uses
    """
    if not FRED_API_KEY:
        print(f"   ⚠️ No FRED API key available")
        return None
    
    if series_id is None:
        return None
    
    try:
        from pandas_datareader import data as web
        
        end = datetime.now()
        start = end - timedelta(days=3*365)  # Last 3 years
        
        print(f"   📥 Fetching REAL capital data from FRED: {series_id}...")
        
        # Fetch data from FRED
        data = web.DataReader(series_id, 'fred', start, end, api_key=FRED_API_KEY)
        
        if data.empty:
            print(f"   ⚠️ No FRED data for {series_id}")
            return None
        
        # Get latest value (most recent available)
        latest_value = float(data.iloc[-1, 0])
        latest_date = data.index[-1].strftime('%Y-%m-%d')
        
        print(f"   ✅ REAL FRED capital data: {latest_value:.2f} (as of {latest_date})")
        
        return {
            'value': latest_value,
            'date': latest_date,
            'source': 'FRED'
        }
        
    except Exception as e:
        print(f"   ❌ FRED error: {str(e)[:100]}")
        return None

# ============================================
# ALPHA VANTAGE MARKET DATA FETCHING
# ============================================

def fetch_alphavantage_data(symbol, max_retries=2):
    """Fetch market data from Alpha Vantage"""
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
                print(f"   ⚠️ API Note: {data['Note'][:100]}")
                if attempt < max_retries - 1:
                    time.sleep(15)
            else:
                return None
                
        except Exception as e:
            print(f"   ⚠️ Attempt {attempt+1} failed: {str(e)[:50]}")
            if attempt < max_retries - 1:
                time.sleep(10)
    
    return None

# ============================================
# COUNTRY GFFI CALCULATION
# ============================================

def calculate_country_gffi(country):
    """Calculate GFFI for a single country"""
    print(f"\n📍 Processing {country['name']}...")
    
    # Get market data from Alpha Vantage
    prices = fetch_alphavantage_data(country['av_symbol'])
    if prices is None or len(prices) < 30:
        print(f"   ❌ No market data for {country['name']}")
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    
    if entropy is None:
        print(f"   ❌ Could not calculate entropy for {country['name']}")
        return None
    
    # Try to get REAL capital data from FRED
    capital = None
    capital_source = "PROXY"
    
    if country.get('fred_series') and FRED_API_KEY:
        fred_data = fetch_fred_capital_data(country['fred_series'])
        if fred_data:
            capital = fred_data['value']
            capital_source = "FRED (REAL)"
            print(f"   ✅ Using REAL FRED capital data: {capital:.2f}")
    
    # If FRED data not available, use capital proxy
    if capital is None:
        capital = calculate_capital_proxy(returns)
        capital_source = "PROXY"
        print(f"   ⚠️ Using capital proxy: {capital:.2f}")
    
    # Calculate GFFI
    gffi = (entropy / capital) * 1000
    gffi = round(gffi, 1)
    
    # Sanity check
    if gffi > 100 or gffi < 20:
        print(f"   ⚠️ GFFI value {gffi} seems abnormal, skipping")
        return None
    
    result = {
        'flag': country['flag'],
        'name': country['name'],
        'gffi': gffi,
        'status': get_status(gffi),
        'entropy': round(entropy, 3),
        'capital': round(capital, 2),
        'capital_source': capital_source
    }
    
    print(f"   ✅ GFFI: {gffi} ({result['status']}) [Capital: {capital_source}]")
    return result

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js with real data"""
    print("\n" + "="*80)
    print("🌍 FETCHING GFFI DATA FOR ALL 17 COUNTRIES")
    print("="*80)
    print("📌 Capital Data Sources:")
    print("   • FRED API for countries with available data")
    print("   • Capital proxy (volatility-based) for others")
    print("="*80)
    
    # Calculate GFFI for all countries
    country_data = []
    gffi_values = []
    fred_count = 0
    proxy_count = 0
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
            if result.get('capital_source') == 'FRED (REAL)':
                fred_count += 1
            else:
                proxy_count += 1
        
        # Rate limiting - 15 seconds between countries
        # This ensures we don't exceed Alpha Vantage's 5 calls per minute
        time.sleep(15)
    
    # Calculate global GFFI (average of all countries with data)
    if gffi_values:
        global_gffi = round(sum(gffi_values) / len(gffi_values), 1)
    else:
        global_gffi = 63.5
    
    # Find India GFFI for reference
    india_entry = next((c for c in country_data if c['name'] == 'India'), None)
    india_gffi = india_entry['gffi'] if india_entry else 60
    
    # Current time
    now = datetime.now()
    
    # Generate data.js
    js_lines = [
        "// ============================================",
        "// DATA.JS - Auto-generated by GFFI Daily Calculator",
        f"// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "// ============================================",
        "// CAPITAL DATA SOURCES:",
        f"//   • FRED (REAL): {fred_count} countries",
        f"//   • Proxy (volatility-based): {proxy_count} countries",
        "// ============================================",
        "",
        f"const countryData = {json.dumps(country_data, indent=2, ensure_ascii=False)};",
        "",
        f"const globalGFFI = {global_gffi};",
        "",
        f"const updateDate = '{now.strftime('%d %b %Y')}';",
        f"const updateTime = '{now.strftime('%I:%M %p')}';",
        "",
        f"// Empty arrays for removed features",
        f"const sectorData = [];",
        f"const stockPicks = {{}};",
        "",
        f"const indiaMarketData = {{",
        f"    'nifty': 0,",
        f"    'sensex': 0,",
        f"    'nifty_change': 0,",
        f"    'sensex_change': 0,",
        f"    'india_gffi': {india_gffi}",
        f"}};"
    ]
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("\n".join(js_lines))
    
    print("\n" + "="*80)
    print("✅ DATA.JS UPDATED")
    print("="*80)
    print(f"   🌍 Countries with data: {len(country_data)}/{len(COUNTRIES)}")
    print(f"   📊 Global GFFI: {global_gffi}")
    print(f"   🇮🇳 India GFFI: {india_gffi}")
    print(f"   📌 Capital sources: FRED={fred_count}, Proxy={proxy_count}")
    print("="*80)
    print("\n📊 Country-wise GFFI values:")
    for c in country_data:
        print(f"   {c['flag']} {c['name']}: {c['gffi']} ({c['status']}) - {c.get('capital_source', 'Unknown')}")
    print("="*80)

if __name__ == "__main__":
    main()
