import numpy as np
from typing import Dict, Any, Tuple
from data_fetcher import DataFetcher
from model_trainer import ModelTrainer

class Predictor:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.model_trainer = ModelTrainer()
    
    def predict_next_day(self, symbol: str) -> Dict[str, Any]:
        """Predict next day closing price for a symbol"""
        # Check if model exists, if not train it
        if not self.model_trainer.model_exists(symbol):
            print(f"Model not found for {symbol}, training new model...")
            historical_data = self.data_fetcher.get_historical_data(symbol, days=90)
            train_result = self.model_trainer.train_model(symbol, historical_data)
            print(f"Model trained: {train_result}")
        
        # Load model and scaler
        model, scaler = self.model_trainer.load_model(symbol)
        
        # Get recent data for prediction
        historical_data = self.data_fetcher.get_historical_data(symbol, days=30)
        close_prices = historical_data['close']
        
        # Prepare current features
        sma_5 = self.model_trainer.calculate_sma(close_prices, 5)
        sma_10 = self.model_trainer.calculate_sma(close_prices, 10)
        rsi_14 = self.model_trainer.calculate_rsi(close_prices, 14)
        
        # Create feature vector for latest data
        current_features = np.array([[
            close_prices[-1],  # Current close
            sma_5[-1],         # SMA 5
            sma_10[-1],        # SMA 10
            rsi_14[-1],        # RSI 14
        ]])
        
        # Scale and predict
        current_features_scaled = scaler.transform(current_features)
        predicted_price = model.predict(current_features_scaled)[0]
        
        # Get current quote
        current_quote = self.data_fetcher.get_quote(symbol)
        current_price = current_quote['price']
        
        return {
            "symbol": symbol,
            "current_price": float(current_price),
            "predicted_price": float(predicted_price),
            "prediction_change": float(predicted_price - current_price),
            "prediction_change_percent": float((predicted_price - current_price) / current_price * 100),
            "features": {
                "sma_5": float(sma_5[-1]),
                "sma_10": float(sma_10[-1]),
                "rsi_14": float(rsi_14[-1])
            }
        }
    
    def generate_signal(self, symbol: str, portfolio_type: str = "balanced") -> Dict[str, Any]:
        """Generate buy/sell/hold signal with reasoning"""
        prediction = self.predict_next_day(symbol)
        
        current_price = prediction['current_price']
        predicted_price = prediction['predicted_price']
        change_percent = prediction['prediction_change_percent']
        rsi = prediction['features']['rsi_14']
        
        # Adjust thresholds based on portfolio type
        if portfolio_type == "aggressive":
            buy_threshold = 1.0  # 1% gain
            sell_threshold = -1.0  # 1% loss
        elif portfolio_type == "long_term":
            buy_threshold = 3.0  # 3% gain
            sell_threshold = -3.0  # 3% loss
        else:  # balanced
            buy_threshold = 2.0  # 2% gain
            sell_threshold = -2.0  # 2% loss
        
        # Generate signal
        signal = "HOLD"
        reason = ""
        confidence = "MEDIUM"
        timing = "Consider monitoring"
        
        if change_percent >= buy_threshold:
            signal = "BUY"
            confidence = "HIGH" if change_percent > buy_threshold * 1.5 else "MEDIUM"
            reason = f"Forecast shows {change_percent:.2f}% upward movement. "
            
            if rsi < 30:
                reason += "RSI indicates oversold conditions - good entry point."
                timing = "Consider buying soon"
            elif rsi < 50:
                reason += "RSI shows neutral momentum with upside potential."
                timing = "Good time to accumulate"
            else:
                reason += "Strong bullish momentum expected."
                timing = "Consider entering position"
        
        elif change_percent <= sell_threshold:
            signal = "SELL"
            confidence = "HIGH" if change_percent < sell_threshold * 1.5 else "MEDIUM"
            reason = f"Forecast shows {abs(change_percent):.2f}% downward movement. "
            
            if rsi > 70:
                reason += "RSI indicates overbought conditions - consider taking profits."
                timing = "Consider selling soon"
            elif rsi > 50:
                reason += "RSI shows weakening momentum."
                timing = "Consider reducing position"
            else:
                reason += "Bearish pressure expected."
                timing = "Consider exiting position"
        
        else:
            signal = "HOLD"
            reason = f"Forecast shows {abs(change_percent):.2f}% movement - within tolerance range. "
            
            if rsi > 70:
                reason += "RSI overbought - wait for better entry."
                timing = "Wait for pullback"
            elif rsi < 30:
                reason += "RSI oversold - watch for reversal signal."
                timing = "Watch for entry opportunity"
            else:
                reason += "Market showing consolidation pattern."
                timing = "Continue monitoring"
        
        return {
            "symbol": symbol,
            "signal": signal,
            "confidence": confidence,
            "reason": reason,
            "timing": timing,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "change_percent": change_percent,
            "portfolio_type": portfolio_type,
            "technical_indicators": {
                "rsi_14": rsi,
                "sma_5": prediction['features']['sma_5'],
                "sma_10": prediction['features']['sma_10']
            }
        }
    
    def get_chart_data(self, symbol: str) -> Dict[str, Any]:
        """Get historical + predicted data for charting"""
        # Get historical data
        historical_data = self.data_fetcher.get_historical_data(symbol, days=30)
        
        # Get prediction
        prediction = self.predict_next_day(symbol)
        
        # Prepare chart data
        dates = historical_data['dates']
        close_prices = historical_data['close']
        
        # Add predicted point
        from datetime import datetime, timedelta
        last_date = datetime.strptime(dates[-1], "%Y-%m-%d")
        next_date = last_date + timedelta(days=1)
        
        # Skip weekends for next trading day
        while next_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            next_date += timedelta(days=1)
        
        prediction_date = next_date.strftime("%Y-%m-%d")
        
        return {
            "symbol": symbol,
            "historical": {
                "dates": dates,
                "prices": close_prices
            },
            "prediction": {
                "date": prediction_date,
                "price": prediction['predicted_price']
            },
            "current_price": prediction['current_price']
        }
