import mongoose from 'mongoose';

const connectDB = async () => {
    try {
        // Set strictQuery option to suppress deprecation warning
        mongoose.set('strictQuery', true);  // Or false, depending on your preference

        await mongoose.connect(process.env.MONGO_URI as string);
        console.log('MongoDB connected');
    } catch (error) {
        console.error('MongoDB connection failed:', (error as Error).message);
        process.exit(1);
    }
};

export default connectDB;
