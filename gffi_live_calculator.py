#!/usr/bin/env python3
"""
GFFI Live Calculator - INDIA MARKET ONLY with yfinance
Fetches live data from Yahoo Finance for Indian market
"""

import os
import json
import time
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🚀 GFFI LIVE CALCULATOR - INDIA MARKET (yfinance)")
print("="*80)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# INDIAN MARKET SYMBOLS
# ============================================
NIFTY_SYMBOL = "^NSEI"
SENSEX_SYMBOL = "^BSESN"

# ============================================
# NIFTY 50 STOCKS (with Yahoo Finance symbols)
# ============================================
NIFTY_50_STOCKS = [
    {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries', 'sector': 'Energy'},
    {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'sector': 'IT'},
    {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank', 'sector': 'Banking'},
    {'symbol': 'INFY.NS', 'name': 'Infosys', 'sector': 'IT'},
    {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank', 'sector': 'Banking'},
    {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever', 'sector': 'FMCG'},
    {'symbol': 'ITC.NS', 'name': 'ITC Ltd', 'sector': 'FMCG'},
    {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'sector': 'Banking'},
    {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel', 'sector': 'Telecom'},
    {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank', 'sector': 'Banking'},
    {'symbol': 'LT.NS', 'name': 'Larsen & Toubro', 'sector': 'Construction'},
    {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints', 'sector': 'FMCG'},
    {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki', 'sector': 'Auto'},
    {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharma', 'sector': 'Pharma'},
    {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors', 'sector': 'Auto'},
    {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank', 'sector': 'Banking'},
    {'symbol': 'NTPC.NS', 'name': 'NTPC Ltd', 'sector': 'Energy'},
    {'symbol': 'ONGC.NS', 'name': 'ONGC', 'sector': 'Energy'},
    {'symbol': 'POWERGRID.NS', 'name': 'Power Grid', 'sector': 'Energy'},
    {'symbol': 'TITAN.NS', 'name': 'Titan Company', 'sector': 'FMCG'},
    {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance', 'sector': 'Banking'},
    {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel', 'sector': 'Metals'},
    {'symbol': 'WIPRO.NS', 'name': 'Wipro', 'sector': 'IT'},
    {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'sector': 'IT'},
    {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel', 'sector': 'Metals'},
    {'symbol': 'CIPLA.NS', 'name': 'Cipla', 'sector': 'Pharma'},
    {'symbol': 'DRREDDY.NS', 'name': "Dr Reddy's Labs", 'sector': 'Pharma'},
    {'symbol': 'BRITANNIA.NS', 'name': 'Britannia', 'sector': 'FMCG'},
    {'symbol': 'HINDALCO.NS', 'name': 'Hindalco', 'sector': 'Metals'},
    {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra', 'sector': 'Auto'},
]

# ============================================
# SECTOR MAPPING
# ============================================
SECTORS = {
    'Banking': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS'],
    'IT': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS'],
    'Pharma': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS'],
    'Auto': ['MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS'],
    'FMCG': ['HINDUNILVR.NS', 'ITC.NS', 'BRITANNIA.NS', 'TITAN.NS'],
    'Energy': ['RELIANCE.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS'],
    'Metals': ['TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS'],
    'Telecom': ['BHARTIARTL.NS'],
    'Construction': ['LT.NS'],
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
# DATA FETCHING FUNCTIONS
# ============================================

def fetch_index_data(symbol, name):
    """Fetch index data and calculate GFFI"""
    print(f"\n📍 Fetching {name} data...")
    
    try:
        # Fetch historical data for GFFI calculation
        hist = yf.download(symbol, period="2mo", progress=False)
        if hist.empty or len(hist) < 30:
            print(f"   ❌ No historical data for {name}")
            return None, None
        
        # Get latest price
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        # Calculate GFFI
        returns = hist['Close'].pct_change().dropna() * 100
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
        
    except Exception as e:
        print(f"   ❌ Error fetching {name}: {str(e)[:50]}")
        return None, None

def fetch_stock_data(symbol, name):
    """Fetch stock data and calculate GFFI"""
    try:
        # Fetch historical data
        hist = yf.download(symbol, period="2mo", progress=False)
        if hist.empty or len(hist) < 30:
            return None
        
        # Get latest price
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        # Calculate GFFI
        returns = hist['Close'].pct_change().dropna() * 100
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
            'symbol': symbol.replace('.NS', ''),
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
        
        for symbol in stocks[:3]:  # Top 3 stocks per sector
            stock_data = fetch_stock_data(symbol, sector)
            if stock_data and 'gffi' in stock_data:
                gffi_values.append(stock_data['gffi'])
                stock_names.append(stock_data['symbol'])
            time.sleep(1)
        
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
    
    for stock in NIFTY_50_STOCKS[:20]:  # Limit to 20 for speed
        data = fetch_stock_data(stock['symbol'], stock['name'])
        if data:
            stocks_data.append(data)
        time.sleep(1)
    
    if len(stocks_data) < 10:
        print("   ❌ Insufficient data for stock picks")
        return {}
    
    # Sort by GFFI
    stocks_data.sort(key=lambda x: x['gffi'])
    
    # Safe picks (lowest GFFI)
    safe_picks = []
    for s in stocks_data[:5]:
        safe_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'BUY',
            'reason': f'Low GFFI indicates stability at ₹{s["price"]}'
        })
    
    # Risky picks (highest GFFI)
    risky_picks = []
    for s in stocks_data[-5:][::-1]:
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
        'watch': watch_picks[:5]
    }

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js"""
    print("\n" + "="*80)
    print("🇮🇳 FETCHING INDIA MARKET DATA (yfinance)")
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
        "// INDIA MARKET DATA - Live from Yahoo Finance",
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
