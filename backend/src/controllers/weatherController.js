const weatherService = require('../services/weatherService');
const logger = require('../utils/logger');

const weatherController = {
  async getWeatherData(req, res, next) {
    try {
      const { latitude, longitude } = req.query;

      if (!latitude || !longitude) {
        return res.status(400).json({
          success: false,
          message: 'Latitude and longitude are required',
        });
      }

      const weather = await weatherService.getWeatherAdvisory(
        parseFloat(latitude),
        parseFloat(longitude)
      );

      res.status(200).json({
        success: true,
        data: weather,
      });
    } catch (error) {
      logger.error('Get weather data controller error:', error.message);
      next(error);
    }
  },

  async getForecast(req, res, next) {
    try {
      const { latitude, longitude } = req.query;

      if (!latitude || !longitude) {
        return res.status(400).json({
          success: false,
          message: 'Latitude and longitude are required',
        });
      }

      const forecast = await weatherService.getForecast(
        parseFloat(latitude),
        parseFloat(longitude)
      );

      res.status(200).json({
        success: true,
        data: forecast,
      });
    } catch (error) {
      logger.error('Get forecast controller error:', error.message);
      next(error);
    }
  },

  async getAdvisory(req, res, next) {
    try {
      const { latitude, longitude, cropType } = req.query;

      if (!latitude || !longitude || !cropType) {
        return res.status(400).json({
          success: false,
          message: 'Latitude, longitude, and crop type are required',
        });
      }

      const weather = await weatherService.getWeatherAdvisory(
        parseFloat(latitude),
        parseFloat(longitude)
      );

      const advisory = await weatherService.generateAgriculturalAdvisory(
        weather,
        cropType
      );

      res.status(200).json({
        success: true,
        data: advisory,
      });
    } catch (error) {
      logger.error('Get advisory controller error:', error.message);
      next(error);
    }
  },

  async getAlerts(req, res, next) {
    try {
      const { latitude, longitude } = req.query;

      if (!latitude || !longitude) {
        return res.status(400).json({
          success: false,
          message: 'Latitude and longitude are required',
        });
      }

      const alerts = await weatherService.getWeatherAlerts(
        parseFloat(latitude),
        parseFloat(longitude)
      );

      res.status(200).json({
        success: true,
        data: alerts,
      });
    } catch (error) {
      logger.error('Get alerts controller error:', error.message);
      next(error);
    }
  },
};

module.exports = weatherController;
