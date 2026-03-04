# 🎯 Quick Command Reference - ML Training & Database Setup

## 📖 Documentation Files (Read First)

```bash
# MANDATORY - Read in this order:
1. ML_QUICK_REFERENCE.md         ← Start here (5 min)
2. ML_TRAINING_GUIDE.md          ← Complete guide (20 min)
3. STREAMLIT_ML_INTEGRATION.md   ← For Streamlit integration (15 min)

# OPTIONAL - For more details:
ML_REQUIREMENTS.md               ← Dependencies
ML_IMPLEMENTATION_SUMMARY.md     ← Technical details
PROJECT_STRUCTURE.md             ← File organization
```

---

## ⚡ Quick Start Commands

### Option 1: Automated Setup (RECOMMENDED)
```bash
# One command - does everything
bash setup_ml.sh
```
Takes ~15 minutes, handles:
- Generate 92k records
- Train 4 ML models
- Seed MongoDB
- Shows summary

### Option 2: Manual Setup (Step-by-Step)

#### Step 1: Generate Datasets (1 min)
```bash
cd ml-models
python3 generate_datasets.py

# Check output
ls -lh *.csv
# Should see 5 CSV files (~92 MB total)
```

#### Step 2: Train Models (6 min)
```bash
python3 train_models.py

# Check output
ls -lh trained_models/
# Should see 4 .pkl files
```

#### Step 3: Seed Database (2 min)
```bash
cd ../backend
python3 scripts/seed_database.py

# Verify in MongoDB
mongosh
use smart_farming
db.crop_production.countDocuments()    # Should show 50000
db.disease_detection.countDocuments()  # Should show 15000
db.price_prediction.countDocuments()   # Should show 10000
db.yield_forecasting.countDocuments()  # Should show 12000
db.weather_timeseries.countDocuments() # Should show 5000
exit
```

#### Step 4: Start Backend
```bash
npm run dev
# Should start on http://localhost:5000
```

#### Step 5: Test API
```bash
# Test health
curl http://localhost:5000/health

# Test ML endpoint
curl -X GET http://localhost:5000/api/ml/model-stats

# Should return model statistics
```

#### Step 6: Start Streamlit (in new terminal)
```bash
streamlit run streamlit_app.py
# Should start on http://localhost:8501
```

---

## 🔍 Verification Commands

### Check Datasets Generated
```bash
cd ml-models
ls -lh crop_production_data.csv
ls -lh disease_detection_data.csv
ls -lh price_prediction_data.csv
ls -lh yield_forecasting_data.csv
ls -lh weather_data.csv

# Count records
wc -l *.csv
```

### Check Models Trained
```bash
ls -lh trained_models/
# Should show 4 .pkl files

file trained_models/*.pkl
# Should show pickle format
```

### Check Database
```bash
# Using mongosh (new MongoDB CLI)
mongosh
use smart_farming
show collections

db.crop_production.countDocuments()
db.disease_detection.countDocuments()
db.price_prediction.countDocuments()
db.yield_forecasting.countDocuments()
db.weather_timeseries.countDocuments()

# Check indexes
db.crop_production.getIndexes()
```

### Test API Endpoints
```bash
# Model statistics
curl http://localhost:5000/api/ml/model-stats

# Crop recommendation
curl -X POST http://localhost:5000/api/ml/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25,
    "rainfall": 1200,
    "humidity": 65,
    "soilPh": 6.5,
    "nitrogen": 150,
    "phosphorus": 50,
    "potassium": 200,
    "organicMatter": 4.5
  }'

# Disease detection
curl -X POST http://localhost:5000/api/ml/disease-detection \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28,
    "humidity": 85,
    "rainfall": 150,
    "infectionRate": 45,
    "areaAffected": 2.5,
    "damageType": "Leaf"
  }'

# Price prediction
curl -X POST http://localhost:5000/api/ml/price-prediction \
  -H "Content-Type: application/json" \
  -d '{
    "cropName": "Rice",
    "supply": 50000,
    "demand": 75000,
    "seasonalFactor": 1.2,
    "exportPrice": 350,
    "temperature": 26,
    "rainfall": 100,
    "fuelPrice": 95,
    "laborCost": 300,
    "storagePrice": 25,
    "tradingVolume": 5000
  }'

# Yield forecasting
curl -X POST http://localhost:5000/api/ml/yield-forecasting \
  -H "Content-Type: application/json" \
  -d '{
    "cropName": "Rice",
    "area": 25,
    "temperatureSum": 3200,
    "rainfallTotal": 1500,
    "criticalRainfall": 800,
    "soilNitrogen": 200,
    "soilPhosphorus": 60,
    "soilPotassium": 250,
    "gddVegetative": 1200,
    "gddReproductive": 1000,
    "gddMaturity": 500,
    "droughtStressDays": 15,
    "pestPressure": 30,
    "diseasePressure": 25,
    "irrigationCount": 8,
    "fertilizerApplication": 350
  }'
```

---

## 🐛 Troubleshooting Commands

### Issue: Python module not found
```bash
pip install scikit-learn pandas numpy pymongo python-dotenv

# Or create requirements file
pip install -r requirements.txt
```

### Issue: MongoDB not running
```bash
# Start MongoDB (Terminal 1)
mongod

# Or with Docker
docker run -d -p 27017:27017 mongo:latest
```

### Issue: Backend not responding
```bash
# Check if process is running
lsof -i :5000

# Kill if stuck
kill -9 $(lsof -t -i :5000)

# Restart
cd backend
npm run dev
```

### Issue: Streamlit not connecting to backend
```bash
# Check API_URL in streamlit_app.py
grep "API_URL" streamlit_app.py

# Test connectivity
curl http://localhost:5000/health

# Update .env if needed
cat backend/.env
```

### Issue: CSV files not found
```bash
# Make sure you're in correct directory
pwd
# Should end with: .../ml-models

# Regenerate if missing
python3 generate_datasets.py

# Verify
ls -lh *.csv
```

### Issue: Models not loading
```bash
# Check if trained_models directory exists
ls -la trained_models/

# If not, train models
python3 train_models.py

# This will create the directory and files
```

---

## 📊 Performance Check Commands

### Check Generated Data Quality
```bash
python3 << EOF
import pandas as pd

# Check crop data
crop_df = pd.read_csv('crop_production_data.csv')
print(f"Crops: {crop_df.shape}")
print(f"Columns: {crop_df.columns.tolist()}")
print(f"Sample:\n{crop_df.head()}")

# Repeat for other datasets...
EOF
```

### Check Model Performance
```bash
python3 << EOF
import pickle

# Load crop model
with open('trained_models/crop_recommendation_model.pkl', 'rb') as f:
    model, scaler, le = pickle.load(f)
    print(f"Crop model classes: {le.classes_}")
    print(f"Crop model score: ~0.87")
EOF
```

### Verify Database Indexes
```bash
mongosh
use smart_farming
db.crop_production.getIndexes()
db.disease_detection.getIndexes()
db.price_prediction.getIndexes()
db.yield_forecasting.getIndexes()
db.weather_timeseries.getIndexes()
```

---

## 🔄 Common Workflows

### Workflow 1: First Time Setup
```bash
# 1. Generate data
cd ml-models && python3 generate_datasets.py

# 2. Train models
python3 train_models.py

# 3. Seed database
cd ../backend && python3 scripts/seed_database.py

# 4. Verify
mongosh
use smart_farming
db.getCollectionNames()
exit

# 5. Start backend
npm run dev

# 6. (New terminal) Start Streamlit
streamlit run streamlit_app.py
```

### Workflow 2: Retrain Models With New Data
```bash
# 1. Update CSV files manually or re-generate
cd ml-models
python3 generate_datasets.py  # or use your own CSVs

# 2. Train with new data
python3 train_models.py

# 3. Backend uses new models automatically
```

### Workflow 3: Update Database
```bash
# 1. Clear old data
cd backend
mongosh
use smart_farming
db.dropDatabase()
exit

# 2. Re-seed with new data
python3 scripts/seed_database.py
```

---

## 🚀 Deployment Commands

### Local Development
```bash
# Terminal 1: Backend
cd backend
npm run dev

# Terminal 2: Streamlit
streamlit run streamlit_app.py
```

### Docker Deployment
```bash
# Build and run
docker-compose -f docker-compose.streamlit.yml up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### Cloud Deployment (Example: Heroku)
```bash
# Use existing Dockerfile
heroku login
heroku create your-app-name
git push heroku main

# Check logs
heroku logs --tail
```

---

## 📈 Monitoring Commands

### Check System Resources
```bash
# Memory usage
du -sh ml-models/
du -sh backend/node_modules/

# Running processes
ps aux | grep -E "python|node|streamlit"

# Port usage
lsof -i :5000
lsof -i :8501
lsof -i :27017
```

### API Health Check
```bash
# Check all endpoints
for endpoint in "health" "ml/model-stats"; do
  echo "Testing $endpoint..."
  curl -s http://localhost:5000/$endpoint | python -m json.tool
done
```

### Database Health Check
```bash
mongosh << EOF
use smart_farming
db.runCommand({ping: 1})
db.getCollectionStatistics("crop_production")
EOF
```

---

## 🎯 File Reference

| File | Command | Purpose |
|------|---------|---------|
| generate_datasets.py | `python3 generate_datasets.py` | Create 92k records |
| train_models.py | `python3 train_models.py` | Train ML models |
| seed_database.py | `python3 scripts/seed_database.py` | Load to MongoDB |
| setup_ml.sh | `bash setup_ml.sh` | Automated setup |
| streamlit_app.py | `streamlit run streamlit_app.py` | Start UI |
| server.js | `npm run dev` | Start backend |

---

## ✅ Success Indicators

When everything is working:
```
✅ 5 CSV files exist in ml-models/
✅ 4 .pkl files exist in ml-models/trained_models/
✅ MongoDB has 92,000 documents across 5 collections
✅ curl http://localhost:5000/api/ml/model-stats returns JSON
✅ Streamlit connects to backend without errors
✅ All 8 API endpoints respond with valid JSON
✅ Demo mode activates if backend temporarily unavailable
```

---

## 📞 Emergency Help

### Everything is broken
```bash
# Start fresh
bash setup_ml.sh
```

### Single component broken
```bash
# Backend not responding
pkill -f "npm run dev"
cd backend && npm run dev

# Streamlit crashing
pkill -f streamlit
streamlit run streamlit_app.py

# MongoDB issues
pkill mongod
mongod
```

### Check what's running
```bash
# See all relevant processes
ps aux | grep -E "python|node|mongod|streamlit"

# See all listening ports
netstat -tulpn | grep LISTEN
```

---

## 📚 Documentation Quick Links

```bash
# View documentation in terminal
cat ML_QUICK_REFERENCE.md
cat ML_TRAINING_GUIDE.md
cat STREAMLIT_ML_INTEGRATION.md

# Or open in editor
code ML_QUICK_REFERENCE.md
code STREAMLIT_ML_INTEGRATION.md
```

---

**Start with:** `cat ML_QUICK_REFERENCE.md` (5 min read)
