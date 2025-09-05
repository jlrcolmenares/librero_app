// Initialize state
const previousBooks = [];
const API_URL = 'http://localhost:8000';

// Get DOM elements
const recommendBtn = document.getElementById('recommendBtn');
const loading = document.getElementById('loading');
const currentRecommendation = document.getElementById('currentRecommendation');
const historyList = document.getElementById('historyList');
const recommendationText = document.getElementById('recommendationText');
const error = document.getElementById('error');
const errorText = document.getElementById('errorText');
const lastBookInput = document.getElementById('lastBookInput');
const lastEnteredBook = document.getElementById('lastEnteredBook');

// Hide all result elements initially
function hideAllResults() {
    loading.style.display = 'none';
    currentRecommendation.style.display = 'none';
    error.style.display = 'none';
}

// Function to get recommendation from the API
async function getRecommendation() {
    // Prevent multiple clicks
    if (recommendBtn.disabled) return;

    // Reset any previous state
    hideAllResults();
    error.style.display = 'none';
    loading.style.display = 'block';
    recommendBtn.disabled = true;
    recommendBtn.textContent = 'Finding your next book...';

    try {
        // Make API call to our FastAPI backend
        const response = await fetch(`${API_URL}/api/recommend`, {
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

        // Update UI with recommendation
        hideAllResults();
        currentRecommendation.style.display = 'block';
        recommendationText.textContent = data.message;

        // Calculate remaining books
        const remainingBooks = data.total_books - previousBooks.length;

        // Enable button for next recommendation unless all books are read
        if (remainingBooks <= 0) {
            recommendBtn.textContent = 'All Books Read!';
            recommendBtn.disabled = true;
        } else {
            recommendBtn.textContent = `Get Next Book (${remainingBooks} remaining)`;
            recommendBtn.disabled = false;
        }

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

    } catch (err) {
        // Hide loading and show error
        hideAllResults();
        errorText.textContent = `Sorry, something went wrong: ${err.message}`;
        error.style.display = 'block';
        console.error('Error getting recommendation:', err);
        // Reset button on error
        recommendBtn.disabled = false;
        recommendBtn.textContent = 'Try Again';
    }
}

// Add click event listener to the button
recommendBtn.addEventListener('click', getRecommendation);

// Function to update the last entered book display
function updateLastEnteredBook() {
    const bookTitle = lastBookInput.value.trim();
    if (bookTitle) {
        // Update UI to show the last entered book
        lastEnteredBook.textContent = bookTitle;
        lastBookInput.value = '';
        return true;
    }
    return false;
}

// Add event listener for the input field
lastBookInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission
        updateLastEnteredBook();
    }
});
