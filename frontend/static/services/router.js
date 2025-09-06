// Simple navigation handler for Librero app
document.addEventListener('DOMContentLoaded', function() {
    // Handle link clicks for navigation
    document.addEventListener('click', e => {
        if (e.target.matches('[data-link]')) {
            e.preventDefault();
            const href = e.target.getAttribute('href');

            // Simple direct navigation
            if (href === '/') {
                window.location.href = 'index.html';
            } else if (href === '/recommendations') {
                window.location.href = 'recommendations.html';
            } else {
                window.location.href = href;
            }
        }
    });
});

// Export a simple router object for compatibility
window.router = {
    navigateTo: function(url) {
        if (url === '/') {
            window.location.href = 'index.html';
        } else if (url === '/recommendations') {
            window.location.href = 'recommendations.html';
        } else {
            window.location.href = url;
        }
    }
};
