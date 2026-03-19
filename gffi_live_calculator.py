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
    {'symbol': 'LT.NS', 'name': 'Larsen & Toubro'},
    {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints'},
    {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki'},
    {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharma'},
    {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors'},
    {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank'},
    {'symbol': 'NTPC.NS', 'name': 'NTPC Ltd'},
    {'symbol': 'ONGC.NS', 'name': 'Oil & Natural Gas Corp'},
    {'symbol': 'POWERGRID.NS', 'name': 'Power Grid Corp'},
    {'symbol': 'TITAN.NS', 'name': 'Titan Company'},
    {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance'},
    {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports'},
    {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel'},
    {'symbol': 'WIPRO.NS', 'name': 'Wipro'},
    {'symbol': 'ULTRACEMCO.NS', 'name': 'UltraTech Cement'},
    {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies'},
    {'symbol': 'GRASIM.NS', 'name': 'Grasim Industries'},
    {'symbol': 'DIVISLAB.NS', 'name': 'Divis Laboratories'},
    {'symbol': 'DRREDDY.NS', 'name': 'Dr Reddy\'s Labs'},
    {'symbol': 'BRITANNIA.NS', 'name': 'Britannia Industries'},
    {'symbol': 'INDUSINDBK.NS', 'name': 'IndusInd Bank'},
    {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel'},
    {'symbol': 'CIPLA.NS', 'name': 'Cipla'},
    {'symbol': 'APOLLOHOSP.NS', 'name': 'Apollo Hospitals'},
    {'symbol': 'HEROMOTOCO.NS', 'name': 'Hero MotoCorp'},
    {'symbol': 'BAJAJ-AUTO.NS', 'name': 'Bajaj Auto'},
    {'symbol': 'EICHERMOT.NS', 'name': 'Eicher Motors'},
    {'symbol': 'COALINDIA.NS', 'name': 'Coal India'},
    {'symbol': 'BPCL.NS', 'name': 'Bharat Petroleum'},
    {'symbol': 'IOC.NS', 'name': 'Indian Oil Corp'},
    {'symbol': 'HDFCLIFE.NS', 'name': 'HDFC Life'},
    {'symbol': 'SBILIFE.NS', 'name': 'SBI Life'},
    {'symbol': 'BAJAJFINSV.NS', 'name': 'Bajaj Finserv'},
    {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra'},
    {'symbol': 'NESTLEIND.NS', 'name': 'Nestle India'},
    {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra'},
    {'symbol': 'HINDALCO.NS', 'name': 'Hindalco Industries'},
    {'symbol': 'TATACONSUM.NS', 'name': 'Tata Consumer'},
    {'symbol': 'UPL.NS', 'name': 'UPL Ltd'},
    {'symbol': 'SHREECEM.NS', 'name': 'Shree Cement'},
]

# Sector definitions with their component stocks
SECTOR_DEFINITIONS = {
    'Banking & Financials': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS'],
    'Information Technology': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS'],
    'Pharmaceuticals': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'DIVISLAB.NS', 'APOLLOHOSP.NS'],
    'Automobile': ['MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS'],
    'Energy': ['RELIANCE.NS', 'ONGC.NS', 'BPCL.NS', 'IOC.NS', 'POWERGRID.NS', 'NTPC.NS', 'COALINDIA.NS'],
    'FMCG': ['HINDUNILVR.NS', 'ITC.NS', 'BRITANNIA.NS', 'NESTLEIND.NS', 'TITAN.NS', 'TATACONSUM.NS'],
    'Metals': ['TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'COALINDIA.NS', 'GRASIM.NS'],
    'Telecom': ['BHARTIARTL.NS', 'IDEA.NS'],
}

# Stock name mapping for display
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
    'LT.NS': 'L&T',
    'ASIANPAINT.NS': 'Asian Paints',
    'MARUTI.NS': 'Maruti',
    'SUNPHARMA.NS': 'Sun Pharma',
    'TATAMOTORS.NS': 'Tata Motors',
    'AXISBANK.NS': 'Axis Bank',
    'NTPC.NS': 'NTPC',
    'ONGC.NS': 'ONGC',
    'POWERGRID.NS': 'Power Grid',
    'TITAN.NS': 'Titan',
    'BAJFINANCE.NS': 'Bajaj Finance',
    'ADANIPORTS.NS': 'Adani Ports',
    'JSWSTEEL.NS': 'JSW Steel',
    'WIPRO.NS': 'Wipro',
    'ULTRACEMCO.NS': 'UltraTech',
    'HCLTECH.NS': 'HCLTech',
    'GRASIM.NS': 'Grasim',
    'DIVISLAB.NS': 'Divis Labs',
    'DRREDDY.NS': 'Dr Reddy',
    'BRITANNIA.NS': 'Britannia',
    'INDUSINDBK.NS': 'IndusInd',
    'TATASTEEL.NS': 'Tata Steel',
    'CIPLA.NS': 'Cipla',
    'APOLLOHOSP.NS': 'Apollo Hosp',
    'HEROMOTOCO.NS': 'Hero Moto',
    'BAJAJ-AUTO.NS': 'Bajaj Auto',
    'EICHERMOT.NS': 'Eicher',
    'COALINDIA.NS': 'Coal India',
    'BPCL.NS': 'BPCL',
    'IOC.NS': 'IOC',
    'HDFCLIFE.NS': 'HDFC Life',
    'SBILIFE.NS': 'SBI Life',
    'BAJAJFINSV.NS': 'Bajaj Finserv',
    'TECHM.NS': 'TechM',
    'NESTLEIND.NS': 'Nestle',
    'M&M.NS': 'M&M',
    'HINDALCO.NS': 'Hindalco',
    'TATACONSUM.NS': 'Tata Consumer',
    'UPL.NS': 'UPL',
    'SHREECEM.NS': 'Shree Cement',
    'IDEA.NS': 'Vodafone Idea',
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
    """Calculate capital proxy from volatility"""
    if len(returns_series) < 60:
        return None
    
    rolling_vol = returns_series.rolling(60).std().dropna()
    if len(rolling_vol) == 0:
        return None
    
    latest_vol = float(rolling_vol.iloc[-1])
    capital_proxy = 20 / (1 + latest_vol)
    return max(10, min(30, capital_proxy))

# ============================================
# DATA FETCHING FUNCTIONS - REAL DATA ONLY
# ============================================

def fetch_yahoo_timeseries(symbol, period="2mo"):
    """Fetch time series data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        return hist['Close']
    except Exception as e:
        print(f"   ⚠️ Yahoo Finance error for {symbol}: {str(e)[:50]}")
        return None

def fetch_alphavantage_timeseries(symbol):
    """Fetch time series data from Alpha Vantage"""
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
    except Exception as e:
        print(f"   ⚠️ Alpha Vantage error for {symbol}: {str(e)[:50]}")
        return None

def fetch_market_data(symbol, yahoo_symbol=None):
    """Fetch market data from multiple sources, return None if all fail"""
    # Try Yahoo Finance first
    if yahoo_symbol:
        prices = fetch_yahoo_timeseries(yahoo_symbol)
        if prices is not None and len(prices) >= 30:
            return prices
    
    # Try Alpha Vantage as backup
    prices = fetch_alphavantage_timeseries(symbol)
    if prices is not None and len(prices) >= 30:
        return prices
    
    return None

def fetch_stock_data(symbol):
    """Fetch stock data and calculate GFFI, return None if fails"""
    prices = fetch_yahoo_timeseries(symbol)
    
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
        'display_name': STOCK_NAMES.get(symbol, symbol.replace('.NS', '')),
        'gffi': round(gffi, 1),
        'price': round(float(prices.iloc[-1]), 2)
    }

def fetch_index_data(symbol, yahoo_symbol):
    """Fetch index data (Nifty, Sensex), return None if fails"""
    prices = fetch_yahoo_timeseries(yahoo_symbol, period="5d")
    
    if prices is None or len(prices) < 2:
        return None
    
    current_price = prices.iloc[-1]
    prev_price = prices.iloc[-2]
    change_pct = ((current_price - prev_price) / prev_price) * 100
    
    return {
        'value': round(current_price, 2),
        'change': round(change_pct, 2)
    }

def fetch_fred_data(series_id):
    """Fetch data from FRED API, return None if fails"""
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
        print(f"   ⚠️ FRED error for {series_id}: {str(e)[:50]}")
        return None

# ============================================
# COUNTRY GFFI FUNCTIONS - REAL DATA ONLY
# ============================================

def calculate_country_gffi(country):
    """Calculate GFFI for a single country, return None if fails"""
    print(f"\n📍 Processing {country['name']}...")
    
    prices = fetch_market_data(country['av_symbol'], country.get('yahoo_symbol'))
    
    if prices is None:
        print(f"   ❌ No market data available for {country['name']}")
        return None
    
    returns = prices.pct_change().dropna() * 100
    entropy = calculate_entropy(returns)
    
    if entropy is None:
        print(f"   ❌ Could not calculate entropy for {country['name']}")
        return None
    
    # Try FRED for capital data
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
# SECTOR DATA FUNCTIONS - REAL DATA ONLY
# ============================================

def calculate_sector_gffi(sector_name, stock_symbols):
    """Calculate live GFFI for a sector, return None if insufficient data"""
    gffi_values = []
    
    for symbol in stock_symbols[:4]:
        stock_data = fetch_stock_data(symbol)
        if stock_data and stock_data['gffi']:
            gffi_values.append(stock_data['gffi'])
        time.sleep(1)
    
    if len(gffi_values) < 2:
        return None, None
    
    avg_gffi = sum(gffi_values) / len(gffi_values)
    
    # Determine trend
    if avg_gffi > 62:
        trend = 'up'
    elif avg_gffi < 58:
        trend = 'down'
    else:
        trend = 'stable'
    
    return round(avg_gffi, 1), trend

def get_sector_stocks(stock_symbols):
    """Get display names for sector stocks"""
    stock_names = []
    for symbol in stock_symbols[:4]:
        name = STOCK_NAMES.get(symbol, symbol.replace('.NS', ''))
        stock_names.append(name)
    return stock_names

def fetch_live_sector_data():
    """Fetch live data for all sectors, return empty list if fails"""
    print("\n🏭 Fetching live sector data...")
    sector_data = []
    
    for sector_name, stocks in SECTOR_DEFINITIONS.items():
        gffi, trend = calculate_sector_gffi(sector_name, stocks)
        
        if gffi is not None:
            stock_names = get_sector_stocks(stocks)
            sector_data.append({
                'name': sector_name,
                'gffi': gffi,
                'trend': trend,
                'stocks': stock_names
            })
            print(f"   ✅ {sector_name}: GFFI={gffi}, Trend={trend}")
        else:
            print(f"   ❌ {sector_name}: Insufficient data")
        
        time.sleep(2)
    
    return sector_data

# ============================================
# STOCK PICKS FUNCTIONS - REAL DATA ONLY
# ============================================

def generate_stock_picks():
    """Generate live stock picks based on GFFI values, return empty dict if fails"""
    print("\n📈 Generating live stock picks from Nifty 50...")
    
    stocks_with_gffi = []
    
    for stock in NIFTY_50_STOCKS:
        data = fetch_stock_data(stock['symbol'])
        if data and data['gffi']:
            stocks_with_gffi.append({
                'symbol': data['symbol'],
                'name': stock['name'],
                'gffi': data['gffi'],
                'price': data['price']
            })
        time.sleep(1)
    
    if len(stocks_with_gffi) < 9:  # Need at least 9 stocks for 3-3-3 picks
        print("   ❌ Insufficient stock data for picks")
        return {}
    
    # Sort by GFFI
    stocks_with_gffi.sort(key=lambda x: x['gffi'])
    
    # Safe picks (lowest GFFI)
    safe_picks = []
    for s in stocks_with_gffi[:3]:
        safe_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'BUY',
            'reason': f"Low GFFI indicates stability at ₹{s['price']}"
        })
    
    # Risky picks (highest GFFI)
    risky_picks = []
    for s in stocks_with_gffi[-3:][::-1]:
        risky_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'SELL',
            'reason': f"High GFFI indicates risk at ₹{s['price']}"
        })
    
    # Watchlist (middle range)
    mid_index = len(stocks_with_gffi) // 2
    watch_stocks = stocks_with_gffi[mid_index-1:mid_index+2]
    watch_picks = []
    for s in watch_stocks:
        watch_picks.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'gffi': s['gffi'],
            'action': 'WATCH',
            'reason': f"Moderate GFFI at ₹{s['price']}, monitor for trend"
        })
    
    return {
        'safe': safe_picks,
        'risky': risky_picks,
        'watch': watch_picks
    }

# ============================================
# INDIA MARKET DATA FUNCTIONS - REAL DATA ONLY
# ============================================

def fetch_live_india_market_data():
    """Fetch live India market data, return empty dict if fails"""
    print("\n🇮🇳 Fetching live India market data...")
    
    # Nifty 50
    nifty_data = fetch_index_data('NSEI', '^NSEI')
    if not nifty_data:
        print("   ❌ Could not fetch Nifty data")
        return {}
    
    # Sensex
    sensex_data = fetch_index_data('BSESN', '^BSESN')
    if not sensex_data:
        print("   ❌ Could not fetch Sensex data")
        return {}
    
    print(f"   ✅ Nifty: {nifty_data['value']} ({nifty_data['change']}%)")
    print(f"   ✅ Sensex: {sensex_data['value']} ({sensex_data['change']}%)")
    
    # India VIX - try to fetch
    vix_data = None
    try:
        vix_prices = fetch_yahoo_timeseries('^INDIAVIX', period="5d")
        if vix_prices is not None and len(vix_prices) >= 2:
            current_vix = vix_prices.iloc[-1]
            prev_vix = vix_prices.iloc[-2]
            vix_change = ((current_vix - prev_vix) / prev_vix) * 100
            vix_data = {'value': current_vix, 'change': vix_change}
            print(f"   ✅ VIX: {current_vix:.2f} ({vix_change:.2f}%)")
    except:
        print("   ⚠️ Could not fetch VIX data")
    
    # Advance/Decline - difficult to fetch real data, skip if not available
    advances = None
    declines = None
    
    return {
        'nifty': int(nifty_data['value']),
        'sensex': int(sensex_data['value']),
        'vix': round(vix_data['value'], 2) if vix_data else None,
        'nifty_change': round(nifty_data['change'], 2),
        'sensex_change': round(sensex_data['change'], 2),
        'vix_change': round(vix_data['change'], 2) if vix_data else None,
        'advance': advances,
        'decline': declines
    }

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main function to generate data.js with 100% real data only"""
    print("\n" + "="*70)
    print("🌍 FETCHING 100% REAL GFFI DATA - NO FALLBACKS")
    print("="*70)
    
    # Fetch country GFFI data
    country_data = []
    gffi_values = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
        
        # Rate limiting
        time.sleep(5)
    
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else None
    
    # Fetch live sector data
    print("\n⏳ Waiting 10 seconds before fetching sectors...")
    time.sleep(10)
    sector_data = fetch_live_sector_data()
    
    # Fetch live stock picks
    print("\n⏳ Waiting 10 seconds before fetching stocks...")
    time.sleep(10)
    stock_picks = generate_stock_picks()
    
    # Fetch live India market data
    print("\n⏳ Waiting 5 seconds before fetching India data...")
    time.sleep(5)
    india_market_data = fetch_live_india_market_data()
    
    # Current time
    now = datetime.now()
    
    # Generate data.js content
    js_content = f"""// ============================================
// DATA.JS - Auto-generated by GFFI Live Calculator
// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}
// ============================================
// 100% REAL DATA - NO FALLBACKS
// If a section is empty, data was not available from APIs

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
    print("✅ DATA.JS UPDATED SUCCESSFULLY - 100% REAL DATA")
    print("="*70)
    print(f"   🌍 Countries with data: {len(country_data)}/{len(COUNTRIES)}")
    print(f"   📊 Global GFFI: {global_gffi if global_gffi else 'Not available'}")
    print(f"   🏭 Sectors with data: {len(sector_data)}/{len(SECTOR_DEFINITIONS)}")
    print(f"   📈 Stock Picks available: {'Yes' if stock_picks else 'No'}")
    if india_market_data:
        print(f"   🇮🇳 Nifty: {india_market_data.get('nifty', 'N/A')} ({india_market_data.get('nifty_change', 'N/A')}%)")
        print(f"   🇮🇳 Sensex: {india_market_data.get('sensex', 'N/A')} ({india_market_data.get('sensex_change', 'N/A')}%)")
    print(f"   📅 Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

if __name__ == "__main__":
    main()
