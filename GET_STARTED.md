# 🚀 GET STARTED - Run the Complete Website in 2 Minutes!

**Smart Farming Ecosystem** is a complete, production-ready web application. Follow these simple steps to get it running on your computer.

---

## ⚡ Prerequisites (30 seconds)

You need **Docker Desktop** installed. That's it!

- **Windows/Mac**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Install Docker and Docker Compose from your package manager

---

## 🎯 Quick Start (2 minutes)

### Option 1: Windows Users
```bash
# Simply double-click:
start.bat
```

### Option 2: Mac/Linux Users
```bash
# Run in terminal:
chmod +x start.sh
./start.sh
```

### Option 3: Manual (Any OS)
```bash
cd docker
docker-compose up -d
```

---

## ✨ That's It! Your Website is Running

After running the startup script, **wait 30-60 seconds** for all services to initialize, then:

1. **Open your browser** and go to:
   ```
   http://localhost:3000
   ```

2. **Create an account** with your details

3. **Start using Smart Farming!**

---

## 🎮 What You Get

The website includes these features immediately:

### 1. **🔐 User Authentication**
- Secure login/registration
- JWT token-based authentication
- Password hashing with bcryptjs
- Session management

### 2. **🌾 crop Management**
- Add and track your crops
- Monitor crop status (planning → growing → harvesting)
- Record expenses per crop
- View yield forecasts

### 3. **🍃 Disease Detection**
- Upload crop leaf images
- AI analyzes diseases (CNN model)
- Get treatment recommendations
- Product suggestions

### 4. **🌤️ Weather Advisory**
- Real-time weather data
- 10-day forecast
- Irrigation recommendations
- Agricultural guidance

### 5. **💰 Price Prediction**
- AI forecasts crop prices (7-day)
- Best selling date recommendations
- Market trend analysis
- Regional price comparison

### 6. **📡 IoT Monitoring**
- Real-time sensor data
- Soil moisture, temperature, pH
- Alert system
- Historical data charts

### 7. **🤖 AI Chatbot**
- 24/7 farming advice
- Multilingual support (English, Hindi, Telugu)
- Disease, weather, price queries
- Instant farming guidance

### 8. **🎯 Admin Dashboard**
- System statistics
- Farmer management
- Subsidy tracking
- Model version management

---

## 📊 Technical Stack (Already Installed)

| Component | Technology |
|-----------|-----------|
| **Frontend** | React 18 + Tailwind CSS |
| **Backend** | Node.js + Express.js |
| **Database** | MongoDB 6.0 |
| **Cache** | Redis 7.0 |
| **Real-time** | Socket.IO + MQTT |
| **AI/ML** | TensorFlow + scikit-learn |
| **Deployment** | Docker + Docker Compose |

---

## 🧪 Test the Website

### Create Your First Account
1. Go to http://localhost:3000
2. Click "Register"
3. Fill in your details:
   - Name: Your Name
   - Email: your@email.com
   - Password: SecurePass123!
   - Phone: 9876543210
4. Click "Create Account"

### Try Disease Detection
1. From dashboard, click "Disease Detection"
2. Add a crop first
3. Upload a leaf image (use any plant photo)
4. Click "Analyze Image"
5. See AI disease predictions

### Check Weather Advisory
1. Click "Weather Advisory"
2. See real-time weather data
3. Get irrigation recommendations
4. View 10-day forecast

### View Price Predictions
1. Click "Price Analysis"
2. Select a crop (Rice, Wheat, etc.)
3. See 7-day price forecast
4. Get sell recommendations

### Monitor IoT Sensors
1. Click "IoT Monitoring"
2. View real-time sensor data
3. Check alerts
4. See historical trends

---

## 🔧 Common Tasks

### Stop Services
```bash
# Windows
cd docker && docker-compose down

# Mac/Linux
cd docker && ./docker-compose down
```

### View Logs
```bash
cd docker && docker-compose logs -f backend
# Or
cd docker && docker-compose logs -f frontend
```

### Restart Services
```bash
cd docker && docker-compose restart
```

### Clean Everything (Reset)
```bash
cd docker && docker-compose down -v
# Then run start.sh or start.bat again
```

---

## 🐛 Troubleshooting

### "Port 3000 already in use"
```bash
# Windows: Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux: 
lsof -ti:3000 | xargs kill -9
```

### "Cannot connect to Backend"
1. Check backend is running:
   ```bash
   curl http://localhost:5000/api/health
   ```
2. If not running, check logs:
   ```bash
   docker logs smart-farming-backend
   ```

### "MongoDB connection error"
```bash
# Restart MongoDB
docker-compose restart mongodb
```

### "Forgot password or locked out"
- Open MongoDB terminal:
  ```bash
  docker exec -it mongodb mongosh smart_farming
  db.farmers.deleteOne({email: "your@email.com"})
  ```
- Then register again with same email

---

## 📱 API Testing (Advanced)

Test API endpoints using cURL:

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Farmer",
    "email": "test@farm.com",
    "password": "Test123!",
    "phone": "9876543210"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@farm.com",
    "password": "Test123!"
  }'
```

### Get Crops (Replace TOKEN with your JWT)
```bash
curl http://localhost:5000/api/crops \
  -H "Authorization: Bearer TOKEN_HERE"
```

---

## 📚 Documentation

For more detailed information:

- **Quick Reference**: [QUICK_START.md](./QUICK_START.md)
- **Full Setup Guide**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **API Reference**: [API_REFERENCE.md](./API_REFERENCE.md)
- **Development Guide**: [DEVELOPMENT_WORKFLOW.md](./DEVELOPMENT_WORKFLOW.md)
- **Complete Features**: [COMPREHENSIVE_README.md](./COMPREHENSIVE_README.md)

---

## 🎓 Learn More

### Frontend Development
- React components in: `frontend/src/pages/` and `frontend/src/components/`
- Styling: `frontend/src/pages/*.css`
- API integration: `frontend/src/services/api.js`

### Backend Development
- API routes: `backend/src/routes/`
- Services: `backend/src/services/`
- Database schemas: `backend/src/models/`
- Controllers: `backend/src/controllers/`

### ML Models
- Disease detection: `ml-models/disease-detection/`
- Price prediction: `ml-models/price-prediction/`
- Voice assistant: `voice-assistant/`
- Chatbot: `chatbot/`

---

## 🌍 Access Anywhere (Optional)

### Local Network
Share your laptop IP (e.g., 192.168.1.100) with others:
```
http://192.168.1.100:3000
```

### Public Internet (Advanced)
Use ngrok to expose locally:
```bash
ngrok http 3000
# Share the URL generated
```

---

## 📦 What's Running

All services are containerized and managed by Docker Compose:

| Service | Port | Container | Status |
|---------|------|-----------|--------|
| Frontend | 3000 | smart-farming-web | Running |
| Backend API | 5000 | smart-farming-api | Running |
| MongoDB | 27017 | mongodb | Running |
| Redis | 6379 | redis | Running |
| MQTT | 1883 | mosquitto | Running |

---

## 🚀 Next Steps

1. **Explore the Dashboard** - Add crops, track yield, monitor expenses
2. **Try Disease Detection** - Upload a leaf image for AI analysis
3. **Set Up IoT Sensors** - Connect soil sensors for real-time monitoring
4. **Check Weather Alerts** - Get irrigation recommendations
5. **Monitor Prices** - Get best selling date predictions
6. **Test Chatbot** - Ask farming questions 24/7

---

## 💡 Tips & Tricks

- **Bookmark the Admin Dashboard**: http://localhost:3000/admin
- **Enable Notifications**: Allows real-time alerts
- **Sync IoT Devices**: More sensors = better insights
- **Update ML Models**: Improve accuracy with new data
- **Export Reports**: CSV export for farm records

---

## 🤝 Support

- **Documentation**: Check the [docs](./DOCUMENTATION_INDEX.md)
- **GitHub Issues**: Report bugs or request features
- **Community Forum**: Ask questions and share tips

---

## 📝 License

Smart Farming Ecosystem - Open Source Agriculture AI

---

## 🎉 Success Checklist

- [ ] Docker Desktop installed
- [ ] Repository cloned
- [ ] `start.sh` or `start.bat` executed
- [ ] Frontend accessible at http://localhost:3000
- [ ] Account created and logged in
- [ ] Dashboard loaded with metrics
- [ ] Disease detection tested
- [ ] Weather advisory checked
- [ ] Price predictions viewed
- [ ] Bookmark the docs for reference

**Congratulations! You now have a complete Smart Farming platform running locally! 🌾🎉**

---

## ⚡ Quick Command Reference

```bash
# Start everything
./start.sh              # Mac/Linux
start.bat              # Windows

# Check services
docker-compose ps      # All services status
docker-compose logs    # View all logs
docker-compose logs backend  # Backend logs only

# Stop everything
docker-compose down    # Stop all services

# Clean reset
docker-compose down -v # Stop + delete data
./start.sh             # Restart fresh

# Backend console
docker exec -it smart-farming-api sh

# Database console
docker exec -it mongodb mongosh smart_farming

# Cache console
docker exec -it redis redis-cli
```

---

**Enjoy your Smart Farming journey! 🌾👨‍🌾👩‍🌾**

*Last Updated: 2024 | Version: 1.0.0 (Production Ready)*
