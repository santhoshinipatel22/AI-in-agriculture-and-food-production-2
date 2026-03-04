# Smart Farming Ecosystem - Setup & Installation Guide

This guide will help you set up and deploy the complete Smart Farming Ecosystem locally or in production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Quick Start (Docker)](#quick-start-docker)
4. [Manual Setup](#manual-setup)
5. [Environment Configuration](#environment-configuration)
6. [Database Seeding](#database-seeding)
7. [API Testing](#api-testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: macOS, Linux, or Windows (with WSL2)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: Minimum 2GB free space

### Software Requirements
- **Node.js**: v18.0 or higher ([Download](https://nodejs.org/))
- **Python**: v3.8 or higher ([Download](https://www.python.org/))
- **Docker & Docker Compose**: v20.0+ ([Download](https://www.docker.com/))
- **MongoDB**: v6.0 (via Docker or local installation)
- **Redis**: v7.0 (via Docker or local installation)
- **Git**: v2.0+ ([Download](https://git-scm.com/))

### API Keys Required
- **OpenWeatherMap**: [Sign up](https://openweathermap.org/api) - Free tier available
- **Google Cloud**: [Setup project](https://console.cloud.google.com/) for Speech/Text-to-Speech APIs
- **Sentinel Hub**: [Register](https://www.sentinel-hub.com/) for satellite imagery (optional)
- **Twilio**: [Sign up](https://www.twilio.com/) for SMS notifications (optional)
- **SendGrid**: [Sign up](https://sendgrid.com/) for email notifications (optional)

---

## Project Structure

```
AI-in-agriculture-and-food-production-2/
├── backend/                          # Node.js Express API server
│   ├── src/
│   │   ├── models/                  # MongoDB schemas
│   │   ├── services/                # Business logic layer
│   │   ├── controllers/             # Request handlers
│   │   ├── routes/                  # API routes
│   │   ├── middleware/              # Auth, error handling
│   │   ├── config/                  # Database, Redis config
│   │   ├── utils/                   # Logger, tokenUtils
│   │   └── server.js                # Express server entry
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
├── frontend/                         # React 18 frontend
│   ├── src/
│   │   ├── pages/                   # Page components + CSS
│   │   ├── components/              # Reusable components + CSS
│   │   ├── App.jsx                  # Router setup
│   │   └── index.js                 # React DOM render
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
├── admin-panel/                      # Admin dashboard
│   └── src/pages/AdminDashboard.jsx
├── ml-models/                        # Python ML models
│   ├── disease-detection/
│   ├── price-prediction/
│   └── crop-recommendation/
├── voice-assistant/                  # Voice AI
│   └── voice_assistant.py
├── chatbot/                          # Farming chatbot
│   └── farming_chatbot.py
├── iot-service/                      # IoT integration
│   └── mqtt-handler.py               # MQTT listener (optional)
├── docker/                           # Docker orchestration
│   └── docker-compose.yml
└── COMPREHENSIVE_README.md           # Full documentation
```

---

## Quick Start (Docker)

### 1. Clone the Repository
```bash
cd /workspaces/AI-in-agriculture-and-food-production-2
```

### 2. Create Environment Files

**Backend (.env)**
```bash
cd backend
cp .env.example .env
# Edit .env with your API keys (see Environment Configuration section)
cd ..
```

**Frontend (.env)**
```bash
cd frontend
cp .env.example .env
# Edit .env with backend API URL
cd ..
```

### 3. Start All Services with Docker Compose

```bash
cd docker
docker-compose up -d
```

This will automatically start:
- **MongoDB** (Port 27017) - Database
- **Redis** (Port 6379) - Cache layer
- **Mosquitto MQTT** (Port 1883) - IoT message broker
- **Backend API** (Port 5000) - Express.js server
- **Frontend** (Port 3000) - React application

### 4. Verify Services are Running

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

### 6. Seed Initial Data

```bash
# Connect to MongoDB container
docker exec -it mongodb mongosh

# Run these commands in mongosh:
use smart_farming
db.subsidies.insertMany([
  {
    subsidyId: "GOV-2024-001",
    name: "Pradhan Mantri Fasal Bima Yojana",
    description: "Crop insurance scheme for farmers",
    governmentBody: "Ministry of Agriculture",
    amount: 15000,
    currency: "INR",
    applicableCrops: ["rice", "wheat", "corn"],
    applicableRegions: ["Tamil Nadu", "Telangana"],
    applicationDeadline: "2024-12-31",
    status: "active"
  }
])

exit
```

### 7. Stop Services

```bash
cd docker
docker-compose down
```

---

## Manual Setup

### Backend Setup

#### 1. Install Node Dependencies
```bash
cd backend
npm install
```

#### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with:
```env
# Server
PORT=5000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/smart_farming
MONGODB_MAX_POOL_SIZE=10
MONGODB_SOCKET_TIMEOUT_MS=45000

# Redis
REDIS_URL=redis://localhost:6379

# MQTT
MQTT_BROKER_URL=mqtt://localhost:1883
MQTT_USERNAME=
MQTT_PASSWORD=

# JWT
JWT_SECRET=your-super-secret-jwt-key-min-32-characters-long-12345
JWT_REFRESH_SECRET=your-super-secret-refresh-key-12345
JWT_EXPIRE=7d
JWT_REFRESH_EXPIRE=30d

# APIs
OPENWEATHERMAP_API_KEY=your-api-key
GOOGLE_CLOUD_API_KEY=your-api-key
SENTINEL_HUB_API_KEY=your-api-key
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
SENDGRID_API_KEY=your-api-key
SENDGRID_FROM_EMAIL=noreply@smartfarming.com

# File Upload
MAX_FILE_SIZE=5242880
UPLOAD_DIR=./uploads

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

#### 3. Start MongoDB & Redis (Local)

```bash
# macOS (using homebrew)
brew services start mongodb-community
brew services start redis

# Linux
sudo systemctl start mongod
sudo systemctl start redis-server

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:6.0
docker run -d -p 6379:6379 --name redis redis:7.0
```

#### 4. Start Backend Server
```bash
npm start
# Or for development with auto-reload
npm run dev
```

Backend will be available at: `http://localhost:5000`

### Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

#### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
REACT_APP_MAPBOX_TOKEN=your-mapbox-token
REACT_APP_ENVIRONMENT=development
```

#### 3. Start Development Server
```bash
npm start
```

Frontend will be available at: `http://localhost:3000`

### ML Models & Voice Assistant Setup

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Setup Google Cloud Credentials
```bash
# Download JSON credentials from Google Cloud Console
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Or create a credentials file
mkdir -p ~/.config/gcloud
cp credentials.json ~/.config/gcloud/
```

#### 3. Test Disease Detection Model
```bash
python ml-models/disease-detection/disease_detection_model.py
```

#### 4. Test Voice Assistant
```bash
python voice-assistant/voice_assistant.py
```

#### 5. Test Chatbot
```bash
python chatbot/farming_chatbot.py
```

---

## Environment Configuration

### Backend .env Details

| Variable | Description | Example |
|----------|-------------|---------|
| `PORT` | API server port | `5000` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/smart_farming` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `JWT_SECRET` | JWT signing secret (min 32 chars) | `your-long-secret-key-here` |
| `OPENWEATHERMAP_API_KEY` | Weather API key | Get from OpenWeatherMap |
| `GOOGLE_CLOUD_API_KEY` | Google Cloud Services API | Get from Google Cloud Console |

### Frontend .env Details

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:5000` |
| `REACT_APP_SOCKET_URL` | WebSocket server URL | `http://localhost:5000` |
| `REACT_APP_MAPBOX_TOKEN` | Mapbox access token | Get from Mapbox |

---

## Database Seeding

### Initial Data Setup

```bash
# Connect to MongoDB
docker exec -it mongodb mongosh smart_farming

# Insert test user
db.farmers.insertOne({
  firstName: "Demo",
  lastName: "Farmer",
  email: "demo@farm.com",
  password: "$2b$10$...", // bcrypted password
  phone: "9876543210",
  farmDetails: {
    location: {
      address: "123 Farm Road",
      coordinates: { type: "Point", coordinates: [78.1234, 11.1234] },
      district: "Villupuram",
      state: "Tamil Nadu"
    },
    farmSize: 25,
    crops: ["rice", "sugarcane"]
  },
  subscription: "basic",
  createdAt: new Date()
})

# Insert sample crops
db.crops.insertMany([
  {
    farmerId: ObjectId("..."),
    cropName: "Rice",
    fieldName: "Field 1",
    fieldArea: 10,
    sowingDate: "2024-01-15",
    expectedHarvestDate: "2024-05-15",
    status: "growing",
    createdAt: new Date()
  }
])

# Insert subsidies (as shown in Quick Start section above)
```

---

## API Testing

### Using Postman

1. **Import Collection**
   - Open Postman
   - Click "Import"
   - Use the API endpoints listed in COMPREHENSIVE_README.md

2. **Setup Postman Environment**
```json
{
  "baseUrl": "http://localhost:5000",
  "authToken": "your-jwt-token-here"
}
```

### Using cURL

#### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Farmer",
    "email": "john@farm.com",
    "password": "SecurePass123!",
    "phone": "9876543210"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@farm.com",
    "password": "SecurePass123!"
  }'
```

#### Get Dashboard Data
```bash
curl -X GET http://localhost:5000/api/crops \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using REST Client (VS Code Extension)

Create a file `requests.http`:
```http
### Register
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Farmer",
  "email": "john@farm.com",
  "password": "SecurePass123!",
  "phone": "9876543210"
}

### Login
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "john@farm.com",
  "password": "SecurePass123!"
}
```

---

## Troubleshooting

### Port Already in Use

```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Kill process using port 3000
lsof -ti:3000 | xargs kill -9

# Kill process using port 27017 (MongoDB)
lsof -ti:27017 | xargs kill -9
```

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
docker ps | grep mongodb

# View MongoDB logs
docker logs mongodb

# Restart MongoDB
docker restart mongodb
```

### Redis Connection Issues

```bash
# Test Redis connection
redis-cli ping
# Expected response: PONG

# Clear Redis cache
redis-cli FLUSHDB

# Reset Redis
docker exec redis redis-cli FLUSHALL
```

### Frontend Not Loading API Data

1. **Check CORS Settings** - Verify `CORS_ORIGINS` in backend `.env`
2. **Verify API URL** - Ensure `REACT_APP_API_URL` matches backend URL
3. **Check Network Tab** - Open DevTools → Network tab to see API calls
4. **Review Logs** - Check browser console and backend logs for errors

### Docker Compose Issues

```bash
# Rebuild images
docker-compose build --no-cache

# Start with verbose logging
docker-compose up --verbose

# Check specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Completely reset (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

### Python Dependency Issues

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Test imports
python -c "import tensorflow; print(tensorflow.__version__)"
```

### JWT Token Issues

```bash
# Generate new JWT secret
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Update .env with new secret
# Restart backend server
```

---

## Production Deployment

### Environment Setup

```env
NODE_ENV=production
PORT=5000

# Database - Use cloud MongoDB Atlas
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/smart_farming

# Redis - Use cloud Redis (e.g., AWS ElastiCache, Redis Cloud)
REDIS_URL=redis://username:password@cloud-redis-host:6379

# CORS - Restrict to your domain
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# Use environment variables from deployment platform
# AWS Secrets Manager, Heroku Config Vars, etc.
```

### Docker Deployment

```bash
# Build production image
docker build -f backend/Dockerfile -t smart-farming-api:latest ./backend
docker build -f frontend/Dockerfile -t smart-farming-web:latest ./frontend

# Push to registry
docker push your-registry/smart-farming-api:latest
docker push your-registry/smart-farming-web:latest

# Deploy on your infrastructure (AWS, GCP, Azure, DigitalOcean, etc.)
```

### Kubernetes Deployment (Optional)

```bash
# Create deployments
kubectl create deployment smart-farming-api --image=your-registry/smart-farming-api:latest
kubectl create deployment smart-farming-web --image=your-registry/smart-farming-web:latest

# Expose services
kubectl expose deployment smart-farming-api --type=LoadBalancer --port=5000
kubectl expose deployment smart-farming-web --type=LoadBalancer --port=3000
```

---

## Support & Documentation

- **API Documentation**: See [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md)
- **Component Documentation**: JSDoc comments in React components
- **ML Model Docs**: Docstrings in Python files
- **Community Support**: GitHub Issues

---

## License & Credits

Created for Smart Agriculture Innovation
For support or questions, see COMPREHENSIVE_README.md

---

**Last Updated**: 2024
**Version**: 1.0.0
