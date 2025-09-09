import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('BINANCE_API_KEY')
    SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
    TESTNET = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
    
    # Binance endpoints
    if TESTNET:
        BASE_URL = 'https://testnet.binancefuture.com'
    else:
        BASE_URL = 'https://fapi.binance.com'