#!/usr/bin/env python3
"""
GFFI Live Calculator - INDIA MARKET ONLY (Alpha Vantage)
Fetches live data from Alpha Vantage for Indian market
Works reliably on GitHub Actions
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
print("🚀 GFFI LIVE CALCULATOR - INDIA MARKET (Alpha Vantage)")
print("="*80)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# CONFIGURATION
# ============================================
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY')

if not ALPHA_VANTAGE_KEY:
    print("❌ ALPHA_VANTAGE_KEY not found in environment variables!")
    exit(1)

# ============================================
# INDIAN MARKET SYMBOLS (Alpha Vantage)
# ============================================
NIFTY_SYMBOL = "NSEI"
SENSEX_SYMBOL = "BSESN"

# ============================================
# NIFTY 50 STOCKS (Alpha Vantage symbols)
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
# SECTOR MAPPING (with Alpha Vantage symbols)
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
        return 15.0
    
    rolling_vol = returns_series.rolling(30).std().dropna()
    if len(rolling_vol) == 0:
        return 15.0
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 20 / (1 + latest_vol)
    return max(10, min(30, capital_proxy))

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
                    wait_time = 15
                    print(f"   ⏳ Rate limit, waiting {wait_time}s...")
                    time.sleep(wait_time)
            else:
                return None
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(10)
    
    return None

def fetch_index_data(symbol, name):
    """Fetch index data and calculate GFFI"""
    print(f"\n📍 Fetching {name} data...")
    
    prices = fetch_alphavantage_data(symbol)
    if prices is None or len(prices) < 30:
        print(f"   ❌ No historical data for {name}")
        return None, None
    
    # Get latest price and change
    current_price = prices.iloc[-1]
    prev_price = prices.iloc[-2] if len(prices) > 1 else current_price
    change_pct = ((current_price - prev_price) / prev_price) * 100
    
    # Calculate GFFI
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    capital = calculate_capital_proxy(returns)
    
    if entropy is None:
        print(f"   ❌ Could not calculate entropy for {name}")
        return None, None
    
    gffi = (entropy / capital) * 1000
    gffi = round(gffi, 1)
    
    # Sanity check
    if gffi > 100 or gffi < 20:
        print(f"   ⚠️ Abnormal GFFI {gffi} for {name}")
        return None, None
    
    print(f"   ✅ {name}: {current_price:.0f} ({change_pct:.2f}%), GFFI={gffi}")
    return {
        'value': float(current_price),
        'change': round(change_pct, 2),
        'gffi': gffi
    }, None

def fetch_stock_data(symbol, name):
    """Fetch stock data and calculate GFFI"""
    try:
        prices = fetch_alphavantage_data(symbol)
        if prices is None or len(prices) < 30:
            return None
        
        # Get latest price
        current_price = prices.iloc[-1]
        prev_price = prices.iloc[-2] if len(prices) > 1 else current_price
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        # Calculate GFFI
        returns = prices.pct_change().dropna() * 100
        entropy = calculate_entropy(returns)
        capital = calculate_capital_proxy(returns)
        
        if entropy is None:
            return None
        
        gffi = (entropy / capital) * 1000
        gffi = round(gffi, 1)
        
        # Sanity check
        if gffi > 100 or gffi < 20:
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
            time.sleep(12)  # Rate limiting
        
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
    
    for stock in NIFTY_50_STOCKS[:15]:  # Limit to 15 for API limits
        data = fetch_stock_data(stock['symbol'], stock['name'])
        if data:
            stocks_data.append(data)
        time.sleep(12)  # Rate limiting
    
    if len(stocks_data) < 5:
        print("   ❌ Insufficient data for stock picks")
        return {}
    
    # Sort by GFFI
    stocks_data.sort(key=lambda x: x['gffi'])
    
    # Safe picks (lowest GFFI)
    safe_picks = []
    for s in stocks_data[:3]:
        safe_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'BUY',
            'reason': f'Low GFFI indicates stability at ₹{s["price"]}'
        })
    
    # Risky picks (highest GFFI)
    risky_picks = []
    for s in stocks_data[-3:][::-1]:
        risky_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'SELL',
            'reason': f'High GFFI indicates risk at ₹{s["price"]}'
        })
    
    # Watchlist (middle range)
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
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js"""
    print("\n" + "="*80)
    print("🇮🇳 FETCHING INDIA MARKET DATA (Alpha Vantage)")
    print("="*80)
    
    # Fetch Nifty data
    nifty_result, _ = fetch_index_data(NIFTY_SYMBOL, "Nifty 50")
    
    # Fetch Sensex data
    sensex_result, _ = fetch_index_data(SENSEX_SYMBOL, "Sensex")
    
    # Prepare India market data
    india_market_data = {
        'nifty': int(nifty_result['value']) if nifty_result else 0,
        'sensex': int(sensex_result['value']) if sensex_result else 0,
        'nifty_change': nifty_result['change'] if nifty_result else 0,
        'sensex_change': sensex_result['change'] if sensex_result else 0,
        'nifty_gffi': nifty_result['gffi'] if nifty_result else None,
        'sensex_gffi': sensex_result['gffi'] if sensex_result else None
    }
    
    # Country data (India only)
    country_data = []
    if nifty_result and nifty_result.get('gffi'):
        country_data.append({
            'flag': '🇮🇳',
            'name': 'India',
            'gffi': nifty_result['gffi'],
            'status': get_status(nifty_result['gffi'])
        })
    
    # Sector data
    sector_data = calculate_sector_gffi()
    
    # Stock picks
    stock_picks = generate_stock_picks()
    
    # Global GFFI (using India GFFI)
    global_gffi = nifty_result['gffi'] if nifty_result else 63.5
    
    # Current time
    now = datetime.now()
    
    # Generate data.js
    js_lines = [
        "// ============================================",
        "// DATA.JS - Auto-generated by GFFI Live Calculator",
        f"// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "// ============================================",
        "// INDIA MARKET DATA - Live from Alpha Vantage",
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
        f"const indiaMarketData = {json.dumps(india_market_data, indent=2, ensure_ascii=False)};"
    ]
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write("\n".join(js_lines))
    
    print("\n" + "="*80)
    print("✅ DATA.JS UPDATED - INDIA MARKET")
    print("="*80)
    print(f"   🇮🇳 Nifty: {india_market_data['nifty']} ({india_market_data['nifty_change']}%)")
    print(f"   🇮🇳 Nifty GFFI: {india_market_data.get('nifty_gffi', 'None')}")
    print(f"   🏭 Sectors: {len(sector_data)}")
    print(f"   📈 Stock Picks: {len(stock_picks.get('safe', []))} Buy, {len(stock_picks.get('risky', []))} Sell, {len(stock_picks.get('watch', []))} Watch")
    print("="*80)

if __name__ == "__main__":
    main()
