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

// Function to add book from input to previousBooks array
function addBookFromInput() {
    const bookTitle = lastBookInput.value.trim();

    if (bookTitle) {
        if (!previousBooks.includes(bookTitle)) {
            previousBooks.push(bookTitle);
            // Update the displayed last entered book
            lastEnteredBook.textContent = bookTitle;
            lastBookInput.value = '';
            return true;
        } else {
            // Book already in list
            errorText.textContent = `You've already added "${bookTitle}" to your reading history.`;
            error.style.display = 'block';
            setTimeout(() => {
                error.style.display = 'none';
            }, 3000);
        }
    }
    return false;
}

// Function to get recommendation from the API
async function getRecommendation() {
    // Prevent multiple clicks
    if (recommendBtn.disabled) return;

    // Add the book from input if available
    addBookFromInput();

    // If no books have been read, show error
    if (previousBooks.length === 0) {
        errorText.textContent = 'Please enter at least one book you have read.';
        error.style.display = 'block';
        return;
    }

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

// Add event listener for the input field
lastBookInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission
        const bookTitle = lastBookInput.value.trim();
        if (bookTitle) {
            // Update display immediately when Enter is pressed
            if (!previousBooks.includes(bookTitle)) {
                lastEnteredBook.textContent = bookTitle;
            }
            getRecommendation();
        }
    }
});

// Add event listener for input changes to show real-time feedback
lastBookInput.addEventListener('input', function() {
    const bookTitle = lastBookInput.value.trim();
    if (bookTitle) {
        lastEnteredBook.textContent = `${bookTitle} (not saved yet)`;
    } else {
        lastEnteredBook.textContent = previousBooks.length > 0 ? previousBooks[previousBooks.length - 1] : 'None';
    }
});

// Display any previously read books on page load
function displayPreviousBooks() {
    if (previousBooks.length > 0) {
        previousBooks.forEach(book => {
            const historyItem = document.createElement('li');
            historyItem.textContent = book;
            historyList.appendChild(historyItem);
        });
    }
}

// Initialize the display
displayPreviousBooks();
