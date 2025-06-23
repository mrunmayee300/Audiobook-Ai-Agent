#!/usr/bin/env python3
"""
Startup script for Audiobook AI Agent
Checks dependencies and launches the Streamlit application
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'streamlit',
        'fitz',  # PyMuPDF
        'dotenv',
        'pydub',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package} is installed")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has API key."""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found")
        print("Please create .env file from env_template.txt and add your Murf API key")
        return False
    
    # Check if API key is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('MURF_API_KEY')
        if not api_key or api_key == 'your_murf_api_key_here':
            print("⚠️  Warning: MURF_API_KEY not properly configured in .env file")
            return False
        print("✅ API key configured")
        return True
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ffmpeg is available")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  Warning: ffmpeg not found in PATH")
    print("Please install ffmpeg:")
    print("  Windows: Download from https://ffmpeg.org/download.html")
    print("  macOS: brew install ffmpeg")
    print("  Ubuntu/Debian: sudo apt install ffmpeg")
    return False

def main():
    """Main startup function."""
    print("🚀 Starting Audiobook AI Agent...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment configuration
    env_ok = check_env_file()
    
    # Check ffmpeg
    ffmpeg_ok = check_ffmpeg()
    
    print("=" * 50)
    
    if not env_ok:
        print("⚠️  App will start but API functionality will be limited")
        print("Please configure your .env file with a valid Murf API key")
    
    if not ffmpeg_ok:
        print("⚠️  Audio processing may fail without ffmpeg")
        print("Please install ffmpeg for full functionality")
    
    # Start the Streamlit app
    print("🌐 Launching Streamlit application...")
    print("The app will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'main.py'], 
                      check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 