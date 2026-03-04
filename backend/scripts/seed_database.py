"""
Database Seed Script - Load 80k+ records into MongoDB
Run this after training ML models
"""

import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/smart_farming')

print("🌾 Database Seeding Script")
print("=" * 70)
print(f"MongoDB URI: {MONGO_URI}")
print("=" * 70)

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client.smart_farming
    
    print("\n✅ Connected to MongoDB")
    
    # ============================================================================
    # 1. SEED CROP PRODUCTION DATA (50,000 records)
    # ============================================================================
    print("\n📊 Seeding Crop Production Data...")
    
    crop_df = pd.read_csv('crop_production_data.csv')
    
    # Prepare documents
    crop_docs = []
    for _, row in crop_df.iterrows():
        doc = {
            'crop_name': row['crop_name'],
            'region': row['region'],
            'year': int(row['year']),
            'area_planted': float(row['area_planted']),
            'area_harvested': float(row['area_harvested']),
            'production': float(row['production']),
            'yield_per_hectare': float(row['yield_per_hectare']),
            'weather': {
                'temperature_avg': float(row['temperature_avg']),
                'rainfall': float(row['rainfall']),
                'humidity_avg': float(row['humidity_avg']),
            },
            'soil': {
                'ph': float(row['soil_ph']),
                'type': row['soil_type'],
                'nitrogen': float(row['nitrogen']),
                'phosphorus': float(row['phosphorus']),
                'potassium': float(row['potassium']),
                'organic_matter': float(row['organic_matter']),
            },
            'farming_practice': {
                'irrigation_used': row['irrigation_used'] == 'Yes',
                'pesticide_type': row['pesticide_type'],
                'fertilizer_usage': float(row['fertilizer_usage']),
            },
            'season': row['season'],
            'quality_score': float(row['crop_quality_score']),
            'water_usage_efficiency': float(row['water_usage_efficiency']),
            'nutrient_efficiency': float(row['nutrient_efficiency']),
            'created_at': datetime.utcnow(),
        }
        crop_docs.append(doc)
    
    # Insert in batches
    batch_size = 1000
    for i in range(0, len(crop_docs), batch_size):
        batch = crop_docs[i:i+batch_size]
        db.crop_production.insert_many(batch)
        print(f"   ✅ Inserted {len(batch)} crop records ({i+len(batch)}/{len(crop_docs)})")
    
    # Create index
    db.crop_production.create_index('crop_name')
    db.crop_production.create_index('region')
    db.crop_production.create_index('year')
    
    print(f"✅ Total Crop Records: {db.crop_production.count_documents({})}")
    
    # ============================================================================
    # 2. SEED DISEASE DATA (15,000 records)
    # ============================================================================
    print("\n🦠 Seeding Disease Detection Data...")
    
    disease_df = pd.read_csv('disease_detection_data.csv')
    
    disease_docs = []
    for _, row in disease_df.iterrows():
        doc = {
            'crop_name': row['crop_name'],
            'disease_name': row['disease_name'],
            'region': row['region'],
            'year': int(row['year']),
            'infection_rate': float(row['infection_rate']),
            'area_affected': float(row['area_affected']),
            'severity': row['severity'],
            'environmental_factors': {
                'temperature': float(row['temperature']),
                'humidity': float(row['humidity']),
                'rainfall': float(row['rainfall']),
            },
            'symptoms': {
                'leaf_color': row['leaf_color'],
                'spot_pattern': row['spot_pattern'],
                'spot_color': row['spot_color'],
                'leaf_texture': row['leaf_texture'],
            },
            'damage_type': row['damage_type'],
            'treatment': {
                'fungicide_effective': row['fungicide_effective'],
                'treatment_days': int(row['treatment_days']),
                'recovery_rate': float(row['recovery_rate']),
            },
            'yield_loss': float(row['yield_loss']),
            'created_at': datetime.utcnow(),
        }
        disease_docs.append(doc)
    
    # Insert in batches
    for i in range(0, len(disease_docs), batch_size):
        batch = disease_docs[i:i+batch_size]
        db.disease_detection.insert_many(batch)
        print(f"   ✅ Inserted {len(batch)} disease records ({i+len(batch)}/{len(disease_docs)})")
    
    # Create indexes
    db.disease_detection.create_index('crop_name')
    db.disease_detection.create_index('disease_name')
    db.disease_detection.create_index('severity')
    
    print(f"✅ Total Disease Records: {db.disease_detection.count_documents({})}")
    
    # ============================================================================
    # 3. SEED PRICE DATA (10,000 records)
    # ============================================================================
    print("\n💰 Seeding Price Prediction Data...")
    
    price_df = pd.read_csv('price_prediction_data.csv')
    price_df['date'] = pd.to_datetime(price_df['date'])
    
    price_docs = []
    for _, row in price_df.iterrows():
        doc = {
            'crop_name': row['crop_name'],
            'region': row['region'],
            'market_type': row['market'],
            'date': row['date'],
            'price': {
                'per_unit': float(row['price_per_unit']),
                'export': float(row['export_price']),
                'import': float(row['import_price']),
            },
            'market_factors': {
                'supply': float(row['supply']),
                'demand': float(row['demand']),
                'seasonal_factor': float(row['seasonal_factor']),
                'trading_volume': int(row['trading_volume']),
            },
            'environmental_factors': {
                'temperature': float(row['temperature']),
                'rainfall': float(row['rainfall']),
            },
            'cost_factors': {
                'fuel_price': float(row['fuel_price']),
                'labor_cost': float(row['labor_cost']),
                'storage_cost': float(row['storage_cost']),
            },
            'government_subsidy': bool(row['government_subsidy']),
            'volatility': float(row['price_volatility']),
            'trend': row['trend'],
            'created_at': datetime.utcnow(),
        }
        price_docs.append(doc)
    
    # Insert in batches
    for i in range(0, len(price_docs), batch_size):
        batch = price_docs[i:i+batch_size]
        db.price_prediction.insert_many(batch)
        print(f"   ✅ Inserted {len(batch)} price records ({i+len(batch)}/{len(price_docs)})")
    
    # Create indexes
    db.price_prediction.create_index('crop_name')
    db.price_prediction.create_index('date')
    db.price_prediction.create_index('region')
    
    print(f"✅ Total Price Records: {db.price_prediction.count_documents({})}")
    
    # ============================================================================
    # 4. SEED YIELD DATA (12,000 records)
    # ============================================================================
    print("\n📈 Seeding Yield Forecasting Data...")
    
    yield_df = pd.read_csv('yield_forecasting_data.csv')
    yield_df['planting_date'] = pd.to_datetime(yield_df['planting_date'])
    yield_df['harvest_date'] = pd.to_datetime(yield_df['harvest_date'])
    
    yield_docs = []
    for _, row in yield_df.iterrows():
        doc = {
            'crop_name': row['crop_name'],
            'region': row['region'],
            'season': row['season'],
            'year': int(row['year']),
            'dates': {
                'planting': row['planting_date'],
                'harvest': row['harvest_date'],
            },
            'area': float(row['area']),
            'yield': {
                'estimate': float(row['yield_estimate']),
                'actual': float(row['actual_yield']),
                'prediction_accuracy': float(row['prediction_accuracy']),
            },
            'thermal_data': {
                'temperature_sum': float(row['temperature_sum']),
                'gdd_vegetative': float(row['gdd_vegetative']),
                'gdd_reproductive': float(row['gdd_reproductive']),
                'gdd_maturity': float(row['gdd_maturity']),
            },
            'water_data': {
                'rainfall_total': float(row['rainfall_total']),
                'critical_rainfall': float(row['critical_rainfall']),
            },
            'soil_nutrients': {
                'nitrogen': float(row['soil_nitrogen']),
                'phosphorus': float(row['soil_phosphorus']),
                'potassium': float(row['soil_potassium']),
            },
            'stress_factors': {
                'drought_stress_days': int(row['drought_stress_days']),
                'pest_pressure': float(row['pest_pressure']),
                'disease_pressure': float(row['disease_pressure']),
            },
            'management': {
                'irrigation_count': int(row['irrigation_count']),
                'fertilizer_application': float(row['fertilizer_application']),
            },
            'created_at': datetime.utcnow(),
        }
        yield_docs.append(doc)
    
    # Insert in batches
    for i in range(0, len(yield_docs), batch_size):
        batch = yield_docs[i:i+batch_size]
        db.yield_forecasting.insert_many(batch)
        print(f"   ✅ Inserted {len(batch)} yield records ({i+len(batch)}/{len(yield_docs)})")
    
    # Create indexes
    db.yield_forecasting.create_index('crop_name')
    db.yield_forecasting.create_index('region')
    db.yield_forecasting.create_index('season')
    
    print(f"✅ Total Yield Records: {db.yield_forecasting.count_documents({})}")
    
    # ============================================================================
    # 5. SEED WEATHER DATA (5,000 records)
    # ============================================================================
    print("\n🌤️  Seeding Weather Time Series Data...")
    
    weather_df = pd.read_csv('weather_data.csv')
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    weather_docs = []
    for _, row in weather_df.iterrows():
        doc = {
            'region': row['region'],
            'date': row['date'],
            'temperature': {
                'min': float(row['temperature_min']),
                'max': float(row['temperature_max']),
                'avg': float(row['temperature_avg']),
            },
            'humidity': {
                'min': float(row['humidity_min']),
                'max': float(row['humidity_max']),
                'avg': float(row['humidity_avg']),
            },
            'precipitation': float(row['rainfall']),
            'wind_speed': float(row['wind_speed']),
            'solar_radiation': float(row['solar_radiation']),
            'atmospheric_pressure': float(row['atmospheric_pressure']),
            'cloud_cover': float(row['cloud_cover']),
            'uv_index': float(row['uv_index']),
            'evapotranspiration': float(row['evapotranspiration']),
            'soil': {
                'moisture': float(row['soil_moisture']),
                'temperature': float(row['soil_temperature']),
            },
            'created_at': datetime.utcnow(),
        }
        weather_docs.append(doc)
    
    # Insert in batches
    for i in range(0, len(weather_docs), batch_size):
        batch = weather_docs[i:i+batch_size]
        db.weather_timeseries.insert_many(batch)
        print(f"   ✅ Inserted {len(batch)} weather records ({i+len(batch)}/{len(weather_docs)})")
    
    # Create indexes
    db.weather_timeseries.create_index('region')
    db.weather_timeseries.create_index('date')
    
    print(f"✅ Total Weather Records: {db.weather_timeseries.count_documents({})}")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 70)
    print("✅ DATABASE SEEDING COMPLETE")
    print("=" * 70)
    
    total = (db.crop_production.count_documents({}) + 
             db.disease_detection.count_documents({}) +
             db.price_prediction.count_documents({}) +
             db.yield_forecasting.count_documents({}) +
             db.weather_timeseries.count_documents({}))
    
    print(f"\n📊 Total Records Seeded: {total:,}")
    print("\n📁 Collections Created:")
    print(f"   • crop_production ({db.crop_production.count_documents({}):,} docs)")
    print(f"   • disease_detection ({db.disease_detection.count_documents({}):,} docs)")
    print(f"   • price_prediction ({db.price_prediction.count_documents({}):,} docs)")
    print(f"   • yield_forecasting ({db.yield_forecasting.count_documents({}):,} docs)")
    print(f"   • weather_timeseries ({db.weather_timeseries.count_documents({}):,} docs)")
    
    print("\n⏰ Seeding completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    client.close()
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
