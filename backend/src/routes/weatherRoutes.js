const express = require('express');
const weatherController = require('../controllers/weatherController');

const router = express.Router();

// Weather routes are public (rate-limited)
router.get('/data', weatherController.getWeatherData);
router.get('/forecast', weatherController.getForecast);
router.get('/advisory', weatherController.getAdvisory);
router.get('/alerts', weatherController.getAlerts);

module.exports = router;
