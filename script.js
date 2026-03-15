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
// RENDER FUNCTIONS
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
        html += `<div class="sector-card" style="background:${bg};color:${color};">
            <div class="sector-name">${s.name} ${s.trend==='up'?'📈':s.trend==='down'?'📉':'➡️'}</div>
            <div class="sector-gffi">${s.gffi.toFixed(1)}</div>
            <div class="sector-status">${s.gffi>=70?'🔴 HIGH':s.gffi>=65?'🟠 ALERT':s.gffi>=58?'🟡 WATCH':'🟢 SAFE'}</div>
            <div style="font-size:0.8rem">${s.stocks.slice(0,3).join(', ')}</div>
        </div>`;
    });
    grid.innerHTML = html;
}

function renderStockPicks() {
    const safe = document.getElementById('safe-picks');
    if (safe) safe.innerHTML = stockPicks.safe.map(s => 
        `<div class="stock-item"><span>${s.symbol}</span> <span>${s.gffi}</span> <span class="stock-action buy">${s.action}</span></div>
         <div style="font-size:0.8rem">${s.reason}</div>`).join('');
    
    const risky = document.getElementById('risky-picks');
    if (risky) risky.innerHTML = stockPicks.risky.map(s => 
        `<div class="stock-item"><span>${s.symbol}</span> <span>${s.gffi}</span> <span class="stock-action sell">${s.action}</span></div>
         <div style="font-size:0.8rem">${s.reason}</div>`).join('');
    
    const watch = document.getElementById('watch-picks');
    if (watch) watch.innerHTML = stockPicks.watch.map(s => 
        `<div class="stock-item"><span>${s.symbol}</span> <span>${s.gffi}</span> <span class="stock-action watch">${s.action}</span></div>
         <div style="font-size:0.8rem">${s.reason}</div>`).join('');
}

// ============================================
// INITIALIZE
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('global-gffi').textContent = globalGFFI;
    document.getElementById('update-time').textContent = updateDate;
    document.getElementById('update-time-hm').textContent = updateTime;
    renderCountryGrid();
    renderSectorAnalysis();
    renderStockPicks();
});
