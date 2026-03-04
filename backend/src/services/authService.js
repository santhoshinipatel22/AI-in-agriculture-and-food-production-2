const Farmer = require('../models/Farmer');
const { generateTokens } = require('../utils/tokenUtils');
const logger = require('../utils/logger');

const authService = {
  async register(userData) {
    try {
      const { email, phone, password, firstName, lastName } = userData;

      // Check if user exists
      const existingFarmer = await Farmer.findOne({
        $or: [{ email }, { phone }],
      });

      if (existingFarmer) {
        throw new Error('Email or phone already registered');
      }

      // Create new farmer
      const farmer = new Farmer({
        ...userData,
        isVerified: false,
      });

      await farmer.save();

      const { accessToken, refreshToken } = generateTokens(farmer._id, farmer.role);

      return {
        success: true,
        farmer: {
          id: farmer._id,
          email: farmer.email,
          firstName: farmer.firstName,
          lastName: farmer.lastName,
          role: farmer.role,
        },
        tokens: { accessToken, refreshToken },
      };
    } catch (error) {
      logger.error('Registration error:', error.message);
      throw error;
    }
  },

  async login(email, password) {
    try {
      const farmer = await Farmer.findOne({ email }).select('+password');

      if (!farmer || !(await farmer.matchPassword(password))) {
        throw new Error('Invalid email or password');
      }

      farmer.lastLogin = new Date();
      await farmer.save();

      const { accessToken, refreshToken } = generateTokens(farmer._id, farmer.role);

      return {
        success: true,
        farmer: {
          id: farmer._id,
          email: farmer.email,
          firstName: farmer.firstName,
          lastName: farmer.lastName,
          farmName: farmer.farmName,
          role: farmer.role,
          subscriptionPlan: farmer.subscriptionPlan,
        },
        tokens: { accessToken, refreshToken },
      };
    } catch (error) {
      logger.error('Login error:', error.message);
      throw error;
    }
  },

  async verifyEmail(token) {
    try {
      const farmer = await Farmer.findOne({ verificationToken: token });

      if (!farmer) {
        throw new Error('Invalid verification token');
      }

      farmer.isVerified = true;
      farmer.verificationToken = undefined;
      await farmer.save();

      return { success: true, message: 'Email verified successfully' };
    } catch (error) {
      logger.error('Email verification error:', error.message);
      throw error;
    }
  },

  async refreshAccessToken(refreshToken) {
    try {
      const decoded = jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET);
      const farmer = await Farmer.findById(decoded.userId);

      if (!farmer) {
        throw new Error('Farmer not found');
      }

      const tokens = generateTokens(farmer._id, farmer.role);
      return { success: true, tokens };
    } catch (error) {
      logger.error('Token refresh error:', error.message);
      throw error;
    }
  },

  async logout(userId) {
    // Add token to blacklist in Redis
    return { success: true, message: 'Logged out successfully' };
  },

  async resetPassword(email) {
    try {
      const farmer = await Farmer.findOne({ email });

      if (!farmer) {
        throw new Error('Farmer not found');
      }

      // Generate reset token
      const resetToken = require('crypto').randomBytes(32).toString('hex');
      farmer.resetPasswordToken = require('crypto').createHash('sha256').update(resetToken).digest('hex');
      farmer.resetPasswordExpire = Date.now() + 30 * 60 * 1000; // 30 minutes
      await farmer.save();

      return { success: true, resetToken };
    } catch (error) {
      logger.error('Password reset error:', error.message);
      throw error;
    }
  },
};

module.exports = authService;
