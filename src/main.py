"""
Main entry point for the Stock Price Prediction Tool.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.stock_agent import StockPredictionAgent
from dotenv import load_dotenv

load_dotenv()


def main():
    """Main CLI interface for the stock prediction tool."""
    
    print("🚀 Stock Price Prediction Tool with LangChain")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        print("Copy .env.example to .env and add your API keys")
        return
    
    try:
        # Initialize the agent
        print("🔧 Initializing AI agent...")
        agent = StockPredictionAgent()
        print("✅ Agent ready!")
        print()
        
        print("Available commands:")
        print("  - Type a stock symbol (e.g., 'AAPL') for comprehensive analysis")
        print("  - Ask questions like 'Compare AAPL and GOOGL'")
        print("  - Type 'market' for market overview")
        print("  - Type 'help' for more options")
        print("  - Type 'quit' to exit")
        print()
        
        while True:
            user_input = input("📈 Stock Analysis > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using the Stock Prediction Tool!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if user_input.lower() == 'market':
                print("🔍 Analyzing market conditions...")
                response = agent.get_market_sentiment()
                print("\n" + "="*60)
                print(response)
                print("="*60 + "\n")
                continue
            
            # Check if it's a simple stock symbol
            if user_input.upper().replace('.', '').replace('-', '').isalnum() and len(user_input) <= 6:
                print(f"🔍 Performing comprehensive analysis of {user_input.upper()}...")
                response = agent.analyze_stock(user_input.upper())
            else:
                print("🤖 Processing your request...")
                response = agent.chat(user_input)
            
            print("\n" + "="*60)
            print(response)
            print("="*60 + "\n")
    
    except KeyboardInterrupt:
        print("\n👋 Thanks for using the Stock Prediction Tool!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your configuration and try again.")


def print_help():
    """Print help information."""
    help_text = """
📚 Stock Prediction Tool - Help

BASIC USAGE:
  AAPL                    - Comprehensive analysis of Apple stock
  GOOGL                   - Comprehensive analysis of Google stock
  market                  - Current market overview and sentiment

ANALYSIS COMMANDS:
  "Analyze TSLA"          - Detailed analysis of Tesla
  "Compare AAPL vs MSFT"  - Compare two stocks
  "What's the outlook for tech stocks?"
  "Should I buy NVDA?"    - Get trading recommendation
  
PREDICTION COMMANDS:
  "Predict AAPL for next 5 days"  - ML forecasting
  "TSLA price target"              - Price predictions
  
PORTFOLIO COMMANDS:
  "Analyze portfolio: AAPL, MSFT, GOOGL"  - Portfolio analysis
  "Best tech stocks to buy"               - Sector recommendations

MARKET ANALYSIS:
  "How's the market today?"       - Market sentiment
  "VIX analysis"                  - Volatility assessment
  "S&P 500 outlook"              - Index analysis

OTHER:
  help                    - Show this help
  quit/exit/q            - Exit the program

TIPS:
- Be specific in your questions for better analysis
- The AI will gather current data before analyzing
- All analysis is for informational purposes only
- Consider multiple timeframes and risk factors
    """
    print(help_text)


if __name__ == "__main__":
    main()