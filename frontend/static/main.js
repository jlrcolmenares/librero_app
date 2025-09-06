// Main entry point for the Librero application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Librero app initialized');
    
    // Set up default route handling
    const currentPath = window.location.pathname;
    
    // If we're on the landing.html page but the URL path is different, update the URL
    if (document.title.includes('Your Personal Book Recommender') && currentPath !== '/') {
        window.history.replaceState(null, '', '/');
    }
    
    // If we're on the index.html page (recommendations) but the URL path is different, update the URL
    if (document.title.includes('Book Recommender') && !document.title.includes('Your Personal') && currentPath !== '/recommendations') {
        window.history.replaceState(null, '', '/recommendations');
    }
    
    // Set up navigation links
    document.querySelectorAll('[data-link]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            
            // Use the router for navigation if available
            if (window.router) {
                window.router.navigateTo(target);
            } else {
                // Fallback for direct navigation
                if (target === '/') {
                    window.location.href = 'index.html';
                } else if (target === '/recommendations') {
                    window.location.href = 'recommendations.html';
                } else {
                    window.location.href = target;
                }
            }
        });
    });
});
