const mongoose = require('mongoose');

const weatherAdvisorySchema = new mongoose.Schema({
  farmerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farmer',
  },
  location: {
    coordinates: {
      type: { type: String, default: 'Point' },
      coordinates: [Number], // [longitude, latitude]
    },
    address: String,
  },
  currentWeather: {
    temperature: Number,
    humidity: Number,
    windSpeed: Number,
    rainfall: Number,
    cloudiness: Number,
    uvIndex: Number,
    visibility: Number,
    condition: String,
    lastUpdated: Date,
  },
  forecast: [{
    date: Date,
    temperature: Number,
    humidity: Number,
    rainfall: Number,
    windSpeed: Number,
    condition: String,
  }],
  alerts: [{
    type: { type: String, enum: ['frost', 'heat', 'heavy_rain', 'drought', 'storm'] },
    severity: { type: String, enum: ['low', 'medium', 'high'] },
    message: String,
    startDate: Date,
    endDate: Date,
  }],
  agricultureAdvisory: {
    sowingAdvisory: String,
    pesticideSprayingAdvisory: String,
    harvestingAdvisory: String,
    irrigationAdvisory: {
      recommendedWater: Number, // in mm
      frequency: String,
      timing: String,
      crops: [String],
    },
    bestCropForSeason: [String],
    wheatCondition: String,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('WeatherAdvisory', weatherAdvisorySchema);
