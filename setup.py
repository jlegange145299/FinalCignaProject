"""
Setup script for Cigna AI Assistant
Helps verify configuration and dependencies
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✅ {description} found at: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT found at: {filepath}")
        return False

def check_env_var(var_name, description):
    """Check if an environment variable is set"""
    value = os.getenv(var_name)
    if value and value != f"your_{var_name.lower()}_here":
        print(f"✅ {description} is configured")
        return True
    else:
        print(f"❌ {description} is NOT configured")
        return False

def main():
    print("=" * 60)
    print("Cigna AI Assistant - Setup Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check Python version
    print("🐍 Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (Need 3.8+)")
        all_good = False
    print()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    required_packages = [
        'openai',
        'streamlit',
        'requests',
        'dotenv',
        'PIL'
    ]
    
    for package in required_packages:
        try:
            __import__(package if package != 'dotenv' else 'dotenv')
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            all_good = False
    print()
    
    # Check configuration files
    print("📁 Checking configuration files...")
    check_file_exists('.env', '.env file')
    check_file_exists('.streamlit/secrets.toml', 'Streamlit secrets')
    check_file_exists('.streamlit/config.toml', 'Streamlit config')
    print()
    
    # Check environment variables
    print("🔑 Checking API keys...")
    from dotenv import load_dotenv
    load_dotenv()
    
    did_api_ok = check_env_var('DID_API', 'D-ID API key')
    
    # Check Streamlit secrets (if file exists)
    secrets_ok = True
    if os.path.exists('.streamlit/secrets.toml'):
        try:
            import streamlit as st
            # This is a simplified check - actual secrets loading happens in Streamlit context
            print("ℹ️  Streamlit secrets file exists - verify OPENAI_API_KEY and ASSISTANT_ID manually")
        except:
            pass
    else:
        secrets_ok = False
    
    print()
    print("=" * 60)
    
    if all_good and did_api_ok:
        print("✅ All checks passed! You're ready to run the app.")
        print()
        print("To start the application, run:")
        print("  streamlit run app7.py")
    else:
        print("⚠️  Some checks failed. Please review the messages above.")
        print()
        print("Setup steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Copy .env.example to .env and add your D-ID API key")
        print("3. Copy .streamlit/secrets.toml.example to .streamlit/secrets.toml")
        print("4. Add your OpenAI API key and Assistant ID to secrets.toml")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
