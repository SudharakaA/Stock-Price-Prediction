# Web Interface Documentation

## 🌐 Stock Price Prediction Web Interface

The Stock Price Prediction tool includes a powerful **Streamlit-based web interface** that provides an intuitive way to analyze stocks using AI and advanced technical analysis.

### ✨ Features

- **📊 Interactive Stock Charts** - Real-time candlestick charts with technical indicators
- **🤖 AI-Powered Analysis** - Chat with an AI analyst for stock insights
- **📈 Technical Analysis** - RSI, MACD, Bollinger Bands, moving averages
- **💬 Chat Interface** - Natural language queries about stocks
- **🌍 Market Overview** - Current market conditions and indices
- **⚡ Real-Time Data** - Live stock prices and financial metrics

### 🚀 Quick Start

#### Option 1: Use the Launch Script (Recommended)
```bash
python run_web_app.py
```

#### Option 2: Direct Streamlit Command
```bash
streamlit run src/interface/web_app.py
```

#### Option 3: Python Module
```bash
python -m streamlit run src/interface/web_app.py
```

### 📋 Prerequisites

1. **Install Dependencies**
   ```bash
   pip install streamlit plotly yfinance pandas numpy python-dotenv
   ```

2. **Set up API Keys** (Optional but recommended for full functionality)
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **API Keys Needed:**
   - `OPENAI_API_KEY` - For AI chat functionality
   - `ALPHA_VANTAGE_API_KEY` - For enhanced stock data (optional)

### 🎯 How to Use

1. **Launch the Web App**
   - Run `python run_web_app.py`
   - Your browser will open to `http://localhost:8501`

2. **Analyze Stocks**
   - Enter a stock symbol (e.g., AAPL, TSLA, GOOGL)
   - Select time period and analysis type
   - Click "🚀 Analyze Stock"

3. **Chat with AI**
   - Use the chat interface to ask questions
   - Examples: "Compare AAPL and MSFT", "What's the market outlook?"

4. **Explore Features**
   - View interactive charts
   - Check key metrics
   - Get market overviews

### 🛠️ Configuration

The web interface can be configured through environment variables:

```env
# .env file
OPENAI_API_KEY=your_openai_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Optional: Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### 📱 Interface Screenshots

*Screenshots will be added after running the application*

### 🔧 Troubleshooting

#### Common Issues:

1. **"Streamlit not found"**
   ```bash
   pip install streamlit
   ```

2. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

3. **API key errors**
   - Ensure your .env file has the correct API keys
   - OpenAI key is needed for AI chat features

4. **Port already in use**
   ```bash
   streamlit run src/interface/web_app.py --server.port 8502
   ```

### 🚀 Advanced Usage

#### Custom Configuration
```bash
streamlit run src/interface/web_app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --theme.base dark
```

#### Environment Variables
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
python run_web_app.py
```

### 📊 Available Analysis Types

1. **Comprehensive Analysis** - Full AI-powered analysis with technical indicators
2. **Technical Analysis Only** - Focus on chart patterns and indicators  
3. **ML Predictions** - Machine learning based forecasts
4. **Quick Overview** - Brief summary of stock performance

### 💡 Tips for Better Experience

- **Use specific stock symbols** (AAPL instead of Apple)
- **Try different time periods** for different insights
- **Ask specific questions** in the chat interface
- **Combine multiple analysis types** for comprehensive insights

### 🌟 What Makes This Special

- **No complex setup** - Just install dependencies and run
- **AI-powered insights** - Get intelligent analysis beyond basic charts
- **Real-time data** - Always up-to-date stock information
- **Interactive interface** - Explore data your way
- **Professional grade** - Built with modern web technologies

---

*For more information, see the main README.md file.*