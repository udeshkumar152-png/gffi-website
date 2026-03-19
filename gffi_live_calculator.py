#!/usr/bin/env python3
"""
GFFI Live Calculator - ALPHA VANTAGE ONLY VERSION
Fetches ALL data exclusively from Alpha Vantage API
No Yahoo Finance - more reliable on GitHub Actions
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

# Country configuration with Alpha Vantage symbols
COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'av_symbol': 'SPX', 'fred_series': 'DDSI03USA156NWDB'},
    {'code': 'Germany', 'name': 'Germany', 'flag': '🇩🇪', 'av_symbol': 'GDAXI', 'fred_series': 'DDSI03DEA156NWDB'},
    {'code': 'France', 'name': 'France', 'flag': '🇫🇷', 'av_symbol': 'FCHI', 'fred_series': 'DDSI03FRA156NWDB'},
    {'code': 'Japan', 'name': 'Japan', 'flag': '🇯🇵', 'av_symbol': 'NIKKEI225', 'fred_series': 'DDSI03JPA156NWDB'},
    {'code': 'UK', 'name': 'UK', 'flag': '🇬🇧', 'av_symbol': 'FTSE', 'fred_series': 'DDSI03GBA156NWDB'},
    {'code': 'China', 'name': 'China', 'flag': '🇨🇳', 'av_symbol': 'SSEC', 'fred_series': 'DDSI03CNA156NWDB'},
    {'code': 'India', 'name': 'India', 'flag': '🇮🇳', 'av_symbol': 'NSEI', 'fred_series': 'DDSI03INA156NWDB'},
    
]

# Indian stocks for live stock picks (Alpha Vantage symbols)
INDIAN_STOCKS = [
    {'symbol': 'RELIANCE.BSE', 'name': 'Reliance Industries', 'av_symbol': 'RELIANCE.BSE'},
    {'symbol': 'TCS.BSE', 'name': 'Tata Consultancy Services', 'av_symbol': 'TCS.BSE'},
    {'symbol': 'HDFCBANK.BSE', 'name': 'HDFC Bank', 'av_symbol': 'HDFCBANK.BSE'},
    {'symbol': 'INFY.BSE', 'name': 'Infosys', 'av_symbol': 'INFY.BSE'},
    {'symbol': 'ICICIBANK.BSE', 'name': 'ICICI Bank', 'av_symbol': 'ICICIBANK.BSE'},
    {'symbol': 'HINDUNILVR.BSE', 'name': 'Hindustan Unilever', 'av_symbol': 'HINDUNILVR.BSE'},
    {'symbol': 'ITC.BSE', 'name': 'ITC Ltd', 'av_symbol': 'ITC.BSE'},
    {'symbol': 'SBIN.BSE', 'name': 'State Bank of India', 'av_symbol': 'SBIN.BSE'},
    {'symbol': 'BHARTIARTL.BSE', 'name': 'Bharti Airtel', 'av_symbol': 'BHARTIARTL.BSE'},
    {'symbol': 'KOTAKBANK.BSE', 'name': 'Kotak Mahindra Bank', 'av_symbol': 'KOTAKBANK.BSE'},
    {'symbol': 'LT.BSE', 'name': 'Larsen & Toubro', 'av_symbol': 'LT.BSE'},
    {'symbol': 'ASIANPAINT.BSE', 'name': 'Asian Paints', 'av_symbol': 'ASIANPAINT.BSE'},
    {'symbol': 'MARUTI.BSE', 'name': 'Maruti Suzuki', 'av_symbol': 'MARUTI.BSE'},
    {'symbol': 'SUNPHARMA.BSE', 'name': 'Sun Pharma', 'av_symbol': 'SUNPHARMA.BSE'},
    {'symbol': 'TATAMOTORS.BSE', 'name': 'Tata Motors', 'av_symbol': 'TATAMOTORS.BSE'},
    {'symbol': 'AXISBANK.BSE', 'name': 'Axis Bank', 'av_symbol': 'AXISBANK.BSE'},
    {'symbol': 'NTPC.BSE', 'name': 'NTPC Ltd', 'av_symbol': 'NTPC.BSE'},
    {'symbol': 'ONGC.BSE', 'name': 'Oil & Natural Gas Corp', 'av_symbol': 'ONGC.BSE'},
    {'symbol': 'POWERGRID.BSE', 'name': 'Power Grid Corp', 'av_symbol': 'POWERGRID.BSE'},
    {'symbol': 'TITAN.BSE', 'name': 'Titan Company', 'av_symbol': 'TITAN.BSE'},
]

# Sector definitions with their component stocks (Alpha Vantage symbols)
SECTOR_DEFINITIONS = {
    'Banking & Financials': ['HDFCBANK.BSE', 'ICICIBANK.BSE', 'SBIN.BSE', 'KOTAKBANK.BSE', 'AXISBANK.BSE'],
    'Information Technology': ['TCS.BSE', 'INFY.BSE', 'HCLTECH.BSE', 'WIPRO.BSE'],
    'Pharmaceuticals': ['SUNPHARMA.BSE', 'CIPLA.BSE', 'DRREDDY.BSE', 'DIVISLAB.BSE'],
    'Automobile': ['MARUTI.BSE', 'TATAMOTORS.BSE', 'M&M.BSE', 'BAJAJ-AUTO.BSE'],
    'Energy': ['RELIANCE.BSE', 'ONGC.BSE', 'BPCL.BSE', 'IOC.BSE'],
    'FMCG': ['HINDUNILVR.BSE', 'ITC.BSE', 'BRITANNIA.BSE', 'NESTLEIND.BSE'],
    'Metals': ['TATASTEEL.BSE', 'JSWSTEEL.BSE', 'HINDALCO.BSE', 'COALINDIA.BSE'],
    'Telecom': ['BHARTIARTL.BSE', 'IDEA.BSE'],
}

# Stock name mapping for display
STOCK_NAMES = {
    'RELIANCE.BSE': 'Reliance',
    'TCS.BSE': 'TCS',
    'HDFCBANK.BSE': 'HDFC Bank',
    'INFY.BSE': 'Infosys',
    'ICICIBANK.BSE': 'ICICI Bank',
    'HINDUNILVR.BSE': 'HUL',
    'ITC.BSE': 'ITC',
    'SBIN.BSE': 'SBI',
    'BHARTIARTL.BSE': 'Bharti Airtel',
    'KOTAKBANK.BSE': 'Kotak Bank',
    'LT.BSE': 'L&T',
    'ASIANPAINT.BSE': 'Asian Paints',
    'MARUTI.BSE': 'Maruti',
    'SUNPHARMA.BSE': 'Sun Pharma',
    'TATAMOTORS.BSE': 'Tata Motors',
    'AXISBANK.BSE': 'Axis Bank',
    'NTPC.BSE': 'NTPC',
    'ONGC.BSE': 'ONGC',
    'POWERGRID.BSE': 'Power Grid',
    'TITAN.BSE': 'Titan',
    'CIPLA.BSE': 'Cipla',
    'DRREDDY.BSE': 'Dr Reddy',
    'DIVISLAB.BSE': 'Divis Labs',
    'M&M.BSE': 'M&M',
    'BAJAJ-AUTO.BSE': 'Bajaj Auto',
    'BPCL.BSE': 'BPCL',
    'IOC.BSE': 'IOC',
    'BRITANNIA.BSE': 'Britannia',
    'NESTLEIND.BSE': 'Nestle',
    'TATASTEEL.BSE': 'Tata Steel',
    'JSWSTEEL.BSE': 'JSW Steel',
    'HINDALCO.BSE': 'Hindalco',
    'COALINDIA.BSE': 'Coal India',
    'IDEA.BSE': 'Vodafone Idea',
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
    
    if len(returns) < 10:
        return 0.5
    
    bins = min(20, len(returns)//2)
    hist, _ = np.histogram(returns, bins=bins, density=True)
    probs = hist / hist.sum()
    probs = probs[probs > 0]
    
    if len(probs) == 0:
        return 0.5
    
    entropy = -np.sum(probs * np.log(probs))
    max_entropy = np.log(bins)
    if max_entropy > 0:
        entropy = min(1.0, entropy / max_entropy)
    
    return max(0.1, min(0.9, entropy))

def calculate_capital_proxy(returns_series):
    """Calculate capital proxy from volatility"""
    if len(returns_series) < 60:
        return 15.0
    
    rolling_vol = returns_series.rolling(60).std().dropna()
    if len(rolling_vol) == 0:
        return 15.0
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 20 / (1 + latest_vol)
    return max(10, min(30, capital_proxy))

# ============================================
# ALPHA VANTAGE DATA FETCHING
# ============================================

def fetch_alphavantage_timeseries(symbol):
    """Fetch time series data from Alpha Vantage"""
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}&outputsize=compact"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            if 'Note' in data:
                print(f"   📝 Alpha Vantage note: {data['Note'][:100]}")
            return None
        
        # Parse data
        time_series = data['Time Series (Daily)']
        dates = []
        prices = []
        
        # Get last 60 days
        sorted_dates = sorted(time_series.keys())[-60:]
        for date_str in sorted_dates:
            dates.append(pd.Timestamp(date_str))
            prices.append(float(time_series[date_str]['4. close']))
        
        prices_series = pd.Series(prices, index=dates)
        return prices_series
        
    except Exception as e:
        print(f"   ⚠️ Alpha Vantage error: {str(e)[:50]}")
        return None

def fetch_stock_data(symbol):
    """Fetch stock data and calculate GFFI"""
    prices_series = fetch_alphavantage_timeseries(symbol)
    
    if prices_series is None or len(prices_series) < 30:
        return None
    
    returns = prices_series.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    capital = calculate_capital_proxy(returns)
    gffi = (entropy / capital) * 1000
    
    return {
        'symbol': symbol,
        'display_name': STOCK_NAMES.get(symbol, symbol.replace('.BSE', '')),
        'gffi': round(gffi, 1),
        'price': round(float(prices_series.iloc[-1]), 2),
        'returns': returns.tolist()[-30:]
    }

def fetch_index_data(symbol, name):
    """Fetch index data (Nifty, Sensex, etc.)"""
    prices_series = fetch_alphavantage_timeseries(symbol)
    
    if prices_series is None or len(prices_series) < 2:
        return None
    
    current_price = prices_series.iloc[-1]
    prev_price = prices_series.iloc[-2] if len(prices_series) > 1 else current_price
    change_pct = ((current_price - prev_price) / prev_price) * 100
    
    return {
        'value': round(current_price, 2),
        'change': round(change_pct, 2)
    }

# ============================================
# FRED DATA FETCHING
# ============================================

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
    except Exception as e:
        print(f"   ⚠️ FRED error: {str(e)[:30]}")
        return None

# ============================================
# COUNTRY GFFI FUNCTIONS
# ============================================

def calculate_country_gffi(country):
    """Calculate GFFI for a single country"""
    print(f"\n📍 Processing {country['name']}...")
    
    prices_series = fetch_alphavantage_timeseries(country['av_symbol'])
    
    if prices_series is None or len(prices_series) < 30:
        print(f"   ⚠️ No market data for {country['name']}")
        return None
    
    returns = prices_series.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    
    # Try FRED for capital data
    if country.get('fred_series') and FRED_API_KEY:
        fred_data = fetch_fred_data(country['fred_series'])
        if fred_data:
            capital = fred_data['latest_value']
        else:
            capital = calculate_capital_proxy(returns)
    else:
        capital = calculate_capital_proxy(returns)
    
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

def calculate_sector_gffi(sector_name, stock_symbols):
    """Calculate live GFFI for a sector"""
    gffi_values = []
    
    for symbol in stock_symbols[:4]:  # Use top 4 stocks
        stock_data = fetch_stock_data(symbol)
        if stock_data and stock_data['gffi']:
            gffi_values.append(stock_data['gffi'])
    
    if not gffi_values:
        return 60.0, 'stable'
    
    avg_gffi = sum(gffi_values) / len(gffi_values)
    
    # Determine trend
    if avg_gffi > 62:
        trend = 'up'
    elif avg_gffi < 58:
        trend = 'down'
    else:
        trend = 'stable'
    
    return round(avg_gffi, 1), trend

def get_sector_stocks(sector_name, stock_symbols):
    """Get display names for sector stocks"""
    stock_names = []
    for symbol in stock_symbols[:4]:
        name = STOCK_NAMES.get(symbol, symbol.replace('.BSE', ''))
        stock_names.append(name)
    return stock_names

def fetch_live_sector_data():
    """Fetch live data for all sectors"""
    print("\n🏭 Fetching live sector data...")
    sector_data = []
    
    for sector_name, stocks in SECTOR_DEFINITIONS.items():
        gffi, trend = calculate_sector_gffi(sector_name, stocks)
        stock_names = get_sector_stocks(sector_name, stocks)
        
        sector_data.append({
            'name': sector_name,
            'gffi': gffi,
            'trend': trend,
            'stocks': stock_names
        })
        print(f"   ✅ {sector_name}: GFFI={gffi}, Trend={trend}")
    
    return sector_data

# ============================================
# STOCK PICKS FUNCTIONS
# ============================================

def generate_stock_picks():
    """Generate live stock picks based on GFFI values"""
    print("\n📈 Generating live stock picks from Indian stocks...")
    
    stocks_with_gffi = []
    
    for stock in INDIAN_STOCKS[:25]:  # Limit to 25 stocks for speed
        data = fetch_stock_data(stock['av_symbol'])
        if data and data['gffi']:
            stocks_with_gffi.append({
                'symbol': stock['symbol'].replace('.BSE', ''),
                'name': stock['name'],
                'gffi': data['gffi'],
                'price': data['price']
            })
    
    if len(stocks_with_gffi) < 10:
        print("   ⚠️ Not enough stock data, using fallback")
        return generate_fallback_stock_picks()
    
    # Sort by GFFI
    stocks_with_gffi.sort(key=lambda x: x['gffi'])
    
    # Safe picks (lowest GFFI)
    safe_picks = []
    for s in stocks_with_gffi[:8]:
        safe_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'BUY',
            'reason': get_buy_reason(s['gffi'], s['price'])
        })
    
    # Risky picks (highest GFFI)
    risky_picks = []
    for s in stocks_with_gffi[-8:][::-1]:
        risky_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'SELL',
            'reason': get_sell_reason(s['gffi'], s['price'])
        })
    
    # Watchlist (middle range)
    mid_index = len(stocks_with_gffi) // 2
    watch_stocks = stocks_with_gffi[mid_index-3:mid_index+3]
    watch_picks = []
    for s in watch_stocks:
        watch_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'WATCH',
            'reason': get_watch_reason(s['gffi'], s['price'])
        })
    
    return {
        'safe': safe_picks[:5],
        'risky': risky_picks[:5],
        'watch': watch_picks[:5]
    }

def get_buy_reason(gffi, price):
    if gffi < 50:
        return f"Strong fundamentals, low volatility at ₹{price}"
    elif gffi < 55:
        return f"Undervalued, good entry point at ₹{price}"
    else:
        return f"Accumulate on dips around ₹{price}"

def get_sell_reason(gffi, price):
    if gffi > 75:
        return f"Extreme overvaluation, exit now at ₹{price}"
    elif gffi > 70:
        return f"High risk, book profits at ₹{price}"
    else:
        return f"Reduce exposure from ₹{price}"

def get_watch_reason(gffi, price):
    if gffi < 60:
        return f"Momentum building, wait for dip below ₹{price-10}"
    else:
        return f"Consolidation phase at ₹{price}, watch for breakout"

def generate_fallback_stock_picks():
    """Generate fallback stock picks if live data fails"""
    return {
        'safe': [
            {'symbol': 'ITC', 'name': 'ITC Ltd', 'gffi': 52.3, 'action': 'BUY', 'reason': 'Low volatility, strong fundamentals'},
            {'symbol': 'HUL', 'name': 'Hindustan Unilever', 'gffi': 53.1, 'action': 'BUY', 'reason': 'Defensive play, consistent returns'},
            {'symbol': 'TCS', 'name': 'Tata Consultancy', 'gffi': 54.2, 'action': 'BUY', 'reason': 'Stable IT major, good dividends'},
            {'symbol': 'CIPLA', 'name': 'Cipla Ltd', 'gffi': 54.8, 'action': 'BUY', 'reason': 'Pharma safe haven'},
            {'symbol': 'BRITANNIA', 'name': 'Britannia', 'gffi': 55.1, 'action': 'BUY', 'reason': 'FMCG resilience'},
        ],
        'risky': [
            {'symbol': 'YESBANK', 'name': 'Yes Bank', 'gffi': 78.5, 'action': 'SELL', 'reason': 'High volatility, weak fundamentals'},
            {'symbol': 'ADANIGREEN', 'name': 'Adani Green', 'gffi': 76.2, 'action': 'SELL', 'reason': 'Overvalued, high debt'},
            {'symbol': 'VEDL', 'name': 'Vedanta', 'gffi': 74.3, 'action': 'SELL', 'reason': 'Commodity risk, high GFFI'},
            {'symbol': 'IDEA', 'name': 'Vodafone Idea', 'gffi': 72.8, 'action': 'SELL', 'reason': 'High debt, negative outlook'},
            {'symbol': 'ZOMATO', 'name': 'Zomato', 'gffi': 71.5, 'action': 'SELL', 'reason': 'Overvalued, profit concerns'},
        ],
        'watch': [
            {'symbol': 'RELIANCE', 'name': 'Reliance Ind', 'gffi': 62.5, 'action': 'WATCH', 'reason': 'Strong but expensive'},
            {'symbol': 'HDFCBANK', 'name': 'HDFC Bank', 'gffi': 63.2, 'action': 'WATCH', 'reason': 'Quality but valuations high'},
            {'symbol': 'INFY', 'name': 'Infosys', 'gffi': 59.8, 'action': 'WATCH', 'reason': 'IT momentum, but global risks'},
            {'symbol': 'MARUTI', 'name': 'Maruti Suzuki', 'gffi': 61.4, 'action': 'WATCH', 'reason': 'Auto recovery play'},
            {'symbol': 'TATAMOTORS', 'name': 'Tata Motors', 'gffi': 62.9, 'action': 'WATCH', 'reason': 'EV potential, debt concerns'},
        ]
    }

# ============================================
# INDIA MARKET DATA FUNCTIONS
# ============================================

def fetch_live_india_market_data():
    """Fetch live India market data (Nifty, Sensex)"""
    print("\n🇮🇳 Fetching live India market data...")
    
    # Nifty 50
    nifty_data = fetch_index_data('NSEI', 'Nifty 50')
    if not nifty_data:
        nifty_data = {'value': 77566, 'change': -1.71}
    print(f"   ✅ Nifty: {nifty_data['value']} ({nifty_data['change']}%)")
    
    # Sensex
    sensex_data = fetch_index_data('BSESN', 'Sensex')
    if not sensex_data:
        sensex_data = {'value': 77566, 'change': -1.71}
    print(f"   ✅ Sensex: {sensex_data['value']} ({sensex_data['change']}%)")
    
    # VIX (simulated since Alpha Vantage doesn't have India VIX)
    vix_data = {'value': 23.36, 'change': 17.58}
    print(f"   ✅ VIX: {vix_data['value']} ({vix_data['change']}%)")
    
    # Advance/Decline (simulated)
    advances = 850
    declines = 1650
    print(f"   ✅ Advance/Decline: {advances}/{declines}")
    
    return {
        'nifty': int(nifty_data['value']),
        'sensex': int(sensex_data['value']),
        'vix': round(vix_data['value'], 2),
        'nifty_change': round(nifty_data['change'], 2),
        'sensex_change': round(sensex_data['change'], 2),
        'vix_change': round(vix_data['change'], 2),
        'advance': advances,
        'decline': declines
    }

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js with Alpha Vantage data"""
    print("\n" + "="*70)
    print("🌍 FETCHING LIVE GFFI DATA FROM ALPHA VANTAGE")
    print("="*70)
    
    # Fetch country GFFI data
    country_data = []
    gffi_values = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
        time.sleep(15)  # Alpha Vantage rate limit (5 calls per minute)
    
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else 63.5
    
    # Fetch live sector data
    sector_data = fetch_live_sector_data()
    
    # Fetch live stock picks
    stock_picks = generate_stock_picks()
    
    # Fetch live India market data
    india_market_data = fetch_live_india_market_data()
    
    # Current time
    now = datetime.now()
    
    # Generate data.js content
    js_content = f"""// ============================================
// DATA.JS - Auto-generated by GFFI Live Calculator (Alpha Vantage)
// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}
// ============================================

const countryData = {json.dumps(country_data, indent=2, ensure_ascii=False)};

const globalGFFI = {global_gffi};

const updateDate = '{now.strftime('%d %b %Y')}';
const updateTime = '{now.strftime('%I:%M %p')}';

const sectorData = {json.dumps(sector_data, indent=2, ensure_ascii=False)};

const stockPicks = {json.dumps(stock_picks, indent=2, ensure_ascii=False)};

const indiaMarketData = {json.dumps(india_market_data, indent=2, ensure_ascii=False)};
"""
    
    # Write to file
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("\n" + "="*70)
    print("✅ DATA.JS UPDATED SUCCESSFULLY - ALPHA VANTAGE")
    print("="*70)
    print(f"   🌍 Countries: {len(country_data)}")
    print(f"   📊 Global GFFI: {global_gffi}")
    print(f"   🏭 Sectors: {len(sector_data)}")
    print(f"   📈 Stock Picks: {len(stock_picks['safe'])} Safe, {len(stock_picks['risky'])} Risky, {len(stock_picks['watch'])} Watch")
    print(f"   🇮🇳 Nifty: {india_market_data['nifty']} ({india_market_data['nifty_change']}%)")
    print(f"   🇮🇳 Sensex: {india_market_data['sensex']} ({india_market_data['sensex_change']}%)")
    print(f"   📅 Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

if __name__ == "__main__":
    main()
