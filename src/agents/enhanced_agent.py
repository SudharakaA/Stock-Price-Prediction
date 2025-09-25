"""
Enhanced Stock Prediction Agent with ML capabilities.
"""

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from typing import Optional, List
import os
from dotenv import load_dotenv

from .stock_tools import StockTools
from ..models.prediction_tools import ModelPredictionTools

load_dotenv()


class EnhancedStockAgent:
    """
    Enhanced LangChain agent with both analysis and ML prediction capabilities.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1):
        """
        Initialize the enhanced stock prediction agent.
        
        Args:
            model_name: OpenAI model name
            temperature: Model temperature for responses
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=self.api_key
        )
        
        # Initialize tools
        self.stock_tools = StockTools()
        self.prediction_tools = ModelPredictionTools()
        
        # Combine all tools
        self.tools = self.stock_tools.create_tools() + self.prediction_tools.create_tools()
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.agent = self._create_enhanced_agent()
    
    def _create_enhanced_agent(self):
        """Create the enhanced LangChain agent with all capabilities."""
        
        system_message = """You are an advanced AI stock market analyst with comprehensive analytical and predictive capabilities.

        Your Enhanced Capabilities:
        1. **Data Analysis**: Real-time stock data, technical indicators, financial metrics
        2. **Technical Analysis**: RSI, MACD, moving averages, Bollinger Bands, support/resistance
        3. **Machine Learning Predictions**: LSTM neural networks and Prophet time series models
        4. **Market Intelligence**: Index analysis, sentiment evaluation, comparative studies
        5. **Trading Insights**: Signals, recommendations, risk assessment

        Available Tools:
        - get_stock_data: Current and historical price data
        - get_stock_info: Company fundamentals and financial metrics
        - get_technical_analysis: Complete technical indicator analysis
        - get_market_overview: Major indices and market sentiment
        - predict_with_prophet: Time series forecasting with seasonality
        - predict_with_lstm: Neural network pattern recognition
        - compare_ml_predictions: Ensemble prediction analysis

        Your Analysis Framework:
        1. **Always gather current data first** using available tools
        2. **Provide multi-dimensional analysis**: Technical + Fundamental + Predictive
        3. **Explain the reasoning** behind your conclusions
        4. **Compare multiple perspectives** (bullish/bearish scenarios)
        5. **Use ML predictions** to enhance traditional analysis
        6. **Assess confidence levels** and model agreement
        7. **Include risk factors** and limitations

        Response Guidelines:
        - Start with current data collection
        - Provide technical analysis with clear explanations
        - Include ML predictions when relevant
        - Explain model differences (Prophet vs LSTM)
        - Give both short-term and medium-term outlook
        - Always include disclaimer about financial advice
        - Structure responses logically with clear sections

        Remember: You're providing analysis for informational purposes. Always emphasize the inherent risks and uncertainties in stock market predictions."""
        
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            system_message=system_message,
            max_iterations=10
        )
    
    def comprehensive_analysis(self, symbol: str) -> str:
        """
        Perform comprehensive analysis including technical analysis and ML predictions.
        
        Args:
            symbol: Stock symbol to analyze
            
        Returns:
            Comprehensive analysis results
        """
        prompt = f"""Perform a comprehensive analysis of {symbol} stock. Please include:

        1. **Current Market Data**: Price, volume, recent performance
        2. **Company Fundamentals**: Key financial metrics and ratios
        3. **Technical Analysis**: All major indicators and their signals
        4. **Machine Learning Predictions**: Both Prophet and LSTM forecasts
        5. **Model Comparison**: Agreement/disagreement between predictions
        6. **Risk Assessment**: Support/resistance levels, volatility indicators
        7. **Trading Perspective**: Entry points, targets, stop-losses
        8. **Market Context**: How this stock relates to broader market trends

        Provide a structured, detailed analysis that combines traditional analysis with modern ML insights."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error in comprehensive analysis for {symbol}: {str(e)}"
    
    def ml_forecast_analysis(self, symbol: str, days_ahead: int = 5) -> str:
        """
        Focus specifically on machine learning predictions.
        
        Args:
            symbol: Stock symbol
            days_ahead: Days to forecast ahead
            
        Returns:
            ML prediction analysis
        """
        prompt = f"""Provide a detailed machine learning forecast analysis for {symbol} over the next {days_ahead} days.

        Please include:
        1. **Prophet Model Predictions**: Trend and seasonality analysis
        2. **LSTM Model Predictions**: Pattern recognition results  
        3. **Model Comparison**: Agreement, differences, and confidence
        4. **Prediction Reliability**: Factors affecting accuracy
        5. **Investment Implications**: What the forecasts suggest for traders
        6. **Risk Considerations**: Uncertainty ranges and model limitations

        Focus on explaining what each model is seeing and how to interpret the predictions."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error in ML forecast analysis for {symbol}: {str(e)}"
    
    def portfolio_analysis(self, symbols: List[str]) -> str:
        """
        Analyze multiple stocks for portfolio construction.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Portfolio analysis
        """
        symbols_str = ", ".join(symbols)
        prompt = f"""Analyze this portfolio of stocks: {symbols_str}

        For each stock, provide:
        1. **Current technical status** and key indicators
        2. **ML prediction outlook** (short-term trend)
        3. **Risk/reward profile** based on analysis

        Then provide:
        4. **Portfolio-level insights**: Correlation, diversification, sector exposure
        5. **Relative ranking**: Which stocks look most/least attractive
        6. **Allocation suggestions**: Based on risk-adjusted outlook
        7. **Market timing considerations**: Entry/exit strategies

        Focus on how these stocks work together as a portfolio."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error in portfolio analysis for {symbols_str}: {str(e)}"
    
    def market_regime_analysis(self) -> str:
        """
        Analyze current market regime and conditions.
        
        Returns:
            Market regime analysis
        """
        prompt = """Analyze the current market regime and overall conditions:

        1. **Market Indices Analysis**: S&P 500, NASDAQ, Dow Jones trends
        2. **Volatility Assessment**: VIX levels and what they indicate
        3. **Market Sentiment**: Risk-on vs risk-off indicators
        4. **Regime Classification**: Bull/bear market, trending/ranging
        5. **Sector Rotation**: Which sectors are leading/lagging
        6. **Trading Environment**: Best strategies for current conditions
        7. **Key Risks**: What could change the current regime

        Provide actionable insights for navigating the current market environment."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error in market regime analysis: {str(e)}"
    
    def chat(self, message: str) -> str:
        """
        General chat interface with enhanced capabilities.
        
        Args:
            message: User question or request
            
        Returns:
            Agent response
        """
        try:
            response = self.agent.run(message)
            return response
        except Exception as e:
            return f"Error processing request: {str(e)}"