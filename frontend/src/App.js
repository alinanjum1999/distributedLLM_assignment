import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [model, setModel] = useState('llama2');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleModelChange = (e) => {
    setModel(e.target.value);
  };

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const result = await axios.post('http://localhost:4000/api/query', {
        model: model,
        query: query
      });

      setResponse(result.data.response);
    } catch (error) {
      console.error('Error querying the LLM:', error);
      setResponse('An error occurred while processing your query.');
    }
  };

  return (
    <div className="App">
      <h1>LLM Query Interface</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Select Model:
            <select value={model} onChange={handleModelChange}>
              <option value="llama2">Llama2</option>
              <option value="mistral">Mistral</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Enter Query:
            <textarea
              value={query}
              onChange={handleQueryChange}
              rows="4"
              cols="50"
            />
          </label>
        </div>
        <button type="submit">Submit</button>
      </form>

      {response && (
        <div>
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default App;
