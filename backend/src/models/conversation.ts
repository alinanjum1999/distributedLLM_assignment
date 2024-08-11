import { Schema, model } from 'mongoose';

const ConversationSchema = new Schema({
    conversationId: { type: String, required: true },
    model: { type: String, required: true },
    history: [{
        query: { type: String, required: true },
        response: { type: String, required: true }
    }]
}, { timestamps: true });

export default model('Conversation', ConversationSchema);
