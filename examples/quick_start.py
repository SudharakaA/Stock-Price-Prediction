"""
Quick start guide and usage examples for the Stock Price Prediction Tool
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.stock_collector import StockDataCollector
from data.technical_analysis import TechnicalAnalyzer


def quick_start():
    """Quick start example - minimal code to get started."""
    
    print("🚀 Quick Start Guide")
    print("=" * 20)
    
    # 1. Get stock data
    collector = StockDataCollector()
    df = collector.get_yahoo_data("AAPL", period="1mo")
    
    print(f"📊 Latest AAPL price: ${df['Close'].iloc[-1]:.2f}")
    
    # 2. Add technical indicators
    analyzer = TechnicalAnalyzer()
    df_with_indicators = analyzer.add_all_indicators(df)
    
    # 3. Get trading signals
    signals = analyzer.get_trading_signals(df_with_indicators)
    print(f"🎯 RSI Signal: {signals.get('RSI', 'N/A')}")
    
    print("✅ Quick start completed!\n")


def data_collection_guide():
    """Guide for data collection features."""
    
    print("📊 Data Collection Guide")
    print("=" * 25)
    
    collector = StockDataCollector()
    
    # Basic stock data
    print("1. Basic Stock Data:")
    df = collector.get_yahoo_data("TSLA", period="1mo")
    print(f"   - Retrieved {len(df)} days of TSLA data")
    
    # Company information
    print("2. Company Information:")
    info = collector.get_stock_info("TSLA")
    print(f"   - Company: {info.get('name', 'N/A')}")
    print(f"   - Sector: {info.get('sector', 'N/A')}")
    
    # Financial metrics
    print("3. Financial Metrics:")
    financials = collector.get_financial_data("TSLA")
    print(f"   - P/E Ratio: {financials.get('pe_ratio', 'N/A')}")
    print(f"   - Profit Margin: {financials.get('profit_margin', 'N/A')}")
    
    # Multiple stocks
    print("4. Multiple Stocks:")
    data = collector.get_multiple_stocks(["AAPL", "MSFT", "GOOGL"], period="1mo")
    print(f"   - Retrieved data for {len(data)} stocks")
    
    # Market indices
    print("5. Market Indices:")
    indices = collector.get_market_indices()
    print(f"   - Retrieved {len(indices)} market indices")
    
    print("✅ Data collection guide completed!\n")


def technical_analysis_guide():
    """Guide for technical analysis features."""
    
    print("📈 Technical Analysis Guide")
    print("=" * 28)
    
    # Get some data
    collector = StockDataCollector()
    df = collector.get_yahoo_data("NVDA", period="6mo")
    
    analyzer = TechnicalAnalyzer()
    
    print("1. Moving Averages:")
    df_ma = analyzer.add_moving_averages(df)
    latest = df_ma.iloc[-1]
    print(f"   - SMA 20: ${latest.get('SMA_20', 0):.2f}")
    print(f"   - SMA 50: ${latest.get('SMA_50', 0):.2f}")
    
    print("2. RSI Indicator:")
    df_rsi = analyzer.add_rsi(df)
    latest_rsi = df_rsi.iloc[-1]
    print(f"   - RSI: {latest_rsi.get('RSI', 0):.2f}")
    
    print("3. MACD Indicator:")
    df_macd = analyzer.add_macd(df)
    latest_macd = df_macd.iloc[-1]
    print(f"   - MACD: {latest_macd.get('MACD', 0):.4f}")
    
    print("4. Bollinger Bands:")
    df_bb = analyzer.add_bollinger_bands(df)
    latest_bb = df_bb.iloc[-1]
    print(f"   - Upper Band: ${latest_bb.get('BB_Upper', 0):.2f}")
    print(f"   - Lower Band: ${latest_bb.get('BB_Lower', 0):.2f}")
    
    print("5. All Indicators at Once:")
    df_all = analyzer.add_all_indicators(df)
    print(f"   - Added {len(df_all.columns) - len(df.columns)} indicators")
    
    print("6. Trading Signals:")
    signals = analyzer.get_trading_signals(df_all)
    for indicator, signal in signals.items():
        print(f"   - {indicator}: {signal}")
    
    print("7. Support/Resistance:")
    support, resistance = analyzer.calculate_support_resistance(df)
    print(f"   - Support: ${support:.2f}")
    print(f"   - Resistance: ${resistance:.2f}")
    
    print("✅ Technical analysis guide completed!\n")


def common_patterns():
    """Show common usage patterns."""
    
    print("🔧 Common Usage Patterns")
    print("=" * 25)
    
    collector = StockDataCollector()
    analyzer = TechnicalAnalyzer()
    
    print("Pattern 1: Daily Stock Check")
    print("-" * 25)
    
    symbol = "AMZN"
    df = collector.get_yahoo_data(symbol, period="1mo")
    df_indicators = analyzer.add_all_indicators(df)
    signals = analyzer.get_trading_signals(df_indicators)
    
    latest = df_indicators.iloc[-1]
    print(f"Stock: {symbol}")
    print(f"Price: ${latest['Close']:.2f}")
    print(f"RSI: {latest.get('RSI', 0):.1f}")
    print(f"Signal: {signals.get('RSI', 'N/A')}")
    
    print("\nPattern 2: Multi-Stock Screening")
    print("-" * 30)
    
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    for symbol in symbols:
        df = collector.get_yahoo_data(symbol, period="1mo")
        if not df.empty:
            price = df['Close'].iloc[-1]
            change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            print(f"{symbol}: ${price:.2f} ({change:+.2f}%)")
    
    print("\nPattern 3: Risk Assessment")
    print("-" * 22)
    
    symbol = "META"
    df = collector.get_yahoo_data(symbol, period="3mo")
    
    # Calculate volatility
    returns = df['Close'].pct_change().dropna()
    volatility = returns.std() * (252 ** 0.5)  # Annualized
    
    # Get support/resistance
    support, resistance = analyzer.calculate_support_resistance(df)
    current_price = df['Close'].iloc[-1]
    
    distance_to_support = ((current_price - support) / current_price) * 100
    distance_to_resistance = ((resistance - current_price) / current_price) * 100
    
    print(f"Stock: {symbol}")
    print(f"Volatility: {volatility:.1%}")
    print(f"Distance to Support: {distance_to_support:.1f}%")
    print(f"Distance to Resistance: {distance_to_resistance:.1f}%")
    
    print("✅ Common patterns guide completed!\n")


def main():
    """Run all quick start examples."""
    
    print("📚 Stock Price Prediction Tool - Usage Guide")
    print("=" * 50)
    print()
    
    # Run all guides
    quick_start()
    data_collection_guide()
    technical_analysis_guide()
    common_patterns()
    
    print("🎉 Usage guide completed!")
    print("\n📝 Next Steps:")
    print("1. Set up your .env file with API keys")
    print("2. Try the CLI interface: python src/main.py")
    print("3. Launch the web app: streamlit run src/interface/web_app.py")
    print("4. Explore the LangChain agent examples")
    print("5. Experiment with ML predictions")


if __name__ == "__main__":
    main()