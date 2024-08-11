import { Router } from 'express';
import conversationRoutes from './conversations';

const router = Router();

router.use('/conversations', conversationRoutes);

export default router;
