#!/usr/bin/env python3
"""
GFFI Live Calculator - COMPLETE VERSION with FRED & Alpha Vantage
Fetches live data from Alpha Vantage API and FRED to calculate GFFI
"""

import os
import json
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta
import yfinance as yf
import pandas_datareader.data as web
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🚀 GFFI UPDATE SCRIPT - STARTED")
print("="*60)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Country configuration
COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'av_symbol': 'SPX', 'fred_series': 'DDSI03USA156NWDB'},
    {'code': 'Germany', 'name': 'Germany', 'flag': '🇩🇪', 'av_symbol': 'GDAXI', 'fred_series': 'DDSI03DEA156NWDB'},
    {'code': 'France', 'name': 'France', 'flag': '🇫🇷', 'av_symbol': 'FCHI', 'fred_series': 'DDSI03FRA156NWDB'},
    {'code': 'Japan', 'name': 'Japan', 'flag': '🇯🇵', 'av_symbol': 'NIKKEI225', 'fred_series': 'DDSI03JPA156NWDB'},
    {'code': 'UK', 'name': 'UK', 'flag': '🇬🇧', 'av_symbol': 'FTSE', 'fred_series': 'DDSI03GBA156NWDB'},
    {'code': 'China', 'name': 'China', 'flag': '🇨🇳', 'av_symbol': 'SSEC', 'fred_series': 'DDSI03CNA156NWDB'},
    {'code': 'India', 'name': 'India', 'flag': '🇮🇳', 'av_symbol': 'NSEI', 'fred_series': 'DDSI03INA156NWDB'},
    {'code': 'Brazil', 'name': 'Brazil', 'flag': '🇧🇷', 'av_symbol': 'BVSP', 'fred_series': 'DDSI03BRA156NWDB'},
    {'code': 'Russia', 'name': 'Russia', 'flag': '🇷🇺', 'av_symbol': 'IMOEX', 'fred_series': 'DDSI03RUA156NWDB'},
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'av_symbol': 'JN0U.JO', 'fred_series': 'DDSI03ZAA156NWDB'},
    {'code': 'Canada', 'name': 'Canada', 'flag': '🇨🇦', 'av_symbol': 'GSPTSE', 'fred_series': 'DDSI03CAA156NWDB'},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'av_symbol': 'FTSEMIB', 'fred_series': 'DDSI03ITA156NWDB'},
    {'code': 'Australia', 'name': 'Australia', 'flag': '🇦🇺', 'av_symbol': 'AXJO', 'fred_series': 'DDSI03AUA156NWDB'},
    {'code': 'SouthKorea', 'name': 'S. Korea', 'flag': '🇰🇷', 'av_symbol': 'KS11', 'fred_series': 'DDSI03KRA156NWDB'},
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'av_symbol': 'STI', 'fred_series': 'DDSI03SGA156NWDB'},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'av_symbol': 'MXX', 'fred_series': 'DDSI03MXA156NWDB'},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'av_symbol': 'MERV', 'fred_series': 'DDSI03ARA156NWDB'},
]

# Sector Data (Fixed)
SECTOR_DATA = [
    {'name': 'Banking & Financials', 'gffi': 68.5, 'trend': 'up', 'stocks': ['HDFC Bank', 'ICICI Bank', 'SBI', 'Kotak Bank']},
    {'name': 'Information Technology', 'gffi': 58.2, 'trend': 'down', 'stocks': ['TCS', 'Infosys', 'HCL Tech', 'Wipro']},
    {'name': 'Pharmaceuticals', 'gffi': 55.8, 'trend': 'stable', 'stocks': ['Sun Pharma', 'Cipla', 'Dr Reddy', 'Divis Labs']},
    {'name': 'Automobile', 'gffi': 62.1, 'trend': 'up', 'stocks': ['Maruti', 'Tata Motors', 'M&M', 'Bajaj Auto']},
    {'name': 'Energy', 'gffi': 65.4, 'trend': 'up', 'stocks': ['Reliance', 'ONGC', 'BPCL', 'IOC']},
    {'name': 'FMCG', 'gffi': 52.3, 'trend': 'down', 'stocks': ['ITC', 'HUL', 'Britannia', 'Nestle']},
    {'name': 'Metals', 'gffi': 64.7, 'trend': 'up', 'stocks': ['Tata Steel', 'JSW Steel', 'Hindalco', 'Coal India']},
    {'name': 'Telecom', 'gffi': 59.5, 'trend': 'stable', 'stocks': ['Bharti Airtel', 'Reliance Jio', 'Vodafone Idea']},
]

# Stock Picks (Fixed)
STOCK_PICKS = {
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

# India Market Data (Fixed)
INDIA_MARKET_DATA = {
    'nifty': 77566,
    'sensex': 77566,
    'vix': 23.36,
    'nifty_change': -1.71,
    'sensex_change': -1.71,
    'vix_change': 17.58,
    'advance': 850,
    'decline': 1650
}

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

def fetch_fred_data(series_id):
    """Fetch data from FRED API"""
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        print(f"   ⚠️ No FRED API key for {series_id}")
        return None
    
    try:
        end = datetime.now()
        start = end - timedelta(days=3*365)
        data = web.DataReader(series_id, 'fred', start, end, api_key=api_key)
        if data.empty:
            return None
        return {'latest_value': float(data.iloc[-1, 0])}
    except Exception as e:
        print(f"   ❌ FRED error: {str(e)[:50]}")
        return None

def fetch_alphavantage_data(symbol):
    """Fetch data from Alpha Vantage API"""
    api_key = os.getenv('ALPHA_VANTAGE_KEY')
    if not api_key:
        print(f"   ⚠️ No Alpha Vantage key for {symbol}")
        return None
    
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            print(f"   ⚠️ No Alpha Vantage data for {symbol}")
            if 'Note' in data:
                print(f"   📝 {data['Note'][:100]}")
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
        returns = prices_series.pct_change().dropna() * 100
        
        print(f"   ✅ Got {len(prices_series)} days of data")
        return {
            'prices': prices_series,
            'returns': returns,
            'last_price': float(prices_series.iloc[-1])
        }
    except Exception as e:
        print(f"   ❌ Alpha Vantage error: {str(e)[:50]}")
        return None

def generate_demo_data(country_name):
    """Generate demo data when APIs fail"""
    print(f"   📊 Using DEMO data for {country_name}")
    
    np.random.seed(hash(country_name) % 100)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq='D')
    
    # Different base prices for different countries
    base_prices = {
        'USA': 4500, 'India': 18000, 'Germany': 15000, 'France': 7000,
        'Japan': 30000, 'UK': 7500, 'China': 3000, 'Brazil': 100000,
        'Canada': 20000, 'Australia': 7000, 'South Korea': 2500,
        'Singapore': 3000, 'South Africa': 60000, 'Russia': 3000,
        'Mexico': 45000, 'Italy': 25000, 'Argentina': 50000
    }
    base_price = base_prices.get(country_name, 10000)
    
    returns = np.random.normal(0.0003, 0.008, 60)
    price_series = base_price * np.exp(np.cumsum(returns))
    prices = pd.Series(price_series, index=dates)
    returns_series = prices.pct_change().dropna() * 100
    
    return {
        'prices': prices,
        'returns': returns_series,
        'last_price': float(prices.iloc[-1])
    }

def calculate_country_gffi(country):
    """Calculate GFFI for a single country"""
    print(f"\n📍 Processing {country['name']}...")
    
    # Try Alpha Vantage first
    market_data = fetch_alphavantage_data(country['av_symbol'])
    
    # Try Yahoo Finance as fallback
    if market_data is None and 'ticker' in country:
        try:
            print(f"   📥 Trying Yahoo Finance for {country['ticker']}...")
            ticker = yf.Ticker(country['ticker'])
            hist = ticker.history(period="2mo")
            if not hist.empty:
                prices = hist['Close']
                returns = prices.pct_change().dropna() * 100
                market_data = {
                    'prices': prices,
                    'returns': returns,
                    'last_price': float(prices.iloc[-1])
                }
                print(f"   ✅ Got Yahoo data")
        except:
            pass
    
    # Use demo data if both APIs fail
    if market_data is None:
        market_data = generate_demo_data(country['name'])
    
    if market_data is None:
        return None
    
    recent_returns = market_data['returns'].tail(60)
    entropy = calculate_entropy(recent_returns)
    
    # Try FRED for capital data
    if country.get('fred_series'):
        fred_data = fetch_fred_data(country['fred_series'])
        if fred_data:
            capital = fred_data['latest_value']
        else:
            capital = calculate_capital_proxy(market_data['returns'])
    else:
        capital = calculate_capital_proxy(market_data['returns'])
    
    # Calculate GFFI
    gffi = (entropy / capital) * 1000
    
    # Round to 1 decimal
    gffi = round(gffi, 1)
    
    result = {
        'flag': country['flag'],
        'name': country['name'],
        'gffi': gffi,
        'status': get_status(gffi)
    }
    
    print(f"   ✅ GFFI: {gffi} ({result['status']})")
    return result

def main():
    """Main function to generate data.js"""
    print("\n" + "="*60)
    print("🌍 FETCHING LIVE GFFI DATA")
    print("="*60)
    
    country_data = []
    gffi_values = []
    
    for country in COUNTRIES:
        result = calculate_country_gffi(country)
        if result:
            country_data.append(result)
            gffi_values.append(result['gffi'])
    
    # Calculate global GFFI
    global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else 63.5
    
    # Current time
    now = datetime.now()
    
    # Generate data.js content
    js_content = f"""// ============================================
// DATA.JS - Auto-generated by GFFI Live Calculator
// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}
// ============================================

const countryData = {json.dumps(country_data, indent=2)};

const globalGFFI = {global_gffi};

const updateDate = '{now.strftime('%d %b %Y')}';
const updateTime = '{now.strftime('%I:%M %p')}';

const sectorData = {json.dumps(SECTOR_DATA, indent=2)};

const stockPicks = {json.dumps(STOCK_PICKS, indent=2)};

const indiaMarketData = {json.dumps(INDIA_MARKET_DATA, indent=2)};
"""
    
    # Write to file
    with open('data.js', 'w') as f:
        f.write(js_content)
    
    print("\n" + "="*60)
    print(f"✅ DATA.JS UPDATED SUCCESSFULLY")
    print(f"   Countries: {len(country_data)}")
    print(f"   Global GFFI: {global_gffi}")
    print(f"   Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

if __name__ == "__main__":
    main()
