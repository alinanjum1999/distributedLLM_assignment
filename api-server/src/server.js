const express = require('express');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = process.env.PORT || 4000; // Backend will run on port 4000

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Initialize SQLite database
const db = new sqlite3.Database(':memory:'); // Using in-memory database for simplicity

// Create table to store conversation history
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS conversations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      model TEXT,
      query TEXT,
      response TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
});

// Route to send query to the Python LLM service
app.post('/api/query', async (req, res) => {
  const { model, query } = req.body;

  if (!model || !query) {
    return res.status(400).json({ error: 'Model and query are required.' });
  }

  try {
    // Send the query to the Python LLM service
    const response = await axios.post('http://python-llm:5000/query', {
      model,
      query
    });

    const llmResponse = response.data.response; // Extract the response from the LLM

    // Save the query and response to the SQLite database
    db.run(
      'INSERT INTO conversations (model, query, response) VALUES (?, ?, ?)',
      [model, query, llmResponse],
      function (err) {
        if (err) {
          return res.status(500).json({ error: 'Failed to save conversation to the database.' });
        }

        // Return the response from the LLM to the user
        res.json({
          id: this.lastID,
          model,
          query,
          response: llmResponse
        });
      }
    );
  } catch (error) {
    console.error('Error querying the Python LLM:', error.message);
    res.status(500).json({ error: 'Failed to query the Python LLM service.' });
  }
});

// Route to list conversation history
app.get('/api/conversations', (req, res) => {
  db.all('SELECT * FROM conversations ORDER BY timestamp DESC', [], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to retrieve conversation history.' });
    }

    res.json(rows);
  });
});

// Route to get details of a specific conversation
app.get('/api/conversations/:id', (req, res) => {
  const conversationId = req.params.id;

  db.get('SELECT * FROM conversations WHERE id = ?', [conversationId], (err, row) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to retrieve conversation details.' });
    }

    if (!row) {
      return res.status(404).json({ error: 'Conversation not found.' });
    }

    res.json(row);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log('Connected to SQLite database');
});
