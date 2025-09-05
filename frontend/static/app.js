// Initialize state
const API_URL = 'http://localhost:8000';

// Book storage service
const bookStorageService = {
  // Save a book to localStorage
  saveBook(bookTitle) {
    if (!bookTitle) return false;
    
    // Get existing books from localStorage
    const books = this.getBooks();
    
    // Don't add duplicates
    if (books.includes(bookTitle)) return false;
    
    // Add new book
    books.push(bookTitle);
    
    // Save back to localStorage
    localStorage.setItem('librero_books', JSON.stringify(books));
    
    return true;
  },
  
  // Get all books from localStorage
  getBooks() {
    const booksJson = localStorage.getItem('librero_books');
    return booksJson ? JSON.parse(booksJson) : [];
  },
  
  // Clear all books from localStorage
  clearBooks() {
    localStorage.removeItem('librero_books');
    return [];
  },
  
  // Future implementation: Send book to backend
  async sendBookToBackend(bookTitle) {
    try {
      const response = await fetch(`${API_URL}/api/books`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: bookTitle })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error sending book to backend:', error);
      throw error;
    }
  }
};

// Initialize previousBooks from localStorage
const previousBooks = bookStorageService.getBooks();

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

// Function to update the last entered book display and save to localStorage
function updateLastEnteredBook() {
    const bookTitle = lastBookInput.value.trim();
    if (bookTitle) {
        // Save to localStorage
        if (bookStorageService.saveBook(bookTitle)) {
            // Update UI
            lastEnteredBook.textContent = bookTitle;
            lastBookInput.value = '';
            
            // Update the previous books array
            previousBooks.length = 0;
            bookStorageService.getBooks().forEach(book => previousBooks.push(book));
            
            // Display all stored books
            displayStoredBooks();
            
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

// Function to display all stored books in the UI
function displayStoredBooks() {
    const books = bookStorageService.getBooks();
    
    // Clear existing list
    historyList.innerHTML = '';
    
    // Add each book to the list
    books.forEach(book => {
        const listItem = document.createElement('li');
        listItem.textContent = book;
        historyList.appendChild(listItem);
    });
}

// Add event listener for the input field
lastBookInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission
        updateLastEnteredBook();
        // Stop event propagation to prevent it from triggering the document-level listener
        event.stopPropagation();
    }
});

// No document-level Enter key handler - recommendations only triggered by button click

// Initialize the UI with stored books on page load
document.addEventListener('DOMContentLoaded', function() {
    // Display any stored books
    displayStoredBooks();
    
    // Update the last entered book display if there are books
    const books = bookStorageService.getBooks();
    if (books.length > 0) {
        lastEnteredBook.textContent = books[books.length - 1];
    }
});
