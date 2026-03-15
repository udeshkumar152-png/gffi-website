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

// ============================================
// SECTOR DATA
// ============================================
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

// ============================================
// STOCK PICKS
// ============================================
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

// ============================================
// INDIA MARKET DATA
// ============================================
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
// TABLE VIEW FUNCTIONS
// ============================================

// Country Grid Toggle
function toggleCountryView() {
    const grid = document.getElementById('country-grid');
    const btn = document.getElementById('toggle-country');
    
    if (grid.classList.contains('table-view')) {
        grid.classList.remove('table-view');
        btn.textContent = '📊 Switch to Table View';
        renderCountryGrid();
    } else {
        grid.classList.add('table-view');
        btn.textContent = '🖼️ Switch to Grid View';
        
        let html = '<table class="data-table"><tr><th>Country</th><th>GFFI</th><th>Status</th></tr>';
        countryData.forEach(c => {
            let statusClass = c.status === 'success' ? 'status-success' : 
                             c.status === 'warning' ? 'status-warning' : 'status-alert';
            html += `<tr>
                <td>${c.flag} ${c.name}</td>
                <td><strong>${c.gffi}</strong></td>
                <td><span class="${statusClass}">${c.status.toUpperCase()}</span></td>
            </tr>`;
        });
        html += '</table>';
        grid.innerHTML = html;
    }
}

// Sector Table Toggle
function toggleSectorView() {
    const grid = document.getElementById('sector-grid');
    const btn = document.getElementById('toggle-sector');
    
    if (grid.classList.contains('table-view')) {
        grid.classList.remove('table-view');
        btn.textContent = '📊 Switch to Table View';
        renderSectorAnalysis();
    } else {
        grid.classList.add('table-view');
        btn.textContent = '🖼️ Switch to Grid View';
        
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
                <td><strong>${s.gffi.toFixed(1)}</strong></td>
                <td><span class="${statusClass}">${statusText}</span></td>
                <td>${trendIcon}</td>
                <td>${s.stocks.slice(0, 3).join(', ')}</td>
            </tr>`;
        });
        html += '</table>';
        grid.innerHTML = html;
    }
}

// Stock Picks Table Toggle
function toggleStockView() {
    const container = document.getElementById('stock-picks-container');
    const btn = document.getElementById('toggle-stock');
    const safeDiv = document.getElementById('safe-picks');
    const riskyDiv = document.getElementById('risky-picks');
    const watchDiv = document.getElementById('watch-picks');
    
    if (container.classList.contains('table-view')) {
        container.classList.remove('table-view');
        btn.textContent = '📊 Switch to Table View';
        renderStockPicks();
    } else {
        container.classList.add('table-view');
        btn.textContent = '🖼️ Switch to Grid View';
        
        let html = '<table class="data-table"><tr><th>Category</th><th>Symbol</th><th>GFFI</th><th>Action</th><th>Reason</th></tr>';
        
        stockPicks.safe.forEach(s => {
            html += `<tr><td>🟢 SAFE</td><td><strong>${s.symbol}</strong></td><td>${s.gffi}</td><td><span class="stock-action buy">${s.action}</span></td><td>${s.reason}</td></tr>`;
        });
        stockPicks.risky.forEach(s => {
            html += `<tr><td>🔴 RISKY</td><td><strong>${s.symbol}</strong></td><td>${s.gffi}</td><td><span class="stock-action sell">${s.action}</span></td><td>${s.reason}</td></tr>`;
        });
        stockPicks.watch.forEach(s => {
            html += `<tr><td>🟡 WATCH</td><td><strong>${s.symbol}</strong></td><td>${s.gffi}</td><td><span class="stock-action watch">${s.action}</span></td><td>${s.reason}</td></tr>`;
        });
        
        html += '</table>';
        
        // Hide individual divs and show table
        safeDiv.style.display = 'none';
        riskyDiv.style.display = 'none';
        watchDiv.style.display = 'none';
        
        let tableDiv = document.getElementById('stock-table');
        if (!tableDiv) {
            tableDiv = document.createElement('div');
            tableDiv.id = 'stock-table';
            container.appendChild(tableDiv);
        }
        tableDiv.innerHTML = html;
    }
}

// India Dashboard Table
function renderIndiaTable() {
    const container = document.querySelector('.india-cards');
    const btn = document.getElementById('toggle-india');
    
    if (container.classList.contains('table-view')) {
        container.classList.remove('table-view');
        btn.textContent = '📊 Switch to Table View';
        renderIndiaMarket();
    } else {
        container.classList.add('table-view');
        btn.textContent = '🖼️ Switch to Cards View';
        
        let html = '<table class="data-table"><tr><th>Indicator</th><th>Value</th><th>Change</th></tr>';
        html += `<tr><td>📈 Nifty 50</td><td><strong>${indiaMarketData.nifty.toLocaleString()}</strong></td><td class="${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.nifty_change > 0 ? '+' : ''}${indiaMarketData.nifty_change}%</td></tr>`;
        html += `<tr><td>📊 Sensex</td><td><strong>${indiaMarketData.sensex.toLocaleString()}</strong></td><td class="${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.sensex_change > 0 ? '+' : ''}${indiaMarketData.sensex_change}%</td></tr>`;
        html += `<tr><td>⚡ India VIX</td><td><strong>${indiaMarketData.vix.toFixed(2)}</strong></td><td class="${indiaMarketData.vix_change > 0 ? 'negative' : 'positive'}">${indiaMarketData.vix_change > 0 ? '+' : ''}${indiaMarketData.vix_change}%</td></tr>`;
        
        const indiaData = countryData.find(c => c.name === 'India');
        html += `<tr><td>🛡️ India GFFI</td><td><strong>${indiaData.gffi}</strong></td><td><span class="status-${indiaData.status}">${indiaData.status.toUpperCase()}</span></td></tr>`;
        html += '</table>';
        
        container.innerHTML = html;
    }
}

// ============================================
// RENDER FUNCTIONS (Original)
// ============================================

function renderCountryGrid() {
    const grid = document.getElementById('country-grid');
    if (!grid) return;
    
    let html = '';
    countryData.forEach(c => {
        html += `<div class="country-card">
            <div class="country-flag">${c.flag}</div>
            <div class="country-name">${c.name}</div>
            <div class="country-gffi">${c.gffi}</div>
            <span class="country-status status-${c.status}">${c.status.toUpperCase()}</span>
        </div>`;
    });
    grid.innerHTML = html;
}

function renderSectorAnalysis() {
    const grid = document.getElementById('sector-grid');
    if (!grid) return;
    
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
    grid.innerHTML = html;
}

function renderStockPicks() {
    const safeDiv = document.getElementById('safe-picks');
    if (safeDiv) {
        safeDiv.style.display = 'block';
        safeDiv.innerHTML = stockPicks.safe.map(s => 
            `<div class="stock-item"><span class="stock-symbol">${s.symbol}</span> <span class="stock-gffi">${s.gffi}</span> <span class="stock-action buy">${s.action}</span></div>
             <div style="font-size:0.8rem; color:#6c757d;">${s.reason}</div>`
        ).join('');
    }
    
    const riskyDiv = document.getElementById('risky-picks');
    if (riskyDiv) {
        riskyDiv.style.display = 'block';
        riskyDiv.innerHTML = stockPicks.risky.map(s => 
            `<div class="stock-item"><span class="stock-symbol">${s.symbol}</span> <span class="stock-gffi">${s.gffi}</span> <span class="stock-action sell">${s.action}</span></div>
             <div style="font-size:0.8rem; color:#6c757d;">${s.reason}</div>`
        ).join('');
    }
    
    const watchDiv = document.getElementById('watch-picks');
    if (watchDiv) {
        watchDiv.style.display = 'block';
        watchDiv.innerHTML = stockPicks.watch.map(s => 
            `<div class="stock-item"><span class="stock-symbol">${s.symbol}</span> <span class="stock-gffi">${s.gffi}</span> <span class="stock-action watch">${s.action}</span></div>
             <div style="font-size:0.8rem; color:#6c757d;">${s.reason}</div>`
        ).join('');
    }
    
    // Remove any existing table
    const existingTable = document.getElementById('stock-table');
    if (existingTable) existingTable.remove();
}

function renderIndiaMarket() {
    const container = document.querySelector('.india-cards');
    container.classList.remove('table-view');
    
    let html = `
        <div class="india-card nifty-card">
            <div class="card-icon">📈</div>
            <div class="card-content">
                <span class="card-label">Nifty 50</span>
                <span class="card-value" id="nifty-value">${indiaMarketData.nifty.toLocaleString()}</span>
                <span class="card-change ${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.nifty_change > 0 ? '+' : ''}${indiaMarketData.nifty_change}%</span>
            </div>
        </div>
        <div class="india-card sensex-card">
            <div class="card-icon">📊</div>
            <div class="card-content">
                <span class="card-label">Sensex</span>
                <span class="card-value" id="sensex-value">${indiaMarketData.sensex.toLocaleString()}</span>
                <span class="card-change ${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.sensex_change > 0 ? '+' : ''}${indiaMarketData.sensex_change}%</span>
            </div>
        </div>
        <div class="india-card vix-card">
            <div class="card-icon">⚡</div>
            <div class="card-content">
                <span class="card-label">India VIX</span>
                <span class="card-value" id="vix-value">${indiaMarketData.vix.toFixed(2)}</span>
                <span class="card-change ${indiaMarketData.vix_change > 0 ? 'negative' : 'positive'}">${indiaMarketData.vix_change > 0 ? '+' : ''}${indiaMarketData.vix_change}%</span>
            </div>
        </div>
        <div class="india-card gffi-card">
            <div class="card-icon">🛡️</div>
            <div class="card-content">
                <span class="card-label">India GFFI</span>
                <span class="card-value" id="india-gffi">${countryData.find(c => c.name === 'India').gffi}</span>
                <span class="card-status status-${countryData.find(c => c.name === 'India').status}">${countryData.find(c => c.name === 'India').status === 'success' ? '🟢 SUCCESS' : '🟡 WATCH'}</span>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Update status bar
    document.getElementById('market-status').textContent = indiaMarketData.nifty_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH';
    
    if (indiaMarketData.vix > 25) document.getElementById('fear-level').textContent = '😱 EXTREME FEAR';
    else if (indiaMarketData.vix > 20) document.getElementById('fear-level').textContent = '😨 FEAR';
    else document.getElementById('fear-level').textContent = '😐 NEUTRAL';
    
    document.getElementById('adv-decl').textContent = `${indiaMarketData.advance} / ${indiaMarketData.decline}`;
}

// ============================================
// ADD TOGGLE BUTTONS TO HTML
// ============================================

function addToggleButtons() {
    // Country toggle
    const countrySection = document.querySelector('.country-grid');
    if (countrySection && !document.getElementById('toggle-country')) {
        const btn = document.createElement('button');
        btn.id = 'toggle-country';
        btn.className = 'toggle-btn';
        btn.textContent = '📊 Switch to Table View';
        btn.onclick = toggleCountryView;
        countrySection.parentNode.insertBefore(btn, countrySection);
    }
    
    // Sector toggle
    const sectorSection = document.getElementById('sector-grid');
    if (sectorSection && !document.getElementById('toggle-sector')) {
        const btn = document.createElement('button');
        btn.id = 'toggle-sector';
        btn.className = 'toggle-btn';
        btn.textContent = '📊 Switch to Table View';
        btn.onclick = toggleSectorView;
        sectorSection.parentNode.insertBefore(btn, sectorSection);
    }
    
    // Stock toggle
    const stockSection = document.getElementById('stock-picks-container');
    if (stockSection && !document.getElementById('toggle-stock')) {
        const btn = document.createElement('button');
        btn.id = 'toggle-stock';
        btn.className = 'toggle-btn';
        btn.textContent = '📊 Switch to Table View';
        btn.onclick = toggleStockView;
        stockSection.parentNode.insertBefore(btn, stockSection);
    }
    
    // India toggle
    const indiaSection = document.querySelector('.india-cards');
    if (indiaSection && !document.getElementById('toggle-india')) {
        const btn = document.createElement('button');
        btn.id = 'toggle-india';
        btn.className = 'toggle-btn';
        btn.textContent = '📊 Switch to Table View';
        btn.onclick = renderIndiaTable;
        indiaSection.parentNode.insertBefore(btn, indiaSection);
    }
}

// ============================================
// CSS STYLES
// ============================================

const styles = `
.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.data-table th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: bold;
    padding: 12px;
    text-align: left;
}
.data-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #e0e0e0;
}
.data-table tr:hover {
    background-color: #f5f5f5;
}
.status-success { background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; }
.status-warning { background: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 4px; }
.status-alert { background: #ffe5d0; color: #9a3412; padding: 4px 8px; border-radius: 4px; }
.status-critical { background: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 4px; }
.positive { color: #00a65a; font-weight: bold; }
.negative { color: #dd4b39; font-weight: bold; }
.toggle-btn {
    margin: 10px 0;
    padding: 8px 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    transition: transform 0.3s;
}
.toggle-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102,126,234,0.4);
}
`;

// Add styles to document
const styleSheet = document.createElement("style");
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// ============================================
// INITIALIZE
// ============================================

function updateDashboard() {
    document.getElementById('global-gffi').textContent = globalGFFI;
    document.getElementById('update-time').textContent = updateDate;
    document.getElementById('update-time-hm').textContent = updateTime;
    
    renderCountryGrid();
    renderSectorAnalysis();
    renderStockPicks();
    renderIndiaMarket();
    addToggleButtons();
}

document.addEventListener('DOMContentLoaded', updateDashboard);
