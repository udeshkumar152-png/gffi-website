// ============================================
// FUNCTIONS.JS - All render functions (NEVER CHANGES)
// ============================================

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
// RENDER FUNCTIONS
// ============================================
function renderCountryGrid() {
    const container = document.getElementById('country-grid');
    if (!container) {
        console.error('country-grid container not found');
        return;
    }
    
    if (!countryData || !Array.isArray(countryData)) {
        console.error('countryData is not available');
        return;
    }
    
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
    console.log('✅ Country grid rendered');
}

function renderSectorGrid() {
    const container = document.getElementById('sector-grid');
    if (!container) {
        console.error('sector-grid container not found');
        return;
    }
    
    if (!sectorData || !Array.isArray(sectorData)) {
        console.error('sectorData is not available');
        return;
    }
    
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
    console.log('✅ Sector grid rendered');
}

function renderStockGrid() {
    const container = document.querySelector('.picks-container');
    if (!container) {
        console.error('picks-container not found');
        return;
    }
    
    if (!stockPicks) {
        console.error('stockPicks is not available');
        return;
    }
    
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
    console.log('✅ Stock grid rendered');
}

function renderIndiaGrid() {
    const container = document.querySelector('.india-cards');
    if (!container) {
        console.error('india-cards container not found');
        return;
    }
    
    // Check if indiaMarketData exists
    if (!indiaMarketData) {
        console.error('indiaMarketData is not available');
        return;
    }
    
    // Check if countryData exists and has India
    let indiaGffi = 64.7;  // default value
    let indiaStatus = 'success';  // default status
    
    if (countryData && Array.isArray(countryData)) {
        const indiaData = countryData.find(c => c && c.name === 'India');
        if (indiaData) {
            indiaGffi = indiaData.gffi;
            indiaStatus = indiaData.status;
        }
    }
    
    let html = `
        <div class="india-card nifty-card">
            <div class="card-icon">📈</div>
            <div class="card-content">
                <span class="card-label">Nifty 50</span>
                <span class="card-value">${indiaMarketData.nifty ? indiaMarketData.nifty.toLocaleString() : '77,566'}</span>
                <span class="card-change ${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.nifty_change > 0 ? '+' : ''}${indiaMarketData.nifty_change || '-1.71'}%</span>
            </div>
        </div>
        <div class="india-card sensex-card">
            <div class="card-icon">📊</div>
            <div class="card-content">
                <span class="card-label">Sensex</span>
                <span class="card-value">${indiaMarketData.sensex ? indiaMarketData.sensex.toLocaleString() : '77,566'}</span>
                <span class="card-change ${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.sensex_change > 0 ? '+' : ''}${indiaMarketData.sensex_change || '-1.71'}%</span>
            </div>
        </div>
        <div class="india-card vix-card">
            <div class="card-icon">⚡</div>
            <div class="card-content">
                <span class="card-label">India VIX</span>
                <span class="card-value">${indiaMarketData.vix ? indiaMarketData.vix.toFixed(2) : '23.36'}</span>
                <span class="card-change ${indiaMarketData.vix_change > 0 ? 'negative' : 'positive'}">${indiaMarketData.vix_change > 0 ? '+' : ''}${indiaMarketData.vix_change || '17.58'}%</span>
            </div>
        </div>
        <div class="india-card gffi-card">
            <div class="card-icon">🛡️</div>
            <div class="card-content">
                <span class="card-label">India GFFI</span>
                <span class="card-value">${indiaGffi}</span>
                <span class="card-status status-${indiaStatus}">${indiaStatus === 'success' ? '🟢 SUCCESS' : '🟡 WATCH'}</span>
            </div>
        </div>
    `;
    container.innerHTML = html;
    
    // Update market status
    const marketStatusEl = document.getElementById('market-status');
    if (marketStatusEl) {
        marketStatusEl.textContent = indiaMarketData.nifty_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH';
    }
    
    const fearLevelEl = document.getElementById('fear-level');
    if (fearLevelEl) {
        const vix = indiaMarketData.vix || 23.36;
        if (vix > 25) fearLevelEl.textContent = '😱 EXTREME FEAR';
        else if (vix > 20) fearLevelEl.textContent = '😨 FEAR';
        else fearLevelEl.textContent = '😐 NEUTRAL';
    }
    
    const advDeclEl = document.getElementById('adv-decl');
    if (advDeclEl) {
        advDeclEl.textContent = `${indiaMarketData.advance || 850} / ${indiaMarketData.decline || 1650}`;
    }
    
    console.log('✅ India grid rendered');
}

// ============================================
// TABLE VIEW FUNCTIONS
// ============================================
function renderCountryTable() {
    const container = document.getElementById('country-grid');
    if (!container) return;
    
    if (!countryData || !Array.isArray(countryData)) {
        console.error('countryData is not available');
        return;
    }
    
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
    if (!container) return;
    
    if (!sectorData || !Array.isArray(sectorData)) {
        console.error('sectorData is not available');
        return;
    }
    
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
    if (!container) return;
    
    if (!stockPicks) {
        console.error('stockPicks is not available');
        return;
    }
    
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
    if (!container) return;
    
    if (!indiaMarketData) {
        console.error('indiaMarketData is not available');
        return;
    }
    
    // Get India data from countryData
    let indiaGffi = 64.7;
    let indiaStatus = 'success';
    
    if (countryData && Array.isArray(countryData)) {
        const indiaData = countryData.find(c => c && c.name === 'India');
        if (indiaData) {
            indiaGffi = indiaData.gffi;
            indiaStatus = indiaData.status;
        }
    }
    
    let html = '<table class="data-table"><tr><th>Indicator</th><th>Value</th><th>Change</th><th>Status</th></tr>';
    
    html += `<tr>
        <td><strong>📈 Nifty 50</strong></td>
        <td class="gffi-value">${indiaMarketData.nifty ? indiaMarketData.nifty.toLocaleString() : '77,566'}</td>
        <td class="${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.nifty_change > 0 ? '+' : ''}${indiaMarketData.nifty_change || '-1.71'}%</td>
        <td>${indiaMarketData.nifty_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH'}</td>
    </tr>`;
    
    html += `<tr>
        <td><strong>📊 Sensex</strong></td>
        <td class="gffi-value">${indiaMarketData.sensex ? indiaMarketData.sensex.toLocaleString() : '77,566'}</td>
        <td class="${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">${indiaMarketData.sensex_change > 0 ? '+' : ''}${indiaMarketData.sensex_change || '-1.71'}%</td>
        <td>${indiaMarketData.sensex_change < 0 ? '🔴 BEARISH' : '🟢 BULLISH'}</td>
    </tr>`;
    
    html += `<tr>
        <td><strong>⚡ India VIX</strong></td>
        <td class="gffi-value">${indiaMarketData.vix ? indiaMarketData.vix.toFixed(2) : '23.36'}</td>
        <td class="${indiaMarketData.vix_change > 0 ? 'negative' : 'positive'}">${indiaMarketData.vix_change > 0 ? '+' : ''}${indiaMarketData.vix_change || '17.58'}%</td>
        <td>${indiaMarketData.vix > 25 ? '😱 EXTREME FEAR' : indiaMarketData.vix > 20 ? '😨 FEAR' : '😐 NEUTRAL'}</td>
    </tr>`;
    
    html += `<tr>
        <td><strong>🛡️ India GFFI</strong></td>
        <td class="gffi-value">${indiaGffi}</td>
        <td>-</td>
        <td><span class="status-${indiaStatus}">${indiaStatus.toUpperCase()}</span></td>
    </tr>`;
    
    html += `<tr>
        <td><strong>📊 Advance/Decline</strong></td>
        <td colspan="3">${indiaMarketData.advance || 850} Advances / ${indiaMarketData.decline || 1650} Declines</td>
    </tr>`;
    
    html += '</table>';
    container.innerHTML = html;
}

// ============================================
// TOGGLE FUNCTIONS
// ============================================
function toggleCountryView() {
    const btn = document.getElementById('toggle-country');
    if (!btn) return;
    
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
    if (!btn) return;
    
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
    if (!btn) return;
    
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
    if (!btn) return;
    
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
// LIVE STATUS UPDATE
// ============================================
function updateLiveStatus() {
    const liveStatusEl = document.getElementById('live-status');
    if (liveStatusEl) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
        liveStatusEl.innerHTML = `🟢 लाइव | अंतिम अपडेट: ${timeStr}`;
    }
}

// Auto-refresh every minute
setInterval(updateLiveStatus, 60000);

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 GFFI Dashboard Initializing...');
    
    // Check if data is loaded
    if (typeof globalGFFI !== 'undefined') {
        document.getElementById('global-gffi').textContent = globalGFFI;
    }
    
    if (typeof updateDate !== 'undefined') {
        document.getElementById('update-time').textContent = updateDate;
    }
    
    if (typeof updateTime !== 'undefined') {
        document.getElementById('update-time-hm').textContent = updateTime;
    }
    
    // Render initial views
    renderCountryGrid();
    renderSectorGrid();
    renderStockGrid();
    renderIndiaGrid();
    
    // Add event listeners
    const toggleCountry = document.getElementById('toggle-country');
    if (toggleCountry) toggleCountry.addEventListener('click', toggleCountryView);
    
    const toggleSector = document.getElementById('toggle-sector');
    if (toggleSector) toggleSector.addEventListener('click', toggleSectorView);
    
    const toggleStock = document.getElementById('toggle-stock');
    if (toggleStock) toggleStock.addEventListener('click', toggleStockView);
    
    const toggleIndia = document.getElementById('toggle-india');
    if (toggleIndia) toggleIndia.addEventListener('click', toggleIndiaView);
    
    // Initial live status
    // ============================================
// CORE METRICS PANEL FUNCTIONS
// ============================================

function calculateCrisisProbability() {
    // Simple probability based on GFFI
    const gffi = globalGFFI || 63.5;
    const threshold = 72.8;
    
    if (gffi >= threshold) {
        return 85; // High probability
    } else if (gffi >= 65) {
        return 60 + (gffi - 65) * 2; // 60-75%
    } else if (gffi >= 58) {
        return 30 + (gffi - 58) * 3; // 30-50%
    } else {
        return 15 + (gffi - 50) * 1.5; // 15-30%
    }
}

function getTrend() {
    if (!countryData || countryData.length === 0) return { direction: 'Stable', change: 0 };
    
    // Calculate average change in last 3 months (simplified)
    const avgGffi = countryData.reduce((sum, c) => sum + c.gffi, 0) / countryData.length;
    const previousAvg = avgGffi * 0.95; // Simplified - in real app, use historical data
    
    const change = ((avgGffi - previousAvg) / previousAvg) * 100;
    
    if (change > 2) return { direction: '↑ Rising', change: change.toFixed(1) };
    if (change < -2) return { direction: '↓ Falling', change: change.toFixed(1) };
    return { direction: '→ Stable', change: change.toFixed(1) };
}

function getRiskLevel(gffi) {
    if (gffi >= 70) return { text: 'CRITICAL', badge: '🔴' };
    if (gffi >= 65) return { text: 'WARNING', badge: '🟠' };
    if (gffi >= 58) return { text: 'WATCH', badge: '🟡' };
    return { text: 'SAFE', badge: '🟢' };
}

function updateCoreMetrics() {
    const gffi = globalGFFI || 63.5;
    
    // Update GFFI Score
    const gffiEl = document.getElementById('global-gffi');
    if (gffiEl) gffiEl.textContent = gffi;
    
    // Update Risk Level
    const risk = getRiskLevel(gffi);
    const riskTextEl = document.getElementById('risk-level-text');
    const riskBadgeEl = document.getElementById('risk-badge');
    if (riskTextEl) riskTextEl.textContent = risk.text;
    if (riskBadgeEl) riskBadgeEl.textContent = risk.badge;
    
    // Update Probability
    const probEl = document.getElementById('crisis-probability');
    if (probEl) probEl.textContent = Math.round(calculateCrisisProbability()) + '%';
    
    // Update Trend
    const trend = getTrend();
    const trendTextEl = document.getElementById('trend-text');
    const trendChangeEl = document.getElementById('trend-change');
    if (trendTextEl) trendTextEl.textContent = trend.direction;
    if (trendChangeEl) {
        trendChangeEl.textContent = (trend.change > 0 ? '+' : '') + trend.change + '%';
        trendChangeEl.className = `metric-change trend-${trend.direction.includes('Rising') ? 'up' : trend.direction.includes('Falling') ? 'down' : 'stable'}`;
    }
}

// Update initialization section
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 GFFI Dashboard Initializing...');
    
    // Update core metrics first
    updateCoreMetrics();
    
    // Set global values
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
    
    // Update live status
    updateLiveStatus();
    setInterval(updateCoreMetrics, 60000); // Update every minute
    
    console.log('✅ GFFI Dashboard Ready!');
});
    updateLiveStatus();
    
    console.log('✅ GFFI Dashboard Ready!');
});
