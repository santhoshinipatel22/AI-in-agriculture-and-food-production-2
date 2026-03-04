const diseaseService = require('../services/diseaseService');
const logger = require('../utils/logger');

const diseaseController = {
  async detectDisease(req, res, next) {
    try {
      const { cropId } = req.params;
      const imagePath = req.file?.path;

      if (!imagePath) {
        return res.status(400).json({
          success: false,
          message: 'Image file is required',
        });
      }

      const detection = await diseaseService.uploadDiseaseImage(
        req.user.userId,
        cropId,
        imagePath
      );

      res.status(201).json({
        success: true,
        data: detection,
      });
    } catch (error) {
      logger.error('Detect disease controller error:', error.message);
      next(error);
    }
  },

  async getDiseases(req, res, next) {
    try {
      const diseases = await diseaseService.getDiseasesByFarmer(req.user.userId);
      res.status(200).json({
        success: true,
        data: diseases,
        count: diseases.length,
      });
    } catch (error) {
      logger.error('Get diseases controller error:', error.message);
      next(error);
    }
  },

  async updateDiseaseStatus(req, res, next) {
    try {
      const { id } = req.params;
      const disease = await diseaseService.updateDiseaseStatus(id, req.body);

      res.status(200).json({
        success: true,
        data: disease,
      });
    } catch (error) {
      logger.error('Update disease status controller error:', error.message);
      next(error);
    }
  },

  async getDiseaseStats(req, res, next) {
    try {
      const stats = await diseaseService.getDiseaseStats(req.user.userId);
      res.status(200).json({
        success: true,
        data: stats,
      });
    } catch (error) {
      logger.error('Get disease stats controller error:', error.message);
      next(error);
    }
  },
};

module.exports = diseaseController;
