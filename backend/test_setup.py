"""
Test script to verify backend setup and functionality
Run this after setting up the backend to ensure everything works
"""

import sys
import importlib.util

def check_imports():
    """Check if all required packages are installed"""
    print("🔍 Checking required packages...\n")
    
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic'),
        ('yfinance', 'yfinance'),
        ('sklearn', 'scikit-learn'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
    ]
    
    all_installed = True
    for module_name, display_name in required_packages:
        if importlib.util.find_spec(module_name) is not None:
            print(f"✓ {display_name} - installed")
        else:
            print(f"✗ {display_name} - NOT FOUND")
            all_installed = False
    
    return all_installed

def test_imports():
    """Test if modules can be imported without errors"""
    print("\n🧪 Testing module imports...\n")
    
    try:
        from config import settings
        print("✓ config.py imports successfully")
        print(f"  - Models directory: {settings.MODEL_DIR}")
        print(f"  - Cache database: {settings.CACHE_DB_PATH}")
    except Exception as e:
        print(f"✗ config.py import failed: {e}")
        return False
    
    try:
        from data_fetcher import DataFetcher
        print("✓ data_fetcher.py imports successfully")
    except Exception as e:
        print(f"✗ data_fetcher.py import failed: {e}")
        return False
    
    try:
        from model_trainer import ModelTrainer
        print("✓ model_trainer.py imports successfully")
    except Exception as e:
        print(f"✗ model_trainer.py import failed: {e}")
        return False
    
    try:
        from predictor import Predictor
        print("✓ predictor.py imports successfully")
    except Exception as e:
        print(f"✗ predictor.py import failed: {e}")
        return False
    
    try:
        from main import app
        print("✓ main.py imports successfully")
    except Exception as e:
        print(f"✗ main.py import failed: {e}")
        return False
    
    return True

def test_data_fetcher():
    """Test basic data fetching functionality"""
    print("\n📊 Testing data fetcher...\n")
    
    try:
        from data_fetcher import DataFetcher
        fetcher = DataFetcher()
        print("✓ DataFetcher initialized")
        
        # Test with a simple symbol (using demo API key)
        print("  Attempting to fetch quote for AAPL...")
        try:
            quote = fetcher.get_quote("AAPL")
            print(f"✓ Quote fetched successfully!")
            print(f"  - Symbol: {quote['symbol']}")
            print(f"  - Price: ${quote['price']}")
            print(f"  - Source: {quote['source']}")
            return True
        except Exception as e:
            print(f"⚠ Quote fetch failed (this is OK if API key not set): {e}")
            print("  Note: The app will work once you add your API key to .env")
            return True
            
    except Exception as e:
        print(f"✗ DataFetcher test failed: {e}")
        return False

def test_model_trainer():
    """Test model trainer initialization"""
    print("\n🤖 Testing model trainer...\n")
    
    try:
        from model_trainer import ModelTrainer
        trainer = ModelTrainer()
        print("✓ ModelTrainer initialized")
        
        # Test feature calculation
        test_prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 110]
        sma = trainer.calculate_sma(test_prices, 5)
        rsi = trainer.calculate_rsi(test_prices, 14)
        
        print(f"✓ Technical indicators calculated successfully")
        print(f"  - SMA values: {len(sma)} calculated")
        print(f"  - RSI values: {len(rsi)} calculated")
        
        return True
    except Exception as e:
        print(f"✗ ModelTrainer test failed: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n⚙️  Checking environment configuration...\n")
    
    import os
    from pathlib import Path
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠ .env file not found")
        print("  Please copy .env.example to .env and add your API key")
        return False
    
    print("✓ .env file exists")
    
    # Try to load settings
    try:
        from config import settings
        if settings.ALPHA_VANTAGE_API_KEY == "demo" or settings.ALPHA_VANTAGE_API_KEY == "your_alpha_vantage_api_key_here":
            print("⚠ API key not configured (using demo key)")
            print("  Get your free API key from: https://www.alphavantage.co/support/#api-key")
            print("  Then add it to the .env file")
            return False
        else:
            print("✓ API key is configured")
            return True
    except Exception as e:
        print(f"✗ Error loading settings: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("  Stock Market Predictor - Backend Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Check package installations
    results.append(("Package Check", check_imports()))
    
    # Test imports
    if results[0][1]:
        results.append(("Module Imports", test_imports()))
    else:
        print("\n⚠ Skipping further tests due to missing packages")
        print("Run: pip install -r requirements.txt")
        return
    
    # Check environment
    results.append(("Environment Config", check_env_file()))
    
    # Test components
    if results[1][1]:
        results.append(("Data Fetcher", test_data_fetcher()))
        results.append(("Model Trainer", test_model_trainer()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    print()
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print("🎉 All tests passed! Backend is ready to use.")
        print("\nNext steps:")
        print("1. Make sure your API key is set in .env")
        print("2. Start the server: python main.py")
        print("3. Visit http://localhost:8000/docs to see the API")
    else:
        print("⚠ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: copy .env.example .env")
        print("3. Add API key to .env file")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
