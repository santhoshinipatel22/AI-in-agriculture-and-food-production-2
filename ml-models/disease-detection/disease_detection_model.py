import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
import joblib
import cv2
from PIL import Image
import json

class CropDiseaseDetectionModel:
    """
    CNN-based model for crop disease detection from leaf images
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.classes = [
            'Healthy',
            'Powdery Mildew',
            'Leaf Rust',
            'Leaf Blight',
            'Brown Spot',
            'Stem Rot',
            'Wilt',
            'Root Rot'
        ]
        self.img_size = 224
        
        if model_path:
            self.load_model(model_path)
        else:
            self.build_model()
    
    def build_model(self):
        """Build CNN model for disease detection"""
        inputs = keras.Input(shape=(self.img_size, self.img_size, 3))
        
        x = layers.Rescaling(1./255)(inputs)
        x = layers.Conv2D(32, 3, activation='relu', padding='same')(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Conv2D(128, 3, activation='relu', padding='same')(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Flatten()(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        outputs = layers.Dense(len(self.classes), activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        img = Image.open(image_path)
        img = img.resize((self.img_size, self.img_size))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def predict(self, image_path):
        """Predict disease from image"""
        if self.model is None:
            raise ValueError("Model not loaded. Train or load a model first.")
        
        img = self.preprocess_image(image_path)
        predictions = self.model.predict(img)
        
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx]) * 100
        disease = self.classes[class_idx]
        
        return {
            'disease': disease,
            'confidence': confidence,
            'all_predictions': {
                self.classes[i]: float(predictions[0][i]) * 100 
                for i in range(len(self.classes))
            }
        }
    
    def save_model(self, path):
        """Save model to disk"""
        self.model.save(path)
    
    def load_model(self, path):
        """Load model from disk"""
        self.model = keras.models.load_model(path)


class CropRecommendationModel:
    """
    Machine learning model for crop recommendation based on soil and weather conditions
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = MinMaxScaler()
        self.crops = [
            'Rice', 'Wheat', 'Corn', 'Cotton', 'Sugarcane',
            'Potato', 'Tomato', 'Onion', 'Cabbage', 'Carrot',
            'Apple', 'Banana', 'Mango', 'Orange', 'Grape',
            'Chilli', 'Turmeric', 'Ginger', 'Garlic', 'Soybean'
        ]
        
        if model_path:
            self.load_model(model_path)
        else:
            self.build_model()
    
    def build_model(self):
        """Build model for crop recommendation"""
        from sklearn.ensemble import RandomForestClassifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def predict(self, features):
        """
        Predict best crops for given conditions
        features: {
            'nitrogen': float,
            'phosphorus': float,
            'potassium': float,
            'ph': float,
            'rainfall': float,
            'temperature': float,
            'humidity': float
        }
        """
        if self.model is None:
            raise ValueError("Model not trained.")
        
        # Features in specific order
        feature_list = [
            features.get('nitrogen', 0),
            features.get('phosphorus', 0),
            features.get('potassium', 0),
            features.get('ph', 7),
            features.get('rainfall', 100),
            features.get('temperature', 25),
            features.get('humidity', 60)
        ]
        
        # Mock prediction logic
        recommendations = {}
        for crop in self.crops:
            # Score based on conditions (simplified)
            score = np.random.rand() * 100
            recommendations[crop] = float(score)
        
        # Sort and return top 5
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'top_crops': [
                {'crop': crop, 'score': float(score)} 
                for crop, score in sorted_recs[:5]
            ],
            'soil_condition': 'Good' if features.get('ph', 7) >= 6 else 'Acidic',
        }
    
    def save_model(self, path):
        """Save model"""
        joblib.dump(self.model, path)
    
    def load_model(self, path):
        """Load model"""
        self.model = joblib.load(path)


if __name__ == '__main__':
    # Initialize models
    disease_model = CropDiseaseDetectionModel()
    recommendation_model = CropRecommendationModel()
    
    print("✓ Disease Detection Model initialized")
    print("✓ Crop Recommendation Model initialized")
