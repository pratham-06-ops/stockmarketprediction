// Main JavaScript for Stock Prediction App

// Global variables
let marketDataInterval;
let notificationQueue = [];

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize animations
    initializeAnimations();
    
    // Initialize market data updates
    initializeMarketData();
    
    // Initialize notifications
    initializeNotifications();
    
    // Initialize theme handling
    initializeTheme();
    
    // Initialize forms
    initializeForms();
    
    console.log('Stock Prediction App initialized successfully');
}

// Animation Helpers
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for scroll animations
    document.querySelectorAll('.card, .feature-card, .stat-item').forEach(el => {
        observer.observe(el);
    });
    
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Market Data Management
function initializeMarketData() {
    // Check if we're on a page that needs market data
    const marketDataContainer = document.getElementById('marketData');
    if (!marketDataContainer) return;
    
    // Start periodic updates
    startMarketDataUpdates();
    
    // Add visibility change handler to pause/resume updates
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            stopMarketDataUpdates();
        } else {
            startMarketDataUpdates();
        }
    });
}

function startMarketDataUpdates() {
    // Clear existing interval
    if (marketDataInterval) {
        clearInterval(marketDataInterval);
    }
    
    // Start new interval
    marketDataInterval = setInterval(updateMarketData, 30000); // 30 seconds
}

function stopMarketDataUpdates() {
    if (marketDataInterval) {
        clearInterval(marketDataInterval);
        marketDataInterval = null;
    }
}

async function updateMarketData() {
    try {
        const response = await fetch('/api/market-overview');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        updateMarketCards(data);
        
    } catch (error) {
        console.warn('Market data update failed:', error);
        // Don't show error to user for automatic updates
    }
}

function updateMarketCards(data) {
    const cards = document.querySelectorAll('.market-card');
    
    data.forEach((stock, index) => {
        if (cards[index]) {
            const card = cards[index];
            const priceValue = card.querySelector('.price-value');
            const changeBadge = card.querySelector('.change-badge');
            
            if (priceValue) {
                const oldPrice = parseFloat(priceValue.textContent.replace('₹', ''));
                const newPrice = stock.price;
                
                // Update price with animation
                priceValue.textContent = `₹${newPrice.toFixed(2)}`;
                
                // Add flash animation if price changed
                if (oldPrice !== newPrice) {
                    priceValue.classList.add('price-update');
                    setTimeout(() => priceValue.classList.remove('price-update'), 1000);
                }
            }
            
            if (changeBadge) {
                const trendIcon = stock.trend === 'up' ? 'trending-up' : 
                                stock.trend === 'down' ? 'trending-down' : 'dash';
                const bgColor = stock.trend === 'up' ? 'success' : 
                              stock.trend === 'down' ? 'danger' : 'secondary';
                
                changeBadge.innerHTML = `
                    <i class="bi bi-${trendIcon}"></i>
                    ${stock.change.toFixed(2)}%
                `;
                changeBadge.className = `badge bg-${bgColor} change-badge`;
            }
            
            // Add card hover effect
            card.addEventListener('click', () => {
                showStockDetails(stock);
            });
        }
    });
}

function showStockDetails(stock) {
    // Create modal or redirect to detailed view
    showNotification(`${stock.company}: ₹${stock.price.toFixed(2)} (${stock.change.toFixed(2)}%)`, 'info');
}

// Notification System
function initializeNotifications() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notificationContainer')) {
        const container = document.createElement('div');
        container.id = 'notificationContainer';
        container.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        `;
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show shadow-sm mb-2`;
    notification.style.cssText = 'animation: slideInRight 0.3s ease-out;';
    
    const icon = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    }[type] || 'info-circle';
    
    notification.innerHTML = `
        <i class="bi bi-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, duration);
}

// Theme Management
function initializeTheme() {
    // Check for saved theme preference or default to 'light' mode
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Create theme toggle button if needed
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    showNotification(`Switched to ${newTheme} theme`, 'info', 2000);
}

// Form Enhancements
function initializeForms() {
    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                
                // Reset button after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });
    
    // Add real-time validation
    document.querySelectorAll('input[required], select[required]').forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldValidation);
    });
}

function validateField(event) {
    const field = event.target;
    const isValid = field.checkValidity();
    
    if (!isValid) {
        field.classList.add('is-invalid');
        showFieldError(field, field.validationMessage);
    } else {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        clearFieldError(field);
    }
}

function clearFieldValidation(event) {
    const field = event.target;
    field.classList.remove('is-invalid', 'is-valid');
    clearFieldError(field);
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    errorDiv.id = `${field.id}-error`;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    const errorDiv = document.getElementById(`${field.id}-error`);
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Chart Utilities
function createSimpleChart(canvasId, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    
    const ctx = canvas.getContext('2d');
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                display: false
            },
            x: {
                display: false
            }
        },
        elements: {
            point: {
                radius: 0
            },
            line: {
                tension: 0.4
            }
        }
    };
    
    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: { ...defaultOptions, ...options }
    });
}

// Utility Functions
function formatCurrency(amount, currency = '₹') {
    return `${currency}${parseFloat(amount).toFixed(2)}`;
}

function formatPercentage(value) {
    const num = parseFloat(value);
    return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`;
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-IN').format(number);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// API Helper Functions
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Error Handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred. Please refresh the page.', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    event.preventDefault();
});

// Performance Monitoring
function measurePerformance(name, fn) {
    return async function(...args) {
        const start = performance.now();
        try {
            const result = await fn.apply(this, args);
            const end = performance.now();
            console.log(`${name} took ${end - start} milliseconds`);
            return result;
        } catch (error) {
            const end = performance.now();
            console.log(`${name} failed after ${end - start} milliseconds`);
            throw error;
        }
    };
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopMarketDataUpdates();
});

// Export functions for use in other scripts
window.StockApp = {
    showNotification,
    updateMarketData,
    createSimpleChart,
    formatCurrency,
    formatPercentage,
    formatNumber,
    apiCall,
    debounce,
    throttle
};