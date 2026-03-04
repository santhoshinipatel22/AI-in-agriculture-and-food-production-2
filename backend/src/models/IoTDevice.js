const mongoose = require('mongoose');

const iotDeviceSchema = new mongoose.Schema({
  farmerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Farmer',
    required: true,
  },
  deviceId: {
    type: String,
    unique: true,
    required: true,
  },
  deviceName: String,
  deviceType: {
    type: String,
    enum: ['soil_moisture', 'temperature', 'humidity', 'ph_sensor', 'ec_sensor', 'npk_sensor'],
    required: true,
  },
  manufacturer: String,
  model: String,
  installationDate: Date,
  fieldName: String,
  status: {
    type: String,
    enum: ['active', 'inactive', 'error', 'maintenance'],
    default: 'active',
  },
  lastDataReceived: Date,
  batteryLevel: Number,
  signalStrength: Number,
  latestReadings: {
    soilMoisture: Number, // percentage
    temperature: Number, // in Celsius
    humidity: Number, // percentage
    ph: Number,
    ec: Number, // electrical conductivity
    nitrogen: Number,
    phosphorus: Number,
    potassium: Number,
    timestamp: Date,
  },
  sensorDataHistory: [{
    timestamp: Date,
    soilMoisture: Number,
    temperature: Number,
    humidity: Number,
    ph: Number,
    ec: Number,
    nitrogen: Number,
    phosphorus: Number,
    potassium: Number,
  }],
  alerts: [{
    type: String,
    threshold: String,
    severity: { type: String, enum: ['low', 'medium', 'high'] },
    message: String,
    createdAt: Date,
    resolved: Boolean,
  }],
  lastMaintenanceDate: Date,
  maintenanceHistory: [{
    date: Date,
    type: String,
    notes: String,
  }],
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('IoTDevice', iotDeviceSchema);
