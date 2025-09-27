"""
Simplified Streamlit web interface for Stock Price Prediction.
This version works with basic dependencies only - no AI features required.
"""

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Page config
st.set_page_config(
    page_title="Stock Price Prediction Tool - Basic",
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

@st.cache_data
def load_stock_data(symbol, period="1y"):
    """Load stock data using yfinance."""
    if not YFINANCE_AVAILABLE:
        return pd.DataFrame()
    
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def calculate_moving_averages(df):
    """Calculate simple moving averages."""
    if df.empty:
        return df
    
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    return df

def plot_stock_chart(df, symbol):
    """Create an interactive stock chart."""
    if df.empty:
        return None
    
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
    if 'SMA_20' in df.columns and not df['SMA_20'].isna().all():
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['SMA_20'],
            mode='lines', name='SMA 20',
            line=dict(color='blue', width=1)
        ))
    
    if 'SMA_50' in df.columns and not df['SMA_50'].isna().all():
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
        st.warning("No data available to display metrics")
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

def basic_analysis(df, symbol):
    """Provide basic technical analysis without AI."""
    if df.empty:
        return
    
    latest = df.iloc[-1]
    
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    st.markdown(f"## 📊 Basic Analysis for {symbol}")
    
    # Price trend
    if len(df) >= 20:
        recent_avg = df['Close'].tail(20).mean()
        if latest['Close'] > recent_avg:
            st.success(f"📈 **Price Trend**: Above 20-day average (${recent_avg:.2f})")
        else:
            st.warning(f"📉 **Price Trend**: Below 20-day average (${recent_avg:.2f})")
    
    # Volume analysis
    avg_volume = df['Volume'].mean()
    if latest['Volume'] > avg_volume * 1.2:
        st.info(f"🔊 **Volume**: High trading volume ({latest['Volume']:,.0f} vs avg {avg_volume:,.0f})")
    elif latest['Volume'] < avg_volume * 0.8:
        st.info(f"🔉 **Volume**: Low trading volume ({latest['Volume']:,.0f} vs avg {avg_volume:,.0f})")
    else:
        st.info(f"📊 **Volume**: Normal trading volume ({latest['Volume']:,.0f})")
    
    # Price range
    price_range = (latest['Close'] - df['Low'].min()) / (df['High'].max() - df['Low'].min()) * 100
    st.info(f"📍 **Price Position**: {price_range:.1f}% of 52-week range")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">📈 Stock Price Prediction Tool</h1>', unsafe_allow_html=True)
    st.markdown("*Basic Version - Works without API keys*")
    
    if not YFINANCE_AVAILABLE:
        st.error("❌ yfinance package is required but not installed.")
        st.info("💡 Please install it with: `pip install yfinance`")
        st.stop()
    
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
    
    if st.sidebar.button("📊 Analyze Stock"):
        if symbol:
            # Load data
            with st.spinner(f"📊 Loading data for {symbol}..."):
                df = load_stock_data(symbol, period)
            
            if df.empty:
                st.error(f"❌ Could not load data for {symbol}. Please check the symbol and try again.")
                return
            
            # Add technical indicators
            df_with_indicators = calculate_moving_averages(df)
            
            # Display metrics
            st.markdown("## 📊 Key Metrics")
            display_metrics(df_with_indicators, symbol)
            
            # Display chart
            st.markdown("## 📈 Price Chart")
            fig = plot_stock_chart(df_with_indicators, symbol)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Basic Analysis
            basic_analysis(df_with_indicators, symbol)
    
    # Info about full version
    st.markdown("## 🚀 Upgrade to Full Version")
    st.info("""
    **This is the basic version of the web interface.** 
    
    For AI-powered analysis, chat features, and advanced insights:
    1. Install full dependencies: `pip install -r requirements.txt`
    2. Get an OpenAI API key and add it to your .env file
    3. Run the full version: `python -m streamlit run src/interface/web_app.py`
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Disclaimer:** This tool provides analysis for informational purposes only. "
        "Not financial advice. Always do your own research and consult with financial advisors."
    )

if __name__ == "__main__":
    main()