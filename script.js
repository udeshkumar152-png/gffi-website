// script.js - GFFI Website Interactivity

// Update current date
function updateDateTime() {
    const now = new Date();
    const dateElement = document.getElementById('current-date');
    const timeElement = document.getElementById('update-time');
    const timeHM = document.getElementById('update-time-hm');
    
    if (dateElement) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        dateElement.textContent = now.toLocaleDateString('en-IN', options);
    }
    
    if (timeElement) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        timeElement.textContent = now.toLocaleDateString('en-IN', options);
    }
    
    if (timeHM) {
        timeHM.textContent = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
    }
}

// Country data (you can update this daily)
const countryData = [
    { name: 'USA', flag: '🇺🇸', gffi: 62.1, status: 'warning' },
    { name: 'Germany', flag: '🇩🇪', gffi: 68.4, status: 'success' },
    { name: 'France', flag: '🇫🇷', gffi: 63.5, status: 'warning' },
    { name: 'Japan', flag: '🇯🇵', gffi: 65.9, status: 'warning' },
    { name: 'UK', flag: '🇬🇧', gffi: 65.0, status: 'success' },
    { name: 'China', flag: '🇨🇳', gffi: 64.6, status: 'warning' },
    { name: 'India', flag: '🇮🇳', gffi: 64.7, status: 'success' },
    { name: 'Brazil', flag: '🇧🇷', gffi: 65.5, status: 'success' },
    { name: 'Russia', flag: '🇷🇺', gffi: 61.5, status: 'success' },
    { name: 'S. Africa', flag: '🇿🇦', gffi: 61.2, status: 'success' },
    { name: 'Canada', flag: '🇨🇦', gffi: 70.8, status: 'warning' },
    { name: 'Italy', flag: '🇮🇹', gffi: 62.5, status: 'warning' },
    { name: 'Australia', flag: '🇦🇺', gffi: 61.5, status: 'warning' },
    { name: 'S. Korea', flag: '🇰🇷', gffi: 61.2, status: 'success' },
    { name: 'Singapore', flag: '🇸🇬', gffi: 62.8, status: 'success' },
    { name: 'Mexico', flag: '🇲🇽', gffi: 61.5, status: 'warning' },
    { name: 'Argentina', flag: '🇦🇷', gffi: 63.2, status: 'warning' }
];

// Function to get status class
function getStatusClass(status) {
    switch(status) {
        case 'normal': return 'status-normal';
        case 'warning': return 'status-watch';
        case 'alert': return 'status-alert';
        case 'critical': return 'status-critical';
        default: return 'status-normal';
    }
}

// Render country grid
function renderCountryGrid() {
    const grid = document.getElementById('country-grid');
    if (!grid) return;
    
    let html = '';
    countryData.forEach(country => {
        html += `
            <div class="country-card">
                <div class="country-flag">${country.flag}</div>
                <div class="country-name">${country.name}</div>
                <div class="country-gffi">${country.gffi}</div>
                <span class="country-status ${getStatusClass(country.status)}">${country.status.toUpperCase()}</span>
            </div>
        `;
    });
    grid.innerHTML = html;
}

// Blog posts data
const blogPosts = [
    {
        date: 'Mar 10, 2026',
        title: 'GFFI Signals: Nifty at Critical Level',
        excerpt: 'India VIX spikes 17% as GFFI crosses 65. What this means for investors...',
        icon: '📊'
    },
    {
        date: 'Mar 9, 2026',
        title: 'Understanding Entropy in Finance',
        excerpt: 'How Shannon entropy predicts market crashes better than traditional indicators.',
        icon: '🧮'
    },
    {
        date: 'Mar 8, 2026',
        title: 'Top 5 Safe Stocks for March',
        excerpt: 'Based on GFFI analysis, these stocks show lowest fragility scores.',
        icon: '🛡️'
    }
];

// Render blog posts
function renderBlogPosts() {
    const blogGrid = document.getElementById('blog-posts');
    if (!blogGrid) return;
    
    let html = '';
    blogPosts.forEach(post => {
        html += `
            <div class="blog-card">
                <div class="blog-image">${post.icon}</div>
                <div class="blog-content">
                    <span class="blog-date">${post.date}</span>
                    <h3>${post.title}</h3>
                    <p>${post.excerpt}</p>
                    <a href="#" class="read-more">Read More <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>
        `;
    });
    blogGrid.innerHTML = html;
}

// Mobile menu toggle
function setupMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuBtn && navMenu) {
        menuBtn.addEventListener('click', () => {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    }
}

// Newsletter form submission
function setupNewsletter() {
    const form = document.getElementById('newsletter-form');
    if (!form) return;
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = form.querySelector('input[type="email"]').value;
        alert(`Thanks for subscribing! You'll receive GFFI updates at ${email}`);
        form.reset();
    });
}

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    updateDateTime();
    renderCountryGrid();
    renderBlogPosts();
    setupMobileMenu();
    setupNewsletter();
    
    // Update time every minute
    setInterval(updateDateTime, 60000);
});
