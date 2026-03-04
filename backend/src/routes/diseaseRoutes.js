const express = require('express');
const diseaseController = require('../controllers/diseaseController');
const { authMiddleware } = require('../middleware/auth');
const multer = require('multer');

const router = express.Router();
const upload = multer({ dest: 'uploads/diseases/' });

// All routes require authentication
router.use(authMiddleware);

router.post('/detect/:cropId', upload.single('image'), diseaseController.detectDisease);
router.get('/', diseaseController.getDiseases);
router.get('/stats', diseaseController.getDiseaseStats);
router.patch('/:id', diseaseController.updateDiseaseStatus);

module.exports = router;
