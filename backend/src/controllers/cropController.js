const cropService = require('../services/cropService');
const logger = require('../utils/logger');

const cropController = {
  async createCrop(req, res, next) {
    try {
      const crop = await cropService.createCrop(req.user.userId, req.body);
      res.status(201).json({
        success: true,
        data: crop,
      });
    } catch (error) {
      logger.error('Create crop controller error:', error.message);
      next(error);
    }
  },

  async getCrops(req, res, next) {
    try {
      const crops = await cropService.getCropsByFarmer(req.user.userId);
      res.status(200).json({
        success: true,
        data: crops,
        count: crops.length,
      });
    } catch (error) {
      logger.error('Get crops controller error:', error.message);
      next(error);
    }
  },

  async getCropById(req, res, next) {
    try {
      const crop = await cropService.getCropById(req.params.id);

      if (!crop) {
        return res.status(404).json({
          success: false,
          message: 'Crop not found',
        });
      }

      res.status(200).json({
        success: true,
        data: crop,
      });
    } catch (error) {
      logger.error('Get crop by ID controller error:', error.message);
      next(error);
    }
  },

  async updateCrop(req, res, next) {
    try {
      const crop = await cropService.updateCrop(req.params.id, req.body);

      if (!crop) {
        return res.status(404).json({
          success: false,
          message: 'Crop not found',
        });
      }

      res.status(200).json({
        success: true,
        data: crop,
      });
    } catch (error) {
      logger.error('Update crop controller error:', error.message);
      next(error);
    }
  },

  async deleteCrop(req, res, next) {
    try {
      const result = await cropService.deleteCrop(req.params.id);
      res.status(200).json(result);
    } catch (error) {
      logger.error('Delete crop controller error:', error.message);
      next(error);
    }
  },

  async getCropMetrics(req, res, next) {
    try {
      const metrics = await cropService.calculateCropMetrics(req.user.userId);
      res.status(200).json({
        success: true,
        data: metrics,
      });
    } catch (error) {
      logger.error('Get crop metrics controller error:', error.message);
      next(error);
    }
  },

  async getCropDiseases(req, res, next) {
    try {
      const diseases = await cropService.getCropDiseases(req.params.id);
      res.status(200).json({
        success: true,
        data: diseases,
      });
    } catch (error) {
      logger.error('Get crop diseases controller error:', error.message);
      next(error);
    }
  },
};

module.exports = cropController;
