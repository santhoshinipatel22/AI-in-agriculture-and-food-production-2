# 🚀 Streamlit Quick Start - Smart Farming AI

**Deploy your Smart Farming AI in seconds!** No complex setup required. 🌾

---

## ⚡ Absolute Fastest Way (30 seconds)

### All-in-One Docker Deployment

**Mac/Linux:**
```bash
cd /workspaces/AI-in-agriculture-and-food-production-2
docker-compose -f docker-compose.streamlit.yml up
```

**Then open:** http://localhost:8501

**That's it!** 🎉

---

## 🎯 What You Get

| Feature | Status | Access |
|---------|--------|--------|
| 🌐 **Streamlit Frontend** | ✅ Ready | http://localhost:8501 |
| 🔌 **Backend API** | ✅ Ready | http://localhost:5000 |
| 📊 **MongoDB Database** | ✅ Ready | localhost:27017 |
| 💾 **Redis Cache** | ✅ Ready | localhost:6379 |
| 🔌 **MQTT IoT Broker** | ✅ Ready | localhost:1883 |

---

## 📱 Key Features Available

✅ User Registration & Login  
✅ Dashboard with Crop Management  
✅ AI Disease Detection (Image Upload)  
✅ Weather Advisory (Real-time)  
✅ Price Prediction (7-day forecast)  
✅ IoT Sensor Monitoring  
✅ 24/7 AI Chatbot  
✅ Account Settings & Profile  

---

## 🔑 Test User (Pre-seeded)

After startup, you can login with:
- **Email**: farmer@example.com
- **Password**: password123

Or create a new account instantly!

---

## 📝 Step-by-Step Setup

### Option 1: Docker (Recommended - Fastest)

```bash
# 1. In project root directory
docker-compose -f docker-compose.streamlit.yml up

# Wait 30 seconds for all services to start

# 2. Open browser
# http://localhost:8501

# Done! 🎉
```

### Option 2: Local Installation

**Terminal 1 - Backend Server:**
```bash
cd backend
npm install
npm start
# Runs on http://localhost:5000
```

**Terminal 2 - Streamlit Frontend:**
```bash
# From project root
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
# Runs on http://localhost:8501
```

### Option 3: Using Helper Scripts

**Mac/Linux:**
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

**Windows:**
```bash
run_streamlit.bat
```

---

## 🎮 Testing the App

### 1. Register New Account
```
1. Go to http://localhost:8501
2. Click "Register" tab
3. Fill in: Name, Email, Password, Phone
4. Click "Register"
5. Login with new credentials
```

### 2. Add a Crop
```
1. Go to "Dashboard"
2. Click "Add Crop" tab
3. Fill in crop details
4. Click "Add Crop"
5. View in "My Crops" tab
```

### 3. Test Disease Detection
```
1. Go to "Disease Detection"
2. Upload a crop image
3. Select crop from dropdown
4. Click "Detect Disease"
5. View AI results
```

### 4. Check Weather
```
1. Go to "Weather"
2. Enter latitude/longitude
3. Click "Get Weather Data"
4. View forecast & advisory
```

### 5. Price Analysis
```
1. Go to "Price Analysis"
2. Select crop and region
3. Click "Get Price Analysis"
4. View predictions & trends
```

---

## 📊 API Endpoints (All Connected)

Your Streamlit app uses all 25+ backend endpoints:

### Authentication
- POST `/auth/register` - Create account
- POST `/auth/login` - Login user

### Crops
- POST `/crops` - Add crop
- GET `/crops` - List crops
- GET `/crops/:id` - Get crop details
- PUT `/crops/:id` - Update crop
- DELETE `/crops/:id` - Delete crop
- GET `/crops/metrics` - Get dashboard metrics

### Diseases
- POST `/diseases/detect/:cropId` - AI detection
- GET `/diseases` - Get detection history

### Weather
- GET `/weather/data` - Current weather
- GET `/weather/forecast` - 10-day forecast
- GET `/weather/advisory` - Farming advice

### Prices
- GET `/prices/prediction` - Price forecast
- GET `/prices/history` - Historical data
- GET `/prices/insights` - Market insights

### IoT
- GET `/iot/devices` - List devices
- GET `/iot/:deviceId/status` - Device status
- GET `/iot/:deviceId/history` - Historical readings

### Chatbot
- POST `/chatbot/query` - Chat with AI

*Full API documentation: See `/backend/API_REFERENCE.md`*

---

## 🌩️ Monitor Services

### Check what's running
```bash
# Docker containers
docker-compose -f docker-compose.streamlit.yml ps

# View logs
docker-compose -f docker-compose.streamlit.yml logs -f streamlit
docker-compose -f docker-compose.streamlit.yml logs -f backend
docker-compose -f docker-compose.streamlit.yml logs -f mongodb
```

### Stop everything
```bash
docker-compose -f docker-compose.streamlit.yml down
```

### Clear all data (fresh restart)
```bash
docker-compose -f docker-compose.streamlit.yml down -v
docker-compose -f docker-compose.streamlit.yml up
```

---

## 🔧 Configuration

### Change Backend URL

If running backend elsewhere, edit `streamlit_app.py` line 21:

```python
API_URL = "http://your-backend-url:5000/api"
```

Then reload Streamlit:
```bash
# Ctrl+C to stop
streamlit run streamlit_app.py
```

### Database Connection

MongoDB runs on **localhost:27017** with:
- Username: `admin`
- Password: `password123`  
- Database: `smartfarming`

To change, update:
1. `docker-compose.streamlit.yml` (MONGO_INITDB_* variables)
2. `backend/.env` (MONGODB_URI)

---

## 📱 Streamlit Features

| Feature | Capability |
|---------|-----------|
| **Charts** | Plotly interactive graphs |
| **File Upload** | Image upload for disease detection |
| **Forms** | User input with validation |
| **Session State** | Remember login & user data |
| **Caching** | Fast API responses |
| **Multi-page** | Dashboard, Disease, Weather, Price, IoT, Chat |
| **Responsive** | Works on mobile, tablet, desktop |
| **Real-time** | Live updates from backend |

---

## 🚀 Next: Deploy to Cloud

### Streamlit Cloud (Easiest)
```bash
# 1. Push to GitHub
git add .
git commit -m "Add Streamlit frontend"
git push

# 2. Go to https://streamlit.io/cloud
# 3. Click "New app"
# 4. Select streamlit_app.py
# 5. Click Deploy!
```

### Docker Hub
```bash
docker build -f Dockerfile.streamlit -t your-username/smart-farming .
docker push your-username/smart-farming
```

Then deploy with:
```bash
docker run -p 8501:8501 \
  -e API_URL=https://your-backend.com/api \
  your-username/smart-farming
```

---

## ❓ Troubleshooting

### "Connection refused" on startup?
```bash
# Check if backend is running
curl http://localhost:5000/health

# If not, start backend in another terminal:
cd backend && npm start
```

### "Streamlit page not loading"?
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache
streamlit run streamlit_app.py --logger.level=debug
```

### "API requests timing out"?
```bash
# Check Docker logs
docker-compose -f docker-compose.streamlit.yml logs backend

# Increase timeout in streamlit_app.py if needed
```

### Port 8501 already in use?
```bash
# Run on different port
streamlit run streamlit_app.py --server.port=8502
```

### Database connection failed?
```bash
# Check MongoDB is running
docker-compose -f docker-compose.streamlit.yml ps mongodb

# Check logs
docker-compose -f docker-compose.streamlit.yml logs mongodb
```

---

## 🎯 Production Deployment

When ready to deploy to production:

1. **Update API URL** in `streamlit_app.py`
2. **Set strong passwords** in `.env` files
3. **Enable HTTPS** on production backend
4. **Configure secrets** in deployment platform
5. **Set up monitoring** (logs, errors, performance)
6. **Create database backups** schedule
7. **Set rate limiting** on API
8. **Test end-to-end** before going live

---

## 💡 Performance Tips

- Use `@st.cache_data` to cache API responses
- Display loading spinners while fetching data
- Paginate long lists (e.g., crop history)
- Use Streamlit session state for expensive operations
- Lazy-load images and heavy components
- Database indexes on frequently queried fields
- Redis for session and data caching

---

## 📞 Support

For issues:

1. **Check logs**: `docker-compose logs -f`
2. **Review API docs**: See `API_REFERENCE.md`
3. **Test API directly**: Use cURL or Postman
4. **Check database**: `mongosh localhost:27017`
5. **Verify configuration**: Check `.env` files

---

## 🎉 Success Checklist

- [ ] All services running (check http://localhost:8501)
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Dashboard shows metrics
- [ ] Can add crops
- [ ] Can upload crop image for disease detection
- [ ] Weather data loads
- [ ] Price predictions display
- [ ] IoT status shows
- [ ] Chatbot responds

---

## 🌾 You're All Set!

Your Smart Farming AI system is **LIVE and READY**! 🚀

- **Frontend**: http://localhost:8501 📱
- **Backend API**: http://localhost:5000 🔌
- **Database**: MongoDB 🗄️
- **Cache**: Redis ⚡
- **IoT Broker**: MQTT 📡

**Start building** or **deploy to cloud** right away!

---

*Smart Farming AI - Making agriculture intelligent with AI 🌾*

Questions? Check the full docs: `STREAMLIT_DEPLOYMENT.md`
