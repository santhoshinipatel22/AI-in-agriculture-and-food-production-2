const express = require('express');
const priceController = require('../controllers/priceController');

const router = express.Router();

// Price routes are public (rate-limited)
router.get('/prediction', priceController.getPricePrediction);
router.get('/history', priceController.getPriceHistory);
router.get('/insights', priceController.getMarketInsights);

module.exports = router;
