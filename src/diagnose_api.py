#!/usr/bin/env python3
"""
Binance API Diagnostic Script
Helps identify and fix API authentication issues
"""

import os
import time
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv

def check_environment():
    """Check if .env file exists and has required variables"""
    print("=== Environment Check ===")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Create .env file with:")
        print("BINANCE_API_KEY=your_api_key")
        print("BINANCE_SECRET_KEY=your_secret_key")
        print("BINANCE_TESTNET=True")
        return False
    
    load_dotenv()
    
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    testnet = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
    
    print(f"✅ .env file found")
    print(f"API Key: {'Present' if api_key else '❌ Missing'}")
    print(f"Secret Key: {'Present' if secret_key else '❌ Missing'}")
    print(f"Testnet: {testnet}")
    
    if api_key:
        print(f"API Key preview: {api_key[:8]}...{api_key[-4:]}")
    if secret_key:
        print(f"Secret Key preview: {secret_key[:8]}...{secret_key[-4:]}")
    
    return bool(api_key and secret_key)

def check_system_time():
    """Check if system time is synchronized"""
    print("\n=== System Time Check ===")
    
    current_time = datetime.now()
    timestamp = int(time.time() * 1000)
    
    print(f"System time: {current_time}")
    print(f"Unix timestamp: {timestamp}")
    
    # Check if time seems reasonable (not too far off)
    expected_2024_timestamp = 1700000000000  # Rough 2023+ timestamp
    if timestamp < expected_2024_timestamp:
        print("❌ System time seems incorrect (too old)")
        return False
    
    print("✅ System time appears correct")
    return True

def test_basic_connectivity():
    """Test basic API connectivity without authentication"""
    print("\n=== Basic Connectivity Test ===")
    
    try:
        load_dotenv()
        testnet = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
        
        # Test without credentials first
        client = Client(testnet=testnet)
        server_time = client.get_server_time()
        
        print("✅ Basic connectivity successful")
        print(f"Server time: {datetime.fromtimestamp(server_time['serverTime']/1000)}")
        
        # Check time difference
        local_time = int(time.time() * 1000)
        time_diff = abs(local_time - server_time['serverTime'])
        
        print(f"Time difference: {time_diff}ms")
        
        if time_diff > 5000:  # 5 seconds
            print("❌ Time difference too large (>5s)")
            print("Sync your system clock!")
            return False
        else:
            print("✅ Time synchronization OK")
            
        return True
        
    except Exception as e:
        print(f"❌ Basic connectivity failed: {e}")
        return False

def test_authenticated_call():
    """Test authenticated API call"""
    print("\n=== Authentication Test ===")
    
    try:
        load_dotenv()
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        testnet = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
        
        if not api_key or not secret_key:
            print("❌ Missing API credentials")
            return False
        
        client = Client(api_key, secret_key, testnet=testnet)
        
        # Try the simplest authenticated call
        account = client.futures_account()
        
        print("✅ Authentication successful!")
        print(f"Account assets: {len(account.get('assets', []))}")
        
        # Check if account has any balance
        usdt_balance = None
        for asset in account.get('assets', []):
            if asset['asset'] == 'USDT':
                usdt_balance = float(asset['walletBalance'])
                break
        
        if usdt_balance:
            print(f"USDT Balance: {usdt_balance}")
        else:
            print("⚠️  No USDT balance found (normal for new testnet accounts)")
            
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        
        # Specific error analysis
        if "Signature for this request is not valid" in str(e):
            print("\n🔍 Signature Error Analysis:")
            print("1. Check API key and secret are correct")
            print("2. Ensure no extra spaces in .env file")
            print("3. Verify you're using testnet credentials for testnet")
            print("4. Check system time synchronization")
            
        elif "Invalid API-key" in str(e):
            print("\n🔍 Invalid API Key:")
            print("1. Verify API key is correct")
            print("2. Check if API key is for testnet (if using testnet)")
            print("3. Ensure API key has futures trading permissions")
            
        return False

def test_futures_permissions():
    """Test if API key has futures permissions"""
    print("\n=== Futures Permissions Test ===")
    
    try:
        load_dotenv()
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        testnet = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
        
        client = Client(api_key, secret_key, testnet=testnet)
        
        # Test futures-specific calls
        exchange_info = client.futures_exchange_info()
        print("✅ Futures API access confirmed")
        print(f"Available symbols: {len(exchange_info['symbols'])}")
        
        # Test if we can get market data
        ticker = client.futures_symbol_ticker(symbol='BTCUSDT')
        print(f"BTC Price: {ticker['price']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Futures permissions test failed: {e}")
        return False

def generate_test_credentials_guide():
    """Provide guide for getting testnet credentials"""
    print("\n=== How to Get Testnet Credentials ===")
    print("1. Go to: https://testnet.binancefuture.com/")
    print("2. Login with GitHub, Google, or create account")
    print("3. Go to API Management")
    print("4. Create New API Key")
    print("5. Enable 'Futures' permissions")
    print("6. Copy API Key and Secret Key to your .env file")
    print("\n📝 .env file format:")
    print("BINANCE_API_KEY=your_api_key_here")
    print("BINANCE_SECRET_KEY=your_secret_key_here")
    print("BINANCE_TESTNET=True")

def main():
    """Run all diagnostic tests"""
    print("🔍 Binance API Diagnostic Tool")
    print("=" * 40)
    
    tests = [
        check_environment,
        check_system_time,
        test_basic_connectivity,
        test_authenticated_call,
        test_futures_permissions
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            if not result and test != test_futures_permissions:  # Continue even if futures test fails
                break
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
            break
    
    print("\n" + "=" * 40)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 40)
    
    test_names = [
        "Environment Setup",
        "System Time", 
        "Basic Connectivity",
        "Authentication",
        "Futures Permissions"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    if not any(results[:4]):  # If first 4 tests fail
        print("\n🚨 CRITICAL ISSUES DETECTED")
        generate_test_credentials_guide()
    elif all(results[:4]):  # If first 4 pass
        print("\n✅ API Setup appears correct!")
        print("Your bot should work now.")
    else:
        print("\n⚠️  Some issues detected - check failed tests above")

if __name__ == "__main__":
    main()