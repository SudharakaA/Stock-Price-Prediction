#!/usr/bin/env python3
"""
Setup script for the Stock Price Prediction Web Interface.
This script helps users get started quickly.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Set up the web interface."""
    
    print("🚀 Stock Price Prediction Web Interface Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Try to install minimal requirements first
    requirements_files = [
        "requirements-web.txt",  # Minimal web requirements
        "requirements.txt"       # Full requirements (fallback)
    ]
    
    installed = False
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"\n📦 Attempting to install dependencies from {req_file}...")
            if run_command(f"{sys.executable} -m pip install -r {req_file}", f"Installing from {req_file}"):
                installed = True
                break
            else:
                print(f"⚠️  Failed to install from {req_file}, trying next option...")
    
    if not installed:
        print("\n📦 Installing essential packages individually...")
        essential_packages = [
            "streamlit",
            "plotly", 
            "yfinance",
            "pandas",
            "numpy", 
            "python-dotenv"
        ]
        
        for package in essential_packages:
            if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
                print(f"⚠️  Failed to install {package}, continuing anyway...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            print("\n🔧 Creating .env file from template...")
            try:
                env_content = env_example.read_text()
                env_file.write_text(env_content)
                print("✅ .env file created! Please edit it to add your API keys.")
            except Exception as e:
                print(f"❌ Failed to create .env file: {e}")
        else:
            print("\n📝 Creating basic .env file...")
            env_content = """# Environment variables for Stock Price Prediction
# Get your free OpenAI API key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Get Alpha Vantage key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
"""
            try:
                env_file.write_text(env_content)
                print("✅ Basic .env file created! Please edit it to add your API keys.")
            except Exception as e:
                print(f"❌ Failed to create .env file: {e}")
    
    # Final setup complete
    print("\n🎉 Setup completed!")
    print("=" * 50)
    print("\n📝 Next steps:")
    print("1. Edit the .env file to add your API keys (optional for basic features)")
    print("2. Run the web interface: python run_web_app.py")
    print("3. Your browser will open to http://localhost:8501")
    print("\n💡 The web interface works even without API keys - you'll get charts and basic data!")
    print("\n🔧 For troubleshooting, see docs/WEB_INTERFACE.md")

if __name__ == "__main__":
    main()