// ============================================
// GLOBAL DATA
// ============================================
const countryData = [
    {flag: '🇺🇸', name: 'USA', gffi: 62.1, status: 'warning'},
    {flag: '🇩🇪', name: 'Germany', gffi: 68.4, status: 'success'},
    {flag: '🇫🇷', name: 'France', gffi: 63.5, status: 'warning'},
    {flag: '🇯🇵', name: 'Japan', gffi: 65.9, status: 'warning'},
    {flag: '🇬🇧', name: 'UK', gffi: 65.0, status: 'success'},
    {flag: '🇨🇳', name: 'China', gffi: 64.6, status: 'warning'},
    {flag: '🇮🇳', name: 'India', gffi: 64.7, status: 'success'},
    {flag: '🇧🇷', name: 'Brazil', gffi: 65.5, status: 'success'},
    {flag: '🇷🇺', name: 'Russia', gffi: 61.5, status: 'success'},
    {flag: '🇿🇦', name: 'S. Africa', gffi: 61.2, status: 'success'},
    {flag: '🇨🇦', name: 'Canada', gffi: 70.8, status: 'warning'},
    {flag: '🇮🇹', name: 'Italy', gffi: 62.5, status: 'warning'},
    {flag: '🇦🇺', name: 'Australia', gffi: 61.5, status: 'warning'},
    {flag: '🇰🇷', name: 'S. Korea', gffi: 61.2, status: 'success'},
    {flag: '🇸🇬', name: 'Singapore', gffi: 62.8, status: 'success'},
    {flag: '🇲🇽', name: 'Mexico', gffi: 61.5, status: 'warning'},
    {flag: '🇦🇷', name: 'Argentina', gffi: 63.2, status: 'warning'}
];

const globalGFFI = 63.5;
const updateDate = '15 Mar 2026';
const updateTime = '11:00 AM';

// Sector Data
const sectorData = [
    { name: 'Banking & Financials', gffi: 68.5, trend: 'up', stocks: ['HDFC Bank', 'ICICI Bank', 'SBI', 'Kotak Bank'] },
    { name: 'Information Technology', gffi: 58.2, trend: 'down', stocks: ['TCS', 'Infosys', 'HCL Tech', 'Wipro'] },
    { name: 'Pharmaceuticals', gffi: 55.8, trend: 'stable', stocks: ['Sun Pharma', 'Cipla', 'Dr Reddy', 'Divis Labs'] },
    { name: 'Automobile', gffi: 62.1, trend: 'up', stocks: ['Maruti', 'Tata Motors', 'M&M', 'Bajaj Auto'] },
    { name: 'Energy', gffi: 65.4, trend: 'up', stocks: ['Reliance', 'ONGC', 'BPCL', 'IOC'] },
    { name: 'FMCG', gffi: 52.3, trend: 'down', stocks: ['ITC', 'HUL', 'Britannia', 'Nestle'] },
    { name: 'Metals', gffi: 64.7, trend: 'up', stocks: ['Tata Steel', 'JSW Steel', 'Hindalco', 'Coal India'] },
    { name: 'Telecom', gffi: 59.5, trend: 'stable', stocks: ['Bharti Airtel', 'Reliance Jio', 'Vodafone Idea'] },
];

// Stock Picks
const stockPicks = {
    safe: [
        { symbol: 'ITC', name: 'ITC Ltd', gffi: 52.3, action: 'BUY', reason: 'Low volatility, strong fundamentals' },
        { symbol: 'HUL', name: 'Hindustan Unilever', gffi: 53.1, action: 'BUY', reason: 'Defensive play, consistent returns' },
        { symbol: 'TCS', name: 'Tata Consultancy', gffi: 54.2, action: 'BUY', reason: 'Stable IT major, good dividends' },
        { symbol: 'CIPLA', name: 'Cipla Ltd', gffi: 54.8, action: 'BUY', reason: 'Pharma safe haven' },
        { symbol: 'BRITANNIA', name: 'Britannia', gffi: 55.1, action: 'BUY', reason: 'FMCG resilience' },
    ],
    risky: [
        { symbol: 'YESBANK', name: 'Yes Bank', gffi: 78.5, action: 'SELL', reason: 'High volatility, weak fundamentals' },
        { symbol: 'ADANIGREEN', name: 'Adani Green', gffi: 76.2, action: 'SELL', reason: 'Overvalued, high debt' },
        { symbol: 'VEDL', name: 'Vedanta', gffi: 74.3, action: 'SELL', reason: 'Commodity risk, high GFFI' },
        { symbol: 'IDEA', name: 'Vodafone Idea', gffi: 72.8, action: 'SELL', reason: 'High debt, negative outlook' },
        { symbol: 'ZOMATO', name: 'Zomato', gffi: 71.5, action: 'SELL', reason: 'Overvalued, profit concerns' },
    ],
    watch: [
        { symbol: 'RELIANCE', name: 'Reliance Ind', gffi: 62.5, action: 'WATCH', reason: 'Strong but expensive' },
        { symbol: 'HDFCBANK', name: 'HDFC Bank', gffi: 63.2, action: 'WATCH', reason: 'Quality but valuations high' },
        { symbol: 'INFY', name: 'Infosys', gffi: 59.8, action: 'WATCH', reason: 'IT momentum, but global risks' },
        { symbol: 'MARUTI', name: 'Maruti Suzuki', gffi: 61.4, action: 'WATCH', reason: 'Auto recovery play' },
        { symbol: 'TATAMOTORS', name: 'Tata Motors', gffi: 62.9, action: 'WATCH', reason: 'EV potential, debt concerns' },
    ]
};

// India Market Data
const indiaMarketData = {
    nifty: 77566,
    sensex: 77566,
    vix: 23.36,
    nifty_change: -1.71,
    sensex_change: -1.71,
    vix_change: 17.58,
    advance: 850,
    decline: 1650
};

// ============================================
// VIEW STATE MANAGEMENT
// ============================================
let currentView = {
    country: 'grid',
    sector: 'grid',
    stocks: 'grid',
    india: 'grid'
};

// ============================================
// GRID VIEW FUNCTIONS
// ============================================
function renderCountryGrid() {
    const container = document.getElementById('country-grid');
    let html = '';
    countryData.forEach(c => {
        html += `<div class="country-card">
            <div class="country-flag">${c.flag}</div>
            <div class="country-name">${c.name}</div>
            <div class="country-gffi">${c.gffi}</div>
            <span class="country-status status-${c.status}">${c.status.toUpperCase()}</span>
        </div>`;
    });
    container.innerHTML = html;
}

function renderSectorGrid() {
    const container = document.getElementById('sector-grid');
    let html = '';
    sectorData.forEach(s => {
        let bg = s.gffi >= 70 ? '#ffcccc' : s.gffi >= 65 ? '#fff3cd' : s.gffi >= 58 ? '#d4edda' : '#cce5ff';
        let color = s.gffi >= 70 ? '#990000' : s.gffi >= 65 ? '#856404' : s.gffi >= 58 ? '#155724' : '#004085';
        let trendIcon = s.trend === 'up' ? '📈' : s.trend === 'down' ? '📉' : '➡️';
        let statusText = s.gffi >= 70 ? '🔴 HIGH' : s.gffi >= 65 ? '🟠 ALERT' : s.gffi >= 58 ? '🟡 WATCH' : '🟢 SAFE';
        
        html += `<div class="sector-card" style="background:${bg};color:${color};">
            <div class="sector-name">${s.name} ${trendIcon}</div>
            <div class="sector-gffi">${s.gffi.toFixed(1)}</div>
            <div class="sector-status">${statusText}</div>
            <div style="font-size:0.8rem">${s.stocks.slice(0,3).join(', ')}</div>
        </div>`;
    });
    container.innerHTML = html;
}

function renderStockGrid() {
    const container = document.querySelector('.picks-container');
    let html = `
        <div class="picks-box safe-picks">
            <h4>🟢 SAFE PICKS (Low GFFI)</h4>
            <div class="picks-list">
                ${stockPicks.safe.map(s => `
                    <div class="stock-item"><span class="stock-symbol">${s.symbol}</span> <span class="stock-gffi">${s.gffi}</span> <span class="stock-action buy">${s.action}</span></div>
                    <div style="font-size:0.8rem; color:#6c757d;">${s.reason}</div>
                `).join('')}
            </div>
        </div>
        <div class="picks-box risky-picks">
            <h4>🔴 RISKY PICKS (High GFFI)</h4>
            <div class="picks-list">
                ${stockPicks.risky.map(s => `
                    <div class="stock-item"><span class="stock-symbol">${s.symbol}</span> <span class="stock-gffi">${s.gffi}</span> <span class="stock-action sell">${s.action}</span></div>
                    <div style="font-size:0.8rem; color:#6c757d;">${s.reason}</div>
                `).join('')}
            </div>
        </div>
        <div class="picks-box watch-picks">
            <h4>🟡 WATCHLIST (Momentum Stocks)</h4>
            <div class="picks-list">
                ${stockPicks.watch.map(s => `
                    <div class="stock-item"><span class="stock-symbol">${s.symbol}</span> <span class="stock-gffi">${s.gffi}</span> <span class="stock-action watch">${s.action}</span></div>
                    <div style="font-size:0.8rem; color:#6c757d;">${s.reason}</div>
                `).join('')}
            </div>
        </div>
    `;
    container.innerHTML = html;
}

function renderIndiaGrid() {
    const container = document.querySelector('.india-cards');
    const indiaData = countryData.find(c => c.name === 'India');
    
    let html = `
        <div class="india-card nifty-card">
            <div class="card-icon">📈</div>
            <div class="card-content">
                <span class="card-label">Nifty 50</span>
                <span class="card-value">${indiaMarketData.nifty.toLocaleString()}</span>
                <span class="card-change ${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.nifty_change > 0 ? '+' : ''}${indiaMarketData.nifty_change}%</span>
            </div>
        </div>
        <div class="india-card sensex-card">
            <div class="card-icon">📊</div>
            <div class="card-content">
                <span class="card-label">Sensex</span>
                <span class="card-value">${indiaMarketData.sensex.toLocaleString()}</span>
                <span class="card-change ${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.sensex_change > 0 ? '+' : ''}${indiaMarketData.sensex_change}%</span>
            </div>
        </div>
        <div class="india-card vix-card">
            <div class="card-icon">⚡</div>
            <div class="card-content">
                <span class="card-label">India VIX</span>
                <span class="card-value">${indiaMarketData.vix.toFixed(2)}</span>
                <span class="card-change ${indiaMarketData.vix_change > 0 ? 'negative' : 'positive'}">${indiaMarketData.vix_change > 0 ? '+' : ''}${indiaMarketData.vix_change}%</span>
            </div>
        </div>
        <div class="india-card gffi-card">
            <div class="card-icon">🛡️</div>
            <div class="card-content">
                <span class="card-label">India GFFI</span>
                <span class="card-value">${indiaData.gffi}</span>
                <span class="card-status status-${indiaData.status}">${indiaData.status === 'success' ? '🟢 SUCCESS' : '🟡 WATCH'}</span>
            </div>
        </div>
    `;
    container.innerHTML = html;
    
    document.getElementById('market-status').textContent = indiaMarketData.nifty_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH';
    
    if (indiaMarketData.vix > 25) document.getElementById('fear-level').textContent = '😱 EXTREME FEAR';
    else if (indiaMarketData.vix > 20) document.getElementById('fear-level').textContent = '😨 FEAR';
    else document.getElementById('fear-level').textContent = '😐 NEUTRAL';
    
    document.getElementById('adv-decl').textContent = `${indiaMarketData.advance} / ${indiaMarketData.decline}`;
}

// ============================================
// TABLE VIEW FUNCTIONS
// ============================================
function renderCountryTable() {
    const container = document.getElementById('country-grid');
    
    let html = '<table class="data-table"><tr><th>Country</th><th>GFFI</th><th>Status</th><th>Risk Level</th></tr>';
    
    countryData.forEach(c => {
        let statusClass = c.status === 'success' ? 'status-success' : 
                         c.status === 'warning' ? 'status-warning' : 'status-alert';
        let riskLevel = c.gffi >= 70 ? '🔴 HIGH' : 
                       c.gffi >= 65 ? '🟠 ALERT' : 
                       c.gffi >= 58 ? '🟡 WATCH' : '🟢 LOW';
        
        html += `<tr>
            <td><strong>${c.flag} ${c.name}</strong></td>
            <td class="gffi-value">${c.gffi}</td>
            <td><span class="${statusClass}">${c.status.toUpperCase()}</span></td>
            <td>${riskLevel}</td>
        </tr>`;
    });
    
    html += '</table>';
    container.innerHTML = html;
}

function renderSectorTable() {
    const container = document.getElementById('sector-grid');
    
    let html = '<table class="data-table"><tr><th>Sector</th><th>GFFI</th><th>Status</th><th>Trend</th><th>Top Stocks</th></tr>';
    
    sectorData.forEach(s => {
        let statusClass = s.gffi >= 70 ? 'status-critical' : 
                         s.gffi >= 65 ? 'status-alert' : 
                         s.gffi >= 58 ? 'status-watch' : 'status-success';
        let statusText = s.gffi >= 70 ? 'CRITICAL' : 
                        s.gffi >= 65 ? 'ALERT' : 
                        s.gffi >= 58 ? 'WATCH' : 'SAFE';
        let trendIcon = s.trend === 'up' ? '📈' : s.trend === 'down' ? '📉' : '➡️';
        
        html += `<tr>
            <td><strong>${s.name}</strong></td>
            <td class="gffi-value">${s.gffi.toFixed(1)}</td>
            <td><span class="${statusClass}">${statusText}</span></td>
            <td>${trendIcon}</td>
            <td>${s.stocks.slice(0, 3).join(', ')}</td>
        </tr>`;
    });
    
    html += '</table>';
    container.innerHTML = html;
}

function renderStockTable() {
    const container = document.querySelector('.picks-container');
    
    let html = '<table class="data-table"><tr><th>Category</th><th>Symbol</th><th>Company</th><th>GFFI</th><th>Action</th><th>Reason</th></tr>';
    
    stockPicks.safe.forEach(s => {
        html += `<tr><td>🟢 SAFE</td><td><strong>${s.symbol}</strong></td><td>${s.name}</td><td class="gffi-value">${s.gffi}</td><td><span class="stock-action buy">${s.action}</span></td><td>${s.reason}</td></tr>`;
    });
    
    stockPicks.risky.forEach(s => {
        html += `<tr><td>🔴 RISKY</td><td><strong>${s.symbol}</strong></td><td>${s.name}</td><td class="gffi-value">${s.gffi}</td><td><span class="stock-action sell">${s.action}</span></td><td>${s.reason}</td></tr>`;
    });
    
    stockPicks.watch.forEach(s => {
        html += `<tr><td>🟡 WATCH</td><td><strong>${s.symbol}</strong></td><td>${s.name}</td><td class="gffi-value">${s.gffi}</td><td><span class="stock-action watch">${s.action}</span></td><td>${s.reason}</td></tr>`;
    });
    
    html += '</table>';
    container.innerHTML = html;
}

function renderIndiaTable() {
    const container = document.querySelector('.india-cards');
    const indiaData = countryData.find(c => c.name === 'India');
    
    let html = '<table class="data-table"><tr><th>Indicator</th><th>Value</th><th>Change</th><th>Status</th></tr>';
    
    html += `<tr>
        <td><strong>📈 Nifty 50</strong></td>
        <td class="gffi-value">${indiaMarketData.nifty.toLocaleString()}</td>
        <td class="${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.nifty_change > 0 ? '+' : ''}${indiaMarketData.nifty_change}%</td>
        <td>${indiaMarketData.nifty_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH'}</td>
    </tr>`;
    
    html += `<tr>
        <td><strong>📊 Sensex</strong></td>
        <td class="gffi-value">${indiaMarketData.sensex.toLocaleString()}</td>
        <td class="${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.sensex_change > 0 ? '+' : ''}${indiaMarketData.sensex_change}%</td>
        <td>${indiaMarketData.sensex_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH'}</td>
    </tr>`;
    
    html += `<tr>
        <td><strong>⚡ India VIX</strong></td>
        <td class="gffi-value">${indiaMarketData.vix.toFixed(2)}</td>
        <td class="${indiaMarketData.vix_change > 0 ? 'negative' : 'positive'}">${indiaMarketData.vix_change > 0 ? '+' : ''}${indiaMarketData.vix_change}%</td>
        <td>${indiaMarketData.vix > 25 ? '😱 EXTREME FEAR' : indiaMarketData.vix > 20 ? '😨 FEAR' : '😐 NEUTRAL'}</td>
    </tr>`;
    
    html += `<tr>
        <td><strong>🛡️ India GFFI</strong></td>
        <td class="gffi-value">${indiaData.gffi}</td>
        <td>-</td>
        <td><span class="status-${indiaData.status}">${indiaData.status.toUpperCase()}</span></td>
    </tr>`;
    
    html += `<tr>
        <td><strong>📊 Advance/Decline</strong></td>
        <td colspan="3">${indiaMarketData.advance} Advances / ${indiaMarketData.decline} Declines</td>
    </tr>`;
    
    html += '</table>';
    container.innerHTML = html;
}

// ============================================
// TOGGLE FUNCTIONS
// ============================================
function toggleCountryView() {
    const btn = document.getElementById('toggle-country');
    if (currentView.country === 'grid') {
        currentView.country = 'table';
        btn.innerHTML = '🖼️ Switch to Grid View';
        renderCountryTable();
    } else {
        currentView.country = 'grid';
        btn.innerHTML = '📊 Switch to Table View';
        renderCountryGrid();
    }
}

function toggleSectorView() {
    const btn = document.getElementById('toggle-sector');
    if (currentView.sector === 'grid') {
        currentView.sector = 'table';
        btn.innerHTML = '🖼️ Switch to Grid View';
        renderSectorTable();
    } else {
        currentView.sector = 'grid';
        btn.innerHTML = '📊 Switch to Table View';
        renderSectorGrid();
    }
}

function toggleStockView() {
    const btn = document.getElementById('toggle-stock');
    if (currentView.stocks === 'grid') {
        currentView.stocks = 'table';
        btn.innerHTML = '🖼️ Switch to Grid View';
        renderStockTable();
    } else {
        currentView.stocks = 'grid';
        btn.innerHTML = '📊 Switch to Table View';
        renderStockGrid();
    }
}

function toggleIndiaView() {
    const btn = document.getElementById('toggle-india');
    if (currentView.india === 'grid') {
        currentView.india = 'table';
        btn.innerHTML = '🖼️ Switch to Grid View';
        renderIndiaTable();
    } else {
        currentView.india = 'grid';
        btn.innerHTML = '📊 Switch to Table View';
        renderIndiaGrid();
    }
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Set global values
    document.getElementById('global-gffi').textContent = globalGFFI;
    document.getElementById('update-time').textContent = updateDate;
    document.getElementById('update-time-hm').textContent = updateTime;
    
    // Render initial views
    renderCountryGrid();
    renderSectorGrid();
    renderStockGrid();
    renderIndiaGrid();
    
    // Add event listeners
    document.getElementById('toggle-country').addEventListener('click', toggleCountryView);
    document.getElementById('toggle-sector').addEventListener('click', toggleSectorView);
    document.getElementById('toggle-stock').addEventListener('click', toggleStockView);
    document.getElementById('toggle-india').addEventListener('click', toggleIndiaView);
});
// ============================================
// AUTO-REFRESH FUNCTIONALITY
// हर 10 मिनट में डेटा रिफ्रेश करें
// ============================================

// Cache busting के साथ डेटा फेच करें
async function refreshMarketData() {
    console.log('⟳ रिफ्रेशिंग डेटा...', new Date().toLocaleTimeString());
    
    try {
        // अगर आपके पास अलग JSON फाइल है तो उसे फेच करें
        // हर रिक्वेस्ट में टाइमस्टैंप जोड़ें ताकि कैश न हो
        const timestamp = new Date().getTime();
        
        // विकल्प 1: अगर आपने JSON फाइल बनाई है
        // const response = await fetch(`data/gffi-data.json?t=${timestamp}`);
        
        // विकल्प 2: अगर नहीं बनाई है, तो पूरा पेज ही रीलोड कर दें
        // यह आसान तरीका है - पूरा पेज रिफ्रेश हो जाएगा
        location.reload();
        
        // विकल्प 3: अगर JSON है तो उसे पार्स करें
        /*
        const data = await response.json();
        
        // GFFI वैल्यू अपडेट करें
        document.getElementById('global-gffi').textContent = data.globalGFFI;
        document.getElementById('update-time').textContent = data.updateDate;
        document.getElementById('update-time-hm').textContent = data.updateTime;
        
        // कंट्री ग्रिड अपडेट करें
        if (typeof renderCountryGrid === 'function' && data.countryData) {
            renderCountryGrid(); // यह फंक्शन आपकी script.js में पहले से है
        }
        
        console.log('✅ डेटा अपडेट हुआ:', new Date().toLocaleTimeString());
        */
        
    } catch (error) {
        console.error('❌ डेटा रिफ्रेश में गड़बड़ी:', error);
    }
}

// विकल्प 4: अगर आप बिना पेज रीलोड के सिर्फ कुछ एलिमेंट अपडेट करना चाहते हैं
function updateSpecificElements() {
    // उदाहरण: ग्लोबल GFFI वैल्यू
    const globalGFFI = document.getElementById('global-gffi');
    if (globalGFFI) {
        // यहां पर कैलकुलेशन करें या API से लाएं
        // फिलहाल सिर्फ डेमो के लिए
        console.log('एलिमेंट्स अपडेट किए जा सकते हैं');
    }
}

// हर 10 मिनट (600,000 milliseconds) में रिफ्रेश करें
// 5 मिनट चाहिए तो: 5 * 60 * 1000 = 300000
// 10 मिनट चाहिए तो: 10 * 60 * 1000 = 600000
const REFRESH_INTERVAL = 10 * 60 * 1000; // 10 मिनट

// पेज लोड होने के बाद टाइमर शुरू करें
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔄 ऑटो-रिफ्रेश शुरू: हर 10 मिनट में');
    
    // तुरंत एक बार चलाएं (पेज लोड होते ही)
    setTimeout(() => {
        refreshMarketData();
    }, 5000); // 5 सेकंड बाद पहला रिफ्रेश
    
    // फिर हर 10 मिनट में
    setInterval(refreshMarketData, REFRESH_INTERVAL);
});

// यूजर को स्टेटस दिखाने के लिए
let lastUpdate = new Date();
setInterval(() => {
    lastUpdate = new Date();
    const statusElement = document.getElementById('live-status');
    if (statusElement) {
        statusElement.textContent = `🟢 लाइव | अंतिम अपडेट: ${lastUpdate.toLocaleTimeString()}`;
    }
}, 1000);
