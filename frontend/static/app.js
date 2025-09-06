// Initialize state
const previousBooks = [];

// bookStorage is loaded from services/bookStorage.js

// DOM elements
let recommendBtn;
let loading;
let currentRecommendation;
let historyList;
let recommendationText;
let error;
let errorText;
let lastBookInput;
let lastEnteredBook;
let readingHistoryList;

// Initialize DOM elements
function initDomElements() {
    recommendBtn = document.getElementById('recommendBtn');
    loading = document.getElementById('loading');
    currentRecommendation = document.getElementById('currentRecommendation');
    historyList = document.getElementById('historyList');
    recommendationText = document.getElementById('recommendationText');
    error = document.getElementById('error');
    errorText = document.getElementById('errorText');
    lastBookInput = document.getElementById('lastBookInput');
    lastEnteredBook = document.getElementById('lastEnteredBook');
    readingHistoryList = document.getElementById('readingHistoryList');
}

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

// Function to display all books from localStorage
function displayReadingHistory() {
    // Clear the current list
    readingHistoryList.innerHTML = '';

    // Get books from localStorage
    const books = bookStorage.getBooks();

    // Display each book
    books.forEach(book => {
        const li = document.createElement('li');
        li.textContent = book;
        readingHistoryList.appendChild(li);
    });

    // Update the last book read display
    if (books.length > 0) {
        lastEnteredBook.textContent = books[books.length - 1];
    } else {
        lastEnteredBook.textContent = 'None';
    }
}

// Function to update the last entered book display
function updateLastEnteredBook() {
    const bookTitle = lastBookInput.value.trim();
    if (bookTitle) {
        // Save to localStorage
        if (bookStorage.saveBook(bookTitle)) {
            // Update UI to show the last entered book
            lastEnteredBook.textContent = bookTitle;
            lastBookInput.value = '';

            // Update the reading history display
            displayReadingHistory();

            return true;
        } else {
            // Book already exists
            errorText.textContent = `You've already added "${bookTitle}" to your reading history.`;
            error.style.display = 'block';
            setTimeout(() => {
                error.style.display = 'none';
            }, 3000);
        }
    }
    return false;
}

// Add event listeners
function addEventListeners() {
    // Add click event listener to the recommend button
    if (recommendBtn) {
        recommendBtn.addEventListener('click', getRecommendation);
    }

    // Add event listener for the input field
    if (lastBookInput) {
        lastBookInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent form submission
                updateLastEnteredBook();
            }
        });
    }

    // Add event listener for clear history button
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearReadingHistory);
    }
}

// Function to clear reading history
function clearReadingHistory() {
    // Clear books from localStorage
    bookStorage.clearBooks();

    // Update UI
    displayReadingHistory();

    // Show confirmation message
    errorText.textContent = 'Reading history cleared successfully';
    error.style.display = 'block';
    setTimeout(() => {
        error.style.display = 'none';
    }, 3000);
}

// Initialize the app when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');

    // Only initialize if we're on the recommendations page
    if (document.getElementById('recommendations-view')) {
        console.log('Recommendations view found, initializing...');

        // Initialize DOM elements
        initDomElements();

        // Load books from localStorage and update the UI
        displayReadingHistory();

        // Add event listeners
        addEventListeners();

        // Reset previousBooks array to ensure recommendations are independent of reading history
        previousBooks.length = 0;

        console.log('Recommendations page initialized successfully');
    }
});
