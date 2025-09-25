"""
Basic example: Stock data collection and analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.stock_collector import StockDataCollector
from data.technical_analysis import TechnicalAnalyzer


def main():
    """Basic example of using the stock data collection features."""
    
    print("🚀 Stock Data Collection Example")
    print("=" * 40)
    
    # Initialize components
    collector = StockDataCollector()
    analyzer = TechnicalAnalyzer()
    
    # Get stock data
    symbol = "AAPL"
    print(f"📊 Fetching data for {symbol}...")
    
    df = collector.get_yahoo_data(symbol, period="6mo")
    
    if df.empty:
        print(f"❌ Could not fetch data for {symbol}")
        return
    
    print(f"✅ Retrieved {len(df)} data points")
    print(f"📅 Date range: {df['Date'].iloc[0]} to {df['Date'].iloc[-1]}")
    
    # Display basic info
    latest = df.iloc[-1]
    print(f"\n📈 Latest Data for {symbol}:")
    print(f"  Date: {latest['Date']}")
    print(f"  Close: ${latest['Close']:.2f}")
    print(f"  Volume: {latest['Volume']:,}")
    
    # Get company info
    print(f"\n🏢 Company Information:")
    info = collector.get_stock_info(symbol)
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Add technical indicators
    print(f"\n🔧 Adding technical indicators...")
    df_with_indicators = analyzer.add_all_indicators(df)
    
    # Show latest technical indicators
    latest_with_indicators = df_with_indicators.iloc[-1]
    print(f"\n📊 Technical Indicators for {symbol}:")
    
    if 'RSI' in df_with_indicators.columns:
        print(f"  RSI: {latest_with_indicators['RSI']:.2f}")
    
    if 'MACD' in df_with_indicators.columns:
        print(f"  MACD: {latest_with_indicators['MACD']:.4f}")
    
    if 'SMA_20' in df_with_indicators.columns:
        print(f"  SMA 20: ${latest_with_indicators['SMA_20']:.2f}")
    
    if 'SMA_50' in df_with_indicators.columns:
        print(f"  SMA 50: ${latest_with_indicators['SMA_50']:.2f}")
    
    # Get trading signals
    print(f"\n🎯 Trading Signals:")
    signals = analyzer.get_trading_signals(df_with_indicators)
    for indicator, signal in signals.items():
        print(f"  {indicator}: {signal}")
    
    # Get support and resistance
    support, resistance = analyzer.calculate_support_resistance(df_with_indicators)
    print(f"\n📊 Support/Resistance Levels:")
    print(f"  Support: ${support:.2f}")
    print(f"  Resistance: ${resistance:.2f}")
    
    print(f"\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()