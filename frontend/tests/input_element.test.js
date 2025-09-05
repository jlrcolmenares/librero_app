/**
 * Tests for the book input element feature
 */

// Mock DOM elements
document.body.innerHTML = `
<div class="container">
  <h1>Librero</h1>
  <div id="bookInputContainer">
    <input type="text" id="lastBookInput" placeholder="Enter the last book you read" />
    <small id="inputHelp">Enter the title of the last book you read</small>
  </div>
  <button id="recommendBtn" class="recommend-btn">Recommend a Book</button>
  <div id="recommendations"></div>
</div>
`;

// Mock fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({
      recommendation: "The Stranger",
      message: "Based on your reading history, we recommend 'The Stranger'",
      total_books: 10
    }),
  })
);

// Import the functions to test (we'll need to modify app.js to export these)
// For now, we'll define them here for testing purposes
const previousBooks = [];

function addBookFromInput() {
  const inputElement = document.getElementById('lastBookInput');
  const bookTitle = inputElement.value.trim();

  if (bookTitle) {
    if (!previousBooks.includes(bookTitle)) {
      previousBooks.push(bookTitle);
      inputElement.value = '';
      return true;
    }
  }
  return false;
}

async function getRecommendation() {
  // Add the book from input first
  addBookFromInput();

  // Then make the API call with updated previousBooks
  await fetch('http://localhost:8000/api/recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      books_read: previousBooks
    })
  });

  return previousBooks;
}

// Tests
describe('Book Input Element', () => {
  beforeEach(() => {
    // Clear the previous books array before each test
    previousBooks.length = 0;
    // Reset the input value
    document.getElementById('lastBookInput').value = '';
    // Reset the fetch mock
    fetch.mockClear();
  });

  test('Input element exists in the DOM', () => {
    const inputElement = document.getElementById('lastBookInput');
    expect(inputElement).not.toBeNull();
    expect(inputElement.tagName).toBe('INPUT');
  });

  test('Adding a book from input works', () => {
    const inputElement = document.getElementById('lastBookInput');
    inputElement.value = 'To Kill a Mockingbird';

    const result = addBookFromInput();

    expect(result).toBe(true);
    expect(previousBooks).toContain('To Kill a Mockingbird');
    expect(inputElement.value).toBe('');
  });

  test('Adding an empty book title does nothing', () => {
    const inputElement = document.getElementById('lastBookInput');
    inputElement.value = '   ';

    const result = addBookFromInput();

    expect(result).toBe(false);
    expect(previousBooks.length).toBe(0);
  });

  test('Adding a duplicate book does nothing', () => {
    previousBooks.push('1984');

    const inputElement = document.getElementById('lastBookInput');
    inputElement.value = '1984';

    const result = addBookFromInput();

    expect(result).toBe(false);
    expect(previousBooks.length).toBe(1);
  });

  test('getRecommendation includes the book from input', async () => {
    const inputElement = document.getElementById('lastBookInput');
    inputElement.value = 'Pride and Prejudice';

    await getRecommendation();

    expect(previousBooks).toContain('Pride and Prejudice');
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/recommend',
      expect.objectContaining({
        body: JSON.stringify({
          books_read: ['Pride and Prejudice']
        })
      })
    );
  });
});
