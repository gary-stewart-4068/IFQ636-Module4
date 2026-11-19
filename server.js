/**
* server.js — Minimal Express API that runs backend/app.py and returns stdout.
*/

require('dotenv').config();
const connectDB = require('./db');
const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.static('public'));
app.get('/', async (req, res) => {
    const cwd = path.join(__dirname, 'backend');
    const PY = process.platform === 'win32' ? 'python' : 'python3';
    exec(`${PY} app.py`, { cwd }, async (error, stdout, stderr) => {
        if (error) {
            return res.status(500).send('Error running Python script');
        }
        try {
            const db = await connectDB();
            await db.collection('job_logs').insertOne({
                timestamp: new Date(),
                output: stdout.trim()
            });
        } catch (dbError) {
            console.error('MongoDB insert failed:', dbError);
        }
        res.type('text/plain').send(stdout.trim());
    });
});

app.listen(PORT, () => {
    console.log(`Node server running at http://localhost:${PORT}`);
});

app.get('/api/logs', async (req, res) => {
    try {
        const db = await connectDB();
        const logs = await db
            .collection('job_logs')
            .find({})
            .sort({ timestamp: -1 })
            .limit(50)
            .toArray();
        res.json(logs);
    } catch (err) {
        console.error(err);
        res.status(500).json({
            error: 'Failed to retrieve logs'
        });
    }
});