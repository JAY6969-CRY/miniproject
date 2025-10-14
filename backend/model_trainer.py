import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Dict, Any, Tuple
from config import settings

class ModelTrainer:
    def __init__(self):
        self.model_dir = settings.MODEL_DIR
        os.makedirs(self.model_dir, exist_ok=True)
    
    def calculate_sma(self, prices: list, window: int) -> list:
        """Calculate Simple Moving Average"""
        df = pd.DataFrame({'price': prices})
        sma = df['price'].rolling(window=window, min_periods=1).mean()
        return sma.tolist()
    
    def calculate_rsi(self, prices: list, period: int = 14) -> list:
        """Calculate Relative Strength Index"""
        df = pd.DataFrame({'price': prices})
        delta = df['price'].diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi = rsi.fillna(50)  # Fill NaN with neutral value
        return rsi.tolist()
    
    def prepare_features(self, historical_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features and target for model training"""
        close_prices = historical_data['close']
        
        # Calculate technical indicators
        sma_5 = self.calculate_sma(close_prices, 5)
        sma_10 = self.calculate_sma(close_prices, 10)
        rsi_14 = self.calculate_rsi(close_prices, 14)
        
        # Create feature matrix
        features = []
        targets = []
        
        # Start from index 10 to have enough data for indicators
        for i in range(10, len(close_prices) - 1):
            feature_row = [
                close_prices[i],      # Current close
                sma_5[i],             # SMA 5
                sma_10[i],            # SMA 10
                rsi_14[i],            # RSI 14
            ]
            features.append(feature_row)
            targets.append(close_prices[i + 1])  # Next day close (target)
        
        return np.array(features), np.array(targets)
    
    def train_model(self, symbol: str, historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train linear regression model for a specific symbol"""
        X, y = self.prepare_features(historical_data)
        
        if len(X) < 20:
            raise ValueError(f"Insufficient data for training. Need at least 30 days, got {len(X) + 10}")
        
        # Split data (use last 20% for validation)
        split_idx = int(len(X) * 0.8)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        
        # Train model
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        # Calculate metrics
        train_score = model.score(X_train_scaled, y_train)
        val_score = model.score(X_val_scaled, y_val)
        
        # Save model and scaler
        model_path = os.path.join(self.model_dir, f"{symbol}_model.pkl")
        scaler_path = os.path.join(self.model_dir, f"{symbol}_scaler.pkl")
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        
        return {
            "symbol": symbol,
            "train_score": float(train_score),
            "validation_score": float(val_score),
            "model_path": model_path,
            "scaler_path": scaler_path,
            "training_samples": len(X_train),
            "validation_samples": len(X_val)
        }
    
    def load_model(self, symbol: str) -> Tuple[Any, Any]:
        """Load trained model and scaler for a symbol"""
        model_path = os.path.join(self.model_dir, f"{symbol}_model.pkl")
        scaler_path = os.path.join(self.model_dir, f"{symbol}_scaler.pkl")
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Model not found for {symbol}. Please train first.")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        return model, scaler
    
    def model_exists(self, symbol: str) -> bool:
        """Check if model exists for a symbol"""
        model_path = os.path.join(self.model_dir, f"{symbol}_model.pkl")
        scaler_path = os.path.join(self.model_dir, f"{symbol}_scaler.pkl")
        return os.path.exists(model_path) and os.path.exists(scaler_path)
