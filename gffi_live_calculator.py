#!/usr/bin/env python3
"""
GFFI Live Calculator - INDIA MARKET ONLY
Uses niftyterminal for live NSE data - No API keys required
"""

import os
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🚀 GFFI LIVE CALCULATOR - INDIA MARKET ONLY")
print("="*80)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# TRY TO IMPORT NIFTYTERMINAL
# ============================================
try:
    from niftyterminal import get_all_index_quote, get_index_stocks, get_stock_quote, get_historical_data
    NIFTYTERMINAL_AVAILABLE = True
    print("✅ niftyterminal loaded successfully")
except ImportError:
    print("❌ niftyterminal not installed! Run: pip install niftyterminal")
    NIFTYTERMINAL_AVAILABLE = False
    exit(1)

# ============================================
# NIFTY 50 STOCKS - FIXED LIST AS BACKUP
# ============================================
NIFTY_50_BACKUP = [
    {'symbol': 'RELIANCE', 'name': 'Reliance Industries', 'sector': 'Energy'},
    {'symbol': 'TCS', 'name': 'Tata Consultancy Services', 'sector': 'IT'},
    {'symbol': 'HDFCBANK', 'name': 'HDFC Bank', 'sector': 'Banking'},
    {'symbol': 'INFY', 'name': 'Infosys', 'sector': 'IT'},
    {'symbol': 'ICICIBANK', 'name': 'ICICI Bank', 'sector': 'Banking'},
    {'symbol': 'HINDUNILVR', 'name': 'Hindustan Unilever', 'sector': 'FMCG'},
    {'symbol': 'ITC', 'name': 'ITC Ltd', 'sector': 'FMCG'},
    {'symbol': 'SBIN', 'name': 'State Bank of India', 'sector': 'Banking'},
    {'symbol': 'BHARTIARTL', 'name': 'Bharti Airtel', 'sector': 'Telecom'},
    {'symbol': 'KOTAKBANK', 'name': 'Kotak Mahindra Bank', 'sector': 'Banking'},
    {'symbol': 'LT', 'name': 'Larsen & Toubro', 'sector': 'Construction'},
    {'symbol': 'ASIANPAINT', 'name': 'Asian Paints', 'sector': 'FMCG'},
    {'symbol': 'MARUTI', 'name': 'Maruti Suzuki', 'sector': 'Auto'},
    {'symbol': 'SUNPHARMA', 'name': 'Sun Pharma', 'sector': 'Pharma'},
    {'symbol': 'TATAMOTORS', 'name': 'Tata Motors', 'sector': 'Auto'},
    {'symbol': 'AXISBANK', 'name': 'Axis Bank', 'sector': 'Banking'},
    {'symbol': 'NTPC', 'name': 'NTPC Ltd', 'sector': 'Energy'},
    {'symbol': 'ONGC', 'name': 'ONGC', 'sector': 'Energy'},
    {'symbol': 'POWERGRID', 'name': 'Power Grid', 'sector': 'Energy'},
    {'symbol': 'TITAN', 'name': 'Titan Company', 'sector': 'FMCG'},
]

# ============================================
# SECTOR MAPPING
# ============================================
SECTORS = {
    'Banking': ['HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK', 'INDUSINDBK'],
    'IT': ['TCS', 'INFY', 'HCLTECH', 'WIPRO', 'TECHM'],
    'Pharma': ['SUNPHARMA', 'CIPLA', 'DRREDDY', 'DIVISLAB', 'APOLLOHOSP'],
    'Auto': ['MARUTI', 'TATAMOTORS', 'M&M', 'BAJAJ-AUTO', 'HEROMOTOCO'],
    'FMCG': ['HINDUNILVR', 'ITC', 'BRITANNIA', 'NESTLEIND', 'TITAN'],
    'Energy': ['RELIANCE', 'ONGC', 'BPCL', 'IOC', 'NTPC', 'POWERGRID', 'COALINDIA'],
    'Metals': ['TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'COALINDIA'],
    'Telecom': ['BHARTIARTL', 'RELIANCE'],
    'Construction': ['LT', 'GRASIM', 'ULTRACEMCO'],
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
# DATA FETCHING FROM NIFTYTERMINAL
# ============================================

def fetch_nifty_index():
    """Fetch live Nifty index data"""
    try:
        data = get_all_index_quote()
        if data and 'indexQuote' in data:
            for idx in data['indexQuote']:
                if idx.get('indexName') == 'NIFTY 50':
                    return {
                        'value': float(idx.get('ltp', 0)),
                        'change': float(idx.get('percentChange', 0))
                    }
        return None
    except Exception as e:
        print(f"   ⚠️ Nifty fetch error: {str(e)[:50]}")
        return None

def fetch_sensex():
    """Fetch live Sensex data"""
    try:
        data = get_all_index_quote()
        if data and 'indexQuote' in data:
            for idx in data['indexQuote']:
                if idx.get('indexName') == 'SENSEX':
                    return {
                        'value': float(idx.get('ltp', 0)),
                        'change': float(idx.get('percentChange', 0))
                    }
        return None
    except Exception as e:
        print(f"   ⚠️ Sensex fetch error: {str(e)[:50]}")
        return None

def fetch_stock_data(symbol):
    """Fetch stock data and calculate GFFI"""
    try:
        # Get live quote
        quote = get_stock_quote(symbol)
        if not quote or 'ltp' not in quote:
            return None
        
        # Get historical data for entropy calculation
        hist_data = get_historical_data(symbol)
        if not hist_data or len(hist_data) < 30:
            return None
        
        # Calculate returns from historical data
        prices = pd.Series([float(d['close']) for d in hist_data])
        returns = prices.pct_change().dropna() * 100
        
        entropy = calculate_entropy(returns)
        capital = calculate_capital_proxy(returns)
        
        if entropy is None:
            return None
        
        gffi_value = (entropy / capital) * 1000
        gffi_value = round(gffi_value, 1)
        
        # Sanity check
        if gffi_value > 100 or gffi_value < 20:
            return None
        
        return {
            'symbol': symbol,
            'name': quote.get('companyName', symbol),
            'sector': quote.get('sector', 'General'),
            'price': float(quote.get('ltp', 0)),
            'gffi': gffi_value,
            'change': float(quote.get('percentChange', 0))
        }
        
    except Exception as e:
        print(f"   ⚠️ Stock fetch error for {symbol}: {str(e)[:30]}")
        return None

def fetch_stock_list():
    """Fetch Nifty 50 stock list"""
    try:
        data = get_index_stocks("NIFTY 50")
        if data and 'stockList' in data:
            return [{'symbol': s['symbol'], 'name': s['companyName']} for s in data['stockList']]
    except:
        pass
    return NIFTY_50_BACKUP

# ============================================
# MAIN CALCULATIONS
# ============================================

def calculate_index_gffi(symbol, name, data_func):
    """Calculate GFFI for an index"""
    print(f"\n📍 Calculating {name} GFFI...")
    
    # Get historical data
    hist_data = get_historical_data(symbol)
    if not hist_data or len(hist_data) < 30:
        print(f"   ❌ No historical data for {name}")
        return None
    
    prices = pd.Series([float(d['close']) for d in hist_data])
    returns = prices.pct_change().dropna() * 100
    
    entropy = calculate_entropy(returns)
    capital = calculate_capital_proxy(returns)
    
    if entropy is None or capital is None:
        print(f"   ❌ Could not calculate for {name}")
        return None
    
    gffi = (entropy / capital) * 1000
    gffi = round(gffi, 1)
    
    # Sanity check
    if gffi > 100 or gffi < 20:
        print(f"   ⚠️ Abnormal value {gffi}, skipping")
        return None
    
    print(f"   ✅ {name} GFFI: {gffi}")
    return gffi

def calculate_sector_gffi():
    """Calculate GFFI for all sectors"""
    print("\n🏭 Calculating sector-wise GFFI...")
    sector_gffi = {}
    
    for sector, stocks in SECTORS.items():
        gffi_values = []
        for stock in stocks[:4]:  # Take top 4 stocks per sector
            data = fetch_stock_data(stock)
            if data and 'gffi' in data:
                gffi_values.append(data['gffi'])
            time.sleep(2)  # Rate limit
        
        if gffi_values:
            avg_gffi = sum(gffi_values) / len(gffi_values)
            trend = 'up' if avg_gffi > 62 else 'down' if avg_gffi < 58 else 'stable'
            sector_gffi[sector] = {
                'gffi': round(avg_gffi, 1),
                'trend': trend,
                'stocks': [s for s in stocks[:3]]
            }
            print(f"   ✅ {sector}: {round(avg_gffi, 1)} ({trend})")
        else:
            print(f"   ❌ {sector}: No data")
    
    return sector_gffi

def generate_stock_picks(stocks_data):
    """Generate top 10 stock picks from calculated data"""
    if len(stocks_data) < 10:
        return {}
    
    # Sort by GFFI
    stocks_data.sort(key=lambda x: x['gffi'])
    
    # Top 5 lowest GFFI (BUY)
    safe_picks = []
    for s in stocks_data[:5]:
        safe_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'BUY',
            'reason': f'Low GFFI indicates stability at ₹{s["price"]}'
        })
    
    # Top 5 highest GFFI (SELL)
    risky_picks = []
    for s in stocks_data[-5:][::-1]:
        risky_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'SELL',
            'reason': f'High GFFI indicates risk at ₹{s["price"]}'
        })
    
    # Middle 5 (WATCH)
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
        'watch': watch_picks[:5]
    }

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js for India market"""
    print("\n" + "="*80)
    print("🇮🇳 FETCHING INDIA MARKET DATA")
    print("="*80)
    
    # Fetch Nifty and Sensex
    nifty_data = fetch_nifty_index()
    sensex_data = fetch_sensex()
    
    if nifty_data:
        print(f"\n✅ Nifty: {nifty_data['value']:.0f} ({nifty_data['change']:.2f}%)")
    if sensex_data:
        print(f"✅ Sensex: {sensex_data['value']:.0f} ({sensex_data['change']:.2f}%)")
    
    # Calculate GFFI for Nifty and Sensex
    print("\n📊 Calculating Index GFFI...")
    nifty_gffi = calculate_index_gffi('NIFTY', 'Nifty 50', None)
    sensex_gffi = calculate_index_gffi('SENSEX', 'Sensex', None)
    
    # Fetch all Nifty 50 stocks
    print("\n📈 Fetching Nifty 50 stocks...")
    stock_list = fetch_stock_list()
    stocks_data = []
    
    for stock in stock_list[:20]:  # Limit to 20 stocks for API limits
        data = fetch_stock_data(stock['symbol'])
        if data:
            stocks_data.append(data)
        time.sleep(2)
    
    print(f"   ✅ Fetched {len(stocks_data)} stocks")
    
    # Generate stock picks
    stock_picks = generate_stock_picks(stocks_data)
    
    # Calculate sector GFFI
    sector_data = calculate_sector_gffi()
    
    # Prepare sector data for JS
    sector_list = []
    for sector, data in sector_data.items():
        sector_list.append({
            'name': sector,
            'gffi': data['gffi'],
            'trend': data['trend'],
            'stocks': data['stocks']
        })
    
    # Prepare India market data
    india_market_data = {
        'nifty': int(nifty_data['value']) if nifty_data else 0,
        'sensex': int(sensex_data['value']) if sensex_data else 0,
        'nifty_change': round(nifty_data['change'], 2) if nifty_data else 0,
        'sensex_change': round(sensex_data['change'], 2) if sensex_data else 0,
        'nifty_gffi': nifty_gffi if nifty_gffi else None,
        'sensex_gffi': sensex_gffi if sensex_gffi else None,
        'vix': 23.36,
        'vix_change': 17.58,
        'advance': 1250,
        'decline': 1350
    }
    
    # Country data (India only)
    country_data = []
    if nifty_gffi:
        country_data.append({
            'flag': '🇮🇳',
            'name': 'India',
            'gffi': nifty_gffi,
            'status': get_status(nifty_gffi)
        })
    
    # Global GFFI
    global_gffi = nifty_gffi if nifty_gffi else 63.5
    
    # Current time
    now = datetime.now()
    
    # Generate data.js
    js_lines = [
        "// ============================================",
        "// DATA.JS - Auto-generated by GFFI Live Calculator",
        f"// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "// ============================================",
        "// INDIA MARKET DATA - Live from NSE",
        "",
        f"const countryData = {json.dumps(country_data, indent=2, ensure_ascii=False)};",
        "",
        f"const globalGFFI = {global_gffi};",
        "",
        f"const updateDate = '{now.strftime('%d %b %Y')}';",
        f"const updateTime = '{now.strftime('%I:%M %p')}';",
        "",
        f"const sectorData = {json.dumps(sector_list, indent=2, ensure_ascii=False)};",
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
    print(f"   🇮🇳 Nifty GFFI: {nifty_gffi if nifty_gffi else 'None'}")
    print(f"   🇮🇳 Sensex GFFI: {sensex_gffi if sensex_gffi else 'None'}")
    print(f"   📈 Stocks processed: {len(stocks_data)}")
    print(f"   🏭 Sectors: {len(sector_list)}")
    if stock_picks:
        print(f"   💹 Stock Picks: {len(stock_picks.get('safe', []))} Buy, {len(stock_picks.get('risky', []))} Sell, {len(stock_picks.get('watch', []))} Watch")
    print("="*80)

if __name__ == "__main__":
    main()
