"""
Model prediction tools for LangChain integration.
"""

from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
import sys
import os
import json
import pandas as pd
from typing import Optional, Dict, Any

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.stock_collector import StockDataCollector
from .lstm_model import LSTMPredictor
from .prophet_model import ProphetPredictor


class PredictionInput(BaseModel):
    """Input for prediction tools."""
    symbol: str = Field(description="Stock symbol (e.g., AAPL, GOOGL, TSLA)")
    days_ahead: int = Field(default=5, description="Number of days to predict ahead")
    model_type: str = Field(default="prophet", description="Model type: 'prophet' or 'lstm'")


class ModelPredictionTools:
    """Collection of machine learning prediction tools for LangChain agents."""
    
    def __init__(self):
        self.data_collector = StockDataCollector()
        self.lstm_models = {}  # Cache for trained LSTM models
        self.prophet_models = {}  # Cache for trained Prophet models
        
    def train_and_predict_prophet(self, symbol: str, days_ahead: int = 5) -> str:
        """
        Train a Prophet model and make predictions.
        
        Args:
            symbol: Stock symbol
            days_ahead: Number of days to predict
            
        Returns:
            JSON string with prediction results
        """
        try:
            # Get historical data (2 years for better training)
            df = self.data_collector.get_yahoo_data(symbol, period="2y")
            
            if df.empty:
                return f"Could not retrieve data for {symbol}"
            
            # Check if model is already trained for this symbol
            if symbol not in self.prophet_models:
                # Train new model
                predictor = ProphetPredictor()
                predictor.train(df, target_column='Close')
                self.prophet_models[symbol] = predictor
            else:
                predictor = self.prophet_models[symbol]
            
            # Make predictions
            forecast = predictor.predict(df, days_ahead=days_ahead)
            
            # Extract relevant forecast information
            future_forecast = forecast.tail(days_ahead)
            current_price = df['Close'].iloc[-1]
            
            predictions = []
            for _, row in future_forecast.iterrows():
                pred_date = row['ds'].strftime('%Y-%m-%d')
                pred_price = round(row['yhat'], 2)
                lower_bound = round(row['yhat_lower'], 2)
                upper_bound = round(row['yhat_upper'], 2)
                
                predictions.append({
                    'date': pred_date,
                    'predicted_price': pred_price,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'confidence_interval': f"{lower_bound} - {upper_bound}"
                })
            
            # Calculate trend
            first_pred = predictions[0]['predicted_price']
            last_pred = predictions[-1]['predicted_price']
            trend_direction = "Upward" if last_pred > first_pred else "Downward"
            trend_magnitude = round(((last_pred - first_pred) / first_pred) * 100, 2)
            
            result = {
                'symbol': symbol,
                'model_type': 'Prophet',
                'current_price': round(current_price, 2),
                'prediction_period': f"{days_ahead} days",
                'predictions': predictions,
                'trend_analysis': {
                    'direction': trend_direction,
                    'magnitude_percent': trend_magnitude
                },
                'model_info': 'Prophet is good for capturing seasonality and trends in time series data'
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error in Prophet prediction for {symbol}: {str(e)}"
    
    def train_and_predict_lstm(self, symbol: str, days_ahead: int = 5) -> str:
        """
        Train an LSTM model and make predictions.
        
        Args:
            symbol: Stock symbol
            days_ahead: Number of days to predict
            
        Returns:
            JSON string with prediction results
        """
        try:
            # Get historical data
            df = self.data_collector.get_yahoo_data(symbol, period="2y")
            
            if df.empty:
                return f"Could not retrieve data for {symbol}"
            
            if len(df) < 100:
                return f"Insufficient data for LSTM training for {symbol} (need at least 100 data points)"
            
            # Check if model is already trained for this symbol
            if symbol not in self.lstm_models:
                # Train new LSTM model
                predictor = LSTMPredictor(sequence_length=60)
                
                # Use 80% of data for training
                train_size = int(len(df) * 0.8)
                train_df = df[:train_size]
                
                # Train the model with fewer epochs for faster execution
                predictor.train(train_df, epochs=20, batch_size=32)
                self.lstm_models[symbol] = predictor
            else:
                predictor = self.lstm_models[symbol]
            
            # Make predictions
            predictions_array = predictor.predict(df, days_ahead=days_ahead)
            current_price = df['Close'].iloc[-1]
            
            # Create prediction results
            predictions = []
            last_date = pd.to_datetime(df['Date'].iloc[-1])
            
            for i, pred_price in enumerate(predictions_array):
                pred_date = (last_date + pd.Timedelta(days=i+1)).strftime('%Y-%m-%d')
                predictions.append({
                    'date': pred_date,
                    'predicted_price': round(float(pred_price), 2)
                })
            
            # Calculate trend
            first_pred = predictions[0]['predicted_price']
            last_pred = predictions[-1]['predicted_price']
            trend_direction = "Upward" if last_pred > first_pred else "Downward"
            trend_magnitude = round(((last_pred - first_pred) / first_pred) * 100, 2)
            
            result = {
                'symbol': symbol,
                'model_type': 'LSTM',
                'current_price': round(current_price, 2),
                'prediction_period': f"{days_ahead} days",
                'predictions': predictions,
                'trend_analysis': {
                    'direction': trend_direction,
                    'magnitude_percent': trend_magnitude
                },
                'model_info': 'LSTM is good for capturing sequential patterns and complex non-linear relationships'
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error in LSTM prediction for {symbol}: {str(e)}"
    
    def compare_predictions(self, symbol: str, days_ahead: int = 5) -> str:
        """
        Compare predictions from both Prophet and LSTM models.
        
        Args:
            symbol: Stock symbol
            days_ahead: Number of days to predict
            
        Returns:
            JSON string with comparison results
        """
        try:
            # Get predictions from both models
            prophet_result = self.train_and_predict_prophet(symbol, days_ahead)
            lstm_result = self.train_and_predict_lstm(symbol, days_ahead)
            
            # Parse results
            try:
                prophet_data = json.loads(prophet_result)
                lstm_data = json.loads(lstm_result)
            except json.JSONDecodeError:
                return f"Error parsing model results for {symbol}"
            
            # Extract final predictions for comparison
            prophet_final = prophet_data['predictions'][-1]['predicted_price']
            lstm_final = lstm_data['predictions'][-1]['predicted_price']
            current_price = prophet_data['current_price']
            
            # Calculate differences
            prophet_change = ((prophet_final - current_price) / current_price) * 100
            lstm_change = ((lstm_final - current_price) / current_price) * 100
            
            comparison = {
                'symbol': symbol,
                'comparison_period': f"{days_ahead} days",
                'current_price': current_price,
                'prophet_prediction': {
                    'final_price': prophet_final,
                    'change_percent': round(prophet_change, 2),
                    'trend': prophet_data['trend_analysis']['direction']
                },
                'lstm_prediction': {
                    'final_price': lstm_final,
                    'change_percent': round(lstm_change, 2),
                    'trend': lstm_data['trend_analysis']['direction']
                },
                'model_agreement': {
                    'same_direction': (prophet_change > 0) == (lstm_change > 0),
                    'average_prediction': round((prophet_final + lstm_final) / 2, 2),
                    'prediction_spread': round(abs(prophet_final - lstm_final), 2)
                },
                'interpretation': {
                    'prophet_strength': 'Better for trend and seasonality detection',
                    'lstm_strength': 'Better for complex pattern recognition',
                    'confidence_note': 'Higher agreement between models suggests higher confidence'
                }
            }
            
            return json.dumps(comparison, indent=2)
            
        except Exception as e:
            return f"Error comparing predictions for {symbol}: {str(e)}"
    
    def create_tools(self) -> list:
        """
        Create LangChain tools for ML predictions.
        
        Returns:
            List of LangChain tools
        """
        return [
            Tool(
                name="predict_with_prophet",
                description="Use Prophet model to predict stock prices for the next few days. Good for trend and seasonality analysis. Input should be a stock symbol like AAPL.",
                func=lambda symbol: self.train_and_predict_prophet(symbol, 5)
            ),
            Tool(
                name="predict_with_lstm",
                description="Use LSTM neural network to predict stock prices for the next few days. Good for complex pattern recognition. Input should be a stock symbol like AAPL.",
                func=lambda symbol: self.train_and_predict_lstm(symbol, 5)
            ),
            Tool(
                name="compare_ml_predictions",
                description="Compare predictions from both Prophet and LSTM models to get a comprehensive forecast. Input should be a stock symbol like AAPL.",
                func=lambda symbol: self.compare_predictions(symbol, 5)
            )
        ]