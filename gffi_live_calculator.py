#!/usr/bin/env python3
"""
GFFI Live Calculator
====================
Fetches live data from Yahoo Finance and FRED to calculate GFFI
"""

import os
import json
import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class GFFILiveCalculator:
    def __init__(self, fred_api_key=None):
        self.fred_api_key = fred_api_key or os.getenv('FRED_API_KEY')
        self.window_entropy = 60
        self.entropy_bins = 20
        self.gffi_threshold = 72.8
        
        # Country to symbol mapping with FRED series for ALL countries
        self.country_symbols = {
            'USA': {'index': '^GSPC', 'fred_series': 'DDSI03USA156NWDB'},
            'India': {'index': '^NSEI', 'fred_series': 'DDSI03INA156NWDB'},
            'Germany': {'index': '^GDAXI', 'fred_series': 'DDSI03DEA156NWDB'},
            'France': {'index': '^FCHI', 'fred_series': 'DDSI03FRA156NWDB'},
            'Japan': {'index': '^N225', 'fred_series': 'DDSI03JPA156NWDB'},
            'UK': {'index': '^FTSE', 'fred_series': 'DDSI03GBA156NWDB'},
            'China': {'index': '000001.SS', 'fred_series': 'DDSI03CNA156NWDB'},
            'Brazil': {'index': '^BVSP', 'fred_series': 'DDSI03BRA156NWDB'},
            'Canada': {'index': '^GSPTSE', 'fred_series': 'DDSI03CAA156NWDB'},
            'Australia': {'index': '^AXJO', 'fred_series': 'DDSI03AUA156NWDB'},
            'South Korea': {'index': '^KS11', 'fred_series': 'DDSI03KRA156NWDB'},
            'Singapore': {'index': '^STI', 'fred_series': 'DDSI03SGA156NWDB'},
            'South Africa': {'index': '^JN0U.JO', 'fred_series': 'DDSI03ZAA156NWDB'},
            'Russia': {'index': 'IMOEX.ME', 'fred_series': 'DDSI03RUA156NWDB'},
            'Mexico': {'index': '^MXX', 'fred_series': 'DDSI03MXA156NWDB'},
            'Italy': {'index': 'FTSEMIB.MI', 'fred_series': 'DDSI03ITA156NWDB'},
            'Argentina': {'index': '^MERV', 'fred_series': 'DDSI03ARA156NWDB'},
        }
        
        # Fixed data
        self.stock_picks = {
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
        
        self.sector_data = [
            {'name': 'Banking & Financials', 'gffi': 68.5, 'trend': 'up', 'stocks': ['HDFC Bank', 'ICICI Bank', 'SBI', 'Kotak Bank']},
            {'name': 'Information Technology', 'gffi': 58.2, 'trend': 'down', 'stocks': ['TCS', 'Infosys', 'HCL Tech', 'Wipro']},
            {'name': 'Pharmaceuticals', 'gffi': 55.8, 'trend': 'stable', 'stocks': ['Sun Pharma', 'Cipla', 'Dr Reddy', 'Divis Labs']},
            {'name': 'Automobile', 'gffi': 62.1, 'trend': 'up', 'stocks': ['Maruti', 'Tata Motors', 'M&M', 'Bajaj Auto']},
            {'name': 'Energy', 'gffi': 65.4, 'trend': 'up', 'stocks': ['Reliance', 'ONGC', 'BPCL', 'IOC']},
            {'name': 'FMCG', 'gffi': 52.3, 'trend': 'down', 'stocks': ['ITC', 'HUL', 'Britannia', 'Nestle']},
            {'name': 'Metals', 'gffi': 64.7, 'trend': 'up', 'stocks': ['Tata Steel', 'JSW Steel', 'Hindalco', 'Coal India']},
            {'name': 'Telecom', 'gffi': 59.5, 'trend': 'stable', 'stocks': ['Bharti Airtel', 'Reliance Jio', 'Vodafone Idea']},
        ]
        
        self.india_market_data = {
            'nifty': 77566,
            'sensex': 77566,
            'vix': 23.36,
            'nifty_change': -1.71,
            'sensex_change': -1.71,
            'vix_change': 17.58,
            'advance': 850,
            'decline': 1650
        }
    
    def get_flag(self, country_name):
        flags = {
            'USA': '🇺🇸', 'India': '🇮🇳', 'Germany': '🇩🇪', 'France': '🇫🇷',
            'Japan': '🇯🇵', 'UK': '🇬🇧', 'China': '🇨🇳', 'Brazil': '🇧🇷',
            'Canada': '🇨🇦', 'Australia': '🇦🇺', 'South Korea': '🇰🇷',
            'Singapore': '🇸🇬', 'South Africa': '🇿🇦', 'Russia': '🇷🇺',
            'Mexico': '🇲🇽', 'Italy': '🇮🇹', 'Argentina': '🇦🇷',
        }
        return flags.get(country_name, '🌍')
    
    def fetch_yahoo_data(self, symbol):
        try:
            print(f"   📥 Fetching Yahoo data for {symbol}...")
            
            # Create ticker with custom session and headers
            import requests
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            })
            
            # Use session with yfinance
            ticker = yf.Ticker(symbol, session=session)
            
            # Try with different periods if 6mo fails
            for period in ['1mo', '3mo', '6mo', '1y']:
                try:
                    data = ticker.history(period=period)
                    if not data.empty:
                        print(f"   ✅ Got {len(data)} days of data (period={period})")
                        prices = data['Adj Close'] if 'Adj Close' in data.columns else data['Close']
                        returns = prices.pct_change().dropna() * 100
                        return {
                            'prices': prices, 
                            'returns': returns, 
                            'last_price': float(prices.iloc[-1])
                        }
                except:
                    continue
            
            print(f"   ⚠️ No data for {symbol} after trying all periods")
            return None
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None
    
    def fetch_fred_data(self, series_id):
        if not self.fred_api_key:
            return None
        try:
            end = datetime.now()
            start = end - timedelta(days=3*365)
            data = web.DataReader(series_id, 'fred', start, end, api_key=self.fred_api_key)
            if data.empty:
                return None
            return {'latest_value': float(data.iloc[-1, 0])}
        except:
            return None
    
    def calculate_entropy(self, returns_series):
        returns = returns_series.dropna().values
        returns = returns[~np.isinf(returns)]
        returns = returns[~np.isnan(returns)]
        if len(returns) < 10:
            return 0.5
        hist, _ = np.histogram(returns, bins=min(self.entropy_bins, len(returns)//2), density=True)
        probs = hist / hist.sum()
        probs = probs[probs > 0]
        if len(probs) == 0:
            return 0.5
        entropy = -np.sum(probs * np.log(probs))
        if len(returns) < 200:
            entropy += (self.entropy_bins - 1) / (2 * len(returns))
        max_entropy = np.log(min(self.entropy_bins, len(returns)//2))
        if max_entropy > 0:
            entropy = min(1.0, entropy / max_entropy)
        return max(0.1, min(0.9, entropy))
    
    def calculate_capital_proxy(self, returns_series):
        if len(returns_series) < 60:
            return 15.0
        rolling_vol = returns_series.rolling(60).std().dropna()
        if len(rolling_vol) == 0:
            return 15.0
        latest_vol = float(rolling_vol.iloc[-1])
        capital_proxy = 20 / (1 + latest_vol)
        return max(10, min(30, capital_proxy))
    
    def calculate_country_gffi(self, country_name):
        if country_name not in self.country_symbols:
            return None
        config = self.country_symbols[country_name]
        market_data = self.fetch_yahoo_data(config['index'])
        if market_data is None:
            return None
        recent_returns = market_data['returns'].tail(60)
        entropy = self.calculate_entropy(recent_returns)
        if config['fred_series'] and self.fred_api_key:
            fred_data = self.fetch_fred_data(config['fred_series'])
            if fred_data:
                capital = fred_data['latest_value']
            else:
                capital = self.calculate_capital_proxy(market_data['returns'])
        else:
            capital = self.calculate_capital_proxy(market_data['returns'])
        gffi = (entropy / capital) * 1000
        if gffi >= 70:
            status = 'critical'
        elif gffi >= 65:
            status = 'warning'
        else:
            status = 'success'
        return {
            'flag': self.get_flag(country_name),
            'name': country_name,
            'gffi': round(gffi, 1),
            'status': status,
            'entropy': round(entropy, 3),
            'capital': round(capital, 2),
            'last_price': market_data['last_price'],
            'last_return': round(market_data['returns'].iloc[-1], 2)
        }
    
    def generate_data_js(self, filename='data.js'):
        country_data = []
        gffi_values = []
        for country in self.country_symbols.keys():
            result = self.calculate_country_gffi(country)
            if result:
                country_data.append(result)
                gffi_values.append(result['gffi'])
        global_gffi = round(sum(gffi_values) / len(gffi_values), 1) if gffi_values else 63.5
        now = datetime.now()
        js_content = f"""// ============================================
// DATA.JS - Auto-generated by GFFI Live Calculator
// Last Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}
// ============================================

const countryData = {json.dumps(country_data, indent=2)};

const globalGFFI = {global_gffi};

const updateDate = '{now.strftime('%d %b %Y')}';
const updateTime = '{now.strftime('%I:%M %p')}';

const sectorData = {json.dumps(self.sector_data, indent=2)};

const stockPicks = {json.dumps(self.stock_picks, indent=2)};

const indiaMarketData = {json.dumps(self.india_market_data, indent=2)};
"""
        with open(filename, 'w') as f:
            f.write(js_content)
        print(f"✅ Data written to {filename}")
        print(f"   Global GFFI: {global_gffi}")
        print(f"   Countries: {len(country_data)}")

if __name__ == "__main__":
    calculator = GFFILiveCalculator()
    calculator.generate_data_js('data.js')
