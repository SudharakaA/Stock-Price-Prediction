#!/usr/bin/env python3
"""
LangChain Stock Tool Demo - Direct Tool Usage
Shows LangChain tools in action with intelligent routing
"""

import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tools import STOCK_TOOLS
from langchain_core.messages import HumanMessage
import warnings

warnings.filterwarnings("ignore")
load_dotenv()

class StockToolDemo:
    """Demo showing LangChain tools with intelligent routing."""
    
    def __init__(self):
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.llm = None
        self.tools_dict = {tool.name: tool for tool in STOCK_TOOLS}
        self.setup_llm()
    
    def setup_llm(self):
        """Initialize Groq LLM."""
        if not self.groq_key or self.groq_key == 'your_groq_api_key_here':
            return False
        
        try:
            self.llm = ChatGroq(
                api_key=self.groq_key,
                model="llama-3.1-8b-instant",
                temperature=0.1
            )
            return True
        except Exception as e:
            print(f"❌ Error setting up LLM: {e}")
            return False
    
    def detect_intent_and_extract(self, user_input: str):
        """Detect user intent and extract relevant information."""
        user_input_lower = user_input.lower()
        
        # Extract stock symbols (improved regex to avoid common words)
        # Look for 1-5 uppercase letters that are likely stock symbols
        potential_symbols = re.findall(r'\b[A-Z]{1,5}\b', user_input.upper())
        
        # Filter out common English words that might be mistaken for symbols
        common_words = {'AND', 'OR', 'THE', 'FOR', 'YOU', 'ARE', 'NOT', 'BUT', 'CAN', 'GET', 'ALL', 'NEW', 'NOW', 'WAY', 'MAY', 'DAY', 'USE', 'HER', 'HIM', 'HIS', 'SHE', 'HAS', 'HAD'}
        symbols = [s for s in potential_symbols if s not in common_words and len(s) >= 2]
        
        # Intent detection
        if any(word in user_input_lower for word in ['price', 'current', 'cost', 'worth', 'value']):
            return 'price', symbols
        elif any(word in user_input_lower for word in ['technical', 'analysis', 'rsi', 'sma', 'macd', 'signals']):
            return 'technical', symbols
        elif any(word in user_input_lower for word in ['news', 'headlines', 'recent']):
            return 'news', symbols
        elif any(word in user_input_lower for word in ['compare', 'vs', 'versus', 'against']):
            return 'compare', symbols
        elif any(word in user_input_lower for word in ['market', 'overview', 'indices', 'general']):
            return 'market', symbols
        else:
            return 'general', symbols
    
    def execute_tool(self, tool_name: str, input_data: str) -> str:
        """Execute a specific tool."""
        if tool_name not in self.tools_dict:
            return f"❌ Tool '{tool_name}' not found"
        
        try:
            tool = self.tools_dict[tool_name]
            result = tool.invoke(input_data)
            return result
        except Exception as e:
            return f"❌ Error executing {tool_name}: {str(e)}"
    
    def process_query(self, user_input: str) -> str:
        """Process user query with intelligent tool routing."""
        intent, symbols = self.detect_intent_and_extract(user_input)
        
        # Route to appropriate tool
        if intent == 'price' and symbols:
            symbol = symbols[0]  # Use first symbol found
            return self.execute_tool('get_stock_price', symbol)
        
        elif intent == 'technical' and symbols:
            symbol = symbols[0]
            return self.execute_tool('get_technical_analysis', symbol)
        
        elif intent == 'news' and symbols:
            symbol = symbols[0]
            return self.execute_tool('get_stock_news', symbol)
        
        elif intent == 'compare' and len(symbols) >= 2:
            symbols_str = ','.join(symbols[:5])  # Max 5 symbols
            return self.execute_tool('compare_stocks', symbols_str)
        
        elif intent == 'market':
            return self.execute_tool('get_market_overview', '')
        
        else:
            # Fallback to AI reasoning with available data
            return self.ai_reasoning(user_input, symbols)
    
    def ai_reasoning(self, user_input: str, symbols: list) -> str:
        """Use AI to reason about the query when tool routing isn't clear."""
        if not self.llm:
            return "❌ AI reasoning unavailable - check Groq API key"
        
        # Create reasoning prompt that acknowledges data limitations
        context_note = ""
        if symbols:
            context_note = f"\nNote: The user is asking about {', '.join(symbols)}. If real-time data is unavailable due to API rate limits, provide general knowledge and analysis about these companies."
        
        prompt = f"""As a knowledgeable stock market analyst, answer this question: "{user_input}"

{context_note}

You have access to tools for:
- Current stock prices and company info
- Technical analysis (RSI, moving averages, etc.)  
- Recent news and headlines
- Stock comparisons
- Market overviews

However, if real-time data is temporarily unavailable due to API rate limits (common with free services), provide helpful general analysis based on your knowledge of these companies and market principles.

For example:
- Company business models and competitive advantages
- Historical performance patterns
- Industry trends and market position
- General investment considerations
- Technical analysis concepts

Always mention this is not financial advice and that current market data would be needed for specific trading decisions.

Keep response informative but concise."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return f"🤖 {response.content}\n\n💡 Note: Real-time data tools are available but may be temporarily rate-limited."
        except Exception as e:
            return f"❌ AI reasoning error: {str(e)[:100]}"

def print_banner():
    """Display banner."""
    print("🚀 LangChain Stock Tools Demo")
    print("=" * 35)
    print("🛠️  Intelligent Tool Routing + AI Reasoning")
    print("🤖 Powered by Groq AI")
    print()

def print_examples():
    """Print usage examples."""
    print("""💡 Try these examples:

📊 Stock Prices:
   • "What's Apple's current price?"
   • "TSLA stock price"
   • "How much is Microsoft worth?"

🔍 Technical Analysis:
   • "Analyze NVDA technical indicators"
   • "What are the RSI signals for AAPL?"
   • "Technical analysis of Tesla"

📰 News & Sentiment:
   • "Recent news about Apple"
   • "MSFT headlines"

📈 Comparisons:
   • "Compare AAPL and GOOGL"
   • "TSLA vs RIVN vs LCID"

🌐 Market Overview:
   • "Market overview"
   • "How are the indices doing?"

Commands: 'examples', 'tools', 'quit'
""")

def main():
    """Main function."""
    print_banner()
    
    demo = StockToolDemo()
    
    if not demo.llm:
        print("❌ Failed to initialize. Check your Groq API key in .env file")
        return
    
    print("✅ LangChain tools loaded and AI ready!")
    print_examples()
    
    while True:
        try:
            user_input = input("💬 Ask about stocks > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for trying LangChain stock tools!")
                break
            elif user_input.lower() == 'examples':
                print_examples()
                continue
            elif user_input.lower() == 'tools':
                print("\n🛠️  Available LangChain Tools:")
                for tool in STOCK_TOOLS:
                    print(f"   • {tool.name}: {tool.description}")
                print()
                continue
            
            print("🔧 Processing with LangChain tools...")
            response = demo.process_query(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n👋 Thanks for trying LangChain stock tools!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()