# AI in Agriculture and Food Production - Smart Farming Ecosystem

A comprehensive, full-stack AI-powered smart farming platform that combines cutting-edge technologies to help farmers make data-driven decisions and maximize productivity.

## 🌾 Features Overview

### 1. **AI Crop Disease Detection**
- Real-time leaf image analysis using CNN deep learning
- Identifies diseases: Powdery Mildew, Leaf Rust, Blight, Root Rot, etc.
- Provides treatment recommendations (organic & chemical)
- Confidence scores and affected area estimation
- Product recommendations with pricing

### 2. **Smart Crop Recommendation Engine**
- Analyzes soil properties (NPK, pH, EC)
- Considers weather conditions and rainfall
- Recommends 5 best crops for current conditions
- Season and region-based suggestions
- Historical yield optimization

### 3. **Real-Time Weather Advisory with Irrigation Guidance**
- 10-day weather forecasts
- Temperature, humidity, rainfall alerts
- Automated irrigation recommendations
- Frost, heat, and drought warnings
- Pesticide spraying timings
- Agricultural advisory based on crop type

### 4. **AI-Powered Crop Price Prediction**
- Machine learning-based market price forecasting
- Historical price trend analysis
- Optimal selling date recommendations
- Market insight dashboards
- Direct market vs. seasonal pricing comparison
- Expected profit calculation

### 5. **Personalized Farmer Dashboard**
- Real-time yield forecasting
- Expense and revenue tracking
- Profit analytics with charts
- Active crop monitoring
- Key metrics at a glance
- Multi-language support (English, Hindi, Telugu)

### 6. **Satellite-Based Crop Monitoring**
- NDVI (vegetation index) analysis
- Field health monitoring
- Early pest/disease detection
- Crop stress identification
- Integration with Sentinel-2 satellite data

### 7. **IoT Sensor Integration**
- Real-time soil moisture monitoring
- Temperature and humidity tracking
- Soil pH and EC measurements
- NPK (Nitrogen, Phosphorus, Potassium) sensors
- MQTT protocol for sensor communication
- Alert system for threshold violations
- Battery level monitoring

### 8. **Multilingual Voice Assistant**
- Telugu, Hindi, and English support
- Voice-activated farming guidance
- Crop disease information via voice
- Market price voice alerts
- Weather updates on demand
- Subsidy information queries

### 9. **24/7 AI Chatbot**
- Intent-based question answering
- Knowledge base of 500+ farming topics
- Real-time disease diagnosis
- Price and market insights
- Irrigation advice
- Government scheme information
- Quick command execution

### 10. **Government Subsidy Alerts**
- Real-time subsidy tracking
- Eligibility checking
- PM-KISAN scheme integration
- Crop insurance information
- Loan and credit facilities
- Application status tracking
- Document upload and verification

### 11. **Secure Farmer Authentication**
- JWT-based authentication
- Two-factor authentication (2FA)
- Email verification
- Password reset functionality
- Refresh token mechanism
- Secure session management

### 12. **Admin Panel**
- System statistics and monitoring
- Farmer management
- AI model version control
- Subsidy management
- System settings and configurations
- Database and server health checks
- Dataset management for model training

## 📊 Technology Stack

### Backend
- **Runtime**: Node.js 18.x
- **Framework**: Express.js 4.18
- **Database**: MongoDB 6.0
- **Cache**: Redis 7.0
- **Message Queue**: Apache Kafka (optional)
- **Message Broker**: Eclipse Mosquitto (MQTT)
- **Authentication**: JWT, 2FA
- **File Upload**: Multer, Sharp
- **Real-time**: Socket.IO
- **Logging**: Winston
- **API Security**: Helmet, Rate Limiting

### Frontend
- **Framework**: React 18.2
- **Routing**: React Router v6
- **State Management**: Zustand
- **Charts**: Recharts, Chart.js
- **Maps**: Leaflet, React-Leaflet
- **Form Handling**: React Hook Form
- **Styling**: Tailwind CSS
- **Icons**: React Icons
- **HTTP Client**: Axios
- **Real-time**: Socket.IO Client
- **Notifications**: React Hot Toast

### AI/ML
- **Deep Learning**: TensorFlow/Keras 4.8
- **Image Processing**: OpenCV, PIL
- **Machine Learning**: Scikit-learn, XGBoost
- **NLP**: NLTK, spaCy
- **Time Series**: Prophet, ARIMA
- **Model Deployment**: TensorFlow Serving

### IoT & Sensors
- **Protocol**: MQTT v3.1.1
- **Gateway**: Mosquitto MQTT Broker
- **Sensor Types**: DHT22, Capacitive Soil Moisture, pH, EC, NPK
- **Microcontrollers**: Arduino, ESP32

### Voice Services
- **Speech Recognition**: Google Cloud Speech-to-Text
- **Text-to-Speech**: Google Cloud Text-to-Speech, pyttsx3
- **Languages**: English, Hindi, Telugu

### Additional Services
- **Weather API**: OpenWeatherMap
- **Satellite Data**: Sentinel Hub
- **SMS/Email**: Twilio, SendGrid
- **Payments**: Razorpay (optional)
- **Video**: AWS S3 for video storage

## 📁 Project Structure

```
AI-in-agriculture-and-food-production-2/
├── backend/                          # Node.js/Express backend
│   ├── src/
│   │   ├── server.js                # Main server entry
│   │   ├── config/                  # Database, Redis, Logger configs
│   │   ├── models/                  # MongoDB schemas
│   │   ├── routes/                  # API routes
│   │   ├── controllers/             # Request handlers
│   │   ├── services/                # Business logic
│   │   ├── middleware/              # Auth, error handling
│   │   └── utils/                   # Helper functions
│   ├── package.json
│   └── Dockerfile
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── App.jsx                  # Main app component
│   │   ├── pages/                   # Page components
│   │   ├── components/              # Reusable components
│   │   ├── services/                # API services
│   │   ├── hooks/                   # Custom hooks
│   │   ├── context/                 # Context API
│   │   └── styles/                  # CSS files
│   ├── package.json
│   └── Dockerfile
├── admin-panel/                      # Admin dashboard
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── services/
│   └── package.json
├── ml-models/                        # AI/ML models
│   ├── disease-detection/           # CNN for disease detection
│   ├── crop-recommendation/         # Recommendation engine
│   ├── price-prediction/            # Price forecasting
│   └── yield-forecasting/           # Yield prediction
├── voice-assistant/                  # Voice assistant service
│   └── voice_assistant.py           # Python implementation
├── chatbot/                          # AI Chatbot
│   └── farming_chatbot.py           # Python implementation
├── iot-service/                      # IoT gateway service
│   └── mqtt_handler.py              # MQTT communication
├── docker/                           # Docker configuration
│   ├── docker-compose.yml           # Multi-container setup
│   └── mosquitto.conf               # MQTT broker config
└── README.md                         # Documentation
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18.x and npm 9.x
- Python 3.8+ (for ML models)
- MongoDB 6.0
- Redis 7.0
- Docker and Docker Compose (recommended)
- MQTT Broker (Mosquitto)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/santhoshinipatel22/AI-in-agriculture-and-food-production-2.git
cd AI-in-agriculture-and-food-production-2
```

#### 2. Setup Backend
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your configuration
npm run dev
```

#### 3. Setup Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with API URL
npm start
```

#### 4. Setup ML Models
```bash
cd ml-models
pip install -r requirements.txt
python disease-detection/disease_detection_model.py
```

#### 5. Setup Voice Assistant
```bash
cd voice-assistant
pip install -r requirements.txt
# Setup Google Cloud credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

### Using Docker (Recommended)

```bash
cd docker
docker-compose up -d
```

This starts:
- MongoDB on port 27017
- Redis on port 6379
- Backend on port 5000
- Frontend on port 3000
- MQTT Broker on port 1883

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new farmer
- `POST /api/auth/login` - Farmer login
- `POST /api/auth/refresh-token` - Refresh access token
- `POST /api/auth/reset-password` - Reset password
- `POST /api/auth/logout` - Logout (requires auth)

### Crops
- `POST /api/crops` - Add new crop
- `GET /api/crops` - Get all crops
- `GET /api/crops/:id` - Get crop details
- `PUT /api/crops/:id` - Update crop
- `DELETE /api/crops/:id` - Delete crop
- `GET /api/crops/metrics` - Crop metrics

### Disease Detection
- `POST /api/diseases/detect/:cropId` - Detect disease from image
- `GET /api/diseases` - Get all disease detections
- `GET /api/diseases/stats` - Disease statistics
- `PATCH /api/diseases/:id` - Update disease status

### Weather
- `GET /api/weather/data` - Current weather
- `GET /api/weather/forecast` - Weather forecast
- `GET /api/weather/advisory` - Agricultural advisory
- `GET /api/weather/alerts` - Weather alerts

### Prices
- `GET /api/prices/prediction` - Price prediction
- `GET /api/prices/history` - Price history
- `GET /api/prices/insights` - Market insights

### IoT Devices
- `POST /api/iot/register` - Register IoT device
- `GET /api/iot/:deviceId/status` - Device status
- `GET /api/iot/:deviceId/history` - Sensor data history
- `GET /api/iot/:deviceId/readings` - Latest readings

### Subsidies
- `GET /api/subsidies` - Get all subsidies
- `GET /api/subsidies/applicable` - Get applicable subsidies
- `POST /api/subsidies/apply/:subsidyId` - Apply for subsidy
- `GET /api/subsidies/applications` - User applications

## 🔐 Security Features

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control (farmer, admin)
   - Two-factor authentication (2FA)
   - Password hashing with bcryptjs

2. **Data Protection**
   - HTTPS/TLS encryption
   - CORS protection
   - Rate limiting on API endpoints
   - Input validation and sanitization
   - SQL injection prevention
   - XSS protection via Helmet

3. **API Security**
   - Rate limiting (100 requests/15 min)
   - API versioning
   - Request/response logging
   - DDoS protection ready

4. **Database Security**
   - Encryption at rest
   - Regular backups
   - Data encryption in transit

## 📊 Data Models

### Farmer
```javascript
{
  _id: ObjectId,
  firstName, lastName, email, phone,
  password: hashed,
  farmLocation: { address, state, district, pinCode, coordinates },
  farmSize: number,
  cropTypes: [String],
  language: 'English|Hindi|Telugu|...',
  role: 'farmer|admin',
  subscriptionPlan: 'free|basic|premium|enterprise',
  totalProfit, totalExpense,
  createdAt, updatedAt
}
```

### Crop
```javascript
{
  _id: ObjectId,
  farmerId: ObjectId,
  cropName: String,
  fieldName, fieldArea,
  sowingDate, expectedHarvestDate,
  status: 'planning|sowing|growing|harvesting|completed',
  estimatedYield, actualYield,
  diseaseAlerts: [...],
  expenses: [...],
  createdAt, updatedAt
}
```

### IoTDevice
```javascript
{
  _id: ObjectId,
  farmerId: ObjectId,
  deviceId: String,
  deviceName, deviceType,
  status: 'active|inactive|error',
  latestReadings: { soilMoisture, temperature, humidity, ph, ec, ... },
  sensorDataHistory: [...],
  alerts: [...],
  batteryLevel, signalStrength
}
```

## 🧪 Testing

### Backend
```bash
cd backend
npm test
npm run test:coverage
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

## 📈 Performance Optimization

1. **Caching**
   - Redis for session management
   - API response caching
   - Image caching

2. **Database**
   - MongoDB indexing on frequently queried fields
   - Query optimization
   - Connection pooling

3. **Frontend**
   - Code splitting with React.lazy
   - Image optimization with Next.js
   - Lazy loading of components

4. **Real-time**
   - WebSocket for efficient communication
   - Binary message format for IoT data

## 🔧 Deployment

### Cloud Platforms Supported
- AWS (EC2, RDS, S3, Lambda)
- Google Cloud Platform (GCP)
- Microsoft Azure
- DigitalOcean
- Heroku (free tier)

### Deployment Steps

#### AWS Deployment
```bash
# Create EC2 instance
# Install Node.js, MongoDB, Redis
# Clone repository
git clone <repo-url>
cd AI-in-agriculture-and-food-production-2

# Run docker-compose
docker-compose up -d

# Setup SSL with Let's Encrypt
# Configure domain with Route53
```

#### Docker Registry (DockerHub)
```bash
# Build images
docker build -t yourname/smart-farming-backend ./backend
docker build -t yourname/smart-farming-frontend ./frontend

# Push to registry
docker push yourname/smart-farming-backend
docker push yourname/smart-farming-frontend
```

## 📱 Mobile App (Future)

React Native/Flutter apps planned for:
- Android
- iOS
- Offline capabilities
- Native camera access
- Push notifications

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Authors

- **Santhoshini Patel** - Project Lead
- Contributors welcome!

## 📞 Support & Contact

- Email: support@smartfarming.com
- WhatsApp: +91-XXXXXXXXXX
- Documentation: https://docs.smartfarming.com
- Website: https://www.smartfarming.com

## 🎯 Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced satellite integration
- [ ] Blockchain for supply chain
- [ ] Carbon credit tracking
- [ ] Farmer cooperative marketplace
- [ ] Real-time trading platform
- [ ] Agricultural advisory bot improvements
- [ ] Multilingual expansion (10+ languages)
- [ ] Drone integration
- [ ] Weather radar integration

## 📚 Additional Resources

- [API Documentation](docs/API.md)
- [ML Models Documentation](docs/ML_MODELS.md)
- [Architecture Document](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Security Policy](docs/SECURITY.md)

---

**Built with ❤️ for Indian Farmers | Reimagining Agriculture with AI**
