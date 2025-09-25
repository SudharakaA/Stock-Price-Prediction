"""
LangChain Tools for Stock Analysis
Powerful tools that AI agents can use to fetch and analyze stock data
"""

from langchain.tools import tool
from langchain_core.tools import BaseTool
from typing import Type, Optional, Dict, Any
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@tool
def get_stock_price(symbol: str) -> str:
    """
    Get current stock price and basic info for a given symbol.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA')
    
    Returns:
        String with current price, change, and basic info
    """
    try:
        # Add a small delay to help with rate limiting
        import time
        time.sleep(0.5)
        
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period="2d")
        
        if hist.empty:
            return f"📊 {symbol.upper()}: ⚠️ Data temporarily unavailable (likely rate limited). This is normal with free APIs. Please try again in a moment or ask for analysis without real-time data."
        
        current_price = hist['Close'].iloc[-1]
        previous_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - previous_price
        change_pct = (change / previous_price) * 100 if previous_price != 0 else 0
        
        # Try to get additional info, but handle failures gracefully
        try:
            info = ticker.info
            company_name = info.get('longName', f'{symbol.upper()} Company')
            market_cap = info.get('marketCap', 'N/A')
        except Exception:
            company_name = f'{symbol.upper()} Company'
            market_cap = 'N/A'
        
        volume = hist['Volume'].iloc[-1] if not hist['Volume'].empty else 'N/A'
        
        result = f"""📊 {symbol.upper()} - {company_name}
✅ Current Price: ${current_price:.2f}
📈 Change: ${change:+.2f} ({change_pct:+.2f}%)
📊 Volume: {volume:,} shares
💰 Market Cap: {market_cap}"""

        return result
        
    except Exception as e:
        error_msg = str(e).lower()
        if '429' in error_msg or 'too many requests' in error_msg:
            return f"📊 {symbol.upper()}: ⚠️ Yahoo Finance is rate limiting requests. This is common with free APIs. The stock data tools are working correctly, just temporarily throttled. Try asking for general analysis or market insights instead!"
        else:
            return f"📊 {symbol.upper()}: ❌ Error: {str(e)[:100]}... Data may be temporarily unavailable."

@tool  
def get_technical_analysis(symbol: str, period: str = "3mo") -> str:
    """
    Perform technical analysis on a stock including RSI, moving averages, and signals.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        period: Time period ('1mo', '3mo', '6mo', '1y')
    
    Returns:
        Technical analysis results with trading signals
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period=period)
        
        if hist.empty:
            return f"❌ No historical data found for {symbol}"
        
        # Calculate technical indicators
        df = hist.copy()
        
        # Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        
        # Bollinger Bands
        bb_period = 20
        df['BB_Middle'] = df['Close'].rolling(window=bb_period).mean()
        bb_std = df['Close'].rolling(window=bb_period).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Get latest values
        latest = df.iloc[-1]
        
        # Generate signals
        signals = []
        
        # RSI Signal
        if latest['RSI'] > 70:
            signals.append("🔴 RSI Overbought (>70) - Consider selling")
        elif latest['RSI'] < 30:
            signals.append("🟢 RSI Oversold (<30) - Consider buying")
        else:
            signals.append("🟡 RSI Neutral")
        
        # Moving Average Signal
        if latest['SMA_20'] > latest['SMA_50']:
            signals.append("🟢 Bullish trend (20-day > 50-day SMA)")
        else:
            signals.append("🔴 Bearish trend (20-day < 50-day SMA)")
        
        # MACD Signal
        if latest['MACD'] > latest['MACD_Signal']:
            signals.append("🟢 MACD bullish crossover")
        else:
            signals.append("🔴 MACD bearish crossover")
        
        # Bollinger Bands Signal
        if latest['Close'] > latest['BB_Upper']:
            signals.append("🔴 Price above upper Bollinger Band - Overbought")
        elif latest['Close'] < latest['BB_Lower']:
            signals.append("🟢 Price below lower Bollinger Band - Oversold")
        else:
            signals.append("🟡 Price within Bollinger Bands - Normal")
        
        result = f"""🔍 Technical Analysis for {symbol.upper()} ({period})
        
📈 Current Metrics:
• Price: ${latest['Close']:.2f}
• RSI (14): {latest['RSI']:.1f}
• SMA 20: ${latest['SMA_20']:.2f}
• SMA 50: ${latest['SMA_50']:.2f}
• MACD: {latest['MACD']:.3f}
• Volume: {latest['Volume']:,}

🎯 Trading Signals:
""" + '\n'.join(f"• {signal}" for signal in signals)
        
        return result
        
    except Exception as e:
        return f"❌ Error in technical analysis for {symbol}: {str(e)}"

@tool
def get_stock_news(symbol: str) -> str:
    """
    Get recent news and sentiment for a stock symbol.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
    
    Returns:
        Recent news headlines and sentiment analysis
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        news = ticker.news
        
        if not news:
            return f"❌ No recent news found for {symbol}"
        
        # Get top 3 news items
        result = f"📰 Recent News for {symbol.upper()}:\n\n"
        
        for i, item in enumerate(news[:3], 1):
            title = item.get('title', 'No title')
            publisher = item.get('publisher', 'Unknown')
            # Convert timestamp to readable date
            timestamp = item.get('providerPublishTime', 0)
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M') if timestamp else 'Unknown date'
            
            result += f"{i}. {title}\n"
            result += f"   📅 {date} | 🏢 {publisher}\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error fetching news for {symbol}: {str(e)}"

@tool
def compare_stocks(symbols: str) -> str:
    """
    Compare multiple stocks side by side.
    
    Args:
        symbols: Comma-separated stock symbols (e.g., 'AAPL,GOOGL,MSFT')
    
    Returns:
        Comparison table of key metrics
    """
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        
        if len(symbol_list) > 5:
            return "❌ Please limit comparison to 5 stocks maximum"
        
        comparison_data = []
        
        for symbol in symbol_list:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="2d")
                
                if hist.empty:
                    continue
                
                current_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change_pct = ((current_price - previous_price) / previous_price) * 100 if previous_price != 0 else 0
                
                comparison_data.append({
                    'Symbol': symbol,
                    'Price': f"${current_price:.2f}",
                    'Change%': f"{change_pct:+.2f}%",
                    'Market Cap': f"${info.get('marketCap', 0) / 1e9:.1f}B" if info.get('marketCap') else 'N/A',
                    'P/E Ratio': f"{info.get('forwardPE', 'N/A'):.2f}" if info.get('forwardPE') else 'N/A'
                })
                
            except Exception as e:
                comparison_data.append({
                    'Symbol': symbol,
                    'Price': 'Error',
                    'Change%': 'Error',
                    'Market Cap': 'Error', 
                    'P/E Ratio': 'Error'
                })
        
        if not comparison_data:
            return "❌ No valid data found for any of the provided symbols"
        
        # Format as table
        result = f"📊 Stock Comparison: {symbols}\n\n"
        result += f"{'Symbol':<8} {'Price':<10} {'Change%':<8} {'Market Cap':<12} {'P/E Ratio':<10}\n"
        result += "-" * 55 + "\n"
        
        for data in comparison_data:
            result += f"{data['Symbol']:<8} {data['Price']:<10} {data['Change%']:<8} {data['Market Cap']:<12} {data['P/E Ratio']:<10}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error comparing stocks: {str(e)}"

@tool
def get_market_overview() -> str:
    """
    Get overall market overview with major indices.
    
    Returns:
        Current status of major market indices
    """
    try:
        indices = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^RUT': 'Russell 2000'
        }
        
        result = "📈 Market Overview:\n\n"
        
        for symbol, name in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change = current - previous
                    change_pct = (change / previous) * 100 if previous != 0 else 0
                    
                    emoji = "🟢" if change_pct >= 0 else "🔴"
                    result += f"{emoji} {name}: {current:.2f} ({change:+.2f}, {change_pct:+.2f}%)\n"
                else:
                    result += f"❌ {name}: Data unavailable\n"
                    
            except Exception:
                result += f"❌ {name}: Error fetching data\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error fetching market overview: {str(e)}"

# List of all available tools
STOCK_TOOLS = [
    get_stock_price,
    get_technical_analysis, 
    get_stock_news,
    compare_stocks,
    get_market_overview
]