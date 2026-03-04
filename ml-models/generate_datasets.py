"""
Generate large agricultural datasets (80k+ records) for ML training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Crop and region data
CROPS = ['Rice', 'Wheat', 'Corn', 'Cotton', 'Sugarcane', 'Potato', 'Tomato', 
         'Onion', 'Cabbage', 'Carrot', 'Apple', 'Banana', 'Mango', 'Orange', 
         'Grape', 'Chilli', 'Turmeric', 'Ginger', 'Garlic', 'Soybean']

REGIONS = ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Karnataka', 
           'Tamil Nadu', 'West Bengal', 'Rajasthan', 'Gujarat', 'Maharashtra']

SOIL_TYPES = ['Loamy', 'Clay', 'Sandy', 'Silty', 'Peaty', 'Chalky']

DISEASES = ['Leaf Rust', 'Powdery Mildew', 'Bacterial Leaf Blight', 'Wheat Head Scab',
            'Fusarium Wilt', 'Brown Spot', 'Early Blight', 'Late Blight', 'Downy Mildew',
            'Septoria Leaf Blotch', 'Anthracnose', 'Damping Off', 'Botrytis', 'Mosaic Virus']

print("🌾 Generating Agricultural Datasets...")
print("=" * 60)

# ============================================================================
# 1. CROP PRODUCTION DATASET (50,000 records)
# ============================================================================
print("\n📊 Generating Crop Production Dataset (50,000 records)...")

crop_data = {
    'crop_id': range(1, 50001),
    'crop_name': [random.choice(CROPS) for _ in range(50000)],
    'region': [random.choice(REGIONS) for _ in range(50000)],
    'year': [random.randint(2015, 2024) for _ in range(50000)],
    'area_planted': np.random.uniform(0.5, 100, 50000),  # hectares
    'area_harvested': np.random.uniform(0.3, 100, 50000),
    'production': np.random.uniform(100, 50000, 50000),  # tonnes
    'yield_per_hectare': np.random.uniform(0.5, 80, 50000),  # tonnes/hectare
    'temperature_avg': np.random.uniform(10, 40, 50000),  # Celsius
    'rainfall': np.random.uniform(200, 3000, 50000),  # mm
    'humidity_avg': np.random.uniform(30, 95, 50000),  # %
    'soil_ph': np.random.uniform(4.5, 8.5, 50000),
    'soil_type': [random.choice(SOIL_TYPES) for _ in range(50000)],
    'nitrogen': np.random.uniform(10, 500, 50000),  # mg/kg
    'phosphorus': np.random.uniform(5, 200, 50000),
    'potassium': np.random.uniform(100, 600, 50000),
    'organic_matter': np.random.uniform(0.5, 8, 50000),  # %
    'irrigation_used': [random.choice(['Yes', 'No']) for _ in range(50000)],
    'pesticide_type': [random.choice(['Organic', 'Chemical', 'Bio-pesticide', 'None']) for _ in range(50000)],
    'fertilizer_usage': np.random.uniform(0, 500, 50000),  # kg/hectare
    'season': [random.choice(['Kharif', 'Rabi', 'Summer']) for _ in range(50000)],
    'crop_quality_score': np.random.uniform(1, 10, 50000),
}

crop_df = pd.DataFrame(crop_data)

# Add derived features
crop_df['water_usage_efficiency'] = crop_df['production'] / (crop_df['rainfall'] + 1)
crop_df['nutrient_efficiency'] = crop_df['production'] / (crop_df['nitrogen'] + crop_df['phosphorus'] + crop_df['potassium'] + 1)

# Save
crop_df.to_csv('crop_production_data.csv', index=False)
print(f"✅ Saved: crop_production_data.csv ({len(crop_df):,} records)")

# ============================================================================
# 2. DISEASE DETECTION DATASET (15,000 records)
# ============================================================================
print("\n🦠 Generating Disease Detection Dataset (15,000 records)...")

disease_data = {
    'disease_id': range(1, 15001),
    'crop_name': [random.choice(CROPS) for _ in range(15000)],
    'disease_name': [random.choice(DISEASES) for _ in range(15000)],
    'region': [random.choice(REGIONS) for _ in range(15000)],
    'year': [random.randint(2018, 2024) for _ in range(15000)],
    'infection_rate': np.random.uniform(0, 100, 15000),  # %
    'area_affected': np.random.uniform(0.1, 100, 15000),  # hectares
    'severity': [random.choice(['Low', 'Medium', 'High', 'Critical']) for _ in range(15000)],
    'temperature': np.random.uniform(10, 40, 15000),
    'humidity': np.random.uniform(30, 100, 15000),
    'rainfall': np.random.uniform(0, 200, 15000),
    'leaf_color': [random.choice(['Green', 'Yellow', 'Brown', 'Black', 'Reddish']) for _ in range(15000)],
    'spot_pattern': [random.choice(['Circular', 'Angular', 'Irregular', 'Linear']) for _ in range(15000)],
    'spot_color': [random.choice(['Brown', 'Black', 'Yellow', 'Red', 'Gray']) for _ in range(15000)],
    'leaf_texture': [random.choice(['Smooth', 'Rough', 'Powdery', 'Fuzzy']) for _ in range(15000)],
    'damage_type': [random.choice(['Leaf', 'Stem', 'Root', 'Fruit', 'Flower']) for _ in range(15000)],
    'fungicide_effective': [random.choice(['Yes', 'No', 'Partial']) for _ in range(15000)],
    'treatment_days': np.random.randint(0, 60, 15000),
    'recovery_rate': np.random.uniform(0, 100, 15000),  # %
    'yield_loss': np.random.uniform(0, 100, 15000),  # %
}

disease_df = pd.DataFrame(disease_data)
disease_df.to_csv('disease_detection_data.csv', index=False)
print(f"✅ Saved: disease_detection_data.csv ({len(disease_df):,} records)")

# ============================================================================
# 3. PRICE PREDICTION DATASET (10,000 records)
# ============================================================================
print("\n💰 Generating Price Prediction Dataset (10,000 records)...")

price_data = {
    'price_id': range(1, 10001),
    'crop_name': [random.choice(CROPS) for _ in range(10000)],
    'region': [random.choice(REGIONS) for _ in range(10000)],
    'market': [random.choice(['Wholesale', 'Retail', 'Futures']) for _ in range(10000)],
    'date': [datetime(2019, 1, 1) + timedelta(days=random.randint(0, 2000)) for _ in range(10000)],
    'price_per_unit': np.random.uniform(100, 5000, 10000),  # Rs/quintal
    'supply': np.random.uniform(1000, 100000, 10000),  # tonnes
    'demand': np.random.uniform(1000, 100000, 10000),
    'seasonal_factor': np.random.uniform(0.5, 2.0, 10000),
    'export_price': np.random.uniform(100, 5000, 10000),
    'import_price': np.random.uniform(100, 5000, 10000),
    'temperature': np.random.uniform(10, 40, 10000),
    'rainfall': np.random.uniform(0, 200, 10000),
    'fuel_price': np.random.uniform(50, 150, 10000),
    'labor_cost': np.random.uniform(100, 500, 10000),
    'storage_cost': np.random.uniform(10, 100, 10000),
    'government_subsidy': [random.choice([True, False]) for _ in range(10000)],
    'trading_volume': np.random.randint(100, 10000, 10000),
    'price_volatility': np.random.uniform(0, 50, 10000),  # %
    'trend': [random.choice(['Upward', 'Downward', 'Stable']) for _ in range(10000)],
}

price_df = pd.DataFrame(price_data)
price_df.to_csv('price_prediction_data.csv', index=False)
print(f"✅ Saved: price_prediction_data.csv ({len(price_df):,} records)")

# ============================================================================
# 4. YIELD FORECASTING DATASET (12,000 records)
# ============================================================================
print("\n📈 Generating Yield Forecasting Dataset (12,000 records)...")

yield_data = {
    'yield_id': range(1, 12001),
    'crop_name': [random.choice(CROPS) for _ in range(12000)],
    'region': [random.choice(REGIONS) for _ in range(12000)],
    'season': [random.choice(['Kharif', 'Rabi', 'Summer']) for _ in range(12000)],
    'year': [random.randint(2015, 2024) for _ in range(12000)],
    'planting_date': [datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3650)) for _ in range(12000)],
    'harvest_date': [datetime(2015, 1, 1) + timedelta(days=random.randint(120, 3750)) for _ in range(12000)],
    'area': np.random.uniform(0.5, 100, 12000),
    'yield_estimate': np.random.uniform(0.5, 80, 12000),  # tonnes/hectare
    'actual_yield': np.random.uniform(0.5, 80, 12000),
    'temperature_sum': np.random.uniform(2000, 5000, 12000),  # degree-days
    'rainfall_total': np.random.uniform(200, 3000, 12000),
    'critical_rainfall': np.random.uniform(100, 2000, 12000),
    'soil_nitrogen': np.random.uniform(10, 500, 12000),
    'soil_phosphorus': np.random.uniform(5, 200, 12000),
    'soil_potassium': np.random.uniform(100, 600, 12000),
    'gdd_vegetative': np.random.uniform(500, 2000, 12000),
    'gdd_reproductive': np.random.uniform(500, 2000, 12000),
    'gdd_maturity': np.random.uniform(200, 1000, 12000),
    'drought_stress_days': np.random.randint(0, 100, 12000),
    'pest_pressure': np.random.uniform(0, 100, 12000),  # %
    'disease_pressure': np.random.uniform(0, 100, 12000),
    'irrigation_count': np.random.randint(0, 15, 12000),
    'fertilizer_application': np.random.uniform(0, 500, 12000),
    'prediction_accuracy': np.random.uniform(60, 99, 12000),  # %
}

yield_df = pd.DataFrame(yield_data)
yield_df.to_csv('yield_forecasting_data.csv', index=False)
print(f"✅ Saved: yield_forecasting_data.csv ({len(yield_df):,} records)")

# ============================================================================
# 5. WEATHER TIME SERIES DATASET (5,000 records)
# ============================================================================
print("\n🌤️  Generating Weather Time Series Dataset (5,000 records)...")

weather_data = {
    'weather_id': range(1, 5001),
    'region': [random.choice(REGIONS) for _ in range(5000)],
    'date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460)) for _ in range(5000)],
    'temperature_min': np.random.uniform(5, 25, 5000),
    'temperature_max': np.random.uniform(20, 45, 5000),
    'temperature_avg': np.random.uniform(15, 35, 5000),
    'humidity_min': np.random.uniform(10, 50, 5000),
    'humidity_max': np.random.uniform(60, 100, 5000),
    'humidity_avg': np.random.uniform(40, 80, 5000),
    'rainfall': np.random.uniform(0, 100, 5000),  # mm
    'wind_speed': np.random.uniform(0, 20, 5000),  # km/h
    'solar_radiation': np.random.uniform(0, 25, 5000),  # MJ/m²
    'atmospheric_pressure': np.random.uniform(1000, 1030, 5000),  # hPa
    'cloud_cover': np.random.uniform(0, 100, 5000),  # %
    'uv_index': np.random.uniform(0, 15, 5000),
    'evapotranspiration': np.random.uniform(1, 10, 5000),  # mm
    'soil_moisture': np.random.uniform(10, 100, 5000),  # %
    'soil_temperature': np.random.uniform(5, 40, 5000),
}

weather_df = pd.DataFrame(weather_data)
weather_df.to_csv('weather_data.csv', index=False)
print(f"✅ Saved: weather_data.csv ({len(weather_df):,} records)")

# ============================================================================
# Summary Statistics
# ============================================================================
print("\n" + "=" * 60)
print("📊 DATASET SUMMARY")
print("=" * 60)

total_records = (len(crop_df) + len(disease_df) + len(price_df) + 
                 len(yield_df) + len(weather_df))

print(f"\n✅ Total Dataset Records: {total_records:,}")
print(f"   • Crop Production:    {len(crop_df):,} records")
print(f"   • Disease Detection:   {len(disease_df):,} records")
print(f"   • Price Prediction:    {len(price_df):,} records")
print(f"   • Yield Forecasting:   {len(yield_df):,} records")
print(f"   • Weather Time Series: {len(weather_df):,} records")

print(f"\n📁 Files created:")
print(f"   • crop_production_data.csv")
print(f"   • disease_detection_data.csv")
print(f"   • price_prediction_data.csv")
print(f"   • yield_forecasting_data.csv")
print(f"   • weather_data.csv")

print(f"\n💾 Ready for ML training!")
print("=" * 60)
