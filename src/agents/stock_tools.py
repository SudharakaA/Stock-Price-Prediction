"""
LangChain tools for stock data analysis.
"""

from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, Dict, Any
import json
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.stock_collector import StockDataCollector
from data.technical_analysis import TechnicalAnalyzer


class StockDataInput(BaseModel):
    """Input for stock data tool."""
    symbol: str = Field(description="Stock symbol (e.g., AAPL, GOOGL, TSLA)")
    period: str = Field(default="1y", description="Time period for data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)")


class StockInfoInput(BaseModel):
    """Input for stock info tool."""
    symbol: str = Field(description="Stock symbol (e.g., AAPL, GOOGL, TSLA)")


class TechnicalAnalysisInput(BaseModel):
    """Input for technical analysis tool."""
    symbol: str = Field(description="Stock symbol (e.g., AAPL, GOOGL, TSLA)")
    period: str = Field(default="6mo", description="Time period for analysis")


class StockTools:
    """Collection of stock analysis tools for LangChain agents."""
    
    def __init__(self):
        self.data_collector = StockDataCollector()
        self.technical_analyzer = TechnicalAnalyzer()
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> str:
        """
        Get historical stock data for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Time period
            
        Returns:
            JSON string with stock data summary
        """
        try:
            df = self.data_collector.get_yahoo_data(symbol, period)
            
            if df.empty:
                return f"Could not retrieve data for {symbol}"
            
            # Get recent data summary
            recent_data = df.tail(5)
            current_price = recent_data['Close'].iloc[-1]
            price_change = current_price - recent_data['Close'].iloc[-2]
            price_change_pct = (price_change / recent_data['Close'].iloc[-2]) * 100
            
            volume_avg = df['Volume'].tail(20).mean()
            high_52w = df['High'].max()
            low_52w = df['Low'].min()
            
            summary = {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_pct, 2),
                "volume_avg_20d": int(volume_avg),
                "52_week_high": round(high_52w, 2),
                "52_week_low": round(low_52w, 2),
                "data_points": len(df),
                "date_range": f"{df['Date'].iloc[0].strftime('%Y-%m-%d')} to {df['Date'].iloc[-1].strftime('%Y-%m-%d')}"
            }
            
            return json.dumps(summary, indent=2)
            
        except Exception as e:
            return f"Error retrieving stock data for {symbol}: {str(e)}"
    
    def get_stock_info(self, symbol: str) -> str:
        """
        Get basic information about a stock.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            JSON string with stock information
        """
        try:
            info = self.data_collector.get_stock_info(symbol)
            financial_data = self.data_collector.get_financial_data(symbol)
            
            combined_info = {**info, **financial_data}
            
            if not combined_info:
                return f"Could not retrieve information for {symbol}"
            
            return json.dumps(combined_info, indent=2)
            
        except Exception as e:
            return f"Error retrieving stock info for {symbol}: {str(e)}"
    
    def get_technical_analysis(self, symbol: str, period: str = "6mo") -> str:
        """
        Perform technical analysis on a stock.
        
        Args:
            symbol: Stock symbol
            period: Time period for analysis
            
        Returns:
            JSON string with technical analysis results
        """
        try:
            df = self.data_collector.get_yahoo_data(symbol, period)
            
            if df.empty:
                return f"Could not retrieve data for {symbol}"
            
            # Add technical indicators
            df_with_indicators = self.technical_analyzer.add_all_indicators(df)
            
            # Get trading signals
            signals = self.technical_analyzer.get_trading_signals(df_with_indicators)
            
            # Get support and resistance
            support, resistance = self.technical_analyzer.calculate_support_resistance(df)
            
            # Get latest values
            latest = df_with_indicators.iloc[-1]
            
            analysis = {
                "symbol": symbol,
                "analysis_date": latest['Date'].strftime('%Y-%m-%d'),
                "current_price": round(latest['Close'], 2),
                "technical_indicators": {
                    "RSI": round(latest.get('RSI', 0), 2),
                    "MACD": round(latest.get('MACD', 0), 4),
                    "MACD_Signal": round(latest.get('MACD_Signal', 0), 4),
                    "SMA_20": round(latest.get('SMA_20', 0), 2),
                    "SMA_50": round(latest.get('SMA_50', 0), 2),
                    "SMA_200": round(latest.get('SMA_200', 0), 2),
                    "BB_Upper": round(latest.get('BB_Upper', 0), 2),
                    "BB_Lower": round(latest.get('BB_Lower', 0), 2)
                },
                "trading_signals": signals,
                "support_level": round(support, 2) if support else None,
                "resistance_level": round(resistance, 2) if resistance else None
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            return f"Error performing technical analysis for {symbol}: {str(e)}"
    
    def get_market_overview(self) -> str:
        """
        Get overview of major market indices.
        
        Returns:
            JSON string with market overview
        """
        try:
            indices_data = self.data_collector.get_market_indices()
            
            overview = {}
            for name, df in indices_data.items():
                if not df.empty:
                    latest = df.iloc[-1]
                    previous = df.iloc[-2] if len(df) > 1 else latest
                    
                    change = latest['Close'] - previous['Close']
                    change_pct = (change / previous['Close']) * 100
                    
                    overview[name] = {
                        "current_value": round(latest['Close'], 2),
                        "change": round(change, 2),
                        "change_percent": round(change_pct, 2),
                        "volume": int(latest.get('Volume', 0))
                    }
            
            return json.dumps({"market_overview": overview}, indent=2)
            
        except Exception as e:
            return f"Error retrieving market overview: {str(e)}"
    
    def create_tools(self) -> list:
        """
        Create LangChain tools for stock analysis.
        
        Returns:
            List of LangChain tools
        """
        return [
            Tool(
                name="get_stock_data",
                description="Get historical stock data and current price information for a stock symbol. Input should be a stock symbol like AAPL, GOOGL, TSLA.",
                func=lambda symbol: self.get_stock_data(symbol)
            ),
            Tool(
                name="get_stock_info",
                description="Get detailed company information including financial metrics for a stock symbol. Input should be a stock symbol like AAPL, GOOGL, TSLA.",
                func=lambda symbol: self.get_stock_info(symbol)
            ),
            Tool(
                name="get_technical_analysis",
                description="Perform technical analysis including RSI, MACD, moving averages, and trading signals for a stock symbol. Input should be a stock symbol like AAPL, GOOGL, TSLA.",
                func=lambda symbol: self.get_technical_analysis(symbol)
            ),
            Tool(
                name="get_market_overview",
                description="Get current overview of major market indices (S&P 500, NASDAQ, Dow Jones, VIX). No input required.",
                func=lambda _: self.get_market_overview()
            )
        ]