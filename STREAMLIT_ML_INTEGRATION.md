# 🌾 Integrating ML Models with Streamlit App

This guide shows how to integrate the trained ML models and database into the Streamlit application.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                          │
│  (streamlit_app.py)                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (Express.js)                      │
│  • Route: /api/ml/*                                             │
│  • Handles authentication, validation, logging                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐    ┌─────────────┐   ┌──────────┐
   │ MongoDB │    │ ML Models   │   │ Analytics│
   │(92k docs│    │(4 models)   │   │(Trends)  │
   └─────────┘    └─────────────┘   └──────────┘
```

---

## 1. Dashboard Page - Crop Recommendations

### Current Implementation
```python
# streamlit_app.py - dashboard_page()
def dashboard_page():
    st.header("🌾 Dashboard")
    # Shows demo crops
    crops = [
        {"name": "Rice", "yield": 45, "health": "Good"},
        {"name": "Wheat", "yield": 38, "health": "Fair"},
        {"name": "Corn", "yield": 52, "health": "Good"}
    ]
```

### Updated with ML
```python
import requests

def dashboard_page():
    st.header("🌾 Dashboard")
    
    # Get ML recommendations
    try:
        response = requests.post(
            f"{API_URL}/ml/crop-recommendation",
            json={
                "temperature": 25,
                "rainfall": 1200,
                "humidity": 65,
                "soilPh": 6.5,
                "nitrogen": 150,
                "phosphorus": 50,
                "potassium": 200,
                "organicMatter": 4.5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()['data']
            st.success("🤖 ML Recommendations")
            for crop, conf in zip(data['recommendations'], data['confidence']):
                st.write(f"• {crop}: {conf:.1%} confidence")
        else:
            st.warning("ML service unavailable - showing demo data")
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
```

---

## 2. Disease Detection Page

### Current Implementation
```python
def disease_detection_page():
    st.header("🦠 Disease Detection")
    # Demo mode with sample results
```

### Updated with ML
```python
def disease_detection_page():
    st.header("🦠 Disease Detection")
    
    st.subheader("Environmental Conditions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temperature = st.slider("Temperature (°C)", -10, 50, 25)
    with col2:
        humidity = st.slider("Humidity (%)", 0, 100, 75)
    with col3:
        rainfall = st.slider("Rainfall (mm)", 0, 300, 100)
    
    if st.button("Analyze for Diseases"):
        try:
            response = requests.post(
                f"{API_URL}/ml/disease-detection",
                json={
                    "temperature": temperature,
                    "humidity": humidity,
                    "rainfall": rainfall,
                    "infectionRate": 45,
                    "areaAffected": 2.5,
                    "damageType": "Leaf"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()['data']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Disease", result['disease'])
                with col2:
                    st.metric("Severity", result['severity'])
                with col3:
                    st.metric("Confidence", f"{result['confidence']:.1%}")
                
                st.info(f"Treatment: {result['treatment']}")
                st.warning(f"Recovery Time: {result['estimatedRecoveryDays']} days")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

---

## 3. Price Analysis Page

### Current Implementation
```python
def price_page():
    st.header("💰 Price Analysis")
    # Shows demo price trends
```

### Updated with ML
```python
def price_page():
    st.header("💰 Price Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crop = st.selectbox("Select Crop", [
            "Rice", "Wheat", "Corn", "Cotton", "Sugarcane"
        ])
    with col2:
        supply = st.number_input("Supply (tonnes)", 1000, 100000, 50000)
    with col3:
        demand = st.number_input("Demand (tonnes)", 1000, 100000, 75000)
    
    if st.button("Predict Price"):
        try:
            response = requests.post(
                f"{API_URL}/ml/price-prediction",
                json={
                    "cropName": crop,
                    "supply": supply,
                    "demand": demand,
                    "seasonalFactor": 1.2,
                    "exportPrice": 350,
                    "temperature": 26,
                    "rainfall": 100,
                    "fuelPrice": 95,
                    "laborCost": 300,
                    "storagePrice": 25,
                    "tradingVolume": 5000
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()['data']
                
                # Display price metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Predicted Price", f"₹{result['predictedPrice']:.0f}")
                with col2:
                    st.metric("Min Price", f"₹{result['priceRange']['min']:.0f}")
                with col3:
                    st.metric("Max Price", f"₹{result['priceRange']['max']:.0f}")
                with col4:
                    st.metric("Trend", result['trend'])
                
                # Confidence and recommendation
                st.progress(result['confidence'])
                st.success(f"💡 {result['recommendation']}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

---

## 4. Yield Forecasting Page

### Current Implementation
```python
def iot_page():
    st.header("📊 IoT Monitoring")
    # Shows demo sensor data
```

### Updated with ML
```python
def yield_forecasting_page():
    st.header("📈 Yield Forecasting")
    
    st.subheader("Crop Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crop = st.selectbox("Crop", ["Rice", "Wheat", "Corn"])
    with col2:
        area = st.number_input("Area (hectares)", 0.5, 1000.0, 25.0)
    with col3:
        season = st.selectbox("Season", ["Kharif", "Rabi", "Summer"])
    
    st.subheader("Environmental Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        temp_sum = st.number_input("Temperature Sum (°C days)", 2000, 5000, 3200)
    with col2:
        rainfall = st.number_input("Total Rainfall (mm)", 200, 3000, 1500)
    with col3:
        irrigation = st.slider("Irrigation Count", 0, 15, 8)
    
    if st.button("Forecast Yield"):
        try:
            response = requests.post(
                f"{API_URL}/ml/yield-forecasting",
                json={
                    "cropName": crop,
                    "area": area,
                    "temperatureSum": temp_sum,
                    "rainfallTotal": rainfall,
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
                    "irrigationCount": irrigation,
                    "fertilizerApplication": 350
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()['data']
                
                # Display yield forecast
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicted Yield", 
                             f"{result['predictedYield']:.1f} T/ha")
                with col2:
                    st.metric("Min Yield", 
                             f"{result['yieldRange']['min']:.1f} T/ha")
                with col3:
                    st.metric("Max Yield", 
                             f"{result['yieldRange']['max']:.1f} T/ha")
                
                # Factors affecting yield
                st.subheader("Factors Affecting Yield")
                if result['factors']:
                    for factor in result['factors']:
                        st.warning(f"⚠️ {factor}")
                else:
                    st.success("✅ Optimal conditions")
                
                # Recommendations
                st.subheader("Optimization Tips")
                for rec in result['recommendations']:
                    st.info(f"💡 {rec}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

---

## 5. Add Analytics Dashboard Page

### New Page - Analytics
```python
def analytics_page():
    st.header("📊 Analytics Dashboard")
    
    st.subheader("Crop Production Analytics")
    
    if st.button("Load Crop Analytics"):
        try:
            response = requests.get(
                f"{API_URL}/ml/analytics/crop-production",
                timeout=10
            )
            
            if response.status_code == 200:
                analytics = response.json()['data']
                
                # Create DataFrame for display
                df = pd.DataFrame(analytics)
                df = df.sort_values('totalProduction', ascending=False)
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Crops", len(df))
                with col2:
                    st.metric("Avg Yield", f"{df['avgYield'].mean():.1f} T/ha")
                with col3:
                    st.metric("Total Production", f"{df['totalProduction'].sum():.0f} T")
                
                # Display table
                st.dataframe(df[['_id', 'avgYield', 'totalProduction', 'count']])
                
                # Visualization
                fig = px.bar(df, x='_id', y='avgYield', title="Average Yield by Crop")
                st.plotly_chart(fig)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.subheader("Disease Trends")
    
    if st.button("Load Disease Trends"):
        try:
            response = requests.get(
                f"{API_URL}/ml/analytics/disease-trends",
                timeout=10
            )
            
            if response.status_code == 200:
                trends = response.json()['data']
                
                df = pd.DataFrame(trends)
                st.dataframe(df[['_id', 'occurrences', 'avgSeverity', 'avgYieldLoss']])
                
                fig = px.bar(df, x='_id', y='occurrences', title="Disease Frequency")
                st.plotly_chart(fig)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

---

## 6. Update Main Navigation

### Current
```python
def main():
    pages = {
        "Dashboard": dashboard_page,
        "Disease Detection": disease_detection_page,
        "Weather": weather_page,
        "Price Analysis": price_page,
        "IoT Monitoring": iot_page,
        "Chatbot": chatbot_page,
        "Settings": settings_page,
    }
```

### Updated
```python
def main():
    pages = {
        "Dashboard": dashboard_page,
        "Disease Detection": disease_detection_page,
        "Weather": weather_page,
        "Price Analysis": price_page,
        "Yield Forecasting": yield_forecasting_page,
        "Analytics": analytics_page,  # NEW
        "Chatbot": chatbot_page,
        "Settings": settings_page,
    }
```

---

## 7. Error Handling & Fallbacks

```python
# Global function to handle ML API calls
def call_ml_api(endpoint, payload, timeout=10):
    """
    Safe ML API caller with error handling and fallback to demo mode
    """
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}",
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            st.warning("ML service error - using demo data")
            return get_demo_data(endpoint)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to ML service")
        return get_demo_data(endpoint)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return get_demo_data(endpoint)

def get_demo_data(endpoint):
    """Return demo data if API is unavailable"""
    demo_data = {
        'ml/crop-recommendation': {
            'recommendations': ['Demo: Rice', 'Demo: Wheat', 'Demo: Corn'],
            'confidence': [0.85, 0.78, 0.70]
        },
        'ml/disease-detection': {
            'disease': 'Demo: Fungal infection',
            'severity': 'Medium',
            'treatment': 'Demo: Apply fungicide spray',
            'estimatedRecoveryDays': 14
        },
        # Add other demo data...
    }
    return demo_data.get(endpoint, {})
```

---

## 8. Testing the Integration

### Step 1: Start MongoDB
```bash
mongod
```

### Step 2: Start Backend
```bash
cd backend
npm run dev
```

### Step 3: Generate & Train Models
```bash
cd ml-models
python3 generate_datasets.py
python3 train_models.py
```

### Step 4: Seed Database
```bash
cd backend
python3 scripts/seed_database.py
```

### Step 5: Start Streamlit
```bash
streamlit run streamlit_app.py
```

### Step 6: Test ML Endpoints
Access Streamlit and click buttons to test each ML endpoint

---

## Configuration

### Environment Variables
```env
# .env
API_BASE_URL=http://localhost:5000
ML_API_TIMEOUT=10
# Enable ML features
USE_ML_MODELS=true
```

### Streamlit Config
```python
# At top of streamlit_app.py
import os
API_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
ML_ENABLED = os.getenv('USE_ML_MODELS', 'true') == 'true'
```

---

## Performance Tips

1. **Cache API calls** to reduce load:
```python
@st.cache_data(ttl=3600)
def get_crop_analytics():
    response = requests.get(f"{API_URL}/ml/analytics/crop-production")
    return response.json()
```

2. **Use session state** to avoid re-computing:
```python
if 'prediction_cache' not in st.session_state:
    st.session_state.prediction_cache = {}
```

3. **Parallel requests** for multiple predictions:
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    crop_future = executor.submit(get_crops_ml, ...)
    price_future = executor.submit(get_price_ml, ...)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Ensure backend is running on port 5000 |
| "Module not found" | Install: `pip install requests pandas` |
| "Timeout error" | Increase timeout or check backend logs |
| "Empty response" | Verify database is seeded with data |

---

## Next Steps

1. ✅ Update all Streamlit pages with ML API calls
2. Add caching for better performance
3. Implement real-time WebSocket updates
4. Add user feedback for model improvements
5. Setup monitoring and alerting

For more details, see [ML_TRAINING_GUIDE.md](ML_TRAINING_GUIDE.md)
