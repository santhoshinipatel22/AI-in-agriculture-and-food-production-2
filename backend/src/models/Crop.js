const mongoose = require('mongoose');

const cropSchema = new mongoose.Schema({
  farmerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farmer',
    required: true,
  },
  cropName: {
    type: String,
    required: true,
    enum: [
      'Rice', 'Wheat', 'Corn', 'Cotton', 'Sugarcane',
      'Potato', 'Tomato', 'Onion', 'Cabbage', 'Carrot',
      'Apple', 'Banana', 'Mango', 'Orange', 'Grape',
      'Chilli', 'Turmeric', 'Ginger', 'Garlic', 'Soybean'
    ]
  },
  fieldName: String,
  fieldArea: Number, // in hectares
  sowingDate: Date,
  expectedHarvestDate: Date,
  sowingMethod: {
    type: String,
    enum: ['broadcast', 'rowing', 'transplanting', 'drip', 'spray']
  },
  seedVariety: String,
  quantity: Number, // in kg
  cost: Number,
  estimatedYield: Number, // in kg/hectare
  actualYield: Number,
  harvestDate: Date,
  status: {
    type: String,
    enum: ['planning', 'sowing', 'growing', 'harvesting', 'completed'],
    default: 'planning'
  },
  yieldPrediction: {
    value: Number,
    confidence: Number,
    predictedAt: Date,
  },
  diseaseAlerts: [{
    diseaseId: mongoose.Schema.Types.ObjectId,
    diseaseName: String,
    severity: { type: String, enum: ['low', 'medium', 'high'] },
    detectedAt: Date,
    recommendation: String,
  }],
  weatherOptimized: {
    isOptimal: Boolean,
    score: Number,
    lastChecked: Date,
  },
  expenses: [{
    description: String,
    amount: Number,
    date: Date,
    category: String,
  }],
  notes: String,
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Crop', cropSchema);
