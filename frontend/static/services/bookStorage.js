/**
 * Book Storage Service
 *
 * Handles storing and retrieving books from localStorage
 * and provides methods for future backend integration.
 */

const bookStorage = {
  /**
   * Save a book to localStorage
   * @param {string} bookTitle - The title of the book to save
   * @returns {boolean} - True if book was saved, false if it was a duplicate or empty
   */
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

  /**
   * Get all books from localStorage
   * @returns {Array<string>} - Array of book titles
   */
  getBooks() {
    const booksJson = localStorage.getItem('librero_books');
    return booksJson ? JSON.parse(booksJson) : [];
  },

  /**
   * Clear all books from localStorage
   * @returns {Array} - Empty array
   */
  clearBooks() {
    localStorage.removeItem('librero_books');
    return [];
  },

  /**
   * Send a book to the backend API
   * @param {string} bookTitle - The title of the book to send
   * @returns {Promise<Object>} - Response from the API
   */
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

// Export the bookStorage object for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = bookStorage;
} else {
  // For browser environment
  window.bookStorage = bookStorage;
}
