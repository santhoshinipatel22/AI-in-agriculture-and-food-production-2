const express = require('express');
const iotController = require('../controllers/iotController');
const { authMiddleware } = require('../middleware/auth');

const router = express.Router();

// All IoT routes require authentication
router.use(authMiddleware);

router.post('/register', iotController.registerDevice);
router.get('/:deviceId/status', iotController.getDeviceStatus);
router.get('/:deviceId/history', iotController.getDeviceHistory);
router.get('/:deviceId/readings', iotController.getLatestReadings);

module.exports = router;
