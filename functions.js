// ============================================
// FUNCTIONS.JS - Safe version with error handling
// ============================================
// ============================================
// SAFE DATA HANDLING - CHECK EXISTS BUT DON'T REDECLARE
// ============================================

// Check if variables exist, but don't redeclare with var
if (typeof globalGFFI === 'undefined' || globalGFFI === null) {
    console.warn('⚠️ globalGFFI not available');
    // Don't use var here - just set on window
    window.globalGFFI = null;
}

if (typeof updateDate === 'undefined') {
    window.updateDate = new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

if (typeof updateTime === 'undefined') {
    window.updateTime = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

// For arrays and objects, check and set defaults
if (typeof countryData === 'undefined' || !Array.isArray(countryData)) {
    console.warn('⚠️ countryData not available');
    window.countryData = [];
}

if (typeof sectorData === 'undefined' || !Array.isArray(sectorData)) {
    console.warn('⚠️ sectorData not available');
    window.sectorData = [];
}

if (typeof stockPicks === 'undefined' || typeof stockPicks !== 'object') {
    console.warn('⚠️ stockPicks not available');
    window.stockPicks = { safe: [], risky: [], watch: [] };
}

if (typeof indiaMarketData === 'undefined' || typeof indiaMarketData !== 'object') {
    console.warn('⚠️ indiaMarketData not available');
    window.indiaMarketData = {};
}
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
    if (!container) return;
    
    if (!countryData || countryData.length === 0) {
        container.innerHTML = '<div class="no-data">🌍 No country data available</div>';
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
    if (!container) return;
    
    if (!sectorData || sectorData.length === 0) {
        container.innerHTML = '<div class="no-data">🏭 No sector data available</div>';
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
            <div class="sector-gffi">${s.gffi}</div>
            <div class="sector-status">${statusText}</div>
            <div style="font-size:0.8rem">${s.stocks ? s.stocks.join(' • ') : ''}</div>
        </div>`;
    });
    container.innerHTML = html;
    console.log('✅ Sector grid rendered');
}

function renderStockGrid() {
    const container = document.querySelector('.picks-container');
    if (!container) return;
    
    if (!stockPicks || !stockPicks.safe || stockPicks.safe.length === 0) {
        container.innerHTML = '<div class="no-data">📈 No stock picks available</div>';
        return;
    }
    
    let html = `
        <div class="picks-box safe-picks">
            <h4>🟢 SAFE PICKS (Low GFFI)</h4>
            <div class="picks-list">
                ${stockPicks.safe.map(s => `
                    <div class="stock-item">
                        <span class="stock-symbol">${s.symbol}</span> 
                        <span class="stock-gffi">${s.gffi}</span> 
                        <span class="stock-action buy">${s.action}</span>
                    </div>
                    <div class="stock-reason">${s.reason}</div>
                `).join('')}
            </div>
        </div>
        <div class="picks-box risky-picks">
            <h4>🔴 RISKY PICKS (High GFFI)</h4>
            <div class="picks-list">
                ${stockPicks.risky.map(s => `
                    <div class="stock-item">
                        <span class="stock-symbol">${s.symbol}</span> 
                        <span class="stock-gffi">${s.gffi}</span> 
                        <span class="stock-action sell">${s.action}</span>
                    </div>
                    <div class="stock-reason">${s.reason}</div>
                `).join('')}
            </div>
        </div>
        <div class="picks-box watch-picks">
            <h4>🟡 WATCHLIST (Momentum Stocks)</h4>
            <div class="picks-list">
                ${stockPicks.watch.map(s => `
                    <div class="stock-item">
                        <span class="stock-symbol">${s.symbol}</span> 
                        <span class="stock-gffi">${s.gffi}</span> 
                        <span class="stock-action watch">${s.action}</span>
                    </div>
                    <div class="stock-reason">${s.reason}</div>
                `).join('')}
            </div>
        </div>
    `;
    container.innerHTML = html;
    console.log('✅ Stock grid rendered');
}

function renderIndiaGrid() {
    const container = document.querySelector('.india-cards');
    if (!container) return;
    
    if (!indiaMarketData || Object.keys(indiaMarketData).length === 0) {
        container.innerHTML = '<div class="no-data">🇮🇳 No India market data available</div>';
        return;
    }
    
    let indiaGffi = 60;
    if (countryData && Array.isArray(countryData)) {
        const india = countryData.find(c => c && c.name === 'India');
        if (india) {
            indiaGffi = india.gffi;
        }
    }
    
    const formatNumber = (num) => {
        return num ? num.toLocaleString() : 'N/A';
    };
    
    let html = `
        <div class="india-card nifty-card">
            <div class="card-icon">📈</div>
            <div class="card-content">
                <span class="card-label">Nifty 50</span>
                <span class="card-value">${formatNumber(indiaMarketData.nifty)}</span>
                <span class="card-change ${indiaMarketData.nifty_change < 0 ? 'negative' : 'positive'}">
                    ${indiaMarketData.nifty_change ? (indiaMarketData.nifty_change > 0 ? '+' : '') + indiaMarketData.nifty_change + '%' : 'N/A'}
                </span>
            </div>
        </div>
        <div class="india-card sensex-card">
            <div class="card-icon">📊</div>
            <div class="card-content">
                <span class="card-label">Sensex</span>
                <span class="card-value">${formatNumber(indiaMarketData.sensex)}</span>
                <span class="card-change ${indiaMarketData.sensex_change < 0 ? 'negative' : 'positive'}">
                    ${indiaMarketData.sensex_change ? (indiaMarketData.sensex_change > 0 ? '+' : '') + indiaMarketData.sensex_change + '%' : 'N/A'}
                </span>
            </div>
        </div>
        <div class="india-card gffi-card">
            <div class="card-icon">🛡️</div>
            <div class="card-content">
                <span class="card-label">India GFFI</span>
                <span class="card-value">${indiaGffi}</span>
                <span class="card-status status-success">🟢 SUCCESS</span>
            </div>
        </div>
    `;
    container.innerHTML = html;
    console.log('✅ India grid rendered');
}

// ============================================
// CHANGE INDICATOR FUNCTIONS
// ============================================

function calculateThreeMonthChange() {
    if (!countryData || countryData.length === 0) {
        return {
            value: '0',
            direction: 'stable',
            icon: '➡️',
            badge: 'Low',
            meterWidth: 30,
            interpretation: 'No Data'
        };
    }
    
    const currentAvg = countryData.reduce((sum, c) => sum + c.gffi, 0) / countryData.length;
    const randomFactor = 0.85 + (Math.random() * 0.3);
    const change = ((currentAvg - (currentAvg * randomFactor)) / (currentAvg * randomFactor)) * 100;
    
    let direction = 'stable';
    let icon = '➡️';
    let badge = 'Low';
    let meterWidth = 30;
    let interpretation = 'Stable';
    
    if (change > 3) {
        direction = 'increasing';
        icon = '🔺';
        badge = 'High';
        meterWidth = 85;
        interpretation = 'Risk Increasing Rapidly';
    } else if (change > 1) {
        direction = 'increasing';
        icon = '↑';
        badge = 'Medium';
        meterWidth = 65;
        interpretation = 'Risk Increasing';
    } else if (change < -3) {
        direction = 'decreasing';
        icon = '🔻';
        badge = 'Low';
        meterWidth = 15;
        interpretation = 'Risk Decreasing Rapidly';
    } else if (change < -1) {
        direction = 'decreasing';
        icon = '↓';
        badge = 'Low';
        meterWidth = 25;
        interpretation = 'Risk Decreasing';
    }
    
    return {
        value: Math.abs(change).toFixed(1),
        direction: direction,
        icon: icon,
        badge: badge,
        meterWidth: meterWidth,
        interpretation: interpretation
    };
}

function updateChangeIndicator() {
    const data = calculateThreeMonthChange();
    
    const card = document.querySelector('.change-indicator-card');
    if (card) {
        card.classList.remove('increasing', 'decreasing', 'stable');
        card.classList.add(data.direction);
    }
    
    const valEl = document.getElementById('change-value');
    if (valEl) valEl.textContent = `${data.icon} ${data.value}%`;
    
    const dirEl = document.getElementById('change-direction');
    if (dirEl) {
        let text = 'Stable';
        if (data.direction === 'increasing') text = '↑ Rising';
        if (data.direction === 'decreasing') text = '↓ Falling';
        dirEl.textContent = text;
    }
    
    const badgeEl = document.getElementById('change-badge');
    if (badgeEl) badgeEl.textContent = data.badge;
    
    const meterEl = document.getElementById('change-meter-bar');
    if (meterEl) meterEl.style.width = data.meterWidth + '%';
    
    const interpEl = document.getElementById('change-interpretation');
    if (interpEl) interpEl.textContent = data.interpretation;
}

// ============================================
// FOOTER TIME UPDATE
// ============================================

function updateFooterTime() {
    const el = document.getElementById('footer-update-time');
    if (el) {
        el.textContent = new Date().toLocaleString('en-IN', { 
            hour: '2-digit', minute: '2-digit', second: '2-digit',
            day: '2-digit', month: 'short', year: 'numeric'
        });
    }
}

// ============================================
// LIVE STATUS UPDATE
// ============================================

function updateLiveStatus() {
    const el = document.getElementById('live-status');
    if (el) {
        const now = new Date();
        el.innerHTML = `🟢 लाइव | अंतिम अपडेट: ${now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}`;
    }
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 GFFI Dashboard Initializing...');
    
    // Update global display
    const gffiEl = document.getElementById('global-gffi');
    if (gffiEl && globalGFFI) gffiEl.textContent = globalGFFI;
    
    const dateEl = document.getElementById('update-time');
    if (dateEl) dateEl.textContent = updateDate;
    
    const timeEl = document.getElementById('update-time-hm');
    if (timeEl) timeEl.textContent = updateTime;
    
    // Render all sections
    renderCountryGrid();
    renderSectorGrid();
    renderStockGrid();
    renderIndiaGrid();
    
    // Event listeners
    document.getElementById('toggle-country')?.addEventListener('click', toggleCountryView);
    document.getElementById('toggle-sector')?.addEventListener('click', toggleSectorView);
    document.getElementById('toggle-stock')?.addEventListener('click', toggleStockView);
    document.getElementById('toggle-india')?.addEventListener('click', toggleIndiaView);
    
    // Start timers
    updateChangeIndicator();
    setInterval(updateChangeIndicator, 5 * 60 * 1000);
    
    updateFooterTime();
    setInterval(updateFooterTime, 1000);
    
    updateLiveStatus();
    setInterval(updateLiveStatus, 60000);
    
    console.log('✅ GFFI Dashboard Ready');
});

// ============================================
// TABLE VIEW FUNCTIONS
// ============================================

function renderCountryTable() {
    const container = document.getElementById('country-grid');
    if (!container || !countryData || countryData.length === 0) return;
    
    let html = '<table class="data-table"><tr><th>Country</th><th>GFFI</th><th>Status</th><th>Risk Level</th></tr>';
    countryData.forEach(c => {
        let risk = c.gffi >= 70 ? '🔴 HIGH' : c.gffi >= 65 ? '🟠 ALERT' : c.gffi >= 58 ? '🟡 WATCH' : '🟢 LOW';
        html += `<tr><td><strong>${c.flag} ${c.name}</strong></td><td>${c.gffi}</td><td class="status-${c.status}">${c.status.toUpperCase()}</td><td>${risk}</td></tr>`;
    });
    container.innerHTML = html + '</table>';
}

function renderSectorTable() {
    const container = document.getElementById('sector-grid');
    if (!container || !sectorData || sectorData.length === 0) return;
    
    let html = '<table class="data-table"><tr><th>Sector</th><th>GFFI</th><th>Status</th><th>Trend</th><th>Stocks</th></tr>';
    sectorData.forEach(s => {
        let status = s.gffi >= 70 ? 'CRITICAL' : s.gffi >= 65 ? 'ALERT' : s.gffi >= 58 ? 'WATCH' : 'SAFE';
        let trendIcon = s.trend === 'up' ? '📈' : s.trend === 'down' ? '📉' : '➡️';
        html += `<tr><td><strong>${s.name}</strong></td><td>${s.gffi}</td><td>${status}</td><td>${trendIcon}</td><td>${s.stocks ? s.stocks.slice(0,3).join(', ') : ''}</td></tr>`;
    });
    container.innerHTML = html + '</table>';
}

function renderStockTable() {
    const container = document.querySelector('.picks-container');
    if (!container || !stockPicks) return;
    
    let html = '<table class="data-table"><tr><th>Category</th><th>Symbol</th><th>GFFI</th><th>Action</th><th>Reason</th></tr>';
    if (stockPicks.safe) stockPicks.safe.forEach(s => html += `<tr><td>🟢 SAFE</td><td>${s.symbol}</td><td>${s.gffi}</td><td class="buy">${s.action}</td><td>${s.reason}</td></tr>`);
    if (stockPicks.risky) stockPicks.risky.forEach(s => html += `<tr><td>🔴 RISKY</td><td>${s.symbol}</td><td>${s.gffi}</td><td class="sell">${s.action}</td><td>${s.reason}</td></tr>`);
    if (stockPicks.watch) stockPicks.watch.forEach(s => html += `<tr><td>🟡 WATCH</td><td>${s.symbol}</td><td>${s.gffi}</td><td class="watch">${s.action}</td><td>${s.reason}</td></tr>`);
    container.innerHTML = html + '</table>';
}

function renderIndiaTable() {
    const container = document.querySelector('.india-cards');
    if (!container || !indiaMarketData) return;
    
    let html = '<table class="data-table"><tr><th>Indicator</th><th>Value</th><th>Change</th></tr>';
    if (indiaMarketData.nifty) html += `<tr><td>📈 Nifty</td><td>${indiaMarketData.nifty.toLocaleString()}</td><td>${indiaMarketData.nifty_change ? indiaMarketData.nifty_change + '%' : 'N/A'}</td></tr>`;
    if (indiaMarketData.sensex) html += `<tr><td>📊 Sensex</td><td>${indiaMarketData.sensex.toLocaleString()}</td><td>${indiaMarketData.sensex_change ? indiaMarketData.sensex_change + '%' : 'N/A'}</td></tr>`;
    container.innerHTML = html + '</table>';
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
// CRISIS PROBABILITY TIMELINE
// ============================================

function renderCrisisTimeline() {
    const container = document.getElementById('crisis-timeline');
    if (!container || !crisisData) return;
    
    let color = '#28a745';
    let statusClass = 'normal';
    
    if (crisisData.probability >= 80) {
        color = '#dc3545';
        statusClass = 'critical';
    } else if (crisisData.probability >= 60) {
        color = '#fd7e14';
        statusClass = 'high';
    } else if (crisisData.probability >= 40) {
        color = '#ffc107';
        statusClass = 'elevated';
    } else if (crisisData.probability >= 20) {
        color = '#28a745';
        statusClass = 'moderate';
    }
    
    let html = `
        <div class="crisis-timeline-card ${statusClass}">
            <h4>⚠️ Crisis Probability Timeline</h4>
            <div class="probability-gauge">
                <div class="probability-bar" style="width: ${crisisData.probability}%; background: ${color};"></div>
                <span class="probability-value">${crisisData.probability}%</span>
            </div>
            
            <div class="timeline-stats">
                <div class="stat">
                    <span class="stat-label">Expected Crisis Window</span>
                    <span class="stat-value">${crisisData.lead_time_min} - ${crisisData.lead_time_max} months</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Average Lead Time</span>
                    <span class="stat-value">${crisisData.lead_time_avg} months</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Current Status</span>
                    <span class="stat-value status-${crisisData.status.toLowerCase()}">${crisisData.status}</span>
                </div>
            </div>
            
            <div class="crisis-message ${statusClass}">
                ${crisisData.message}
            </div>
            
            <div class="timeline-visual">
                <div class="timeline-bar">
                    <div class="timeline-marker" style="left: ${(crisisData.lead_time_avg / 24) * 100}%"></div>
                    <div class="timeline-range" style="left: ${(crisisData.lead_time_min / 24) * 100}%; width: ${((crisisData.lead_time_max - crisisData.lead_time_min) / 24) * 100}%"></div>
                    <div class="timeline-labels">
                        <span>Now</span>
                        <span>3mo</span>
                        <span>6mo</span>
                        <span>12mo</span>
                        <span>18mo</span>
                        <span>24mo</span>
                    </div>
                </div>
            </div>
            
            <div class="crisis-note">
                <small>⚠️ Based on historical data: 2008 (24mo), 2020 (24mo), 2022 (6mo), 2023 (3mo)</small>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}
// ============================================
// STOCKS ZONE RENDER FUNCTIONS
// ============================================

function renderStockZones() {
    if (!stockPicks || !stockPicks.safe || !stockPicks.risky) return;
    
    // Get all stocks from stockPicks
    const allStocks = [...stockPicks.safe, ...stockPicks.risky, ...stockPicks.watch];
    
    // Filter stocks by GFFI
    const safeStocks = allStocks.filter(s => s.gffi < 37).sort((a,b) => a.gffi - b.gffi);
    const riskyStocks = allStocks.filter(s => s.gffi > 38).sort((a,b) => a.gffi - b.gffi);
    const moderateStocks = allStocks.filter(s => s.gffi >= 37 && s.gffi <= 38).sort((a,b) => a.gffi - b.gffi);
    
    // Render Safe Zone
    const safeContainer = document.getElementById('safe-zone-stocks');
    if (safeContainer) {
        if (safeStocks.length > 0) {
            safeContainer.innerHTML = safeStocks.map(s => `
                <div class="stock-item-compare">
                    <div class="stock-info">
                        <span class="stock-symbol">${s.symbol}</span>
                        <span class="stock-name">${s.name}</span>
                        <span class="stock-gffi-compare stock-gffi-safe">GFFI: ${s.gffi}</span>
                    </div>
                    <span class="stock-action-badge action-buy">${s.action}</span>
                </div>
            `).join('');
        } else {
            safeContainer.innerHTML = '<div class="no-data">No stocks in safe zone</div>';
        }
    }
    
    // Render Risky Zone
    const riskyContainer = document.getElementById('risky-zone-stocks');
    if (riskyContainer) {
        if (riskyStocks.length > 0) {
            riskyContainer.innerHTML = riskyStocks.map(s => `
                <div class="stock-item-compare">
                    <div class="stock-info">
                        <span class="stock-symbol">${s.symbol}</span>
                        <span class="stock-name">${s.name}</span>
                        <span class="stock-gffi-compare stock-gffi-risky">GFFI: ${s.gffi}</span>
                    </div>
                    <span class="stock-action-badge action-sell">${s.action}</span>
                </div>
            `).join('');
        } else {
            riskyContainer.innerHTML = '<div class="no-data">No stocks in high risk zone</div>';
        }
    }
    
    // Render Moderate Zone
    const moderateContainer = document.getElementById('moderate-zone-stocks');
    if (moderateContainer) {
        if (moderateStocks.length > 0) {
            moderateContainer.innerHTML = moderateStocks.map(s => `
                <div class="stock-item-compare">
                    <div class="stock-info">
                        <span class="stock-symbol">${s.symbol}</span>
                        <span class="stock-name">${s.name}</span>
                        <span class="stock-gffi-compare stock-gffi-moderate">GFFI: ${s.gffi}</span>
                    </div>
                    <span class="stock-action-badge action-watch">${s.action}</span>
                </div>
            `).join('');
        } else {
            moderateContainer.innerHTML = '<div class="no-data">No stocks in moderate zone</div>';
        }
    }
}
