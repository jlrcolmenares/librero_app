// Landing page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Landing page loaded');

    // Initialize any landing page specific functionality here
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', function(e) {
            e.preventDefault();
            // Use the router to navigate
            window.router.navigateTo('/recommendations');
        });
    }
});
