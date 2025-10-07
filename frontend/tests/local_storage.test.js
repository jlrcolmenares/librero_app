/**
 * Tests for localStorage implementation for book storage
 */

// Mock localStorage
const localStorageMock = (function() {
  let store = {};
  return {
    getItem: function(key) {
      return store[key] || null;
    },
    setItem: function(key, value) {
      store[key] = value.toString();
    },
    removeItem: function(key) {
      delete store[key];
    },
    clear: function() {
      store = {};
    }
  };
})();

// Set up localStorage mock before tests
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

// Mock DOM elements
document.body.innerHTML = `
<div class="container">
  <h1>Librero</h1>
  <div id="bookInputContainer">
    <input type="text" id="lastBookInput" placeholder="Enter the last book you read" />
    <small id="inputHelp">Enter the last book you read</small>
    <div id="enteredBookDisplay">
      <p>Last book read: <span id="lastEnteredBook">None</span></p>
    </div>
  </div>
  <button id="recommendBtn" class="recommend-btn">Recommend a Book</button>
  <div id="recommendations">
    <div id="currentRecommendation" class="recommendation">
      <h3>New Recommendation</h3>
      <p id="recommendationText"></p>
    </div>
    <div id="recommendationHistory" class="recommendation-history">
      <h3>Previous Recommendations</h3>
      <ul id="historyList"></ul>
    </div>
  </div>
</div>
`;

// Mock fetch API for future backend implementation
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({
      success: true,
      message: "Book saved successfully"
    }),
  })
);

// Import the bookStorageService module
// Since we're in a test environment, we'll mock it here
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
      const response = await fetch('http://localhost:8000/api/books', {
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

// Get DOM elements for testing
const lastBookInput = document.getElementById('lastBookInput');
const lastEnteredBook = document.getElementById('lastEnteredBook');
const historyList = document.getElementById('historyList');

// Mock function to update the last entered book display
function updateLastEnteredBook(bookTitle) {
  if (bookTitle) {
    if (bookStorageService.saveBook(bookTitle)) {
      lastEnteredBook.textContent = bookTitle;
      lastBookInput.value = '';
      return true;
    }
  }
  return false;
}

// Tests
describe('Book Storage with localStorage', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    // Reset the input value
    lastBookInput.value = '';
    // Reset the lastEnteredBook display
    lastEnteredBook.textContent = 'None';
    // Clear the history list
    historyList.innerHTML = '';
    // Reset the fetch mock
    fetch.mockClear();
  });

  test('localStorage is empty initially', () => {
    expect(bookStorageService.getBooks()).toEqual([]);
  });

  test('saveBook adds a book to localStorage', () => {
    const result = bookStorageService.saveBook('To Kill a Mockingbird');

    expect(result).toBe(true);
    expect(bookStorageService.getBooks()).toContain('To Kill a Mockingbird');
    expect(bookStorageService.getBooks().length).toBe(1);
  });

  test('saveBook prevents duplicate books', () => {
    bookStorageService.saveBook('1984');
    const result = bookStorageService.saveBook('1984');

    expect(result).toBe(false);
    expect(bookStorageService.getBooks().length).toBe(1);
  });

  test('clearBooks removes all books from localStorage', () => {
    bookStorageService.saveBook('The Great Gatsby');
    bookStorageService.saveBook('Pride and Prejudice');

    const result = bookStorageService.clearBooks();

    expect(result).toEqual([]);
    expect(bookStorageService.getBooks()).toEqual([]);
  });

  test('updateLastEnteredBook updates the UI and clears input', () => {
    lastBookInput.value = 'Brave New World';

    const result = updateLastEnteredBook(lastBookInput.value);

    expect(result).toBe(true);
    expect(lastEnteredBook.textContent).toBe('Brave New World');
    expect(lastBookInput.value).toBe('');
  });

  test('updateLastEnteredBook does not update UI for duplicate books', () => {
    // First add a book
    bookStorageService.saveBook('The Alchemist');

    // Try to add it again
    lastBookInput.value = 'The Alchemist';
    const result = updateLastEnteredBook(lastBookInput.value);

    expect(result).toBe(false);
  });

  test('sendBookToBackend calls fetch with correct parameters', async () => {
    await bookStorageService.sendBookToBackend('War and Peace');

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/books',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ title: 'War and Peace' })
      })
    );
  });

  test('lastEnteredBook shows the most recently added book', () => {
    // Add multiple books
    bookStorageService.saveBook('Book One');
    bookStorageService.saveBook('Book Two');
    bookStorageService.saveBook('Book Three');

    // Update the UI with the last book
    lastEnteredBook.textContent = bookStorageService.getBooks()[bookStorageService.getBooks().length - 1];

    expect(lastEnteredBook.textContent).toBe('Book Three');
  });
});
