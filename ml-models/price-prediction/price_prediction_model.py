import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import joblib
import json

class PricePredictionModel:
    """
    Time series prediction model for crop prices
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = MinMaxScaler()
        self.lookback_days = 30
        
        if model_path:
            self.load_model(model_path)
        else:
            self.build_model()
    
    def build_model(self):
        """Build gradient boosting model for price prediction"""
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            random_state=42
        )
    
    def create_features(self, price_history):
        """
        Create features from price history
        price_history: list of daily prices [30 days]
        """
        if len(price_history) < self.lookback_days:
            raise ValueError(f"Need at least {self.lookback_days} days of data")
        
        features = []
        
        # Moving averages
        ma_7 = np.mean(price_history[-7:])
        ma_14 = np.mean(price_history[-14:])
        ma_30 = np.mean(price_history[-30:])
        
        # Volatility
        volatility = np.std(price_history[-14:])
        
        # Trend (slope of 7-day prices)
        x = np.arange(7)
        y = np.array(price_history[-7:])
        trend = np.polyfit(x, y, 1)[0]
        
        # Min-Max in period
        min_price = np.min(price_history[-30:])
        max_price = np.max(price_history[-30:])
        
        # Current price change
        price_change = ((price_history[-1] - price_history[-7]) / price_history[-7]) * 100
        
        features = [ma_7, ma_14, ma_30, volatility, trend, min_price, max_price, price_change]
        
        return features
    
    def predict(self, price_history, days_ahead=7):
        """
        Predict future price
        price_history: list of historical daily prices
        days_ahead: number of days to predict ahead
        """
        if self.model is None:
            raise ValueError("Model not trained.")
        
        features = self.create_features(price_history)
        current_price = price_history[-1]
        
        # Mock prediction logic
        # Would use self.model.predict([[features]]) in production
        
        predicted_prices = []
        for i in range(days_ahead):
            # Simple trend-based mock
            trend_factor = 1.01 + (np.random.rand() * 0.02)
            predicted_price = current_price * trend_factor
            predicted_prices.append(predicted_price)
            current_price = predicted_price
        
        return {
            'predicted_prices': predicted_prices,
            'average_price': float(np.mean(predicted_prices)),
            'price_trend': 'uptrend' if predicted_prices[-1] > price_history[-1] else 'downtrend',
            'recommendation': 'sell' if predicted_prices[-1] > price_history[-1] * 1.05 else 'hold',
            'best_sell_date': (datetime.now() + timedelta(days=np.argmax(predicted_prices) + 1)).isoformat(),
        }
    
    def save_model(self, path):
        """Save model"""
        joblib.dump(self.model, path)
    
    def load_model(self, path):
        """Load model"""
        self.model = joblib.load(path)


class YieldForecastingModel:
    """
    Model to forecast crop yield based on various factors
    """
    
    def __init__(self, model_path=None):
        self.model = None
        
        if model_path:
            self.load_model(model_path)
        else:
            self.build_model()
    
    def build_model(self):
        """Build model for yield forecasting"""
        self.model = GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
    
    def predict(self, features):
        """
        Predict crop yield
        features: {
            'crop_name': str,
            'area': float (hectares),
            'soil_nitrogen': float,
            'soil_phosphorus': float,
            'soil_potassium': float,
            'average_temperature': float,
            'rainfall': float,
            'humidity': float,
            'days_to_harvest': int,
        }
        """
        if self.model is None:
            raise ValueError("Model not trained.")
        
        # Base yields for different crops (kg/hectare)
        base_yields = {
            'rice': 5000,
            'wheat': 4500,
            'corn': 6000,
            'sugarcane': 70000,
            'potato': 20000,
            'tomato': 40000,
            'cotton': 2000,
        }
        
        crop = features.get('crop_name', 'rice').lower()
        base_yield = base_yields.get(crop, 5000)
        
        # Calculate yield based on conditions
        soil_score = (
            (features.get('soil_nitrogen', 20) / 50) +
            (features.get('soil_phosphorus', 15) / 40) +
            (features.get('soil_potassium', 150) / 400)
        ) / 3
        
        weather_score = 1.0
        if 20 <= features.get('average_temperature', 25) <= 35:
            weather_score *= 1.1
        
        if 400 <= features.get('rainfall', 500) <= 2000:
            weather_score *= 1.05
        
        # Days to harvest impact
        days_to_harvest = features.get('days_to_harvest', 150)
        progress_score = min(days_to_harvest / 150, 1.0)
        
        predicted_yield = base_yield * soil_score * weather_score * (0.7 + progress_score * 0.3)
        
        return {
            'estimated_yield': float(predicted_yield),
            'yield_per_hectare': float(predicted_yield / features.get('area', 1)),
            'confidence': 75 + int(progress_score * 20),
            'factors': {
                'soil_condition': float(soil_score * 100),
                'weather_favorable': float(weather_score * 100),
                'crop_maturity': float(progress_score * 100),
            }
        }
    
    def save_model(self, path):
        """Save model"""
        joblib.dump(self.model, path)
    
    def load_model(self, path):
        """Load model"""
        self.model = joblib.load(path)


if __name__ == '__main__':
    price_model = PricePredictionModel()
    yield_model = YieldForecastingModel()
    
    print("✓ Price Prediction Model initialized")
    print("✓ Yield Forecasting Model initialized")
