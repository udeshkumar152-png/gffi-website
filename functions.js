// ============================================
// FUNCTIONS.JS (GFFI V2 - VOLATILITY MODEL)
// ============================================

// =============================
// SAFE DATA CHECK
// =============================
if (typeof countryData === 'undefined') window.countryData = [];
if (typeof globalGFFI === 'undefined') window.globalGFFI = 0;
if (typeof updateDate === 'undefined') window.updateDate = '';
if (typeof updateTime === 'undefined') window.updateTime = '';

// =============================
// NEW GFFI STATUS FUNCTION
// =============================
function getGFFIStatus(gffi) {
    if (gffi >= 15) return { text: "CRITICAL", color: "red" };
    if (gffi >= 10) return { text: "WARNING", color: "orange" };
    if (gffi >= 5) return { text: "MODERATE", color: "gold" };
    return { text: "SAFE", color: "green" };
}

// =============================
// COUNTRY GRID
// =============================
function renderCountryGrid() {
    const container = document.getElementById("country-grid");
    if (!container) return;

    let html = "";

    countryData.forEach(c => {
        const status = getGFFIStatus(c.gffi);

        html += `
        <div class="country-card">
            <div>${c.flag}</div>
            <div>${c.name}</div>
            <div>${c.gffi}</div>
            <div style="color:${status.color}">
                ${status.text}
            </div>
        </div>`;
    });

    container.innerHTML = html;
}

// =============================
// TABLE VIEW
// =============================
function renderCountryTable() {
    const container = document.getElementById("country-grid");
    if (!container) return;

    let html = `
    <table class="data-table">
    <tr>
        <th>Country</th>
        <th>GFFI</th>
        <th>Status</th>
    </tr>`;

    countryData.forEach(c => {
        const status = getGFFIStatus(c.gffi);

        html += `
        <tr>
            <td>${c.flag} ${c.name}</td>
            <td>${c.gffi}</td>
            <td style="color:${status.color}">
                ${status.text}
            </td>
        </tr>`;
    });

    html += "</table>";
    container.innerHTML = html;
}

// =============================
// INDIA CARD
// =============================
function renderIndia() {
    const container = document.querySelector(".india-cards");
    if (!container) return;

    const india = countryData.find(c => c.name === "India");

    if (!india) return;

    const status = getGFFIStatus(india.gffi);

    container.innerHTML = `
    <div class="india-card">
        <h3>🇮🇳 India</h3>
        <h2>${india.gffi}</h2>
        <p style="color:${status.color}">
            ${status.text}
        </p>
    </div>`;
}

// =============================
// GLOBAL GFFI
// =============================
function updateGlobal() {
    const el = document.getElementById("global-gffi");
    if (el) el.innerText = globalGFFI;
}

// =============================
// CHANGE INDICATOR (SIMPLIFIED)
// =============================
function updateChangeIndicator() {
    const el = document.getElementById("change-indicator");
    if (!el) return;

    const avg = countryData.reduce((a, b) => a + b.gffi, 0) / countryData.length;

    let text = "Stable";

    if (avg > 10) text = "Risk Increasing";
    if (avg > 15) text = "High Risk";

    el.innerText = text;
}

// =============================
// TOGGLE VIEW
// =============================
let isTable = false;

function toggleView() {
    isTable = !isTable;

    if (isTable) {
        renderCountryTable();
    } else {
        renderCountryGrid();
    }
}

// =============================
// INIT
// =============================
document.addEventListener("DOMContentLoaded", () => {
    console.log("🚀 GFFI Dashboard Loaded");

    updateGlobal();
    renderCountryGrid();
    renderIndia();
    updateChangeIndicator();

    document.getElementById("toggle-view")?.addEventListener("click", toggleView);
});
