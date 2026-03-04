# ML & Database Integration Requirements

## Python Packages for ML Training

```
# Core ML Libraries
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
pickle5>=0.0.12

# Database
pymongo>=4.4.0
mongoengine>=0.28.0

# Backend Integration
python-dotenv>=1.0.0
requests>=2.31.0

# Data Processing
scipy>=1.10.0
```

## Installation Commands

### For ML Training & Database Seeding

```bash
# Install ML dependencies
pip install pandas numpy scikit-learn pymongo python-dotenv

# For Jupyter Notebook (optional)
pip install jupyter matplotlib seaborn plotly
```

### For Backend API Integration

```bash
# Node packages (add to backend/package.json)
npm install python-shell
```

## Quick Setup Steps

### 1. Generate Datasets (92,000+ records)
```bash
cd ml-models
python3 generate_datasets.py
```

Output files:
- `crop_production_data.csv` (50,000 rows)
- `disease_detection_data.csv` (15,000 rows)
- `price_prediction_data.csv` (10,000 rows)
- `yield_forecasting_data.csv` (12,000 rows)
- `weather_data.csv` (5,000 rows)

### 2. Train ML Models
```bash
cd ml-models
python3 train_models.py
```

Output models:
- `trained_models/crop_recommendation_model.pkl`
- `trained_models/disease_detection_model.pkl`
- `trained_models/price_prediction_model.pkl`
- `trained_models/yield_forecasting_model.pkl`

### 3. Seed MongoDB Database
```bash
cd backend
python3 scripts/seed_database.py
```

Creates 5 collections with 92,000 total documents

### 4. Start ML API Server
```bash
cd backend
npm install
npm run dev
```

API available at `http://localhost:5000/api/ml/*`

---

## Environment Variables

Create `.env` file in backend root:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/smart_farming

# Python Integration
PYTHON_PATH=/usr/bin/python3

# API
PORT=5000
NODE_ENV=development

# ML Models Path
ML_MODELS_PATH=../ml-models/trained_models
```

---

## Database Schemas

### Index Creation

The seed script automatically creates indexes on:
- `crop_production`: crop_name, region, year
- `disease_detection`: crop_name, disease_name, severity
- `price_prediction`: crop_name, date, region
- `yield_forecasting`: crop_name, region, season
- `weather_timeseries`: region, date

---

## Testing the Setup

### 1. Check Dataset Files
```bash
ls -lh ml-models/*.csv
```

Expected output:
```
crop_production_data.csv          (~50MB, 50,000 rows)
disease_detection_data.csv        (~15MB, 15,000 rows)
price_prediction_data.csv         (~10MB, 10,000 rows)
yield_forecasting_data.csv        (~12MB, 12,000 rows)
weather_data.csv                  (~5MB, 5,000 rows)
```

### 2. Check Trained Models
```bash
ls -lh ml-models/trained_models/
```

Expected output:
```
crop_recommendation_model.pkl     (~50MB)
disease_detection_model.pkl       (~25MB)
price_prediction_model.pkl        (~30MB)
yield_forecasting_model.pkl       (~35MB)
```

### 3. Check Database
```bash
mongosh  # or mongo

use smart_farming
db.crop_production.countDocuments()
db.disease_detection.countDocuments()
db.price_prediction.countDocuments()
db.yield_forecasting.countDocuments()
db.weather_timeseries.countDocuments()
```

Expected total: 92,000+ documents

### 4. Test ML API
```bash
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
```

---

## Streamlit Integration

Update Streamlit app to use ML API:

```python
import requests

API_BASE = os.getenv("API_BASE_URL", "http://localhost:5000")

# Call crop recommendation API
response = requests.post(f"{API_BASE}/api/ml/crop-recommendation", 
    json={
        "temperature": temp_input,
        "rainfall": rainfall_input,
        # ... other parameters
    }
)

if response.status_code == 200:
    recommendations = response.json()['data']['recommendations']
    st.success(f"Recommended crops: {', '.join(recommendations)}")
else:
    st.error("ML service not available")
```

---

## File Structure

```
AI-in-agriculture-and-food-production-2/
├── ml-models/
│   ├── generate_datasets.py       # Generate 92k+ records
│   ├── train_models.py             # Train 4 ML models
│   ├── predict_crops.py            # Crop recommendation inference
│   ├── predict_disease.py          # Disease detection inference
│   ├── predict_price.py            # Price prediction inference
│   ├── predict_yield.py            # Yield forecasting inference
│   ├── trained_models/             # Pickled models
│   ├── *.csv                       # Generated datasets
│   └── crop-recommendation/        # Model documentation
│
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   └── ml.js               # ML API endpoints
│   │   ├── models/                 # Mongoose schemas
│   │   └── scripts/
│   │       └── seed_database.py    # MongoDB seeding
│   ├── package.json                # Node dependencies
│   └── .env                        # Configuration
│
├── streamlit_app.py                # Updated with ML API calls
├── setup_ml.sh                     # Automated setup script
├── ML_TRAINING_GUIDE.md            # Complete documentation
└── requirements_streamlit.txt      # Streamlit dependencies

```

---

## Performance Notes

### Dataset Generation Time
- **Total**: ~30-60 seconds
- 50k crop records: ~10 seconds
- 15k disease records: ~5 seconds
- 10k price records: ~3 seconds
- 12k yield records: ~8 seconds
- 5k weather records: ~2 seconds

### Model Training Time
- **Total**: ~5-10 minutes
- Crop Recommendation: ~2 minutes
- Disease Detection: ~2 minutes
- Price Prediction: ~1.5 minutes
- Yield Forecasting: ~2.5 minutes

### Database Seeding Time
- **Total**: ~2-5 minutes (depends on MongoDB performance)
- Batch size: 1,000 records
- Total inserts: 92 batches

---

## Common Issues & Solutions

### Issue: "No module named 'sklearn'"
```bash
pip install scikit-learn
```

### Issue: "MongoDB connection refused"
```bash
# Start MongoDB
mongod

# Or with Docker
docker run -d -p 27017:27017 mongo:latest
```

### Issue: Python not found in Node
```javascript
// In Node.js, update options:
const options = {
    pythonPath: '/usr/bin/python3',  // Specify full path
    scriptPath: './ml-models',
};
```

### Issue: CSV files not found
```bash
# Ensure you're in the ml-models directory
cd ml-models
python3 generate_datasets.py
```

---

## Next Steps

1. ✅ Generate datasets
2. ✅ Train models
3. ✅ Seed database
4. Update Streamlit pages to use ML API
5. Add real-time model monitoring
6. Implement model versioning
7. Setup automated retraining

---

## Support & References

- **Scikit-learn docs**: https://scikit-learn.org
- **MongoDB docs**: https://docs.mongodb.com
- **Python-shell**: https://github.com/extrabacon/python-shell
