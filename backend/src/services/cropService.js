const Crop = require('../models/Crop');
const DiseaseDetection = require('../models/DiseaseDetection');
const logger = require('../utils/logger');

const cropService = {
  async createCrop(farmerId, cropData) {
    try {
      const crop = new Crop({
        farmerId,
        ...cropData,
      });

      await crop.save();
      return crop;
    } catch (error) {
      logger.error('Create crop error:', error.message);
      throw error;
    }
  },

  async getCropsByFarmer(farmerId) {
    try {
      const crops = await Crop.find({ farmerId }).sort({ createdAt: -1 });
      return crops;
    } catch (error) {
      logger.error('Get crops error:', error.message);
      throw error;
    }
  },

  async getCropById(cropId) {
    try {
      const crop = await Crop.findById(cropId).populate('diseases');
      return crop;
    } catch (error) {
      logger.error('Get crop error:', error.message);
      throw error;
    }
  },

  async updateCrop(cropId, updateData) {
    try {
      const crop = await Crop.findByIdAndUpdate(
        cropId,
        { ...updateData, updatedAt: new Date() },
        { new: true }
      );
      return crop;
    } catch (error) {
      logger.error('Update crop error:', error.message);
      throw error;
    }
  },

  async deleteCrop(cropId) {
    try {
      await Crop.findByIdAndDelete(cropId);
      return { success: true, message: 'Crop deleted successfully' };
    } catch (error) {
      logger.error('Delete crop error:', error.message);
      throw error;
    }
  },

  async getCropDiseases(cropId) {
    try {
      const diseases = await DiseaseDetection.find({ cropId });
      return diseases;
    } catch (error) {
      logger.error('Get crop diseases error:', error.message);
      throw error;
    }
  },

  async calculateCropMetrics(farmerId) {
    try {
      const crops = await Crop.find({ farmerId });
      
      const metrics = {
        totalCrops: crops.length,
        activeCrops: crops.filter(c => c.status !== 'completed').length,
        totalExpense: crops.reduce((sum, crop) => sum + (crop.cost || 0), 0),
        totalYield: crops.reduce((sum, crop) => sum + (crop.actualYield || 0), 0),
        averageYield: 0,
      };

      metrics.averageYield = crops.length > 0 
        ? metrics.totalYield / crops.length 
        : 0;

      return metrics;
    } catch (error) {
      logger.error('Calculate crop metrics error:', error.message);
      throw error;
    }
  },
};

module.exports = cropService;
