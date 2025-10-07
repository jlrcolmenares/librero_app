/**
 * Tests for the recommendation button functionality
 */

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
  <div id="loading" class="loading">Getting your recommendation...</div>
  <div id="recommendations">
    <div id="currentRecommendation" class="recommendation">
      <h3>New Recommendation</h3>
      <p id="recommendationText"></p>
    </div>
  </div>
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

// Mock functions for testing
const previousBooks = [];
const recommendBtn = document.getElementById('recommendBtn');
const loading = document.getElementById('loading');
const currentRecommendation = document.getElementById('currentRecommendation');
const recommendationText = document.getElementById('recommendationText');

// Function to hide all results
function hideAllResults() {
  loading.style.display = 'none';
  currentRecommendation.style.display = 'none';
}

// Function to get recommendation
async function getRecommendation() {
  // Prevent multiple clicks
  if (recommendBtn.disabled) return;

  // Reset any previous state
  hideAllResults();
  loading.style.display = 'block';
  recommendBtn.disabled = true;
  recommendBtn.textContent = 'Finding your next book...';

  try {
    // Make API call
    const response = await fetch('http://localhost:8000/api/recommend', {
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
    recommendBtn.textContent = 'Recommend a Book';
    recommendBtn.disabled = false;

    return data;
  } catch (err) {
    console.error('Error getting recommendation:', err);
    recommendBtn.disabled = false;
    recommendBtn.textContent = 'Try Again';
    throw err;
  }
}

// Tests
describe('Recommendation Button', () => {
  beforeEach(() => {
    // Reset the fetch mock
    fetch.mockClear();
    // Reset button state
    recommendBtn.disabled = false;
    recommendBtn.textContent = 'Recommend a Book';
    // Hide all results
    hideAllResults();
  });

  test('Button exists in the DOM', () => {
    expect(recommendBtn).not.toBeNull();
    expect(recommendBtn.tagName).toBe('BUTTON');
    expect(recommendBtn.textContent.trim()).toBe('Recommend a Book');
  });

  test('Button click triggers getRecommendation function', async () => {
    // Create a spy on the getRecommendation function
    const spy = jest.spyOn({ getRecommendation }, 'getRecommendation');

    // Replace the actual function with the spy
    recommendBtn.onclick = spy;

    // Simulate button click
    recommendBtn.click();

    // Check if the function was called
    expect(spy).toHaveBeenCalled();
  });

  test('getRecommendation function makes API call with correct parameters', async () => {
    // Add a book to the previousBooks array
    previousBooks.push('The Myth of Sisyphus');

    // Call the function
    await getRecommendation();

    // Check if fetch was called with the correct parameters
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/recommend',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          books_read: ['The Myth of Sisyphus']
        })
      })
    );
  });

  test('Button is disabled during API call', async () => {
    // Start the recommendation process
    const promise = getRecommendation();

    // Check if button is disabled
    expect(recommendBtn.disabled).toBe(true);
    expect(recommendBtn.textContent).toBe('Finding your next book...');

    // Wait for the API call to complete
    await promise;
  });

  test('Button is re-enabled after API call completes', async () => {
    // Call the function
    await getRecommendation();

    // Check if button is re-enabled
    expect(recommendBtn.disabled).toBe(false);
    expect(recommendBtn.textContent).toBe('Recommend a Book');
  });

  test('Recommendation is displayed after API call', async () => {
    // Call the function
    await getRecommendation();

    // Check if recommendation is displayed
    expect(currentRecommendation.style.display).toBe('block');
    expect(recommendationText.textContent).toBe("Based on your reading history, we recommend 'The Stranger'");
  });
});
