# Smart Farming Development Workflow Guide

This guide outlines best practices for developing, testing, and deploying features within the Smart Farming Ecosystem.

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Git Workflow](#git-workflow)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [ML Model Development](#ml-model-development)
7. [Testing Strategy](#testing-strategy)
8. [Code Standards](#code-standards)
9. [Debugging Tips](#debugging-tips)
10. [Deployment Pipeline](#deployment-pipeline)

---

## Development Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd AI-in-agriculture-and-food-production-2
```

### 2. Install Development Tools
```bash
# Node.js and npm (required)
node --version  # Should be v18+
npm --version   # Should be v9+

# Python (required for ML models and voice assistant)
python --version  # Should be v3.8+

# Docker (optional but recommended)
docker --version
docker-compose --version
```

### 3. Setup Local Environment
```bash
# Create .env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install

# Install Python dependencies
cd ../
pip install -r requirements.txt
```

### 4. Start Development Services
```bash
# Terminal 1: Start MongoDB & Redis (via Docker)
docker run -d -p 27017:27017 --name mongodb mongo:6.0
docker run -d -p 6379:6379 --name redis redis:7.0
docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto:latest

# Terminal 2: Start Backend
cd backend
npm run dev

# Terminal 3: Start Frontend
cd frontend
npm start

# Terminal 4: Optional - Start Chatbot/Voice services
python chatbot/farming_chatbot.py
```

---

## Project Structure

```
AI-in-agriculture-and-food-production-2/
│
├── backend/                          # Node.js API Server
│   ├── src/
│   │   ├── config/                  # Configuration files
│   │   │   ├── database.js          # MongoDB connection
│   │   │   └── redis.js             # Redis client
│   │   ├── models/                  # Mongoose schemas
│   │   │   ├── Farmer.js
│   │   │   ├── Crop.js
│   │   │   ├── DiseaseDetection.js
│   │   │   ├── PricePrediction.js
│   │   │   ├── WeatherAdvisory.js
│   │   │   ├── IoTDevice.js
│   │   │   └── Subsidy.js
│   │   ├── services/                # Business logic
│   │   │   ├── authService.js
│   │   │   ├── cropService.js
│   │   │   ├── diseaseService.js
│   │   │   ├── weatherService.js
│   │   │   ├── priceService.js
│   │   │   └── iotService.js
│   │   ├── controllers/             # Request handlers
│   │   │   ├── authController.js
│   │   │   ├── cropController.js
│   │   │   ├── diseaseController.js
│   │   │   ├── weatherController.js
│   │   │   ├── priceController.js
│   │   │   └── iotController.js
│   │   ├── routes/                  # API routes
│   │   │   ├── authRoutes.js
│   │   │   ├── cropRoutes.js
│   │   │   ├── diseaseRoutes.js
│   │   │   ├── weatherRoutes.js
│   │   │   ├── priceRoutes.js
│   │   │   ├── iotRoutes.js
│   │   │   └── subsidyRoutes.js
│   │   ├── middleware/              # Express middleware
│   │   │   └── auth.js              # JWT authentication
│   │   ├── utils/                   # Utilities
│   │   │   ├── logger.js            # Winston logger
│   │   │   └── tokenUtils.js        # JWT utilities
│   │   └── server.js                # Express server entry
│   ├── logs/                        # Application logs
│   ├── uploads/                     # Uploaded files
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Example env
│   ├── package.json                 # Dependencies
│   └── Dockerfile                   # Docker config
│
├── frontend/                         # React Application
│   ├── public/                      # Static assets
│   ├── src/
│   │   ├── pages/                   # Page components
│   │   │   ├── LoginPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DiseaseDetection.jsx
│   │   │   ├── WeatherAdvisory.jsx
│   │   │   ├── PriceAnalysis.jsx
│   │   │   ├── IoTMonitoring.jsx
│   │   │   └── [page-styles].css
│   │   ├── components/              # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Chatbot.jsx
│   │   │   ├── [component-styles].css
│   │   │   └── ...
│   │   ├── services/                # API clients
│   │   │   ├── api.js               # Axios instance
│   │   │   └── ...                  # Service files
│   │   ├── hooks/                   # Custom hooks
│   │   ├── context/                 # Context API
│   │   ├── utils/                   # Utilities
│   │   ├── App.jsx                  # Main App component
│   │   ├── index.js                 # Entry point
│   │   └── [global-styles].css      # Global styles
│   ├── package.json                 # Dependencies
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Example env
│   └── Dockerfile                   # Docker config
│
├── admin-panel/                      # Admin Dashboard
│   └── src/pages/AdminDashboard.jsx
│
├── ml-models/                        # Python ML Models
│   ├── disease-detection/
│   │   └── disease_detection_model.py
│   ├── price-prediction/
│   │   └── price_prediction_model.py
│   ├── crop-recommendation/
│   │   └── crop_recommendation_model.py
│   └── yield-forecasting/
│       └── yield_forecasting_model.py
│
├── voice-assistant/                  # Voice AI
│   └── voice_assistant.py
│
├── chatbot/                          # Chatbot
│   └── farming_chatbot.py
│
├── iot-service/                      # IoT Integration
│   └── mqtt-handler.py
│
├── docker/                           # Docker Setup
│   └── docker-compose.yml
│
├── COMPREHENSIVE_README.md           # Complete documentation
├── API_REFERENCE.md                  # API documentation
├── SETUP_GUIDE.md                    # Setup instructions
├── QUICK_START.md                    # Quick start
├── requirements.txt                  # Python dependencies
└── README.md                         # Project overview
```

---

## Git Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/disease-detection-improvement
# Or for bug fixes:
git checkout -b bugfix/login-error
```

### 2. Make Changes and Commit
```bash
# Check status
git status

# Stage changes
git add .
# Or specific files
git add backend/src/services/diseaseService.js

# Commit with descriptive message
git commit -m "feat: improve disease detection accuracy by 5%"
# or
git commit -m "fix: resolve login timeout issue"
```

### 3. Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Scope**: Feature area (disease, weather, price, iot, etc.)
**Subject**: Brief description in imperative mood

**Examples:**
```
feat(disease): add new disease classification model
fix(auth): prevent JWT token expiration loop
docs(api): update price prediction endpoint documentation
refactor(weather): optimize advisory generation logic
test(crop): add unit tests for crop metrics calculation
```

### 4. Push and Create Pull Request
```bash
git push origin feature/disease-detection-improvement

# Create PR on GitHub with description
# - What changes were made
# - Why they were needed
# - How to test them
```

### 5. Code Review and Merge
```bash
# After approval
git checkout main
git pull origin main
git merge feature/disease-detection-improvement
git push origin main
```

---

## Backend Development

### Adding a New API Endpoint

#### 1. Create Model (if needed)
**File**: `backend/src/models/NewFeature.js`
```javascript
const mongoose = require('mongoose');

const newFeatureSchema = new mongoose.Schema({
  farmerId: { type: mongoose.Schema.Types.ObjectId, ref: 'Farmer', required: true },
  data: String,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('NewFeature', newFeatureSchema);
```

#### 2. Create Service
**File**: `backend/src/services/newFeatureService.js`
```javascript
const NewFeature = require('../models/NewFeature');

class NewFeatureService {
  static async create(farmerId, data) {
    try {
      const feature = new NewFeature({ farmerId, data });
      return await feature.save();
    } catch (error) {
      throw new Error(`Failed to create feature: ${error.message}`);
    }
  }

  static async getByFarmerId(farmerId) {
    return NewFeature.find({ farmerId });
  }

  static async updateById(id, updateData) {
    return NewFeature.findByIdAndUpdate(id, updateData, { new: true });
  }

  static async deleteById(id) {
    return NewFeature.findByIdAndDelete(id);
  }
}

module.exports = NewFeatureService;
```

#### 3. Create Controller
**File**: `backend/src/controllers/newFeatureController.js`
```javascript
const NewFeatureService = require('../services/newFeatureService');
const logger = require('../utils/logger');

class NewFeatureController {
  static async create(req, res) {
    try {
      const { data } = req.body;
      const result = await NewFeatureService.create(req.user.id, data);
      res.status(201).json({ success: true, data: result });
    } catch (error) {
      logger.error('Error creating feature:', error);
      res.status(500).json({ success: false, message: error.message });
    }
  }

  static async getByFarmer(req, res) {
    try {
      const result = await NewFeatureService.getByFarmerId(req.user.id);
      res.json({ success: true, data: result });
    } catch (error) {
      logger.error('Error fetching features:', error);
      res.status(500).json({ success: false, message: error.message });
    }
  }
}

module.exports = NewFeatureController;
```

#### 4. Create Routes
**File**: `backend/src/routes/newFeatureRoutes.js`
```javascript
const express = require('express');
const router = express.Router();
const NewFeatureController = require('../controllers/newFeatureController');
const authMiddleware = require('../middleware/auth');

router.post('/', authMiddleware, NewFeatureController.create);
router.get('/', authMiddleware, NewFeatureController.getByFarmer);

module.exports = router;
```

#### 5. Register Routes in Server
**File**: `backend/src/server.js`
```javascript
const newFeatureRoutes = require('./routes/newFeatureRoutes');
app.use('/api/newfeature', newFeatureRoutes);
```

#### 6. Test the Endpoint
```bash
curl -X POST http://localhost:5000/api/newfeature \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

---

## Frontend Development

### Adding a New Page Component

#### 1. Create Page Component
**File**: `frontend/src/pages/NewPage.jsx`
```jsx
import React, { useState, useEffect } from 'react';
import './NewPage.css';

function NewPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/newfeature');
      const result = await response.json();
      setData(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="new-page">
      <h1>New Feature</h1>
      {/* Content here */}
    </div>
  );
}

export default NewPage;
```

#### 2. Create Styles
**File**: `frontend/src/pages/NewPage.css`
```css
.new-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.new-page h1 {
  color: #333;
  margin-bottom: 20px;
}
```

#### 3. Add Route
**File**: `frontend/src/App.jsx`
```jsx
import NewPage from './pages/NewPage';

function App() {
  return (
    <Router>
      <Routes>
        {/* ... other routes ... */}
        <Route path="/newpage" element={<NewPage />} />
      </Routes>
    </Router>
  );
}
```

### Hot Reload Development
```bash
cd frontend
npm start
# Changes automatically reload in browser
```

---

## ML Model Development

### Training a Disease Detection Model

**File**: `ml-models/disease-detection/train_model.py`
```python
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

class DiseaseDetectionTrainer:
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(8, activation='softmax')  # 8 disease classes
        ])
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def train(self, train_data, val_data, epochs=50):
        history = self.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            verbose=1
        )
        return history
    
    def save_model(self, filepath):
        self.model.save(filepath)
        print(f"Model saved to {filepath}")

# Usage
if __name__ == "__main__":
    trainer = DiseaseDetectionTrainer()
    # Load training data
    # trainer.train(train_data, val_data)
    # trainer.save_model('disease_model.h5')
```

---

## Testing Strategy

### Backend Testing

#### Unit Tests
```bash
cd backend
npm install --save-dev jest supertest

# Create test file: backend/src/__tests__/services.test.js
npm test
```

#### Run Single Test
```bash
npm test -- --testNamePattern="auth"
```

### Frontend Testing

#### Run Tests
```bash
cd frontend
npm test
```

#### Test Coverage
```bash
npm test -- --coverage
```

---

## Code Standards

### JavaScript (Backend & Frontend)

1. **Use Const/Let (No Var)**
```javascript
// ✅ Good
const user = await User.findById(id);
let count = 0;

// ❌ Avoid
var user = await User.findById(id);
```

2. **Use Async/Await (No Callbacks)**
```javascript
// ✅ Good
async function getUser(id) {
  const user = await User.findById(id);
  return user;
}

// ❌ Avoid
function getUser(id, callback) {
  User.findById(id, (err, user) => {
    callback(user);
  });
}
```

3. **Error Handling**
```javascript
// ✅ Good
try {
  const result = await someOperation();
  return { success: true, data: result };
} catch (error) {
  logger.error('Operation failed:', error);
  return { success: false, message: error.message };
}

// ❌ Avoid
const result = await someOperation(); // No error handling
```

4. **Comments**
```javascript
// ✅ Good - Explain WHY, not WHAT
// Cache for 24 hours to reduce API calls to weather service
const cacheKey = `weather_${farmerId}`;

// ❌ Avoid - Obvious from code
// Get the weather
const weather = getWeather(farmerId);
```

### React

1. **Use Functional Components**
```jsx
// ✅ Good
function Dashboard() {
  const [data, setData] = useState(null);
  useEffect(() => { /* ... */ }, []);
  return <div>{/* ... */}</div>;
}

// ❌ Avoid
class Dashboard extends React.Component { /* ... */ }
```

2. **Props Destructuring**
```jsx
// ✅ Good
function Card({ title, description, onClick }) {
  return <div onClick={onClick}>{title}</div>;
}

// ❌ Avoid
function Card(props) {
  return <div onClick={props.onClick}>{props.title}</div>;
}
```

3. **Use Keys in Lists**
```jsx
// ✅ Good
{crops.map(crop => (
  <CropCard key={crop.id} crop={crop} />
))}

// ❌ Avoid
{crops.map((crop, index) => (
  <CropCard key={index} crop={crop} />
))}
```

---

## Debugging Tips

### Backend Debugging

#### 1. Enable Detailed Logging
```javascript
// In backend/.env
LOG_LEVEL=debug

// In code, use logger extensively
logger.debug('Checking user permissions', { userId, role });
logger.info('Crop created successfully', { cropId });
logger.error('Database connection failed', error);
```

#### 2. Use VS Code Debugger
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Backend",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/backend/src/server.js",
      "env": { "NODE_ENV": "development" }
    }
  ]
}
```

#### 3. MongoDB Debugging
```bash
# Connect to MongoDB
mongosh smart_farming

# View collections
db.crops.find()

# Check indexes
db.crops.getIndexes()

# Clear collection for testing
db.crops.deleteMany({})
```

### Frontend Debugging

#### 1. Browser DevTools
- Ctrl+Shift+I (Inspector)
- Ctrl+Shift+J (Console)
- Ctrl+Shift+K (Network)
- Ctrl+Shift+E (Storage)

#### 2. React DevTools Extension
Install Chrome/Firefox extension for easier component inspection

#### 3. API Monitoring
```javascript
// Add interceptor to monitor all API calls
import axios from 'axios';

axios.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response;
  },
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

---

## Deployment Pipeline

### 1. Development Environment
- Local development with hot reload
- Testing on localhost:3000 and localhost:5000

### 2. Staging Environment
```bash
# Build production images
docker build -f backend/Dockerfile -t smart-farming-api:latest ./backend
docker build -f frontend/Dockerfile -t smart-farming-web:latest ./frontend

# Push to registry
docker tag smart-farming-api:latest registry.example.com/smart-farming-api:latest
docker push registry.example.com/smart-farming-api:latest
```

### 3. Production Deployment
```bash
# Update docker-compose with production images and environment
# Deploy to production infrastructure
docker-compose -f docker/docker-compose.prod.yml up -d
```

### 4. Monitoring in Production
```bash
# Check logs
docker logs -f api-container-name

# Monitor performance
docker stats

# Check health
curl http://api-url/api/health
```

---

## Common Development Tasks

### Update Dependencies
```bash
# Backend
cd backend
npm update
npm audit fix

# Frontend
cd frontend
npm update
npm audit fix
```

### Database Migration
```bash
# Connect to MongoDB
mongosh smart_farming

# Add new field to schema
db.crops.updateMany({}, { $set: { newField: null } })
```

### Clear Cache
```bash
# Redis
redis-cli FLUSHDB

# Or via Docker
docker exec redis redis-cli FLUSHDB
```

---

## Quick Reference Commands

```bash
# Development
npm install              # Install dependencies
npm start               # Start with hot reload
npm run dev             # Start with nodemon (backend)
npm test                # Run tests
npm run build           # Build for production

# Docker
docker-compose up       # Start all services
docker-compose down     # Stop all services
docker-compose logs     # View logs
docker ps               # List running containers
docker exec -it <id> sh # Connect to container

# Git
git status              # Check changes
git add .               # Stage all changes
git commit -m "msg"     # Commit changes
git push origin branch   # Push to remote
git pull                # Pull latest changes
git log --oneline       # View commit history
```

---

**Happy Coding! 🚀**

For questions or issues, refer to the main documentation or GitHub issues.

---

**Last Updated**: 2024
**Version**: 1.0.0
