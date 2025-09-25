# 🚀 Stock Price Prediction Tool

## 📁 **Clean Project Structure**

```
Stock_Price_Prediction/
├── 📄 .env                          # Your API keys (Groq + Alpha Vantage)
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # Project documentation
├── 📄 PROJECT_SUMMARY.md            # Complete feature overview
├── 📄 GROQ_SETUP.md                 # How to get free Groq API key
│
├── 🚀 groq_demo.py                  # Main tool (Recommended)
├── 🛠️ langchain_tools_demo.py       # LangChain version with smart tools
├── 🔧 langchain_tools.py            # LangChain tool definitions
│
├── 📁 src/                          # Core modules
│   ├── 📁 agents/                   # LangChain agents
│   ├── 📁 data/                     # Stock data collection
│   ├── 📁 interface/                # Streamlit web app
│   ├── 📁 models/                   # ML prediction models
│   └── 📄 main.py                   # Original CLI version
│
├── 📁 examples/                     # Usage examples
└── 📁 .venv/                        # Python virtual environment
```

## 🎯 **How to Use (3 Main Options)**

### **1. Quick Start (Recommended):**
```bash
./.venv/bin/python groq_demo.py
```

### **2. LangChain Demo (Advanced):**
```bash
./.venv/bin/python langchain_tools_demo.py
```

### **3. Web Interface:**
```bash
./.venv/bin/python -m streamlit run src/interface/web_app.py
```

## 🎊 **You're All Set!**

Your project is now clean, organized, and ready to use! 🚀