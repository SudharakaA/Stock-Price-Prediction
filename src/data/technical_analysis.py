"""
Technical analysis indicators for stock data.
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, Tuple


class TechnicalAnalyzer:
    """Calculates technical indicators for stock data."""
    
    def __init__(self):
        pass
    
    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add moving averages to the dataframe.
        
        Args:
            df: DataFrame with stock data (must have 'Close' column)
            
        Returns:
            DataFrame with moving averages added
        """
        df = df.copy()
        
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        return df
    
    def add_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add RSI (Relative Strength Index) to the dataframe.
        
        Args:
            df: DataFrame with stock data
            period: RSI period
            
        Returns:
            DataFrame with RSI added
        """
        df = df.copy()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=period).rsi()
        return df
    
    def add_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add MACD indicators to the dataframe.
        
        Args:
            df: DataFrame with stock data
            
        Returns:
            DataFrame with MACD indicators added
        """
        df = df.copy()
        
        macd_indicator = ta.trend.MACD(df['Close'])
        df['MACD'] = macd_indicator.macd()
        df['MACD_Signal'] = macd_indicator.macd_signal()
        df['MACD_Histogram'] = macd_indicator.macd_diff()
        
        return df
    
    def add_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
        """
        Add Bollinger Bands to the dataframe.
        
        Args:
            df: DataFrame with stock data
            period: Period for moving average
            std_dev: Standard deviation multiplier
            
        Returns:
            DataFrame with Bollinger Bands added
        """
        df = df.copy()
        
        bollinger = ta.volatility.BollingerBands(df['Close'], window=period, window_dev=std_dev)
        df['BB_Upper'] = bollinger.bollinger_hband()
        df['BB_Middle'] = bollinger.bollinger_mavg()
        df['BB_Lower'] = bollinger.bollinger_lband()
        df['BB_Width'] = bollinger.bollinger_wband()
        df['BB_Percent'] = bollinger.bollinger_pband()
        
        return df
    
    def add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add volume-based indicators to the dataframe.
        
        Args:
            df: DataFrame with stock data (must have 'Volume' column)
            
        Returns:
            DataFrame with volume indicators added
        """
        df = df.copy()
        
        # Volume Moving Average
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        
        # On-Balance Volume
        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['Close'], df['Volume']).on_balance_volume()
        
        # Volume Price Trend
        df['VPT'] = ta.volume.VolumePriceTrendIndicator(df['Close'], df['Volume']).volume_price_trend()
        
        return df
    
    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add all technical indicators to the dataframe.
        
        Args:
            df: DataFrame with stock data
            
        Returns:
            DataFrame with all indicators added
        """
        df = self.add_moving_averages(df)
        df = self.add_rsi(df)
        df = self.add_macd(df)
        df = self.add_bollinger_bands(df)
        
        if 'Volume' in df.columns:
            df = self.add_volume_indicators(df)
        
        return df
    
    def get_trading_signals(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on technical indicators.
        
        Args:
            df: DataFrame with technical indicators
            
        Returns:
            Dictionary with trading signals
        """
        signals = {}
        
        if len(df) < 2:
            return {"error": "Insufficient data for signals"}
        
        latest = df.iloc[-1]
        previous = df.iloc[-2]
        
        # RSI signals
        if 'RSI' in df.columns:
            rsi = latest['RSI']
            if rsi > 70:
                signals['RSI'] = 'Overbought - Consider Selling'
            elif rsi < 30:
                signals['RSI'] = 'Oversold - Consider Buying'
            else:
                signals['RSI'] = 'Neutral'
        
        # MACD signals
        if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
            macd_current = latest['MACD']
            signal_current = latest['MACD_Signal']
            macd_prev = previous['MACD']
            signal_prev = previous['MACD_Signal']
            
            if macd_current > signal_current and macd_prev <= signal_prev:
                signals['MACD'] = 'Bullish Crossover - Buy Signal'
            elif macd_current < signal_current and macd_prev >= signal_prev:
                signals['MACD'] = 'Bearish Crossover - Sell Signal'
            else:
                signals['MACD'] = 'No Clear Signal'
        
        # Moving Average signals
        if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
            sma20 = latest['SMA_20']
            sma50 = latest['SMA_50']
            
            if sma20 > sma50:
                signals['SMA'] = 'Bullish Trend'
            else:
                signals['SMA'] = 'Bearish Trend'
        
        # Bollinger Bands signals
        if 'BB_Upper' in df.columns and 'BB_Lower' in df.columns:
            price = latest['Close']
            bb_upper = latest['BB_Upper']
            bb_lower = latest['BB_Lower']
            
            if price >= bb_upper:
                signals['Bollinger'] = 'Price at Upper Band - Potential Resistance'
            elif price <= bb_lower:
                signals['Bollinger'] = 'Price at Lower Band - Potential Support'
            else:
                signals['Bollinger'] = 'Price within Bands'
        
        return signals
    
    def calculate_support_resistance(self, df: pd.DataFrame, window: int = 20) -> Tuple[float, float]:
        """
        Calculate support and resistance levels.
        
        Args:
            df: DataFrame with stock data
            window: Window for calculation
            
        Returns:
            Tuple of (support_level, resistance_level)
        """
        if len(df) < window:
            return (None, None)
        
        recent_data = df.tail(window)
        support = recent_data['Low'].min()
        resistance = recent_data['High'].max()
        
        return (support, resistance)