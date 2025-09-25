"""
LangChain agent for stock price prediction and analysis.
"""

from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

from .stock_tools import StockTools

load_dotenv()


class StockPredictionAgent:
    """
    LangChain agent for stock price prediction and analysis.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1):
        """
        Initialize the stock prediction agent.
        
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
        
        self.stock_tools = StockTools()
        self.tools = self.stock_tools.create_tools()
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the LangChain agent with stock analysis tools."""
        
        system_message = """You are a professional stock market analyst and financial advisor AI assistant. 
        You have access to real-time and historical stock data, technical analysis tools, and market information.
        
        Your capabilities include:
        - Retrieving current stock prices and historical data
        - Performing technical analysis (RSI, MACD, moving averages, Bollinger Bands)
        - Providing trading signals and recommendations
        - Analyzing market trends and company fundamentals
        - Explaining financial concepts in simple terms
        
        Guidelines for your responses:
        1. Always use the available tools to get current data before making any analysis
        2. Provide specific, data-driven insights based on the retrieved information
        3. Explain technical indicators and what they suggest about the stock
        4. Include both bullish and bearish perspectives when relevant
        5. Always mention that your analysis is for informational purposes only and not financial advice
        6. Be clear about the timeframe of your analysis
        7. If asked about predictions, explain the limitations and uncertainties involved
        
        Remember: Always start by gathering current data using the tools before providing analysis."""
        
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            system_message=system_message
        )
    
    def analyze_stock(self, symbol: str, query: Optional[str] = None) -> str:
        """
        Analyze a specific stock with optional custom query.
        
        Args:
            symbol: Stock symbol to analyze
            query: Optional specific question about the stock
            
        Returns:
            Analysis results as string
        """
        if query:
            prompt = f"Analyze {symbol} stock with focus on: {query}"
        else:
            prompt = f"Provide a comprehensive analysis of {symbol} stock including current price, technical indicators, trading signals, and outlook."
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error analyzing {symbol}: {str(e)}"
    
    def predict_price_movement(self, symbol: str, timeframe: str = "short-term") -> str:
        """
        Predict price movement for a stock.
        
        Args:
            symbol: Stock symbol
            timeframe: Prediction timeframe (short-term, medium-term, long-term)
            
        Returns:
            Price movement prediction
        """
        prompt = f"""Analyze {symbol} and predict its {timeframe} price movement. 
        Please consider:
        1. Current technical indicators and their signals
        2. Recent price action and trends
        3. Market sentiment indicators
        4. Support and resistance levels
        
        Provide a structured prediction with reasoning and confidence level."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error predicting price movement for {symbol}: {str(e)}"
    
    def compare_stocks(self, symbols: list) -> str:
        """
        Compare multiple stocks.
        
        Args:
            symbols: List of stock symbols to compare
            
        Returns:
            Comparison analysis
        """
        symbols_str = ", ".join(symbols)
        prompt = f"""Compare these stocks: {symbols_str}. 
        For each stock, analyze:
        1. Current price and recent performance
        2. Technical indicators (RSI, MACD, moving averages)
        3. Key financial metrics
        4. Trading signals
        
        Then provide a ranking and recommendation based on the analysis."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error comparing stocks {symbols_str}: {str(e)}"
    
    def get_market_sentiment(self) -> str:
        """
        Analyze overall market sentiment.
        
        Returns:
            Market sentiment analysis
        """
        prompt = """Analyze the current market sentiment by examining major market indices 
        (S&P 500, NASDAQ, Dow Jones) and the VIX (fear index). 
        Provide insights on:
        1. Overall market direction and trends
        2. Market volatility indicators
        3. Risk appetite
        4. Potential market drivers
        """
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error analyzing market sentiment: {str(e)}"
    
    def chat(self, message: str) -> str:
        """
        General chat interface for stock-related questions.
        
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
    
    def get_trading_recommendation(self, symbol: str, risk_tolerance: str = "moderate") -> str:
        """
        Get trading recommendation for a stock.
        
        Args:
            symbol: Stock symbol
            risk_tolerance: Risk tolerance level (conservative, moderate, aggressive)
            
        Returns:
            Trading recommendation
        """
        prompt = f"""Provide a trading recommendation for {symbol} considering {risk_tolerance} risk tolerance.
        
        Include:
        1. Technical analysis summary
        2. Entry points and price targets
        3. Stop-loss levels
        4. Position sizing suggestions
        5. Time horizon recommendation
        6. Risk factors to consider
        
        Remember to mention this is for informational purposes only."""
        
        try:
            response = self.agent.run(prompt)
            return response
        except Exception as e:
            return f"Error generating trading recommendation for {symbol}: {str(e)}"