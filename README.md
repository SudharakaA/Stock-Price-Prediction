# Stock Price Prediction Tool with LangChain

A comprehensive stock price prediction tool that leverages LangChain for intelligent analysis and conversation, combined with machine learning models for price forecasting.

## Features

- **Stock Data Collection**: Fetch real-time and historical stock data from multiple sources
- **LangChain Integration**: Conversational AI for stock analysis and insights
- **Multiple ML Models**: LSTM, Prophet, and traditional forecasting models
- **Technical Analysis**: Automated calculation of technical indicators
- **Interactive Interface**: Streamlit web app for easy interaction
- **Natural Language Queries**: Ask questions about stocks in plain English

## Project Structure

```
src/
├── data/           # Data collection and processing modules
├── models/         # Machine learning prediction models
├── agents/         # LangChain agents and chains
└── interface/      # User interfaces (CLI, web)
examples/           # Example scripts and notebooks
```

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run the application: `python src/main.py`

## Usage

### Basic Example
```python
from src.agents.stock_agent import StockPredictionAgent

agent = StockPredictionAgent()
result = agent.predict("What's the outlook for AAPL stock?")
print(result)
```

### Web Interface
```bash
streamlit run src/interface/web_app.py
```

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

## License

MIT License