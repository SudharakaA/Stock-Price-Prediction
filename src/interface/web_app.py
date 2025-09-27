"""
Streamlit web interface for the Stock Price Prediction Tool.
"""

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.enhanced_agent import EnhancedStockAgent
from data.stock_collector import StockDataCollector
from data.technical_analysis import TechnicalAnalyzer
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Stock Price Prediction Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .metric-card {
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .analysis-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'collector' not in st.session_state:
    st.session_state.collector = StockDataCollector()
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = TechnicalAnalyzer()


@st.cache_data
def load_stock_data(symbol, period="1y"):
    """Load and cache stock data."""
    collector = StockDataCollector()
    return collector.get_yahoo_data(symbol, period)


def initialize_agent():
    """Initialize the LangChain agent."""
    if not os.getenv('OPENAI_API_KEY'):
        st.warning("⚠️ No OPENAI_API_KEY found. AI chat features will be disabled.")
        st.info("💡 To enable AI features, create a .env file with your OpenAI API key.")
        st.session_state.agent = None
        return
    
    if st.session_state.agent is None:
        with st.spinner("🔧 Initializing AI agent..."):
            try:
                st.session_state.agent = EnhancedStockAgent()
                st.success("✅ AI agent ready!")
            except Exception as e:
                st.error(f"❌ Error initializing agent: {e}")
                st.warning("🔄 Continuing with basic features (charts and metrics only)")
                st.session_state.agent = None


def plot_stock_chart(df, symbol):
    """Create an interactive stock chart."""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=symbol,
        increasing_line_color='green',
        decreasing_line_color='red'
    ))
    
    # Add moving averages if available
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['SMA_20'],
            mode='lines', name='SMA 20',
            line=dict(color='blue', width=1)
        ))
    
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['SMA_50'],
            mode='lines', name='SMA 50',
            line=dict(color='orange', width=1)
        ))
    
    fig.update_layout(
        title=f"{symbol} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        height=500,
        showlegend=True
    )
    
    return fig


def display_metrics(df, symbol):
    """Display key stock metrics."""
    if df.empty:
        return
    
    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Current price
    price_change = latest['Close'] - previous['Close']
    price_change_pct = (price_change / previous['Close']) * 100
    
    with col1:
        st.metric(
            "Current Price",
            f"${latest['Close']:.2f}",
            f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
        )
    
    # Volume
    with col2:
        st.metric(
            "Volume",
            f"{latest['Volume']:,.0f}",
            f"Avg: {df['Volume'].tail(20).mean():,.0f}"
        )
    
    # 52-week high/low
    with col3:
        high_52w = df['High'].max()
        st.metric("52W High", f"${high_52w:.2f}")
    
    with col4:
        low_52w = df['Low'].min()
        st.metric("52W Low", f"${low_52w:.2f}")


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">📈 Stock Price Prediction Tool</h1>', unsafe_allow_html=True)
    st.markdown("*Powered by LangChain and Advanced ML Models*")
    
    # Initialize agent
    initialize_agent()
    
    # Sidebar
    st.sidebar.header("🔧 Configuration")
    
    # Stock symbol input
    symbol = st.sidebar.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        placeholder="e.g., AAPL, GOOGL, TSLA"
    ).upper()
    
    # Time period selection
    period = st.sidebar.selectbox(
        "Time Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )
    
    # Analysis type
    analysis_type = st.sidebar.selectbox(
        "Analysis Type",
        ["Comprehensive Analysis", "Technical Analysis Only", "ML Predictions", "Quick Overview"]
    )
    
    if st.sidebar.button("🚀 Analyze Stock"):
        if symbol:
            # Load data
            with st.spinner(f"📊 Loading data for {symbol}..."):
                df = load_stock_data(symbol, period)
            
            if df.empty:
                st.error(f"❌ Could not load data for {symbol}")
                return
            
            # Add technical indicators
            df_with_indicators = st.session_state.analyzer.add_all_indicators(df)
            
            # Display metrics
            st.markdown("## 📊 Key Metrics")
            display_metrics(df_with_indicators, symbol)
            
            # Display chart
            st.markdown("## 📈 Price Chart")
            fig = plot_stock_chart(df_with_indicators, symbol)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Analysis (only if agent is available)
            if st.session_state.agent is not None:
                st.markdown("## 🤖 AI Analysis")
                
                with st.spinner("🧠 AI is analyzing the stock..."):
                    try:
                        if analysis_type == "Comprehensive Analysis":
                            response = st.session_state.agent.comprehensive_analysis(symbol)
                        elif analysis_type == "Technical Analysis Only":
                            response = st.session_state.agent.chat(f"Provide detailed technical analysis for {symbol}")
                        elif analysis_type == "ML Predictions":
                            response = st.session_state.agent.ml_forecast_analysis(symbol)
                        else:  # Quick Overview
                            response = st.session_state.agent.chat(f"Give me a quick overview of {symbol} stock")
                        
                        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                        st.markdown(response)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ AI analysis failed: {e}")
                        st.info("📊 Chart and metrics are still available above!")
            else:
                st.markdown("## 🤖 AI Analysis")
                st.info("💡 AI analysis is not available. Please configure your OPENAI_API_KEY to enable this feature.")
                st.markdown("**To enable AI features:**")
                st.markdown("1. Create a `.env` file in the project root")
                st.markdown("2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`")
                st.markdown("3. Restart the web application")
    
    # Chat interface (only if agent is available)
    if st.session_state.agent is not None:
        st.markdown("## 💬 Chat with AI Analyst")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat input
        user_question = st.text_input(
            "Ask me anything about stocks:",
            placeholder="e.g., 'Compare AAPL and MSFT' or 'What's the market outlook?'"
        )
        
        if st.button("Send") and user_question:
            # Add user message to history
            st.session_state.chat_history.append(("user", user_question))
            
            # Get AI response
            with st.spinner("🤖 Thinking..."):
                try:
                    response = st.session_state.agent.chat(user_question)
                    # Add AI response to history
                    st.session_state.chat_history.append(("assistant", response))
                except Exception as e:
                    st.error(f"❌ Chat failed: {e}")
                    response = f"Sorry, I encountered an error: {e}"
                    st.session_state.chat_history.append(("assistant", response))
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 💭 Chat History")
            for role, message in st.session_state.chat_history[-6:]:  # Show last 6 messages
                if role == "user":
                    st.markdown(f"**You:** {message}")
                else:
                    st.markdown(f"**AI Analyst:** {message}")
                    st.markdown("---")
    else:
        st.markdown("## 💬 Chat with AI Analyst")
        st.info("💡 AI chat is not available. Please configure your OPENAI_API_KEY to enable this feature.")
    
    # Market overview sidebar (only if agent is available)
    st.sidebar.markdown("## 🌍 Market Overview")
    if st.session_state.agent is not None:
        if st.sidebar.button("📊 Get Market Overview"):
            with st.spinner("📈 Analyzing market conditions..."):
                try:
                    market_response = st.session_state.agent.market_regime_analysis()
                    st.sidebar.markdown("### Current Market")
                    st.sidebar.info(market_response[:500] + "..." if len(market_response) > 500 else market_response)
                except Exception as e:
                    st.sidebar.error(f"❌ Market analysis failed: {e}")
    else:
        st.sidebar.info("💡 Market overview requires AI features. Please configure your OPENAI_API_KEY.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Disclaimer:** This tool provides analysis for informational purposes only. "
        "Not financial advice. Always do your own research and consult with financial advisors."
    )


if __name__ == "__main__":
    main()