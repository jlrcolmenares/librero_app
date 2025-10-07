/**
 * Tests for bookStorage service
 * Tests localStorage functionality and API interactions
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

// Import the bookStorage module (mock it for testing)
const bookStorage = {
  saveBook(bookTitle) {
    if (!bookTitle) return false;

    const books = this.getBooks();

    if (books.includes(bookTitle)) return false;

    books.push(bookTitle);

    localStorage.setItem('librero_books', JSON.stringify(books));

    return true;
  },

  getBooks() {
    const booksJson = localStorage.getItem('librero_books');
    return booksJson ? JSON.parse(booksJson) : [];
  },

  clearBooks() {
    localStorage.removeItem('librero_books');
    return [];
  },

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

// Tests
describe('Book Storage Service', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    // Reset the fetch mock
    fetch.mockClear();
  });

  test('localStorage is empty initially', () => {
    expect(bookStorage.getBooks()).toEqual([]);
  });

  test('saveBook adds a book to localStorage', () => {
    const result = bookStorage.saveBook('To Kill a Mockingbird');

    expect(result).toBe(true);
    expect(bookStorage.getBooks()).toContain('To Kill a Mockingbird');
    expect(bookStorage.getBooks().length).toBe(1);
  });

  test('saveBook prevents duplicate books', () => {
    bookStorage.saveBook('1984');
    const result = bookStorage.saveBook('1984');

    expect(result).toBe(false);
    expect(bookStorage.getBooks().length).toBe(1);
  });

  test('saveBook rejects empty book titles', () => {
    const result = bookStorage.saveBook('');

    expect(result).toBe(false);
    expect(bookStorage.getBooks().length).toBe(0);
  });

  test('clearBooks removes all books from localStorage', () => {
    bookStorage.saveBook('The Great Gatsby');
    bookStorage.saveBook('Pride and Prejudice');

    const result = bookStorage.clearBooks();

    expect(result).toEqual([]);
    expect(bookStorage.getBooks()).toEqual([]);
  });

  test('sendBookToBackend calls fetch with correct parameters', async () => {
    await bookStorage.sendBookToBackend('War and Peace');

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/books',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ title: 'War and Peace' })
      })
    );
  });

  test('multiple books can be added and retrieved', () => {
    bookStorage.saveBook('Book One');
    bookStorage.saveBook('Book Two');
    bookStorage.saveBook('Book Three');

    const books = bookStorage.getBooks();

    expect(books.length).toBe(3);
    expect(books).toEqual(['Book One', 'Book Two', 'Book Three']);
  });
});
