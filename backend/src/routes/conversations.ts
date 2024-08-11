import { Router } from 'express';
import { createConversation, listConversations, getConversationDetail } from '../controllers/conversationController';

const router = Router();

router.post('/', createConversation);
router.get('/', listConversations);
router.get('/:id', getConversationDetail);

export default router;
