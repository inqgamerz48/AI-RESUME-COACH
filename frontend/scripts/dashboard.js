// ========================================
// DASHBOARD JAVASCRIPT
// ========================================

const API_URL = 'http://localhost:8000';
let currentUser = null;
let authToken = null;

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    authToken = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');

    if (!authToken || !userStr) {
        window.location.href = 'login.html';
        return;
    }

    currentUser = JSON.parse(userStr);

    // Update UI with user info
    updateUserInfo();

    // Setup event listeners
    setupEventListeners();

    // Load usage stats
    loadUsageStats();
});

// ========================================
// USER INFO
// ========================================

function updateUserInfo() {
    document.getElementById('userName').textContent = currentUser.full_name;
    document.getElementById('userPlan').textContent = currentUser.plan;
}

// ========================================
// EVENT LISTENERS
// ========================================

function setupEventListeners() {
    // Logout
    document.getElementById('logoutBtn').addEventListener('click', logout);

    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', handleNavigation);
    });

    // AI Tools
    document.getElementById('improveBulletBtn').addEventListener('click', improveBulletPoint);
}

// ========================================
// NAVIGATION
// ========================================

function handleNavigation(e) {
    e.preventDefault();
    const sectionName = e.currentTarget.getAttribute('data-section');
    showSection(sectionName);
}

function showSection(sectionName) {
    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-section') === sectionName) {
            item.classList.add('active');
        }
    });

    // Update content sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    const targetSection = document.getElementById(`section-${sectionName}`);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

// Make showSection available globally for onclick handlers
window.showSection = showSection;

// ========================================
// LOGOUT
// ========================================

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// ========================================
// AI TOOLS - BULLET POINT REWRITER
// ========================================

async function improveBulletPoint() {
    const text = document.getElementById('bulletText').value.trim();
    const tone = document.getElementById('tone').value;
    const resultContainer = document.getElementById('bulletResult');
    const btn = document.getElementById('improveBulletBtn');
    const btnText = document.getElementById('improveBtnText');
    const btnSpinner = document.getElementById('improveBtnSpinner');

    // Validation
    if (!text) {
        showResult(resultContainer, 'Please enter a resume bullet point to improve', 'error');
        return;
    }

    // Set loading state
    btn.disabled = true;
    btnText.textContent = 'AI is working...';
    btnSpinner.classList.remove('hidden');
    resultContainer.classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}/api/v1/chat/rewrite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ text, tone })
        });

        const data = await response.json();

        if (response.ok) {
            // Success - show result
            resultContainer.innerHTML = `
                <div class="result-header">
                    <h3>✨ AI-Improved Version</h3>
                </div>
                <div class="result-text">${data.result}</div>
                <div class="usage-info">
                    <span class="usage-label">AI Usage:</span>
                    <span class="usage-value">${data.usage.used}/${data.usage.limit}</span>
                    <span class="usage-label">(${data.usage.remaining} remaining)</span>
                </div>
            `;
            resultContainer.classList.remove('hidden');

            // Update usage stats
            updateUsageDisplay(data.usage);
        } else {
            // Error
            if (response.status === 403) {
                // Limit reached
                showResult(resultContainer, `
                    <strong>Usage Limit Reached!</strong><br><br>
                    You've used all ${data.detail.limit || 3} AI improvements for your FREE plan.<br><br>
                    <button class="btn btn-primary" onclick="showSection('upgrade')">Upgrade to PRO</button>
                `, 'error');
            } else if (response.status === 401) {
                // Token expired
                showResult(resultContainer, 'Session expired. Please login again.', 'error');
                setTimeout(() => {
                    logout();
                }, 2000);
            } else {
                showResult(resultContainer, data.detail || 'Failed to improve text', 'error');
            }
        }
    } catch (error) {
        console.error('AI request error:', error);
        showResult(resultContainer, 'Network error. Please check if the backend is running.', 'error');
    } finally {
        // Reset button state
        btn.disabled = false;
        btnText.textContent = 'Improve with AI';
        btnSpinner.classList.add('hidden');
    }
}

function showResult(container, message, type = 'success') {
    container.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    container.classList.remove('hidden');
}

// ========================================
// USAGE STATISTICS
// ========================================

async function loadUsageStats() {
    // For now, we'll update usage after each API call
    // In a full implementation, we'd have a dedicated endpoint
    updateUsageDisplay({ used: 0, limit: 3, remaining: 3 });
}

function updateUsageDisplay(usage) {
    const usedEl = document.getElementById('usageUsed');
    const limitEl = document.getElementById('usageLimit');
    const progressEl = document.getElementById('usageProgress');

    if (usedEl && limitEl && progressEl) {
        usedEl.textContent = usage.used;
        limitEl.textContent = usage.limit;

        const percentage = (usage.used / usage.limit) * 100;
        progressEl.style.width = `${percentage}%`;

        // Change color based on usage
        if (percentage >= 100) {
            progressEl.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
        } else if (percentage >= 80) {
            progressEl.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
        } else {
            progressEl.style.background = 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)';
        }
    }
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

function showNotification(message, type = 'info') {
    // Simple notification - could be enhanced with a toast library
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '1000';
    notification.style.minWidth = '300px';
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.3s';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ========================================
// ERROR HANDLING
// ========================================

window.addEventListener('error', (e) => {
    console.error('Global error:', e);
});

// Handle network errors
window.addEventListener('offline', () => {
    showNotification('You are offline. Please check your connection.', 'error');
});

window.addEventListener('online', () => {
    showNotification('Connection restored!', 'success');
});
