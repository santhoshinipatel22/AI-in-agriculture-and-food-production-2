const redis = require('ioredis');

const redisClient = new redis(process.env.REDIS_URL || 'redis://localhost:6379', {
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  },
  maxRetriesPerRequest: 3,
  enableReadyCheck: false,
  enableOfflineQueue: false,
});

redisClient.on('connect', () => {
  console.log('✓ Redis connected');
});

redisClient.on('error', (error) => {
  console.error('✗ Redis connection error:', error);
});

module.exports = redisClient;
