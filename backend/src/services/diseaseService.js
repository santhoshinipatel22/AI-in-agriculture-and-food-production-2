const DiseaseDetection = require('../models/DiseaseDetection');
const logger = require('../utils/logger');
const axios = require('axios');

const diseaseService = {
  async uploadDiseaseImage(farmerId, cropId, imagePath) {
    try {
      // This would integrate with your ML model
      // For now, returning mock data
      
      const diseaseDetection = new DiseaseDetection({
        farmerId,
        cropId,
        imagePath,
        diseaseName: 'Leaf Rust',
        severity: 'medium',
        confidence: 85,
        affectedArea: 20,
        treatment: {
          organic: ['Neem oil spray', 'Sulfur dust'],
          chemical: ['Mancozeb 75% WP', 'Tebuconazole 10% WP'],
          integrated: ['Spray neem oil + sulfur mixture'],
        },
        preventiveMeasures: [
          'Maintain proper spacing between plants',
          'Remove infected leaves immediately',
          'Ensure good air circulation',
          'Water at soil level only',
        ],
        status: 'detected',
      });

      await diseaseDetection.save();
      return diseaseDetection;
    } catch (error) {
      logger.error('Disease detection upload error:', error.message);
      throw error;
    }
  },

  async getDiseasesByFarmer(farmerId) {
    try {
      const diseases = await DiseaseDetection.find({ farmerId })
        .populate('cropId', 'cropName')
        .sort({ detectionDate: -1 });
      return diseases;
    } catch (error) {
      logger.error('Get diseases error:', error.message);
      throw error;
    }
  },

  async updateDiseaseStatus(diseaseId, updateData) {
    try {
      const disease = await DiseaseDetection.findByIdAndUpdate(
        diseaseId,
        updateData,
        { new: true }
      );
      return disease;
    } catch (error) {
      logger.error('Update disease error:', error.message);
      throw error;
    }
  },

  async getDiseaseStats(farmerId) {
    try {
      const diseases = await DiseaseDetection.find({ farmerId });

      const stats = {
        totalDetections: diseases.length,
        bySeverity: {
          high: diseases.filter(d => d.severity === 'high').length,
          medium: diseases.filter(d => d.severity === 'medium').length,
          low: diseases.filter(d => d.severity === 'low').length,
        },
        recovered: diseases.filter(d => d.recovery?.status === 'completed').length,
        inTreatment: diseases.filter(d => d.recovery?.status === 'in_progress').length,
      };

      return stats;
    } catch (error) {
      logger.error('Get disease stats error:', error.message);
      throw error;
    }
  },
};

module.exports = diseaseService;
