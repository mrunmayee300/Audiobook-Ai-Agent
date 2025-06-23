#!/usr/bin/env python3
"""
Test script to verify Audiobook AI Agent installation
Run this script to check if everything is set up correctly
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    modules = [
        ('streamlit', 'Streamlit web framework'),
        ('fitz', 'PyMuPDF for PDF processing'),
        ('dotenv', 'Environment variable management'),
        ('pydub', 'Audio processing'),
        ('requests', 'HTTP requests'),
        ('PIL', 'Image processing (Pillow)')
    ]
    
    all_good = True
    for module_name, description in modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description} (Error: {e})")
            all_good = False
    
    return all_good

def test_local_modules():
    """Test if local modules can be imported."""
    print("\n🔍 Testing local modules...")
    
    local_modules = [
        ('utils.pdf_reader', 'PDF text extraction'),
        ('utils.murf_api', 'Murf AI API integration'),
        ('utils.audio_utils', 'Audio processing utilities')
    ]
    
    all_good = True
    for module_name, description in local_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description} (Error: {e})")
            all_good = False
    
    return all_good

def test_env_configuration():
    """Test environment configuration."""
    print("\n🔍 Testing environment configuration...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found")
        print("   Please create .env file from env_template.txt")
        return False
    
    # Try to load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('MURF_API_KEY')
        if not api_key:
            print("❌ MURF_API_KEY not found in .env file")
            return False
        elif api_key == 'your_murf_api_key_here':
            print("⚠️  MURF_API_KEY not properly configured")
            print("   Please replace with your actual Murf API key")
            return False
        else:
            print("✅ MURF_API_KEY configured")
            return True
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing functionality."""
    print("\n🔍 Testing PDF processing...")
    
    try:
        from utils.pdf_reader import extract_text_from_pdf, clean_text
        
        # Test text cleaning
        test_text = "This   is   a   test   text   with   extra   spaces."
        cleaned = clean_text(test_text)
        
        if cleaned == "This is a test text with extra spaces.":
            print("✅ Text cleaning function works")
            return True
        else:
            print("❌ Text cleaning function failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def test_audio_processing():
    """Test audio processing functionality."""
    print("\n🔍 Testing audio processing...")
    
    try:
        from utils.audio_utils import split_text, format_duration
        
        # Test text splitting
        test_text = "This is a test sentence. This is another test sentence. " * 100
        chunks = split_text(test_text, 100)
        
        if len(chunks) > 1:
            print("✅ Text splitting function works")
        else:
            print("❌ Text splitting function failed")
            return False
        
        # Test duration formatting
        duration_str = format_duration(3661)  # 1 hour, 1 minute, 1 second
        if duration_str == "1h 1m 1s":
            print("✅ Duration formatting function works")
            return True
        else:
            print("❌ Duration formatting function failed")
            return False
            
    except Exception as e:
        print(f"❌ Audio processing test failed: {e}")
        return False

def test_murf_api():
    """Test Murf API configuration."""
    print("\n🔍 Testing Murf API configuration...")
    
    try:
        from utils.murf_api import get_murf_api
        
        api = get_murf_api()
        print("✅ Murf API class initialized")
        
        # Test API status check (without making actual API call)
        print("✅ Murf API integration ready")
        return True
        
    except Exception as e:
        print(f"❌ Murf API test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Audiobook AI Agent - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Local Modules", test_local_modules),
        ("Environment Config", test_env_configuration),
        ("PDF Processing", test_pdf_processing),
        ("Audio Processing", test_audio_processing),
        ("Murf API Config", test_murf_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your installation is ready.")
        print("You can now run the app with: python run_app.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("Refer to the README.md for troubleshooting guidance.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 