const { PricePrediction } = require('../models/PricePrediction');
const logger = require('../utils/logger');
const axios = require('axios');

const priceService = {
  async getPricePrediction(cropName, region) {
    try {
      let prediction = await PricePrediction.findOne({
        cropName,
        region,
      }).sort({ createdAt: -1 });

      // Check if prediction is stale (older than 24 hours)
      if (!prediction || (Date.now() - prediction.createdAt) > 24 * 60 * 60 * 1000) {
        // Fetch fresh data from external APIs
        prediction = await this.fetchAndStorePricePrediction(cropName, region);
      }

      return prediction;
    } catch (error) {
      logger.error('Get price prediction error:', error.message);
      throw error;
    }
  },

  async fetchAndStorePricePrediction(cropName, region) {
    try {
      // Integration with external price APIs
      // Example: Agricultural commodity prices API
      
      const mockPrediction = {
        cropName,
        region,
        currentPrice: 2500,
        predictedPrice: 2650,
        predictedDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        confidence: 78,
        trend: 'uptrend',
        recommendation: {
          action: 'hold',
          reasoning: 'Prices expected to rise further in next 2 weeks',
          expectedProfit: 150,
          bestSellDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000),
        },
        accuracy: 82,
      };

      const prediction = new PricePrediction(mockPrediction);
      await prediction.save();

      return prediction;
    } catch (error) {
      logger.error('Fetch price prediction error:', error.message);
      throw error;
    }
  },

  async getPriceHistory(cropName, days = 30) {
    try {
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - days);

      // Fetch from external API (AGMARKNET, ENAM, etc.)
      const history = await PricePrediction.aggregate([
        {
          $match: {
            cropName,
            createdAt: { $gte: startDate },
          },
        },
        {
          $sort: { createdAt: 1 },
        },
      ]);

      return history;
    } catch (error) {
      logger.error('Get price history error:', error.message);
      throw error;
    }
  },

  async getMarketInsights(cropName, region) {
    try {
      const predictions = await PricePrediction.find({
        cropName,
        region,
      })
        .sort({ createdAt: -1 })
        .limit(10);

      if (predictions.length === 0) {
        return null;
      }

      const insights = {
        cropName,
        region,
        currentTrend: predictions[0].trend,
        averagePrice: predictions.reduce((sum, p) => sum + p.currentPrice, 0) / predictions.length,
        minPrice: Math.min(...predictions.map(p => p.currentPrice)),
        maxPrice: Math.max(...predictions.map(p => p.currentPrice)),
        recommendation: predictions[0].recommendation,
        predictions,
      };

      return insights;
    } catch (error) {
      logger.error('Get market insights error:', error.message);
      throw error;
    }
  },
};

module.exports = priceService;
