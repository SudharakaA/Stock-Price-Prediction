#!/usr/bin/env python3
"""
Stock Price Prediction Tool - Groq Version
A comprehensive stock analysis tool with AI chat powered by Groq (FREE!)
"""

import os
import sys
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def print_banner():
    """Display the welcome banner."""
    print("🚀 Stock Price Prediction Tool - Groq Version")
    print("=" * 55)
    print("🤖 Powered by Groq AI (Free & Fast!)")
    print()

def check_environment():
    """Check if required environment variables are set."""
    print("🔧 Checking environment...")
    
    # Check Groq API key
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key and groq_key != 'your_groq_api_key_here':
        print("   Groq API: ✅ Configured")
        groq_status = True
    else:
        print("   Groq API: ❌ Not configured")
        groq_status = False
    
    # Check Alpha Vantage API key
    av_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if av_key and av_key != 'your_alpha_vantage_api_key_here':
        print("   Alpha Vantage: ✅ Configured")
    else:
        print("   Alpha Vantage: ❌ Not configured")
    
    return groq_status

def test_stock_data():
    """Test stock data collection."""
    print("📊 Testing stock data collection...")
    
    try:
        print("   Attempting to fetch AAPL data...")
        ticker = yf.Ticker("AAPL")
        
        # Try to get recent data with a longer period to avoid rate limits
        hist = ticker.history(period="5d")
        
        if not hist.empty:
            latest_price = hist['Close'].iloc[-1]
            print(f"   ✅ AAPL latest price: ${latest_price:.2f}")
            return True
        else:
            print("   ⚠️  No data returned")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Stock data temporarily unavailable (rate limited)")
        print("   This is normal - Yahoo Finance limits requests")
        return False

def simple_analysis_demo():
    """Run a simple analysis without external APIs."""
    print("\n🔧 Running Simple Analysis Demo...")
    print("=" * 40)
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    # Simulate stock price
    prices = []
    base_price = 150.0
    
    for i in range(len(dates)):
        if i == 0:
            prices.append(base_price)
        else:
            change = np.random.normal(0.001, 0.02)  # Small daily changes
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 1.0))
    
    df = pd.DataFrame({
        'Date': dates,
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    })
    
    # Calculate indicators
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()
    
    # RSI calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Get latest values
    latest = df.iloc[-1]
    
    print(f"📈 Sample Stock Analysis (DEMO-STOCK):")
    print(f"   Current Price: ${latest['Close']:.2f}")
    print(f"   20-day SMA: ${latest['SMA_20']:.2f}")
    print(f"   50-day SMA: ${latest['SMA_50']:.2f}")
    print(f"   RSI: {latest['RSI']:.1f}")
    
    print(f"\n🎯 Trading Signals:")
    if latest['RSI'] > 70:
        print(f"   RSI: Overbought (Consider Selling)")
    elif latest['RSI'] < 30:
        print(f"   RSI: Oversold (Consider Buying)")
    else:
        print(f"   RSI: Neutral")
    
    if latest['SMA_20'] > latest['SMA_50']:
        print(f"   Trend: Bullish (20-day > 50-day SMA)")
    else:
        print(f"   Trend: Bearish (20-day < 50-day SMA)")

def ai_chat_demo():
    """Demonstrate AI chat capabilities using Groq."""
    print("\n🤖 Groq AI Chat Demo...")
    print("=" * 25)
    
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key or groq_key == 'your_groq_api_key_here':
        print("❌ Groq API key not configured")
        print("   📝 To get a free API key:")
        print("   1. Go to: https://console.groq.com")
        print("   2. Sign up for free")
        print("   3. Generate an API key")
        print("   4. Add GROQ_API_KEY=your_key_here to your .env file")
        return False
    
    try:
        # Import and test Groq
        from groq import Groq
        
        print("✅ Groq API key found!")
        print("🔧 Testing Groq connection...")
        
        # Initialize Groq client
        client = Groq(api_key=groq_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Current fast model
            messages=[
                {"role": "user", "content": "Hello! Can you help with stock analysis? Just say yes or no."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        ai_response = response.choices[0].message.content
        print(f"🎉 Groq AI is working! Response: {ai_response}")
        return True
        
    except ImportError as e:
        print(f"❌ Groq package error: {e}")
        print("   Try: pip install groq")
        return False
    except Exception as e:
        print(f"❌ Groq connection error: {e}")
        print("   Check your API key at https://console.groq.com")
        return False

def handle_stock_question(question):
    """Handle stock-related questions using Groq AI."""
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key or groq_key == 'your_groq_api_key_here':
        return "❌ Groq API key needed. Get one free at https://console.groq.com"
    
    try:
        from groq import Groq
        
        # Initialize Groq client
        client = Groq(api_key=groq_key)
        
        # Create a stock analysis prompt
        prompt = f"""You are a professional stock market analyst. Answer this question about stocks or investing: "{question}"

Provide a helpful, informative response. If the question involves specific stock symbols, mention that real-time data would be needed for current analysis.

Keep your response concise but informative (max 150 words)."""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast and free model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except ImportError as e:
        return f"❌ Groq package error. Try: pip install groq"
    except Exception as e:
        return f"❌ Groq error: {str(e)[:100]}..."

def ai_chat_interactive():
    """Interactive AI chat mode with Groq."""
    print("\n💬 Groq AI Chat Mode (type 'back' to return)")
    print("-" * 40)
    
    while True:
        try:
            question = input("💰 Ask about stocks > ").strip()
            
            if question.lower() in ['back', 'exit', 'quit']:
                break
            
            if question:
                print("🤖 Thinking...")
                response = handle_stock_question(question)
                print(f"\n🤖 {response}\n")
        except KeyboardInterrupt:
            print("\n")
            break

def interactive_mode():
    """Run interactive mode for user queries."""
    print("\n💬 Interactive Mode")
    print("=" * 20)
    print("Available commands:")
    print("  'demo' - Run analysis demo")
    print("  'test' - Test stock data connection")
    print("  'ai' - Test Groq AI connection")
    print("  'chat' - Interactive Groq AI chat")
    print("  'help' - Show this help")
    print("  'quit' - Exit")
    print("Or ask stock questions directly!")
    
    while True:
        try:
            user_input = input("\n> ").strip().lower()
            
            if user_input in ['quit', 'exit', 'q']:
                print("👋 Thanks for using the Stock Price Prediction Tool!")
                break
            elif user_input == 'demo':
                simple_analysis_demo()
            elif user_input == 'test':
                test_stock_data()
            elif user_input == 'ai':
                ai_chat_demo()
            elif user_input == 'chat':
                ai_chat_interactive()
            elif user_input in ['help', 'h']:
                print("\nAvailable commands:")
                print("  'demo' - Run analysis demo")
                print("  'test' - Test stock data connection") 
                print("  'ai' - Test Groq AI connection")
                print("  'chat' - Interactive Groq AI chat")
                print("  'help' - Show this help")
                print("  'quit' - Exit")
            elif user_input:
                # Treat as stock question
                print("🤖 Analyzing your question...")
                response = handle_stock_question(user_input)
                print(f"\n🤖 {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Thanks for using the Stock Price Prediction Tool!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function to run the stock prediction tool."""
    print_banner()
    
    # Check environment setup
    groq_available = check_environment()
    
    # Test stock data
    stock_data_available = test_stock_data()
    
    # Test AI capabilities
    if groq_available:
        ai_available = ai_chat_demo()
    else:
        ai_available = False
    
    # Show system status
    print(f"\n📊 System Status:")
    if stock_data_available:
        print(f"   Stock Data: ✅ Available")
    else:
        print(f"   Stock Data: ⚠️  Limited")
    
    if ai_available:
        print(f"   Groq AI: ✅ Ready")
    else:
        print(f"   Groq AI: ❌ Needs Setup")
    
    # Run demo analysis
    simple_analysis_demo()
    
    # Start interactive mode
    print(f"\n🎮 Starting Interactive Mode...")
    interactive_mode()

if __name__ == "__main__":
    main()
