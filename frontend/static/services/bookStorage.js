/**
 * Book Storage Service
 *
 * Handles storing and retrieving books from localStorage
 * and provides methods for future backend integration.
 */

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
