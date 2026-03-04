"""
ML Training Pipeline for Agricultural Models
Trains crop recommendation, disease detection, price prediction, and yield forecasting models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error
import pickle
import os
from datetime import datetime

print("🤖 Agricultural ML Training Pipeline")
print("=" * 70)

# ============================================================================
# 1. CROP RECOMMENDATION MODEL
# ============================================================================
print("\n🌾 Training Crop Recommendation Model...")

try:
    crop_df = pd.read_csv('crop_production_data.csv')
    
    # Prepare data
    X = crop_df[['temperature_avg', 'rainfall', 'humidity_avg', 'soil_ph', 
                  'nitrogen', 'phosphorus', 'potassium', 'organic_matter']]
    y = crop_df['crop_name']
    
    # Encode labels
    le_crop = LabelEncoder()
    y_encoded = le_crop.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Scale features
    scaler_crop = StandardScaler()
    X_train_scaled = scaler_crop.fit_transform(X_train)
    X_test_scaled = scaler_crop.transform(X_test)
    
    # Train model
    crop_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    crop_model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = crop_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"   ✅ Accuracy: {accuracy:.4f}")
    print(f"   ✅ Features: {len(X.columns)}")
    print(f"   ✅ Crops: {len(le_crop.classes_)}")
    
    # Save model
    os.makedirs('trained_models', exist_ok=True)
    with open('trained_models/crop_recommendation_model.pkl', 'wb') as f:
        pickle.dump((crop_model, scaler_crop, le_crop), f)
    print("   ✅ Model saved: crop_recommendation_model.pkl")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# ============================================================================
# 2. DISEASE DETECTION MODEL
# ============================================================================
print("\n🦠 Training Disease Detection Model...")

try:
    disease_df = pd.read_csv('disease_detection_data.csv')
    
    # Prepare data
    X = disease_df[['temperature', 'humidity', 'rainfall', 'infection_rate', 
                     'area_affected', 'damage_type']]
    
    # Encode categorical features
    le_damage = LabelEncoder()
    X['damage_type_encoded'] = le_damage.fit_transform(X['damage_type'])
    X = X.drop('damage_type', axis=1)
    
    # Use severity as target
    y = disease_df['severity']
    le_disease = LabelEncoder()
    y_encoded = le_disease.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Scale features
    scaler_disease = StandardScaler()
    X_train_scaled = scaler_disease.fit_transform(X_train)
    X_test_scaled = scaler_disease.transform(X_test)
    
    # Train model
    disease_model = GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, random_state=42)
    disease_model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = disease_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"   ✅ Accuracy: {accuracy:.4f}")
    print(f"   ✅ F1-Score: {f1:.4f}")
    print(f"   ✅ Severity Classes: {len(le_disease.classes_)}")
    
    # Save model
    with open('trained_models/disease_detection_model.pkl', 'wb') as f:
        pickle.dump((disease_model, scaler_disease, le_disease, le_damage), f)
    print("   ✅ Model saved: disease_detection_model.pkl")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# ============================================================================
# 3. PRICE PREDICTION MODEL
# ============================================================================
print("\n💰 Training Price Prediction Model...")

try:
    price_df = pd.read_csv('price_prediction_data.csv')
    price_df['date'] = pd.to_datetime(price_df['date'])
    
    # Prepare data
    X = price_df[['supply', 'demand', 'seasonal_factor', 'export_price', 
                   'temperature', 'rainfall', 'fuel_price', 'labor_cost', 
                   'storage_cost', 'trading_volume']]
    y = price_df['price_per_unit']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler_price = StandardScaler()
    X_train_scaled = scaler_price.fit_transform(X_train)
    X_test_scaled = scaler_price.transform(X_test)
    
    # Train model
    price_model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    price_model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = price_model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = price_model.score(X_test_scaled, y_test)
    
    print(f"   ✅ RMSE: {rmse:.2f}")
    print(f"   ✅ R² Score: {r2:.4f}")
    print(f"   ✅ Features: {len(X.columns)}")
    
    # Save model
    with open('trained_models/price_prediction_model.pkl', 'wb') as f:
        pickle.dump((price_model, scaler_price), f)
    print("   ✅ Model saved: price_prediction_model.pkl")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# ============================================================================
# 4. YIELD FORECASTING MODEL
# ============================================================================
print("\n📈 Training Yield Forecasting Model...")

try:
    yield_df = pd.read_csv('yield_forecasting_data.csv')
    
    # Prepare data
    X = yield_df[['area', 'temperature_sum', 'rainfall_total', 'critical_rainfall',
                   'soil_nitrogen', 'soil_phosphorus', 'soil_potassium',
                   'gdd_vegetative', 'gdd_reproductive', 'gdd_maturity',
                   'drought_stress_days', 'pest_pressure', 'disease_pressure',
                   'irrigation_count', 'fertilizer_application']]
    y = yield_df['actual_yield']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler_yield = StandardScaler()
    X_train_scaled = scaler_yield.fit_transform(X_train)
    X_test_scaled = scaler_yield.transform(X_test)
    
    # Train model
    yield_model = RandomForestRegressor(n_estimators=250, random_state=42, n_jobs=-1)
    yield_model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = yield_model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = yield_model.score(X_test_scaled, y_test)
    
    print(f"   ✅ RMSE: {rmse:.2f} tonnes/hectare")
    print(f"   ✅ R² Score: {r2:.4f}")
    print(f"   ✅ Features: {len(X.columns)}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': yield_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n   Top 5 Important Features:")
    for idx, row in feature_importance.head(5).iterrows():
        print(f"      • {row['feature']}: {row['importance']:.4f}")
    
    # Save model
    with open('trained_models/yield_forecasting_model.pkl', 'wb') as f:
        pickle.dump((yield_model, scaler_yield), f)
    print("   ✅ Model saved: yield_forecasting_model.pkl")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# ============================================================================
# Summary Report
# ============================================================================
print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE")
print("=" * 70)
print("\n📁 Trained Models saved in: trained_models/")
print("   • crop_recommendation_model.pkl")
print("   • disease_detection_model.pkl")
print("   • price_prediction_model.pkl")
print("   • yield_forecasting_model.pkl")
print("\n⏰ Training completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 70)
