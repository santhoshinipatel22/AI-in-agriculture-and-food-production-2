const IoTDevice = require('../models/IoTDevice');
const logger = require('../utils/logger');
const mqtt = require('mqtt');

// MQTT client configuration
const mqttClient = mqtt.connect(process.env.MQTT_BROKER_URL || 'mqtt://localhost:1883', {
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD,
});

const iotService = {
  connectMQTT() {
    return new Promise((resolve, reject) => {
      mqttClient.on('connect', () => {
        logger.info('✓ Connected to MQTT broker');
        mqttClient.subscribe('farm/+/sensors/+', (err) => {
          if (err) reject(err);
          else resolve();
        });
      });

      mqttClient.on('error', (error) => {
        logger.error('MQTT connection error:', error);
        reject(error);
      });

      mqttClient.on('message', async (topic, message) => {
        try {
          await iotService.processSensorData(topic, JSON.parse(message.toString()));
        } catch (error) {
          logger.error('Error processing sensor data:', error.message);
        }
      });
    });
  },

  async processSensorData(topic, data) {
    try {
      // Parse topic: farm/{deviceId}/sensors/{sensorType}
      const [, deviceId] = topic.match(/farm\/(.+?)\/sensors/) || [, null];

      if (!deviceId) return;

      const device = await IoTDevice.findOne({ deviceId });

      if (!device) {
        logger.warn(`Device not found: ${deviceId}`);
        return;
      }

      // Update latest readings
      device.latestReadings = {
        soilMoisture: data.soilMoisture || device.latestReadings.soilMoisture,
        temperature: data.temperature || device.latestReadings.temperature,
        humidity: data.humidity || device.latestReadings.humidity,
        ph: data.ph || device.latestReadings.ph,
        ec: data.ec || device.latestReadings.ec,
        nitrogen: data.nitrogen || device.latestReadings.nitrogen,
        phosphorus: data.phosphorus || device.latestReadings.phosphorus,
        potassium: data.potassium || device.latestReadings.potassium,
        timestamp: new Date(),
      };

      // Store in history
      device.sensorDataHistory.push(device.latestReadings);
      device.lastDataReceived = new Date();
      device.batteryLevel = data.batteryLevel || device.batteryLevel;

      // Check alerts
      await this.checkAndCreateAlerts(device);

      await device.save();
    } catch (error) {
      logger.error('Process sensor data error:', error.message);
    }
  },

  async checkAndCreateAlerts(device) {
    try {
      const readings = device.latestReadings;

      // Define thresholds (configurable)
      const thresholds = {
        soilMoisture: { min: 20, max: 80 },
        temperature: { min: 10, max: 45 },
        ph: { min: 6.0, max: 7.5 },
        ec: { min: 0.5, max: 3.0 },
      };

      if (readings.soilMoisture < thresholds.soilMoisture.min) {
        device.alerts.push({
          type: 'Low soil moisture',
          threshold: `< ${thresholds.soilMoisture.min}%`,
          severity: 'high',
          message: 'Urgent: Activate irrigation immediately',
          createdAt: new Date(),
          resolved: false,
        });
      }

      if (readings.temperature > thresholds.temperature.max) {
        device.alerts.push({
          type: 'High temperature',
          threshold: `> ${thresholds.temperature.max}°C`,
          severity: 'medium',
          message: 'Increase irrigation to manage heat stress',
          createdAt: new Date(),
          resolved: false,
        });
      }

      // Keep only last 50 alerts
      if (device.alerts.length > 50) {
        device.alerts = device.alerts.slice(-50);
      }
    } catch (error) {
      logger.error('Check and create alerts error:', error.message);
    }
  },

  async registerDevice(farmerId, deviceData) {
    try {
      const device = new IoTDevice({
        farmerId,
        ...deviceData,
        status: 'active',
      });

      await device.save();

      // Subscribe to device topics
      mqttClient.subscribe(`farm/${device.deviceId}/sensors/+`);

      return device;
    } catch (error) {
      logger.error('Register device error:', error.message);
      throw error;
    }
  },

  async getDeviceStatus(deviceId) {
    try {
      const device = await IoTDevice.findOne({ deviceId });
      return {
        deviceId: device.deviceId,
        status: device.status,
        lastDataReceived: device.lastDataReceived,
        batteryLevel: device.batteryLevel,
        signalStrength: device.signalStrength,
        latestReadings: device.latestReadings,
      };
    } catch (error) {
      logger.error('Get device status error:', error.message);
      throw error;
    }
  },

  async getDeviceHistory(deviceId, hours = 24) {
    try {
      const device = await IoTDevice.findOne({ deviceId });
      const cutoffTime = new Date(Date.now() - hours * 60 * 60 * 1000);

      const history = device.sensorDataHistory.filter(
        reading => reading.timestamp >= cutoffTime
      );

      return history;
    } catch (error) {
      logger.error('Get device history error:', error.message);
      throw error;
    }
  },
};

module.exports = iotService;
