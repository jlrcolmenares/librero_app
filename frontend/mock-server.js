/**
 * Mock server for Librero App
 * 
 * This file provides mock endpoints for frontend development
 * before the actual backend is implemented.
 * 
 * Usage: node mock-server.js
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 8000;

// In-memory storage for books
let books = [];

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'librero-recommender-mock'
  });
});

// Book storage endpoint
app.post('/api/books', (req, res) => {
  const { title } = req.body;
  
  if (!title) {
    return res.status(400).json({
      success: false,
      message: 'Book title is required'
    });
  }
  
  // Check for duplicates (case-insensitive)
  const isDuplicate = books.some(book => 
    book.toLowerCase() === title.toLowerCase()
  );
  
  if (isDuplicate) {
    return res.status(409).json({
      success: false,
      message: `Book "${title}" already exists`
    });
  }
  
  // Add book to storage
  books.push(title);
  
  res.status(201).json({
    success: true,
    message: `Book "${title}" saved successfully`,
    bookCount: books.length
  });
});

// Get all books endpoint
app.get('/api/books', (req, res) => {
  res.json({
    success: true,
    books: books
  });
});

// Recommendation endpoint
app.post('/api/recommend', (req, res) => {
  const { books_read } = req.body;
  
  if (!books_read || !Array.isArray(books_read)) {
    return res.status(400).json({
      success: false,
      message: 'books_read array is required'
    });
  }
  
  // Mock book recommendations
  const mockRecommendations = [
    'The Stranger',
    'The Plague',
    'The Myth of Sisyphus',
    'The Fall',
    'The Rebel',
    'A Happy Death',
    'The First Man',
    'Exile and the Kingdom',
    'Caligula'
  ];
  
  // Filter out books already read (case-insensitive)
  const unreadBooks = mockRecommendations.filter(book => 
    !books_read.some(readBook => 
      readBook.toLowerCase() === book.toLowerCase()
    )
  );
  
  if (unreadBooks.length === 0) {
    return res.json({
      recommendation: 'No recommendation available',
      message: 'You have read all available books!',
      total_books: mockRecommendations.length
    });
  }
  
  // Select a random book from unread books
  const randomIndex = Math.floor(Math.random() * unreadBooks.length);
  const recommendation = unreadBooks[randomIndex];
  
  res.json({
    recommendation: recommendation,
    message: `Based on your reading history, we recommend '${recommendation}'`,
    total_books: mockRecommendations.length
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Mock server running at http://localhost:${PORT}`);
  console.log('Available endpoints:');
  console.log('  GET  /health');
  console.log('  POST /api/books');
  console.log('  GET  /api/books');
  console.log('  POST /api/recommend');
});
