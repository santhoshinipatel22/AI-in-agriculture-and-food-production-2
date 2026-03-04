const priceService = require('../services/priceService');
const logger = require('../utils/logger');

const priceController = {
  async getPricePrediction(req, res, next) {
    try {
      const { cropName, region } = req.query;

      if (!cropName || !region) {
        return res.status(400).json({
          success: false,
          message: 'Crop name and region are required',
        });
      }

      const prediction = await priceService.getPricePrediction(cropName, region);

      res.status(200).json({
        success: true,
        data: prediction,
      });
    } catch (error) {
      logger.error('Get price prediction controller error:', error.message);
      next(error);
    }
  },

  async getPriceHistory(req, res, next) {
    try {
      const { cropName, days = 30 } = req.query;

      if (!cropName) {
        return res.status(400).json({
          success: false,
          message: 'Crop name is required',
        });
      }

      const history = await priceService.getPriceHistory(
        cropName,
        parseInt(days)
      );

      res.status(200).json({
        success: true,
        data: history,
      });
    } catch (error) {
      logger.error('Get price history controller error:', error.message);
      next(error);
    }
  },

  async getMarketInsights(req, res, next) {
    try {
      const { cropName, region } = req.query;

      if (!cropName || !region) {
        return res.status(400).json({
          success: false,
          message: 'Crop name and region are required',
        });
      }

      const insights = await priceService.getMarketInsights(cropName, region);

      res.status(200).json({
        success: true,
        data: insights,
      });
    } catch (error) {
      logger.error('Get market insights controller error:', error.message);
      next(error);
    }
  },
};

module.exports = priceController;
