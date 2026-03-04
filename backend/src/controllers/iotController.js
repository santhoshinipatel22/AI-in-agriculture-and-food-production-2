const iotService = require('../services/iotService');
const logger = require('../utils/logger');

const iotController = {
  async registerDevice(req, res, next) {
    try {
      const device = await iotService.registerDevice(req.user.userId, req.body);

      res.status(201).json({
        success: true,
        data: device,
      });
    } catch (error) {
      logger.error('Register device controller error:', error.message);
      next(error);
    }
  },

  async getDeviceStatus(req, res, next) {
    try {
      const { deviceId } = req.params;
      const status = await iotService.getDeviceStatus(deviceId);

      res.status(200).json({
        success: true,
        data: status,
      });
    } catch (error) {
      logger.error('Get device status controller error:', error.message);
      next(error);
    }
  },

  async getDeviceHistory(req, res, next) {
    try {
      const { deviceId } = req.params;
      const { hours = 24 } = req.query;

      const history = await iotService.getDeviceHistory(
        deviceId,
        parseInt(hours)
      );

      res.status(200).json({
        success: true,
        data: history,
        count: history.length,
      });
    } catch (error) {
      logger.error('Get device history controller error:', error.message);
      next(error);
    }
  },

  async getLatestReadings(req, res, next) {
    try {
      const { deviceId } = req.params;
      const status = await iotService.getDeviceStatus(deviceId);

      res.status(200).json({
        success: true,
        data: status.latestReadings,
      });
    } catch (error) {
      logger.error('Get latest readings controller error:', error.message);
      next(error);
    }
  },
};

module.exports = iotController;
