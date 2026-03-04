const mongoose = require('mongoose');
const logger = require('../utils/logger');

const dbConfig = {
  mongodb: {
    uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/smart-farming',
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      maxPoolSize: 10,
      socketTimeoutMS: 45000,
    }
  },
  redis: {
    url: process.env.REDIS_URL || 'redis://localhost:6379'
  }
};

const connectDB = async () => {
  try {
    await mongoose.connect(dbConfig.mongodb.uri, dbConfig.mongodb.options);
    logger.info('✓ MongoDB connected successfully');
    return mongoose.connection;
  } catch (error) {
    logger.error('✗ MongoDB connection failed:', error.message);
    process.exit(1);
  }
};

const disconnectDB = async () => {
  try {
    await mongoose.disconnect();
    logger.info('✓ MongoDB disconnected');
  } catch (error) {
    logger.error('✗ MongoDB disconnection failed:', error.message);
  }
};

module.exports = {
  dbConfig,
  connectDB,
  disconnectDB
};
