const authService = require('../services/authService');
const logger = require('../utils/logger');

const authController = {
  async register(req, res, next) {
    try {
      const result = await authService.register(req.body);
      res.status(201).json(result);
    } catch (error) {
      logger.error('Register controller error:', error.message);
      next(error);
    }
  },

  async login(req, res, next) {
    try {
      const { email, password } = req.body;

      if (!email || !password) {
        return res.status(400).json({
          success: false,
          message: 'Email and password are required',
        });
      }

      const result = await authService.login(email, password);
      res.status(200).json(result);
    } catch (error) {
      logger.error('Login controller error:', error.message);
      res.status(401).json({
        success: false,
        message: error.message,
      });
    }
  },

  async verifyEmail(req, res, next) {
    try {
      const { token } = req.params;
      const result = await authService.verifyEmail(token);
      res.status(200).json(result);
    } catch (error) {
      logger.error('Verify email controller error:', error.message);
      next(error);
    }
  },

  async refreshToken(req, res, next) {
    try {
      const { refreshToken } = req.body;

      if (!refreshToken) {
        return res.status(400).json({
          success: false,
          message: 'Refresh token is required',
        });
      }

      const result = await authService.refreshAccessToken(refreshToken);
      res.status(200).json(result);
    } catch (error) {
      logger.error('Refresh token controller error:', error.message);
      res.status(401).json({
        success: false,
        message: error.message,
      });
    }
  },

  async logout(req, res, next) {
    try {
      const result = await authService.logout(req.user.userId);
      res.status(200).json(result);
    } catch (error) {
      logger.error('Logout controller error:', error.message);
      next(error);
    }
  },

  async resetPasswordRequest(req, res, next) {
    try {
      const { email } = req.body;
      const result = await authService.resetPassword(email);
      res.status(200).json(result);
    } catch (error) {
      logger.error('Reset password request controller error:', error.message);
      next(error);
    }
  },
};

module.exports = authController;
