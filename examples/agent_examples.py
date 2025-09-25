"""
Example: Using the LangChain agent for stock analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.stock_agent import StockPredictionAgent
from dotenv import load_dotenv

load_dotenv()


def main():
    """Example of using the LangChain stock prediction agent."""
    
    print("🤖 LangChain Stock Agent Example")
    print("=" * 40)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        return
    
    try:
        # Initialize agent
        print("🔧 Initializing LangChain agent...")
        agent = StockPredictionAgent()
        print("✅ Agent initialized successfully!")
        
        # Example 1: Analyze a single stock
        print("\n📈 Example 1: Single Stock Analysis")
        print("-" * 30)
        
        symbol = "TSLA"
        print(f"Analyzing {symbol}...")
        result = agent.analyze_stock(symbol)
        print(f"\nAnalysis Result:\n{result}")
        
        # Example 2: Compare stocks
        print("\n📊 Example 2: Stock Comparison")
        print("-" * 30)
        
        symbols = ["AAPL", "MSFT", "GOOGL"]
        print(f"Comparing {', '.join(symbols)}...")
        comparison = agent.compare_stocks(symbols)
        print(f"\nComparison Result:\n{comparison}")
        
        # Example 3: Price prediction
        print("\n🔮 Example 3: Price Movement Prediction")
        print("-" * 30)
        
        symbol = "NVDA"
        print(f"Predicting short-term movement for {symbol}...")
        prediction = agent.predict_price_movement(symbol, "short-term")
        print(f"\nPrediction Result:\n{prediction}")
        
        # Example 4: Market sentiment
        print("\n🌍 Example 4: Market Sentiment Analysis")
        print("-" * 30)
        
        print("Analyzing overall market sentiment...")
        sentiment = agent.get_market_sentiment()
        print(f"\nMarket Sentiment:\n{sentiment}")
        
        # Example 5: Trading recommendation
        print("\n💰 Example 5: Trading Recommendation")
        print("-" * 30)
        
        symbol = "AMZN"
        print(f"Getting trading recommendation for {symbol}...")
        recommendation = agent.get_trading_recommendation(symbol, "moderate")
        print(f"\nTrading Recommendation:\n{recommendation}")
        
        # Example 6: Free-form chat
        print("\n💬 Example 6: Free-form Chat")
        print("-" * 30)
        
        questions = [
            "What are the best tech stocks to buy right now?",
            "How is the cryptocurrency market affecting traditional stocks?",
            "Should I be worried about inflation's impact on my portfolio?"
        ]
        
        for question in questions:
            print(f"\nQuestion: {question}")
            answer = agent.chat(question)
            print(f"Answer: {answer}")
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()