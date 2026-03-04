"""
Crop Recommendation Prediction Script
"""

import pickle
import sys
import json
import numpy as np
from pathlib import Path

def predict_crops(temperature, rainfall, humidity, soil_ph, nitrogen, phosphorus, potassium, organic_matter):
    """Predict recommended crops based on environmental factors"""
    
    try:
        # Load trained model, scaler, and label encoder
        model_path = Path(__file__).parent / 'trained_models' / 'crop_recommendation_model.pkl'
        
        if not model_path.exists():
            return {
                'recommendations': ['Demo Mode: Rice', 'Demo Mode: Wheat', 'Demo Mode: Corn'],
                'confidence': [0.92, 0.85, 0.78],
                'reasoning': 'Model not loaded - showing demo recommendations'
            }
        
        with open(model_path, 'rb') as f:
            model, scaler, label_encoder = pickle.load(f)
        
        # Prepare features
        features = np.array([[temperature, rainfall, humidity, soil_ph, 
                             nitrogen, phosphorus, potassium, organic_matter]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Get predictions
        predictions = model.predict_proba(features_scaled)[0]
        top_indices = np.argsort(predictions)[-3:][::-1]
        
        top_crops = [label_encoder.classes_[i] for i in top_indices]
        top_probs = [float(predictions[i]) for i in top_indices]
        
        return {
            'recommendations': top_crops,
            'confidence': top_probs,
            'reasoning': f'Based on temperature ({temperature}°C), rainfall ({rainfall}mm), and soil conditions'
        }
    
    except Exception as e:
        return {
            'recommendations': ['Tomato', 'Potato', 'Onion'],
            'confidence': [0.80, 0.75, 0.70],
            'reasoning': f'Demo mode: {str(e)}'
        }

if __name__ == '__main__':
    temperature = float(sys.argv[1])
    rainfall = float(sys.argv[2])
    humidity = float(sys.argv[3])
    soil_ph = float(sys.argv[4])
    nitrogen = float(sys.argv[5])
    phosphorus = float(sys.argv[6])
    potassium = float(sys.argv[7])
    organic_matter = float(sys.argv[8])
    
    result = predict_crops(temperature, rainfall, humidity, soil_ph, 
                          nitrogen, phosphorus, potassium, organic_matter)
    print(json.dumps(result))
