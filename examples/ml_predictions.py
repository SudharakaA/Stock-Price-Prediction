"""
Example: Machine Learning predictions with Prophet and LSTM
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.stock_collector import StockDataCollector
from models.prophet_model import ProphetPredictor
import pandas as pd


def prophet_example():
    """Example using Prophet for stock prediction."""
    
    print("🔮 Prophet Model Example")
    print("=" * 30)
    
    # Get stock data
    collector = StockDataCollector()
    symbol = "AAPL"
    
    print(f"📊 Fetching 2 years of data for {symbol}...")
    df = collector.get_yahoo_data(symbol, period="2y")
    
    if df.empty:
        print(f"❌ Could not fetch data for {symbol}")
        return
    
    print(f"✅ Retrieved {len(df)} data points")
    
    # Initialize and train Prophet model
    print("🔧 Training Prophet model...")
    prophet_model = ProphetPredictor()
    
    # Train the model
    prophet_model.train(df, target_column='Close')
    print("✅ Model trained successfully!")
    
    # Make predictions
    days_ahead = 7
    print(f"🔮 Making {days_ahead}-day predictions...")
    
    forecast = prophet_model.predict(df, days_ahead=days_ahead)
    
    # Display predictions
    future_predictions = forecast.tail(days_ahead)
    
    print(f"\n📈 {symbol} Price Predictions (Next {days_ahead} days):")
    print("-" * 50)
    
    current_price = df['Close'].iloc[-1]
    print(f"Current Price: ${current_price:.2f}")
    print()
    
    for _, row in future_predictions.iterrows():
        date = row['ds'].strftime('%Y-%m-%d')
        predicted_price = row['yhat']
        lower_bound = row['yhat_lower']
        upper_bound = row['yhat_upper']
        
        change_pct = ((predicted_price - current_price) / current_price) * 100
        
        print(f"Date: {date}")
        print(f"  Predicted Price: ${predicted_price:.2f}")
        print(f"  Confidence Range: ${lower_bound:.2f} - ${upper_bound:.2f}")
        print(f"  Change from current: {change_pct:+.2f}%")
        print()
    
    # Analyze trend
    first_pred = future_predictions['yhat'].iloc[0]
    last_pred = future_predictions['yhat'].iloc[-1]
    
    if last_pred > first_pred:
        trend = "📈 Upward"
        trend_pct = ((last_pred - first_pred) / first_pred) * 100
    else:
        trend = "📉 Downward"
        trend_pct = ((first_pred - last_pred) / first_pred) * 100
    
    print(f"🎯 Overall Trend: {trend} ({trend_pct:.2f}%)")
    
    # Get model evaluation
    print("\n📊 Model Evaluation:")
    try:
        metrics = prophet_model.evaluate(df)
        for metric, value in metrics.items():
            print(f"  {metric.upper()}: {value:.4f}")
    except Exception as e:
        print(f"  Evaluation error: {e}")


def main():
    """Main function to run ML examples."""
    
    print("🚀 Machine Learning Prediction Examples")
    print("=" * 50)
    
    # Run Prophet example
    prophet_example()
    
    print("\n" + "="*50)
    print("✅ ML examples completed!")
    
    print("\n📝 Notes:")
    print("- Prophet is good for capturing trends and seasonality")
    print("- LSTM models require more training time but can capture complex patterns")
    print("- Both models work better with more historical data")
    print("- Consider ensemble approaches for better predictions")


if __name__ == "__main__":
    main()