const express = require('express');
const { Subsidy, FarmerSubsidyApplication } = require('../models/Subsidy');
const { authMiddleware } = require('../middleware/auth');
const logger = require('../utils/logger');

const router = express.Router();

// Get all active subsidies (public)
router.get('/', async (req, res) => {
  try {
    const subsidies = await Subsidy.find({ status: 'active' });
    res.status(200).json({
      success: true,
      data: subsidies,
    });
  } catch (error) {
    logger.error('Get subsidies error:', error.message);
    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
});

// Get subsidies applicable for a farmer (requires auth)
router.get('/applicable', authMiddleware, async (req, res) => {
  try {
    const { cropTypes, region } = req.query;

    const subsidies = await Subsidy.find({
      status: 'active',
      applicableCrops: { $in: cropTypes?.split(',') || [] },
      applicableRegions: { $in: region ? [region] : [] },
    });

    res.status(200).json({
      success: true,
      data: subsidies,
    });
  } catch (error) {
    logger.error('Get applicable subsidies error:', error.message);
    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
});

// Apply for a subsidy (requires auth)
router.post('/apply/:subsidyId', authMiddleware, async (req, res) => {
  try {
    const application = new FarmerSubsidyApplication({
      farmerId: req.user.userId,
      subsidyId: req.params.subsidyId,
      documents: req.body.documents,
    });

    await application.save();

    res.status(201).json({
      success: true,
      data: application,
    });
  } catch (error) {
    logger.error('Apply for subsidy error:', error.message);
    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
});

// Get farmer subsidy applications (requires auth)
router.get('/applications', authMiddleware, async (req, res) => {
  try {
    const applications = await FarmerSubsidyApplication.find({
      farmerId: req.user.userId,
    }).populate('subsidyId');

    res.status(200).json({
      success: true,
      data: applications,
    });
  } catch (error) {
    logger.error('Get subsidy applications error:', error.message);
    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
});

module.exports = router;
