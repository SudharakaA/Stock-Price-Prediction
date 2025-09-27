#!/usr/bin/env python3
"""
Launch script for the Stock Price Prediction Web Interface.
This script makes it easier to start the Streamlit web application.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import streamlit
        return True, "full"
    except ImportError:
        return False, None

def main():
    """Launch the Streamlit web application."""
    
    print("🚀 Starting Stock Price Prediction Web Interface...")
    print("=" * 55)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    web_app_path = project_root / "src" / "interface" / "web_app.py"
    web_app_basic_path = project_root / "src" / "interface" / "web_app_basic.py"
    
    # Check dependencies
    has_streamlit, version = check_dependencies()
    
    if not has_streamlit:
        print("❌ Error: Streamlit is not installed.")
        print("💡 Please install it with: pip install streamlit")
        print("   Or run the setup script: python setup_web.py")
        sys.exit(1)
    
    # Determine which web app to run
    app_path = web_app_path
    app_type = "Full Version (with AI features)"
    
    # Check if AI dependencies are available
    try:
        # Check if .env file exists
        env_file = project_root / ".env"
        if not env_file.exists():
            print("⚠️  Warning: No .env file found. Using basic version without AI features.")
            print("   To enable AI features, copy .env.example to .env and add your API keys.")
            if web_app_basic_path.exists():
                app_path = web_app_basic_path
                app_type = "Basic Version (charts and data only)"
    except Exception:
        pass
    
    if not app_path.exists():
        print("❌ Error: Web app not found at", app_path)
        sys.exit(1)
    
    print(f"🎯 Launching: {app_type}")
    print("🌐 Web interface will open in your browser at:")
    print("   http://localhost:8501")
    print()
    print("📝 To stop the server, press Ctrl+C in this terminal")
    print("=" * 55)
    print()
    
    try:
        # Launch Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)]
        subprocess.run(cmd, cwd=project_root)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped.")
    except FileNotFoundError:
        print("❌ Error: Streamlit not found. Please run:")
        print("   pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()