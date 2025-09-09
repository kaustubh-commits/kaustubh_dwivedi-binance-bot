# Binance Futures Trading Bot

A comprehensive CLI-based trading bot for Binance USDT-M Futures that supports multiple order types with robust logging, validation, and advanced trading strategies.
## 🚀 Features
### Core Orders (Mandatory)

### Market Orders: 
Execute immediate buy/sell orders at current market prices  
### Limit Orders: 
Place orders at specific price levels with customizable time-in-force options  

## Advanced Orders (Bonus Implementation)

### OCO Orders (One-Cancels-the-Other): 
Simultaneously place take-profit and stop-loss orders  
### TWAP Orders (Time-Weighted Average Price): 
Split large orders into smaller chunks executed over time  
### Grid Orders: 
Automated buy-low/sell-high strategy within a specified price range  

# Additional Features

✅ Comprehensive input validation (symbol format, quantities, prices)  
✅ Structured logging with timestamps and error traces  
✅ Colorized CLI output for better user experience  
✅ Testnet support for safe testing  
✅ Modular architecture for easy extension  

# 📁 Project Structure
```bash
binance-futures-bot/
│
├── src/                        # Source code directory
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # Main CLI interface
│   ├── config.py               # Configuration management
│   ├── validator.py            # Input validation utilities
│   ├── bot_logger.py           # Logging configuration
│   ├── market_orders.py        # Market order operations
│   ├── limit_orders.py         # Limit order operations
│   └── advanced/               # Advanced trading strategies
│       ├── __init__.py
│       ├── oco.py              # OCO order implementation
│       ├── twap.py             # TWAP strategy
│       └── grid.py             # Grid trading strategy
│
├── logs/                       # Log files (auto-generated)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not included)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

# 🛠️ Setup Instructions
1. Clone the Repository
bashgit clone https://github.com/[username]/binance-futures-bot.git
cd binance-futures-bot  
2. Install Dependencies
bashpip install -r requirements.txt  
3. API Configuration
Create a .env file in the project root:
envBINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=True  
Important Security Notes:

Never commit your .env file to version control  
Use testnet for development and testing  
Ensure your API keys have only futures trading permissions  
Use IP restrictions on your Binance API keys  

4. API Key Setup

Visit Binance API Management  
Create a new API key  
Enable "Enable Futures" permission  
Restrict to your IP address for security  
For testing, use Binance Testnet  

##  🎯 Usage Examples
Basic Market Orders  
bash# Buy 0.001 BTC at market price  
python src/cli.py market buy BTCUSDT 0.001  

Sell 0.001 BTC at market price  
python src/cli.py market sell BTCUSDT 0.001  
Limit Orders  
bash# Place a buy limit order  
python src/cli.py limit buy BTCUSDT 0.001 45000.00  

Place a sell limit order with IOC time-in-force  
python src/cli.py limit sell BTCUSDT 0.001 50000.00 --tif IOC  

Cancel a limit order  
python src/cli.py limit cancel BTCUSDT 123456789  

Advanced Orders  
OCO Orders (Take Profit + Stop Loss)  
bash# Place OCO order with take profit at 50000 and stop loss at 40000  
python src/cli.py advanced oco BTCUSDT BUY 0.001 50000.00 40000.00  

TWAP Orders  
bash# Execute 0.01 BTC over 60 minutes with 1-minute intervals  
python src/cli.py advanced twap BTCUSDT BUY 0.01 60 --interval 60  

Grid Trading  
bash# Create grid orders between 40000-50000 with 5 levels, 0.001 per level  
python src/cli.py advanced grid BTCUSDT 40000.00 50000.00 5 0.001  

# 📊 Logging System
The bot generates structured logs in the logs/ directory:

File Format: bot_YYYYMMDD.log  
Log Levels: DEBUG, INFO, WARNING, ERROR  
Console Output: INFO level and above  
File Output: All levels including detailed traces  

Sample Log Entry  
2024-01-15 14:30:25 - binance_bot - INFO - place_market_order:45 - Market order placed successfully: 123456789  
## 🔍 Input Validation  
The bot includes comprehensive validation for:  

Symbol Format: USDT-M futures format (e.g., BTCUSDT, ETHUSDT)  
Quantities: Positive decimal numbers  
Prices: Positive decimal numbers  
Order Sides: BUY/SELL validation  
Time in Force: GTC/IOC/FOK validation  

⚠️ Error Handling  
Robust error handling for:  

Binance API exceptions  
Network connectivity issues  
Invalid parameters  
Insufficient balance  
Order execution failures  

# 🧪 Testing  
Testnet Configuration  
Set BINANCE_TESTNET=True in your .env file to use Binance testnet for safe testing.  
Test Scenarios  

Basic Orders: Test market and limit orders with small amounts  
Advanced Strategies: Verify OCO, TWAP, and Grid order functionality  
Error Cases: Test with invalid symbols, quantities, and network issues  
Logging: Verify all actions are properly logged  

# 🔒 Security Best Practices  

### API Key Management:  

Use environment variables  
Never hardcode keys in source code  
Enable IP restrictions  
Use minimal required permissions  


### Testnet First:  

Always test on testnet before live trading  
Verify all strategies with paper trading  


### Risk Management:  

Set appropriate position sizes  
Use stop-loss orders  
Monitor account balance regularly  



# 📈 Performance Considerations  

Rate Limits: Built-in respect for Binance API rate limits  
Threading: TWAP orders use background threads for execution  
Memory Usage: Efficient order tracking and cleanup  
Network Optimization: Minimal API calls with proper error retry  

# 🐛 Troubleshooting  
Common Issues  

API Key Errors:  
Error: Invalid API key or secret  
Solution: Verify .env file configuration and key permissions  

Symbol Not Found:  
Error: Invalid symbol format  
Solution: Use USDT-M futures symbols (e.g., BTCUSDT)  

Insufficient Balance:  
Error: Account has insufficient balance  
Solution: Check account balance and reduce order quantity  


# 📚 Dependencies  

python-binance: Official Binance API client  
click: Command-line interface framework  
colorama: Colored terminal output  
python-dotenv: Environment variable management  

# 🤝 Contributing  

Fork the repository  
Create a feature branch  
Implement changes with proper tests  
Update documentation  
Submit a pull request  
 
# 📄 License   
This project is for educational purposes. Please ensure compliance with local trading regulations.  
⚠️ Disclaimer  
IMPORTANT: This bot is for educational purposes only. Cryptocurrency trading involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software. Always test thoroughly on testnet before live trading and never risk more than you can afford to lose.  

📞 Support  
For questions or issues:  
 
Review this README for common solutions  
Test on Binance testnet first  
Ensure API keys have correct permissions  


Happy Trading! 🚀  
