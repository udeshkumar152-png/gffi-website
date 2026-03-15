#!/usr/bin/env python3
"""
GFFI Daily Update Script - WITH INDIA MARKET DATA
"""

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
import json
import sys
import os
import traceback

print("="*60)
print("🚀 GFFI UPDATE SCRIPT - WITH INDIA MARKET DATA")
print("="*60)
print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📂 Current directory: {os.getcwd()}")

# ============================================
# CONFIGURATION
# ============================================

COUNTRIES = [
    {'code': 'US', 'name': 'USA', 'flag': '🇺🇸', 'ticker': '^GSPC'},
    {'code': 'Germany', 'name': 'Germany', 'flag': '🇩🇪', 'ticker': '^GDAXI'},
    {'code': 'France', 'name': 'France', 'flag': '🇫🇷', 'ticker': '^FCHI'},
    {'code': 'Japan', 'name': 'Japan', 'flag': '🇯🇵', 'ticker': '^N225'},
    {'code': 'UK', 'name': 'UK', 'flag': '🇬🇧', 'ticker': '^FTSE'},
    {'code': 'China', 'name': 'China', 'flag': '🇨🇳', 'ticker': '000001.SS'},
    {'code': 'India', 'name': 'India', 'flag': '🇮🇳', 'ticker': '^NSEI'},
    {'code': 'Brazil', 'name': 'Brazil', 'flag': '🇧🇷', 'ticker': '^BVSP'},
    {'code': 'Russia', 'name': 'Russia', 'flag': '🇷🇺', 'ticker': 'IMOEX.ME'},
    {'code': 'SouthAfrica', 'name': 'S. Africa', 'flag': '🇿🇦', 'ticker': '^JN0U.JO'},
    {'code': 'Canada', 'name': 'Canada', 'flag': '🇨🇦', 'ticker': '^GSPTSE'},
    {'code': 'Italy', 'name': 'Italy', 'flag': '🇮🇹', 'ticker': 'FTSEMIB.MI'},
    {'code': 'Australia', 'name': 'Australia', 'flag': '🇦🇺', 'ticker': '^AXJO'},
    {'code': 'SouthKorea', 'name': 'S. Korea', 'flag': '🇰🇷', 'ticker': '^KS11'},
    {'code': 'Singapore', 'name': 'Singapore', 'flag': '🇸🇬', 'ticker': '^STI'},
    {'code': 'Mexico', 'name': 'Mexico', 'flag': '🇲🇽', 'ticker': '^MXX'},
    {'code': 'Argentina', 'name': 'Argentina', 'flag': '🇦🇷', 'ticker': '^MERV'},
]

# ============================================
# INDIA MARKET DATA
# ============================================

def fetch_india_market_data():
    """Fetch live India market data"""
    try:
        print("\n📊 Fetching India Market Data...")
        
        # Nifty 50
        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period="5d")
        
        # Sensex
        sensex = yf.Ticker("^BSESN")
        sensex_hist = sensex.history(period="5d")
        
        # India VIX
        vix = yf.Ticker("^INDIAVIX")
        vix_hist = vix.history(period="5d")
        
        market_data = {}
        
        # Process Nifty
        if not nifty_hist.empty:
            nifty_current = nifty_hist['Close'].iloc[-1]
            nifty_prev = nifty_hist['Close'].iloc[-2] if len(nifty_hist) > 1 else nifty_current
            nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
            market_data['nifty'] = round(nifty_current, 2)
            market_data['nifty_change'] = round(nifty_change, 2)
            print(f"   ✅ Nifty: {nifty_current:.2f} ({nifty_change:+.2f}%)")
        
        # Process Sensex
        if not sensex_hist.empty:
            sensex_current = sensex_hist['Close'].iloc[-1]
            sensex_prev = sensex_hist['Close'].iloc[-2] if len(sensex_hist) > 1 else sensex_current
            sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
            market_data['sensex'] = round(sensex_current, 2)
            market_data['sensex_change'] = round(sensex_change, 2)
            print(f"   ✅ Sensex: {sensex_current:.2f} ({sensex_change:+.2f}%)")
        
        # Process VIX
        if not vix_hist.empty:
            vix_current = vix_hist['Close'].iloc[-1]
            vix_prev = vix_hist['Close'].iloc[-2] if len(vix_hist) > 1 else vix_current
            vix_change = ((vix_current - vix_prev) / vix_prev) * 100
            market_data['vix'] = round(vix_current, 2)
            market_data['vix_change'] = round(vix_change, 2)
            print(f"   ✅ India VIX: {vix_current:.2f} ({vix_change:+.2f}%)")
        
        # Advance/Decline (simulated for now)
        market_data['advance'] = 850
        market_data['decline'] = 1650
        
        return market_data
        
    except Exception as e:
        print(f"⚠️ Error fetching India data: {e}")
        return None

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_status(gffi):
    if gffi >= 75:
        return 'critical'
    elif gffi >= 65:
        return 'alert'
    elif gffi >= 58:
        return 'warning'
    else:
        return 'success'

def calculate_gffi(price_history):
    if len(price_history) < 5:
        return 60 + np.random.normal(0, 5)
    
    returns = np.diff(price_history) / price_history[:-1] * 100
    volatility = np.std(returns)
    gffi = 50 + volatility * 2
    return max(40, min(85, gffi))

def fetch_country_data(country):
    try:
        print(f"   📊 Fetching {country['name']}...", end=' ')
        ticker = yf.Ticker(country['ticker'])
        hist = ticker.history(period="1mo")
        
        if hist.empty:
            print(f"⚠️ No data")
            return None
        
        prices = hist['Close'].values
        gffi = calculate_gffi(prices)
        print(f"✅ GFFI={gffi:.1f}")
        
        return {
            'flag': country['flag'],
            'name': country['name'],
            'gffi': round(gffi, 1),
            'status': get_status(gffi)
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ============================================
# GENERATE SCRIPT.JS WITH INDIA DATA
# ============================================

def generate_script_js(country_data, global_gffi, india_market_data):
    now = datetime.now()
    
    # Sector data
    sector_data = [
        {'name': 'Banking & Financials', 'gffi': 68.5, 'trend': 'up', 'stocks': ['HDFC Bank', 'ICICI Bank', 'SBI', 'Kotak Bank']},
        {'name': 'Information Technology', 'gffi': 58.2, 'trend': 'down', 'stocks': ['TCS', 'Infosys', 'HCL Tech', 'Wipro']},
        {'name': 'Pharmaceuticals', 'gffi': 55.8, 'trend': 'stable', 'stocks': ['Sun Pharma', 'Cipla', 'Dr Reddy', 'Divis Labs']},
        {'name': 'Automobile', 'gffi': 62.1, 'trend': 'up', 'stocks': ['Maruti', 'Tata Motors', 'M&M', 'Bajaj Auto']},
        {'name': 'Energy', 'gffi': 65.4, 'trend': 'up', 'stocks': ['Reliance', 'ONGC', 'BPCL', 'IOC']},
        {'name': 'FMCG', 'gffi': 52.3, 'trend': 'down', 'stocks': ['ITC', 'HUL', 'Britannia', 'Nestle']},
        {'name': 'Metals', 'gffi': 64.7, 'trend': 'up', 'stocks': ['Tata Steel', 'JSW Steel', 'Hindalco', 'Coal India']},
        {'name': 'Telecom', 'gffi': 59.5, 'trend': 'stable', 'stocks': ['Bharti Airtel', 'Reliance Jio', 'Vodafone Idea']},
    ]
    
    # Stock picks
    stock_picks = {
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
    
    # Sector performance for India dashboard
    sector_performance = [
        {'name': 'Banking', 'change': -2.3, 'status': 'bearish'},
        {'name': 'IT', 'change': 0.5, 'status': 'bullish'},
        {'name': 'Pharma', 'change': -0.2, 'status': 'neutral'},
        {'name': 'Auto', 'change': -1.5, 'status': 'bearish'},
        {'name': 'FMCG', 'change': 0.8, 'status': 'bullish'},
        {'name': 'Energy', 'change': -1.8, 'status': 'bearish'},
        {'name': 'Metals', 'change': -2.1, 'status': 'bearish'},
        {'name': 'Realty', 'change': -0.5, 'status': 'neutral'}
    ]
    
    js_content = f"""// Auto-generated by GFFI Bot on {now.strftime('%Y-%m-%d %H:%M:%S')}
const countryData = {json.dumps(country_data, indent=2)};
const globalGFFI = {global_gffi:.1f};
const updateDate = '{now.strftime("%d %b %Y")}';
const updateTime = '{now.strftime("%I:%M %p")}';

// India Market Data
const indiaMarketData = {json.dumps(india_market_data, indent=2) if india_market_data else 'null'};

// Sector data
const sectorData = {json.dumps(sector_data, indent=2)};

// Stock picks
const stockPicks = {json.dumps(stock_picks, indent=2)};

// Sector performance
const sectorPerformance = {json.dumps(sector_performance, indent=2)};

// Function to update India market dashboard
function updateIndiaMarket() {{
    if (!indiaMarketData) return;
    
    // Update Nifty
    const niftyEl = document.getElementById('nifty-value');
    if (niftyEl) niftyEl.textContent = indiaMarketData.nifty?.toLocaleString();
    
    const niftyChange = document.getElementById('nifty-change');
    if (niftyChange) {{
        niftyChange.textContent = indiaMarketData.nifty_change ? 
            (indiaMarketData.nifty_change > 0 ? `+${{indiaMarketData.nifty_change}}%` : `${{indiaMarketData.nifty_change}}%`) : '';
        niftyChange.className = indiaMarketData.nifty_change > 0 ? 'card-change positive' : 'card-change negative';
    }}
    
    // Update Sensex
    const sensexEl = document.getElementById('sensex-value');
    if (sensexEl) sensexEl.textContent = indiaMarketData.sensex?.toLocaleString();
    
    const sensexChange = document.getElementById('sensex-change');
    if (sensexChange) {{
        sensexChange.textContent = indiaMarketData.sensex_change ? 
            (indiaMarketData.sensex_change > 0 ? `+${{indiaMarketData.sensex_change}}%` : `${{indiaMarketData.sensex_change}}%`) : '';
        sensexChange.className = indiaMarketData.sensex_change > 0 ? 'card-change positive' : 'card-change negative';
    }}
    
    // Update VIX
    const vixEl = document.getElementById('vix-value');
    if (vixEl) vixEl.textContent = indiaMarketData.vix?.toFixed(2);
    
    const vixChange = document.getElementById('vix-change');
    if (vixChange) {{
        vixChange.textContent = indiaMarketData.vix_change ? 
            (indiaMarketData.vix_change > 0 ? `+${{indiaMarketData.vix_change}}%` : `${{indiaMarketData.vix_change}}%`) : '';
        vixChange.className = indiaMarketData.vix_change > 0 ? 'card-change negative' : 'card-change positive';
    }}
    
    // Update India GFFI (from countryData)
    const indiaData = countryData.find(c => c.name === 'India');
    const indiaGFFIEl = document.getElementById('india-gffi');
    if (indiaGFFIEl && indiaData) indiaGFFIEl.textContent = indiaData.gffi;
    
    const indiaStatus = document.getElementById('india-status');
    if (indiaStatus && indiaData) {{
        const status = indiaData.status.toUpperCase();
        indiaStatus.textContent = status === 'SUCCESS' ? '🟢 SUCCESS' : 
                                  status === 'WARNING' ? '🟡 WATCH' : 
                                  status === 'ALERT' ? '🟠 ALERT' : '🔴 CRITICAL';
    }}
    
    // Update market status
    const marketStatusEl = document.getElementById('market-status');
    if (marketStatusEl && indiaMarketData.nifty_change) {{
        marketStatusEl.textContent = indiaMarketData.nifty_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH';
    }}
    
    const fearLevelEl = document.getElementById('fear-level');
    if (fearLevelEl && indiaMarketData.vix) {{
        fearLevelEl.textContent = indiaMarketData.vix > 25 ? '😱 EXTREME FEAR' :
                                 indiaMarketData.vix > 20 ? '😨 FEAR' : '😌 NEUTRAL';
    }}
    
    const advDeclEl = document.getElementById('adv-decl');
    if (advDeclEl && indiaMarketData.advance) {{
        advDeclEl.textContent = `${{indiaMarketData.advance}} / ${{indiaMarketData.decline}}`;
    }}
    
    // Update sector tags
    updateSectorTags();
}}

// Update sector tags
function updateSectorTags() {{
    const sectorTagsEl = document.getElementById('sector-tags');
    if (!sectorTagsEl || !sectorPerformance) return;
    
    let html = '';
    sectorPerformance.forEach(sector => {{
        let bgColor, textColor;
        if (sector.status === 'bullish') {{
            bgColor = '#d4edda';
            textColor = '#155724';
        }} else if (sector.status === 'bearish') {{
            bgColor = '#f8d7da';
            textColor = '#721c24';
        }} else {{
            bgColor = '#fff3cd';
            textColor = '#856404';
        }}
        
        const changeIcon = sector.change > 0 ? '▲' : '▼';
        html += `
            <span class="sector-tag" style="background: ${{bgColor}}; color: ${{textColor}};">
                ${{sector.name}} ${{changeIcon}} ${{Math.abs(sector.change)}}%
            </span>
        `;
    }});
    sectorTagsEl.innerHTML = html;
}}

// Function to render sector analysis
function renderSectorAnalysis() {{
    const sectorGrid = document.getElementById('sector-grid');
    if (!sectorGrid) return;
    
    let html = '';
    sectorData.forEach(sector => {{
        let bgColor, textColor;
        if (sector.gffi >= 70) {{
            bgColor = '#ffcccc'; textColor = '#990000';
        }} else if (sector.gffi >= 65) {{
            bgColor = '#fff3cd'; textColor = '#856404';
        }} else if (sector.gffi >= 58) {{
            bgColor = '#d4edda'; textColor = '#155724';
        }} else {{
            bgColor = '#cce5ff'; textColor = '#004085';
        }}
        
        const trendIcon = sector.trend === 'up' ? '📈' : sector.trend === 'down' ? '📉' : '➡️';
        
        html += `
            <div class="sector-card" style="background: ${{bgColor}}; color: ${{textColor}};">
                <div class="sector-name">${{sector.name}} ${{trendIcon}}</div>
                <div class="sector-gffi">${{sector.gffi.toFixed(1)}}</div>
                <div class="sector-status">${{sector.gffi >= 70 ? '🔴 HIGH' : sector.gffi >= 65 ? '🟠 ALERT' : sector.gffi >= 58 ? '🟡 WATCH' : '🟢 SAFE'}}</div>
                <div style="font-size: 0.8rem; margin-top: 8px;">
                    <strong>Top Picks:</strong> ${{sector.stocks.slice(0, 3).join(', ')}}
                </div>
            </div>
        `;
    }});
    sectorGrid.innerHTML = html;
}}

// Function to render stock picks
function renderStockPicks() {{
    // Safe picks
    const safeDiv = document.getElementById('safe-picks');
    if (safeDiv) {{
        let html = '';
        stockPicks.safe.forEach(stock => {{
            html += `
                <div class="stock-item">
                    <span class="stock-symbol">${{stock.symbol}}</span>
                    <span class="stock-gffi">${{stock.gffi}}</span>
                    <span class="stock-action buy">${{stock.action}}</span>
                </div>
                <div style="font-size: 0.8rem; color: #6c757d; margin-bottom: 5px;">${{stock.reason}}</div>
            `;
        }});
        safeDiv.innerHTML = html;
    }}
    
    // Risky picks
    const riskyDiv = document.getElementById('risky-picks');
    if (riskyDiv) {{
        let html = '';
        stockPicks.risky.forEach(stock => {{
            html += `
                <div class="stock-item">
                    <span class="stock-symbol">${{stock.symbol}}</span>
                    <span class="stock-gffi">${{stock.gffi}}</span>
                    <span class="stock-action sell">${{stock.action}}</span>
                </div>
                <div style="font-size: 0.8rem; color: #6c757d; margin-bottom: 5px;">${{stock.reason}}</div>
            `;
        }});
        riskyDiv.innerHTML = html;
    }}
    
    // Watch picks
    const watchDiv = document.getElementById('watch-picks');
    if (watchDiv) {{
        let html = '';
        stockPicks.watch.forEach(stock => {{
            html += `
                <div class="stock-item">
                    <span class="stock-symbol">${{stock.symbol}}</span>
                    <span class="stock-gffi">${{stock.gffi}}</span>
                    <span class="stock-action watch">${{stock.action}}</span>
                </div>
                <div style="font-size: 0.8rem; color: #6c757d; margin-bottom: 5px;">${{stock.reason}}</div>
            `;
        }});
        watchDiv.innerHTML = html;
    }}
}}

// Main update function
function updateDashboard() {{
    // Update global GFFI
    const globalEl = document.getElementById('global-gffi');
    if (globalEl) globalEl.textContent = globalGFFI;
    
    const dateEl = document.getElementById('update-time');
    if (dateEl) dateEl.textContent = updateDate;
    
    const timeEl = document.getElementById('update-time-hm');
    if (timeEl) timeEl.textContent = updateTime;
    
    // Update country grid
    const countryGrid = document.getElementById('country-grid');
    if (countryGrid) {{
        let html = '';
        countryData.forEach(country => {{
            html += `
                <div class="country-card">
                    <div class="country-flag">${{country.flag}}</div>
                    <div class="country-name">${{country.name}}</div>
                    <div class="country-gffi">${{country.gffi}}</div>
                    <span class="country-status status-${{country.status}}">${{country.status.toUpperCase()}}</span>
                </div>
            `;
        }});
        countryGrid.innerHTML = html;
    }}
    
    // Render new features
    renderSectorAnalysis();
    renderStockPicks();
    updateIndiaMarket();
}}

document.addEventListener('DOMContentLoaded', updateDashboard);
"""
    
    return js_content

def main():
    """Main function"""
    try:
        # Fetch country data
        country_data = []
        success_count = 0
        
        print("\n📡 Fetching global market data...")
        for country in COUNTRIES:
            data = fetch_country_data(country)
            if data:
                country_data.append(data)
                success_count += 1
        
        print(f"\n✅ Successfully fetched {success_count}/{len(COUNTRIES)} countries")
        
        # Fetch India market data
        india_market_data = fetch_india_market_data()
        
        # Calculate global GFFI
        if country_data:
            gffi_values = [c['gffi'] for c in country_data]
            global_gffi = sum(gffi_values) / len(gffi_values)
        else:
            global_gffi = 63.5
            print("⚠️ No country data, using default global GFFI")
        
        # Generate script.js
        js_content = generate_script_js(country_data, global_gffi, india_market_data)
        
        # Write to file
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"\n✅ script.js updated with {len(country_data)} countries")
        if india_market_data:
            print(f"📊 India Market Data: Nifty={india_market_data.get('nifty', 'N/A')}, VIX={india_market_data.get('vix', 'N/A')}")
        print(f"🌍 Global GFFI: {global_gffi:.1f}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in main: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
        # Add this function to your existing update_gffi.py

def fetch_india_market_data():
    """Fetch live India market data"""
    try:
        print("📊 Fetching India market data...")
        
        # Nifty 50
        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period="5d")
        
        # Sensex
        sensex = yf.Ticker("^BSESN")
        sensex_hist = sensex.history(period="5d")
        
        # India VIX
        vix = yf.Ticker("^INDIAVIX")
        vix_hist = vix.history(period="5d")
        
        market_data = {}
        
        # Process Nifty
        if not nifty_hist.empty:
            nifty_current = nifty_hist['Close'].iloc[-1]
            nifty_prev = nifty_hist['Close'].iloc[-2] if len(nifty_hist) > 1 else nifty_current
            nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
            market_data['nifty'] = round(nifty_current, 2)
            market_data['nifty_change'] = round(nifty_change, 2)
            print(f"   ✅ Nifty: {nifty_current:.2f} ({nifty_change:+.2f}%)")
        
        # Process Sensex
        if not sensex_hist.empty:
            sensex_current = sensex_hist['Close'].iloc[-1]
            sensex_prev = sensex_hist['Close'].iloc[-2] if len(sensex_hist) > 1 else sensex_current
            sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
            market_data['sensex'] = round(sensex_current, 2)
            market_data['sensex_change'] = round(sensex_change, 2)
            print(f"   ✅ Sensex: {sensex_current:.2f} ({sensex_change:+.2f}%)")
        
        # Process VIX
        if not vix_hist.empty:
            vix_current = vix_hist['Close'].iloc[-1]
            vix_prev = vix_hist['Close'].iloc[-2] if len(vix_hist) > 1 else vix_current
            vix_change = ((vix_current - vix_prev) / vix_prev) * 100
            market_data['vix'] = round(vix_current, 2)
            market_data['vix_change'] = round(vix_change, 2)
            print(f"   ✅ India VIX: {vix_current:.2f} ({vix_change:+.2f}%)")
        
        return market_data
        
    except Exception as e:
        print(f"⚠️ Error fetching India data: {e}")
        return None
