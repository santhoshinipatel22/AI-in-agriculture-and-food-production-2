const mongoose = require('mongoose');

const diseaseDetectionSchema = new mongoose.Schema({
  farmerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farmer',
    required: true,
  },
  cropId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Crop',
  },
  imageUrl: String,
  imagePath: String,
  diseaseName: String,
  severity: {
    type: String,
    enum: ['none', 'low', 'medium', 'high', 'critical'],
    default: 'none'
  },
  confidence: Number, // 0-100
  affectedArea: Number, // percentage
  treatment: {
    organic: [String],
    chemical: [String],
    integrated: [String],
  },
  preventiveMeasures: [String],
  costOfTreatment: Number,
  recommendedProducts: [{
    name: String,
    quantity: String,
    price: Number,
    supplier: String,
    link: String,
  }],
  detectionDate: {
    type: Date,
    default: Date.now,
  },
  treatmentStarted: Boolean,
  treatmentDate: Date,
  recovery: {
    status: { type: String, enum: ['not_started', 'in_progress', 'completed'] },
    progressPercent: Number,
  },
  notes: String,
});

module.exports = mongoose.model('DiseaseDetection', diseaseDetectionSchema);
