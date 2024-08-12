import express from 'express';
import mongoose from 'mongoose';
import axios from 'axios';
import Conversation  from './models/conversation';

const app = express();
app.use(express.json());

const MONGO_URI = process.env.MONGO_URI || 'mongodb+srv://alinanjum1999:alinanjum1999@cluster0.l3sztjr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
const PYTHON_LLM_URL = process.env.PYTHON_LLM_URL || 'http://localhost:5000';

mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.log('Failed to connect to MongoDB', err));

app.post('/api/query', async (req, res) => {
  const { conversation_id, query } = req.body;

  try {
    const response = await axios.post(`${PYTHON_LLM_URL}/query`, { conversation_id, query });
    const { data } = response;

    const conversation = await Conversation.findById(conversation_id);
    if (conversation) {
      conversation.history.push({ query, response: data.response });
      await conversation.save();
    }

    res.json(data);
  } catch (err: unknown) {
    if (err instanceof Error) {
      res.status(500).json({ error: err.message });
    } else {
      res.status(500).json({ error: "An unknown error occurred." });
    }
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
