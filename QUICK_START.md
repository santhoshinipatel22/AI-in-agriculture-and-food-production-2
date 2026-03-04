# 🚀 Quick Start Guide (5 Minutes)

Welcome to Smart Farming Ecosystem! This guide will get you up and running in minutes.

## Option 1: Docker (Recommended - Easiest)

### Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/))
- Git installed

### Steps

1. **Clone and navigate to project**
   ```bash
   cd /workspaces/AI-in-agriculture-and-food-production-2
   ```

2. **Create environment files**
   ```bash
   # Backend
   cd backend
   cp .env.example .env
   
   # Update .env with API keys (OpenWeatherMap, Google Cloud, etc.)
   # At minimum, add:
   # OPENWEATHERMAP_API_KEY=your_key_here
   # GOOGLE_CLOUD_API_KEY=your_key_here
   # JWT_SECRET=your-random-secret-min-32-chars-long
   
   cd ..
   
   # Frontend
   cd frontend
   cp .env.example .env
   cd ..
   ```

3. **Start all services**
   ```bash
   cd docker
   docker-compose up -d
   ```

4. **Wait 30 seconds and access**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MongoDB: localhost:27017
   - Redis: localhost:6379

5. **Create test account**
   - Open http://localhost:3000
   - Click Register
   - Fill in details and submit
   - You're in! 👨‍🌾

### Stop Services
```bash
docker-compose down
```

---

## Option 2: Manual Setup (Advanced)

### Prerequisites
- Node.js 18+ ([Download](https://nodejs.org/))
- Python 3.8+ ([Download](https://www.python.org/))
- MongoDB ([Download](https://www.mongodb.com/try/download/community))
- Redis ([Download](https://redis.io/download))

### Backend Setup

1. **Install dependencies**
   ```bash
   cd backend
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Ensure MongoDB and Redis are running**
   ```bash
   # macOS
   brew services start mongodb-community
   brew services start redis
   
   # Linux
   sudo systemctl start mongod
   sudo systemctl start redis-server
   ```

4. **Start backend server**
   ```bash
   npm start
   # Backend runs on http://localhost:5000
   ```

### Frontend Setup (New Terminal)

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Verify REACT_APP_API_URL=http://localhost:5000
   ```

3. **Start development server**
   ```bash
   npm start
   # Frontend will open at http://localhost:3000
   ```

---

## Test the Application

### 1. Register a New Farmer Account
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Farmer",
    "email": "test@farm.com",
    "password": "TestPass123!",
    "phone": "9999999999"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@farm.com",
    "password": "TestPass123!"
  }'
```

Save the `accessToken` from response.

### 3. Create a Crop
```bash
curl -X POST http://localhost:5000/api/crops \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cropName": "Rice",
    "fieldName": "Field 1",
    "fieldArea": 10,
    "sowingDate": "2024-01-15",
    "expectedHarvestDate": "2024-05-15"
  }'
```

### 4. Get Dashboard Data
```bash
curl http://localhost:5000/api/crops \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Key Features to Test

### 1. **Disease Detection**
- Go to Dashboard → Disease Detection
- Upload a crop leaf image
- AI analyzes and suggests treatment

### 2. **Weather Advisory**
- Check real-time weather data
- Get irrigation recommendations
- View 10-day forecast

### 3. **Price Prediction**
- See current and predicted prices
- Get optimal selling date
- View market trends

### 4. **IoT Monitoring**
- View real-time sensor data
- Check soil moisture, temperature, pH
- Get alerts for critical values

### 5. **AI Chatbot**
- Click the chatbot icon (bottom right)
- Ask farming questions in English/Hindi/Telugu
- Get instant farming advice

### 6. **Admin Dashboard**
- Access at `/admin` route (if admin user)
- View platform statistics
- Manage subsidies and models

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### MongoDB Not Connecting
```bash
# Check if running
mongosh
# If not, start MongoDB services
```

### Frontend Can't Reach API
- Ensure backend is running: `curl http://localhost:5000/api/health`
- Check `REACT_APP_API_URL` in frontend .env matches backend URL
- Clear browser cache: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)

### Python Dependencies Issue
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Environment Variables Quick Reference

### Backend .env (Essential)
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/smart_farming
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-random-secret-key-min-32-characters
OPENWEATHERMAP_API_KEY=your-api-key
GOOGLE_CLOUD_API_KEY=your-api-key
CORS_ORIGINS=http://localhost:3000
```

### Frontend .env (Essential)
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
```

---

## Next Steps

After successful setup:

1. **Read the Full Documentation**
   - [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md) - Complete feature details
   - [API_REFERENCE.md](./API_REFERENCE.md) - All API endpoints
   - [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Detailed setup & troubleshooting

2. **Explore Features**
   - Create crops and track yield
   - Upload disease images for AI analysis
   - Check weather and get farming advice
   - View price predictions
   - Set up IoT sensors

3. **Customize for Your Needs**
   - Add more crops to knowledge base
   - Integrate with your IoT sensors
   - Connect to your weather station
   - Customize UI colors and branding

4. **Deploy to Production**
   - Follow deployment section in [SETUP_GUIDE.md](./SETUP_GUIDE.md)
   - Use Docker containers
   - Configure production database
   - Set up SSL certificate

---

## Support & Resources

- 📚 **Docs**: [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md)
- 🔌 **API Docs**: [API_REFERENCE.md](./API_REFERENCE.md)
- 🛠️ **Setup Help**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- 🐛 **Issues**: Check project GitHub
- 💬 **Questions**: Review documentation first

---

## Default Test Accounts (Optional - For Development)

After setup, you can seed test data:

```bash
# Access MongoDB
docker exec -it mongodb mongosh smart_farming

# Insert test farmer
db.farmers.insertOne({
  firstName: "Demo",
  lastName: "Farmer",
  email: "demo@farm.com",
  phone: "9876543210",
  subscription: "basic"
})

# Insert test subsidy
db.subsidies.insertOne({
  subsidyId: "TEST-001",
  name: "Test Subsidy",
  amount: 10000,
  currency: "INR",
  status: "active"
})

exit
```

---

## Project Stack

| Component | Technology |
|-----------|-----------|
| Backend API | Node.js + Express + MongoDB |
| Frontend UI | React 18 + Recharts + Leaflet |
| Real-time | WebSocket (Socket.IO) + MQTT |
| ML/AI | TensorFlow + scikit-learn + Python |
| Mobile | Responsive CSS + Mobile-first design |
| Deployment | Docker + Docker Compose |
| Auth | JWT + bcryptjs |

---

## What's Included

✅ Complete smart farming platform
✅ AI disease detection (CNN model)
✅ Crop price prediction (ML model)
✅ Weather-based advisory
✅ IoT sensor integration
✅ Multilingual voice assistant
✅ 24/7 AI chatbot
✅ Government subsidy finder
✅ Admin dashboard
✅ Mobile-responsive design
✅ Real-time notifications
✅ Production-ready code
✅ Docker deployment ready
✅ Comprehensive documentation
✅ API endpoints (25+)
✅ Database schemas (7)

---

**You're all set! Happy farming! 🌾👨‍🌾👩‍🌾**

For detailed information, see the full [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md)

---

**Last Updated**: 2024
**Version**: 1.0.0
