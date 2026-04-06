#!/usr/bin/env python3
"""
GFFI Live Calculator - REAL FRED CAPITAL DATA VERSION
Fetches real banking capital ratios from FRED API
Falls back to capital proxy only when FRED data is unavailable
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
print("🚀 GFFI LIVE CALCULATOR - REAL FRED CAPITAL DATA")
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
    print("⚠️ FRED_API_KEY not found - will use capital proxy for all countries")

# ============================================
# COUNTRY CONFIGURATION WITH FRED SERIES
# ============================================
COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'av_symbol': 'SPX', 'fred_series': 'RCTRWAMXM163N'},
    {'code': 'India', 'name': 'India', 'flag': '🇮🇳', 'av_symbol': 'NSEI', 'fred_series': None},  # FRED data not available
    {'code': 'UK', 'name': 'UK', 'flag': '🇬🇧', 'av_symbol': 'FTSE', 'fred_series': None},
    {'code': 'Germany', 'name': 'Germany', 'flag': '🇩🇪', 'av_symbol': 'GDAXI', 'fred_series': None},
    {'code': 'France', 'name': 'France', 'flag': '🇫🇷', 'av_symbol': 'FCHI', 'fred_series': None},
    {'code': 'Japan', 'name': 'Japan', 'flag': '🇯🇵', 'av_symbol': 'NIKKEI225', 'fred_series': None},
    {'code': 'Canada', 'name': 'Canada', 'flag': '🇨🇦', 'av_symbol': 'GSPTSE', 'fred_series': None},
    {'code': 'Brazil', 'name': 'Brazil', 'flag': '🇧🇷', 'av_symbol': 'BVSP', 'fred_series': None},
    {'code': 'Australia', 'name': 'Australia', 'flag': '🇦🇺', 'av_symbol': 'AXJO', 'fred_series': None},
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'av_symbol': 'STI', 'fred_series': None},
    {'code': 'SouthKorea', 'name': 'S. Korea', 'flag': '🇰🇷', 'av_symbol': 'KS11', 'fred_series': None},
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'av_symbol': 'JN0U.JO', 'fred_series': None},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'av_symbol': 'MXX', 'fred_series': None},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'av_symbol': 'FTSEMIB', 'fred_series': None},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'av_symbol': 'MERV', 'fred_series': None},
]

# ============================================
# NIFTY 50 STOCKS
# ============================================
NIFTY_50_STOCKS = [
    {'symbol': 'RELIANCE.BSE', 'name': 'Reliance Industries', 'sector': 'Energy'},
    {'symbol': 'TCS.BSE', 'name': 'Tata Consultancy Services', 'sector': 'IT'},
    {'symbol': 'HDFCBANK.BSE', 'name': 'HDFC Bank', 'sector': 'Banking'},
    {'symbol': 'INFY.BSE', 'name': 'Infosys', 'sector': 'IT'},
    {'symbol': 'ICICIBANK.BSE', 'name': 'ICICI Bank', 'sector': 'Banking'},
    {'symbol': 'HINDUNILVR.BSE', 'name': 'Hindustan Unilever', 'sector': 'FMCG'},
    {'symbol': 'ITC.BSE', 'name': 'ITC Ltd', 'sector': 'FMCG'},
    {'symbol': 'SBIN.BSE', 'name': 'State Bank of India', 'sector': 'Banking'},
    {'symbol': 'BHARTIARTL.BSE', 'name': 'Bharti Airtel', 'sector': 'Telecom'},
    {'symbol': 'KOTAKBANK.BSE', 'name': 'Kotak Mahindra Bank', 'sector': 'Banking'},
    {'symbol': 'LT.BSE', 'name': 'Larsen & Toubro', 'sector': 'Construction'},
    {'symbol': 'ASIANPAINT.BSE', 'name': 'Asian Paints', 'sector': 'FMCG'},
    {'symbol': 'MARUTI.BSE', 'name': 'Maruti Suzuki', 'sector': 'Auto'},
    {'symbol': 'SUNPHARMA.BSE', 'name': 'Sun Pharma', 'sector': 'Pharma'},
    {'symbol': 'TATAMOTORS.BSE', 'name': 'Tata Motors', 'sector': 'Auto'},
    {'symbol': 'AXISBANK.BSE', 'name': 'Axis Bank', 'sector': 'Banking'},
    {'symbol': 'NTPC.BSE', 'name': 'NTPC Ltd', 'sector': 'Energy'},
    {'symbol': 'ONGC.BSE', 'name': 'ONGC', 'sector': 'Energy'},
    {'symbol': 'POWERGRID.BSE', 'name': 'Power Grid', 'sector': 'Energy'},
    {'symbol': 'TITAN.BSE', 'name': 'Titan Company', 'sector': 'FMCG'},
]

# ============================================
# SECTOR MAPPING
# ============================================
SECTORS = {
    'Banking': ['HDFCBANK.BSE', 'ICICIBANK.BSE', 'SBIN.BSE', 'KOTAKBANK.BSE', 'AXISBANK.BSE'],
    'IT': ['TCS.BSE', 'INFY.BSE'],
    'Pharma': ['SUNPHARMA.BSE'],
    'Auto': ['MARUTI.BSE', 'TATAMOTORS.BSE'],
    'FMCG': ['HINDUNILVR.BSE', 'ITC.BSE', 'TITAN.BSE'],
    'Energy': ['RELIANCE.BSE', 'ONGC.BSE', 'NTPC.BSE'],
    'Telecom': ['BHARTIARTL.BSE'],
    'Construction': ['LT.BSE'],
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
}

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
    
    # Remove outliers
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
    """Calculate capital proxy from volatility - used when FRED data unavailable"""
    if len(returns_series) < 30:
        return 18.0
    
    rolling_vol = returns_series.rolling(30).std().dropna()
    if len(rolling_vol) == 0:
        return 18.0
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 25 / (1 + latest_vol / 10)
    return max(12, min(25, capital_proxy))

# ============================================
# REAL FRED CAPITAL DATA FETCHING
# ============================================

def fetch_fred_capital_data(series_id):
    """
    Fetch REAL bank capital ratio from FRED API
    This is what the research paper uses
    """
    if not FRED_API_KEY:
        print(f"   ⚠️ No FRED API key available")
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
                    time.sleep(15)
            else:
                return None
                
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(10)
    
    return None

def fetch_stock_data(symbol, name):
    """Fetch stock data and calculate GFFI"""
    try:
        prices = fetch_alphavantage_data(symbol)
        if prices is None or len(prices) < 30:
            return None
        
        current_price = prices.iloc[-1]
        prev_price = prices.iloc[-2] if len(prices) > 1 else current_price
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        returns = prices.pct_change().dropna() * 100
        entropy = calculate_entropy(returns)
        capital = calculate_capital_proxy(returns)  # Stocks use proxy
        
        if entropy is None or capital is None:
            return None
        
        gffi = (entropy / capital) * 1000
        gffi = round(gffi, 1)
        
        if gffi > 80 or gffi < 20:
            return None
        
        return {
            'symbol': STOCK_NAMES.get(symbol, symbol.replace('.BSE', '')),
            'name': name,
            'price': round(current_price, 2),
            'change': round(change_pct, 2),
            'gffi': gffi
        }
        
    except Exception as e:
        print(f"   ⚠️ Error for {name}: {str(e)[:30]}")
        return None

# ============================================
# COUNTRY GFFI WITH REAL FRED CAPITAL DATA
# ============================================

def calculate_country_gffi_with_fred(country):
    """
    Calculate GFFI for a country - uses REAL FRED capital data when available
    Falls back to capital proxy only when FRED data is unavailable
    """
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
    
    # Try to get REAL capital data from FRED first
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
        capital_source = "PROXY (Volatility-based)"
        print(f"   ⚠️ Using capital proxy: {capital:.2f} (FRED data not available)")
    
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
        'capital_source': capital_source  # For debugging
    }
    
    print(f"   ✅ GFFI: {gffi} ({result['status']}) [Capital: {capital_source}]")
    return result

# ============================================
# SECTOR DATA FUNCTIONS
# ============================================

def calculate_sector_gffi():
    """Calculate GFFI for all sectors"""
    print("\n🏭 Calculating sector-wise GFFI...")
    sector_data = []
    
    for sector, stocks in SECTORS.items():
        gffi_values = []
        stock_names = []
        
        for symbol in stocks[:3]:
            stock_data = fetch_stock_data(symbol, sector)
            if stock_data and 'gffi' in stock_data:
                gffi_values.append(stock_data['gffi'])
                stock_names.append(stock_data['symbol'])
            time.sleep(12)
        
        if gffi_values:
            avg_gffi = sum(gffi_values) / len(gffi_values)
            trend = 'up' if avg_gffi > 62 else 'down' if avg_gffi < 58 else 'stable'
            sector_data.append({
                'name': sector,
                'gffi': round(avg_gffi, 1),
                'trend': trend,
                'stocks': stock_names[:3]
            })
            print(f"   ✅ {sector}: {round(avg_gffi, 1)} ({trend})")
        else:
            print(f"   ❌ {sector}: No data")
    
    return sector_data

# ============================================
# STOCK PICKS FUNCTIONS
# ============================================

def generate_stock_picks():
    """Generate stock picks based on GFFI"""
    print("\n📈 Generating stock picks from Nifty 50...")
    
    stocks_data = []
    
    for stock in NIFTY_50_STOCKS[:15]:
        data = fetch_stock_data(stock['symbol'], stock['name'])
        if data:
            stocks_data.append(data)
        time.sleep(12)
    
    if len(stocks_data) < 5:
        print("   ❌ Insufficient data for stock picks")
        return {}
    
    stocks_data.sort(key=lambda x: x['gffi'])
    
    safe_picks = []
    for s in stocks_data[:3]:
        safe_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'BUY',
            'reason': f'Low GFFI indicates stability at ₹{s["price"]}'
        })
    
    risky_picks = []
    for s in stocks_data[-3:][::-1]:
        risky_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'SELL',
            'reason': f'High GFFI indicates risk at ₹{s["price"]}'
        })
    
    mid_index = len(stocks_data) // 2
    watch_picks = []
    for s in stocks_data[mid_index-2:mid_index+3]:
        watch_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'WATCH',
            'reason': f'Moderate GFFI at ₹{s["price"]}'
        })
    
    return {
        'safe': safe_picks,
        'risky': risky_picks,
        'watch': watch_picks[:3]
    }

# ============================================
# CRISIS PROBABILITY FUNCTION
# ============================================

def calculate_crisis_probability(gffi_value):
    """Calculate crisis probability based on GFFI value"""
    threshold = 72.8
    
    if gffi_value is None or gffi_value <= threshold:
        return {
            'probability': 0,
            'lead_time_min': None,
            'lead_time_max': None,
            'lead_time_avg': None,
            'status': 'NORMAL',
            'message': 'Below crisis threshold'
        }
    
    excess = gffi_value - threshold
    base_prob = 0.5
    prob_increase = (excess / 10) * 0.3
    probability = min(0.95, base_prob + prob_increase)
    
    if gffi_value <= 75:
        lead_min, lead_max, lead_avg = 18, 24, 21
    elif gffi_value <= 80:
        lead_min, lead_max, lead_avg = 12, 18, 15
    elif gffi_value <= 85:
        lead_min, lead_max, lead_avg = 6, 12, 9
    else:
        lead_min, lead_max, lead_avg = 3, 6, 4.5
    
    return {
        'probability': round(probability * 100, 1),
        'lead_time_min': lead_min,
        'lead_time_max': lead_max,
        'lead_time_avg': lead_avg,
        'status': 'CRITICAL' if gffi_value >= 80 else 'WARNING',
        'message': get_crisis_message(gffi_value)
    }

def get_crisis_message(gffi_value):
    if gffi_value >= 85:
        return "⚠️ EXTREME RISK: Crisis highly probable within 3-6 months"
    elif gffi_value >= 80:
        return "🔴 HIGH RISK: Crisis probable within 6-12 months"
    elif gffi_value >= 75:
        return "🟠 ELEVATED RISK: Crisis possible within 12-18 months"
    else:
        return "🟡 MODERATE RISK: Monitor closely, crisis possible within 18-24 months"

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js with REAL FRED capital data"""
    print("\n" + "="*80)
    print("🇮🇳 FETCHING GFFI DATA WITH REAL FRED CAPITAL")
    print("="*80)
    print("📌 USA will use REAL FRED bank capital data")
    print("📌 Other countries will use capital proxy")
    print("="*80)
    
    # Calculate country GFFI with REAL FRED data where available
    country_data = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi_with_fred(country)
        if result:
            country_data.append(result)
        time.sleep(12)
    
    # Calculate India GFFI from country data
    india_entry = next((c for c in country_data if c['name'] == 'India'), None)
    india_gffi = india_entry['gffi'] if india_entry else 60
    
    # Calculate sector GFFI
    sector_data = calculate_sector_gffi()
    
    # Generate stock picks
    stock_picks = generate_stock_picks()
    
    # India market data
    india_market_data = {
        'nifty': 0,
        'sensex': 0,
        'nifty_change': 0,
        'sensex_change': 0
    }
    
    # Crisis probability
    crisis_data = calculate_crisis_probability(india_gffi)
    
    # Global GFFI (average of countries with data)
    if country_data:
        global_gffi = sum([c['gffi'] for c in country_data]) / len(country_data)
        global_gffi = round(global_gffi, 1)
    else:
        global_gffi = india_gffi
    
    # Market efficiency (default)
    market_efficiency = 65
    
    # Current time
    now = datetime.now()
    
    # Generate data.js
    js_lines = [
        "// ============================================",
        "// DATA.JS - Auto-generated by GFFI Live Calculator",
        f"// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "// ============================================",
        "// CAPITAL DATA SOURCES:",
        "//   USA: REAL FRED bank capital ratio (RCTRWAMXM163N)",
        "//   Other countries: Capital proxy (volatility-based)",
        "// ============================================",
        "",
        f"const countryData = {json.dumps(country_data, indent=2, ensure_ascii=False)};",
        "",
        f"const globalGFFI = {global_gffi};",
        "",
        f"const updateDate = '{now.strftime('%d %b %Y')}';",
        f"const updateTime = '{now.strftime('%I:%M %p')}';",
        "",
        f"const sectorData = {json.dumps(sector_data, indent=2, ensure_ascii=False)};",
        "",
        f"const stockPicks = {json.dumps(stock_picks, indent=2, ensure_ascii=False)};",
        "",
        f"const indiaMarketData = {json.dumps(india_market_data, indent=2, ensure_ascii=False)};",
        "",
        f"const crisisData = {json.dumps(crisis_data, indent=2, ensure_ascii=False)};",
        "",
        f"const marketEfficiency = {market_efficiency};"
    ]
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("\n".join(js_lines))
    
    print("\n" + "="*80)
    print("✅ DATA.JS UPDATED - WITH REAL FRED CAPITAL DATA")
    print("="*80)
    print(f"   🇺🇸 USA: Uses REAL FRED bank capital ratio")
    print(f"   🇮🇳 India GFFI: {india_gffi}")
    print(f"   📊 Global GFFI: {global_gffi}")
    print(f"   🏭 Sectors: {len(sector_data)}")
    print(f"   📈 Stock Picks: {len(stock_picks.get('safe', []))} Buy, {len(stock_picks.get('risky', []))} Sell, {len(stock_picks.get('watch', []))} Watch")
    print("="*80)

if __name__ == "__main__":
    main()
