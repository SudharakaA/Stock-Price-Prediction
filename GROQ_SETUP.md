# 🚀 How to Get Your FREE Groq API Key

## Step 1: Visit Groq Console
Go to: **https://console.groq.com**

## Step 2: Sign Up (Free)
- Click "Sign Up" 
- Use your email or GitHub/Google account
- No credit card required!

## Step 3: Generate API Key
- Once logged in, click "API Keys" in the sidebar
- Click "Create API Key"
- Give it a name like "Stock Prediction Tool"
- Copy the generated key (starts with `gsk_...`)

## Step 4: Add to Your .env File
Open your `.env` file and replace:
```
GROQ_API_KEY=your_groq_api_key_here
```

With:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

## Step 5: Test Your Setup
Run the Groq-powered version:
```bash
cd "/Users/sudharakaashen/Documents/VS code Projects/Stock_Price_Prediction"
./.venv/bin/python groq_demo.py
```

## 🎉 Why Groq is Awesome:
- ✅ **Completely FREE** - No credit card required
- ⚡ **Super FAST** - One of the fastest AI APIs available
- 🔄 **14,400 tokens per minute** free tier
- 🤖 **Great Models** - Llama 3.1, Mixtral, Gemma
- 🚀 **Easy to use** - Same interface as OpenAI

## Available Models:
- `llama3-8b-8192` - Fast and smart (recommended)
- `llama3-70b-8192` - More powerful but slower
- `mixtral-8x7b-32768` - Great for complex reasoning
- `gemma-7b-it` - Good alternative

That's it! Your stock prediction tool will now have FREE AI chat capabilities! 🎊