# 🚀 Stock Price Prediction Tool with LangChain & AI

A powerful, AI-driven stock analysis tool that combines real-time data, technical analysis, and intelligent conversation using LangChain and Groq AI.

## ✨ Features

- 🤖 **Free AI Chat** - Powered by Groq AI (no credits required!)
- 📊 **Real-Time Stock Data** - Live prices, technical analysis, news
- 🛠️ **LangChain Tools** - Intelligent tool selection and routing
- 📈 **Technical Analysis** - RSI, SMA, MACD, Bollinger Bands
- 🎯 **Smart Fallbacks** - AI reasoning when APIs are rate-limited
- 💬 **Natural Language** - Ask questions in plain English
- 🌐 **Multiple Interfaces** - CLI, web app, and interactive modes
- 🚀 **Easy Launch** - Simple web interface with `python run_web_app.py`

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/SudharakaA/Stock-Price-Prediction.git
cd Stock-Price-Prediction
pip install -r requirements.txt
```

### 2. Get Free API Keys
- **Groq AI (Free)**: Get your key at [console.groq.com](https://console.groq.com)
- **Alpha Vantage (Free)**: Get your key at [alphavantage.co](https://www.alphavantage.co/support/#api-key)

### 3. Configure Environment
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### 4. Run the Tool
```bash
# Simple version (recommended)
python groq_demo.py

# LangChain version (advanced)
python langchain_tools_demo.py

# Web interface (NEW!)
python run_web_app.py

# Or directly with Streamlit
python -m streamlit run src/interface/web_app.py
```

## 🌐 Web Interface

The tool includes a powerful **Streamlit-based web interface** for interactive stock analysis!

### ✨ Web Features
- **📊 Interactive Charts** - Real-time candlestick charts with technical indicators
- **🤖 AI Chat** - Natural language queries about stocks
- **📈 Technical Analysis** - RSI, MACD, Bollinger Bands visualization
- **💬 Market Insights** - AI-powered market analysis
- **⚡ Real-Time Data** - Live stock prices and metrics

### 🚀 Quick Web Launch
```bash
# Easy way (recommended)
python run_web_app.py

# Direct Streamlit
streamlit run src/interface/web_app.py
```

**📝 Note:** The web interface works with or without API keys - basic charts and data are always available!

For detailed web interface documentation, see [`docs/WEB_INTERFACE.md`](docs/WEB_INTERFACE.md).

## 💡 Usage Examples

### Basic Stock Chat
```bash
python groq_demo.py
> chat
Ask about stocks > What do you think about Apple stock?
```

### LangChain Intelligence
```bash
python langchain_tools_demo.py
> Compare AAPL and GOOGL
> What's Tesla's current price?
> Technical analysis of NVIDIA
```

## 🛠️ LangChain Tools Available

- **`get_stock_price`** - Current prices and company info
- **`get_technical_analysis`** - RSI, SMA, MACD analysis
- **`get_stock_news`** - Recent headlines and sentiment
- **`compare_stocks`** - Side-by-side comparisons  
- **`get_market_overview`** - Major indices status

## 🎯 What Makes This Special

### Without LangChain (Manual):
- Hard-coded responses for each query type
- Breaks when APIs fail
- No intelligent routing
- Limited flexibility

### With LangChain (Intelligent):
- ✅ **Auto tool selection** - AI picks right tools
- ✅ **Smart fallbacks** - AI reasoning when data unavailable  
- ✅ **Natural language** - Understands "compare Apple and Google"
- ✅ **Graceful degradation** - Professional responses even with API limits

## 📁 Project Structure

```
Stock_Price_Prediction/
├── groq_demo.py              # Main tool (recommended)
├── langchain_tools_demo.py   # LangChain version
├── langchain_tools.py        # Tool definitions
├── src/                      # Core modules
│   ├── agents/              # LangChain agents
│   ├── data/                # Stock data collection
│   ├── interface/           # Streamlit web app
│   └── models/              # ML prediction models
└── examples/                 # Usage examples
```

## 🔧 Technical Details

### Dependencies
- **LangChain** - AI agent framework
- **Groq** - Fast, free AI inference
- **yfinance** - Stock data collection
- **Streamlit** - Web interface
- **Pandas/NumPy** - Data processing

### Architecture
1. **Data Layer** - Real-time stock data APIs
2. **Analysis Layer** - Technical indicators and ML models  
3. **AI Layer** - LangChain agents and tools
4. **Interface Layer** - CLI, web, and chat interfaces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Not financial advice. Always consult with financial professionals before making investment decisions.

## 📝 License

MIT License - see LICENSE file for details.

---

**🎯 Built to showcase the power of LangChain for intelligent tool routing and AI reasoning!**
```
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

## License

MIT License