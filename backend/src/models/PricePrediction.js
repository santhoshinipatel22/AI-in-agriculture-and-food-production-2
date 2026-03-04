const mongoose = require('mongoose');

const priceHistorySchema = new mongoose.Schema({
  cropName: {
    type: String,
    required: true,
  },
  region: String,
  marketName: String,
  date: Date,
  minPrice: Number,
  maxPrice: Number,
  avgPrice: Number,
  tradedQuantity: Number,
  source: String,
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

const pricePredictionSchema = new mongoose.Schema({
  farmerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farmer',
  },
  cropName: {
    type: String,
    required: true,
  },
  region: String,
  currentPrice: Number,
  predictedPrice: Number,
  predictedDate: Date,
  confidence: Number, // 0-100
  trend: {
    type: String,
    enum: ['uptrend', 'downtrend', 'stable'],
  },
  recommendation: {
    action: { type: String, enum: ['sell', 'hold', 'wait'] },
    reasoning: String,
    expectedProfit: Number,
    bestSellDate: Date,
  },
  historicalData: [priceHistorySchema],
  predictionDate: {
    type: Date,
    default: Date.now,
  },
  accuracy: Number, // historical accuracy of the model
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = {
  PriceHistory: mongoose.model('PriceHistory', priceHistorySchema),
  PricePrediction: mongoose.model('PricePrediction', pricePredictionSchema),
};
