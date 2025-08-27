// Initialize state
const previousBooks = [];

// Get DOM elements
const recommendBtn = document.getElementById('recommendBtn');
const loading = document.getElementById('loading');
const currentRecommendation = document.getElementById('currentRecommendation');
const historyList = document.getElementById('historyList');
const recommendationText = document.getElementById('recommendationText');
const error = document.getElementById('error');
const errorText = document.getElementById('errorText');

// Hide all result elements initially
function hideAllResults() {
    loading.style.display = 'none';
    currentRecommendation.style.display = 'none';
    error.style.display = 'none';
}

// Function to get recommendation from the API
async function getRecommendation() {
    try {
        // Show loading state
        hideAllResults();
        loading.style.display = 'block';
        recommendBtn.disabled = true;
        recommendBtn.textContent = 'Getting recommendation...';

        // Make API call to our FastAPI backend
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                books_read: previousBooks
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading and show recommendation
        hideAllResults();
        const fullMessage = data.message;
        recommendationText.textContent = fullMessage;
        currentRecommendation.style.display = 'block';

        // Add to history if it's a valid book recommendation
        if (data.recommendation !== 'No recommendation available') {
            const historyItem = document.createElement('li');
            historyItem.textContent = data.recommendation;
            historyList.insertBefore(historyItem, historyList.firstChild);

            // Add to previous books if not already there
            if (!previousBooks.includes(data.recommendation)) {
                previousBooks.push(data.recommendation);
            }
        }

        // Keep only the last N items in history based on total available books
        while (historyList.children.length > data.total_books) {
            historyList.removeChild(historyList.lastChild);
        }

        // Disable button if all books have been read
        if (previousBooks.length >= data.total_books) {
            recommendBtn.disabled = true;
            recommendBtn.title = 'You have read all available books!';
        }

    } catch (err) {
        // Hide loading and show error
        hideAllResults();
        errorText.textContent = `Sorry, something went wrong: ${err.message}`;
        error.style.display = 'block';
        console.error('Error getting recommendation:', err);
    } finally {
        // Only enable button if not all books are read
        recommendBtn.disabled = previousBooks.length >= data.total_books;
        recommendBtn.textContent = 'Recommend a Book';
    }
}

// Add click event listener to the button
recommendBtn.addEventListener('click', getRecommendation);

// Optional: Allow Enter key to trigger recommendation
document.addEventListener('keypress', function(event) {
    if (event.key === 'Enter' && !recommendBtn.disabled) {
        getRecommendation();
    }
});
