require('dotenv').config();
const { MongoClient } = require('mongodb');
const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);
let db;

async function connectDB() {
    if (!db) {
        await client.connect();
        db = client.db('job_scheduler');
        console.log('Connected to MongoDB Atlas');
    }
    return db;
}

module.exports = connectDB;