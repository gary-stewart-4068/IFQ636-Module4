const connectDB = require('./db');

async function test() {
    try {
        const db = await connectDB();
        await db.collection('job_logs')
            .insertOne({
                message: 'Connection test',
                createdAt: new Date()
            });
        console.log('MongoDB connection successful');
    } 
    catch (err) {console.error(err); } 
    finally {process.exit();}
}

test();