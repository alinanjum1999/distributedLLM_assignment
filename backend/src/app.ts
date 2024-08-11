import express, { Application } from 'express';
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import routes from './routes';
import connectDB from './utils/connectDB';

dotenv.config();

const app: Application = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use('/api', routes);

connectDB();

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
