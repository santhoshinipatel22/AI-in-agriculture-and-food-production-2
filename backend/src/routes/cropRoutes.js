const express = require('express');
const cropController = require('../controllers/cropController');
const { authMiddleware } = require('../middleware/auth');

const router = express.Router();

// All routes require authentication
router.use(authMiddleware);

router.post('/', cropController.createCrop);
router.get('/', cropController.getCrops);
router.get('/metrics', cropController.getCropMetrics);
router.get('/:id', cropController.getCropById);
router.put('/:id', cropController.updateCrop);
router.delete('/:id', cropController.deleteCrop);
router.get('/:id/diseases', cropController.getCropDiseases);

module.exports = router;
