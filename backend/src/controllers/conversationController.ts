import { Request, Response } from 'express';
import Conversation from '../models/conversation';
import axios from 'axios';

const pythonApiUrl = process.env.PYTHON_API_URL;

export const createConversation = async (req: Request, res: Response) => {
    const { model, query } = req.body;

    try {
        const modelResponse = await axios.post(`${pythonApiUrl}/select-model`, { model });
        const { conversation_id } = modelResponse.data;

        const queryResponse = await axios.post(`${pythonApiUrl}/query`, { conversation_id, query });

        const newConversation = new Conversation({
            conversationId: conversation_id,
            model: model,
            history: queryResponse.data
        });

        await newConversation.save();

        res.status(201).json(newConversation);
    } catch (error) {
        const err = error as Error;
        res.status(500).json({ message: err.message });
    }
};

export const listConversations = async (req: Request, res: Response) => {
    try {
        const conversations = await Conversation.find().sort({ createdAt: -1 });
        res.status(200).json(conversations);
    } catch (error) {
        const err = error as Error;
        res.status(500).json({ message: err.message });
    }
};

export const getConversationDetail = async (req: Request, res: Response) => {
    const { id } = req.params;

    try {
        const conversation = await Conversation.findById(id);
        if (!conversation) return res.status(404).json({ message: 'Conversation not found' });

        res.status(200).json(conversation);
    } catch (error) {
        const err = error as Error;
        res.status(500).json({ message: err.message });
    }
};
