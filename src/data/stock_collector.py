"""
Stock data collection module using multiple data sources.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class StockDataCollector:
    """Collects stock data from multiple sources."""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
    def get_yahoo_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            
        Returns:
            DataFrame with stock data
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            print(f"Error fetching Yahoo data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_alpha_vantage_data(self, symbol: str, outputsize: str = "compact") -> pd.DataFrame:
        """
        Fetch stock data from Alpha Vantage.
        
        Args:
            symbol: Stock symbol
            outputsize: 'compact' (last 100 data points) or 'full' (20+ years)
            
        Returns:
            DataFrame with stock data
        """
        if not self.alpha_vantage_key:
            print("Alpha Vantage API key not found")
            return pd.DataFrame()
            
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': outputsize,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                df = pd.DataFrame(data['Time Series (Daily)']).T
                df.index = pd.to_datetime(df.index)
                df = df.astype(float)
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df.reset_index(inplace=True)
                df.rename(columns={'index': 'Date'}, inplace=True)
                return df.sort_values('Date')
            else:
                print(f"Error in Alpha Vantage response: {data}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error fetching Alpha Vantage data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get basic stock information.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock information
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', 0),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            return {}
    
    def get_financial_data(self, symbol: str) -> Dict:
        """
        Get financial data for a stock.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with financial data
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'profit_margin': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'dividend_yield': info.get('dividendYield', 0)
            }
        except Exception as e:
            print(f"Error fetching financial data for {symbol}: {e}")
            return {}
    
    def get_multiple_stocks(self, symbols: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Get data for multiple stocks.
        
        Args:
            symbols: List of stock symbols
            period: Time period
            
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.get_yahoo_data(symbol, period)
        return data
    
    def get_market_indices(self) -> Dict[str, pd.DataFrame]:
        """
        Get data for major market indices.
        
        Returns:
            Dictionary with market indices data
        """
        indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'Dow Jones': '^DJI',
            'VIX': '^VIX'
        }
        
        data = {}
        for name, symbol in indices.items():
            data[name] = self.get_yahoo_data(symbol, period="1y")
        
        return data