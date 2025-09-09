from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from src.validator import OrderValidator
from src.bot_logger import setup_logger as sl
from src.config import Config

logger = sl()

class MarketOrderManager:
    """Handle market order operations for Binance Futures."""
    
    def __init__(self):
        self.client = Client(
            Config.API_KEY,
            Config.SECRET_KEY,
            testnet=Config.TESTNET
        )
        self.validator = OrderValidator()
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Place a market order.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            
        Returns:
            dict: Order response or error details
        """
        try:
            # Validate inputs
            if not self.validator.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if not self.validator.validate_side(side):
                raise ValueError(f"Invalid side: {side}. Must be BUY or SELL")
            
            if not self.validator.validate_quantity(quantity):
                raise ValueError(f"Invalid quantity: {quantity}")
            
            logger.info(f"Placing market order: {side} {quantity} {symbol}")
            
            # Place the order
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"Market order placed successfully: {order['orderId']}")
            return {
                'success': True,
                'order': order,
                'message': f"Market order placed: {order['orderId']}"
            }
            
        except BinanceAPIException as e:
            error_msg = f"Binance API Error: {e.message} (Code: {e.code})"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
            
        except BinanceOrderException as e:
            error_msg = f"Binance Order Error: {e.message} (Code: {e.code})"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_market_price(self, symbol: str) -> float:
        """Get current market price for a symbol."""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol.upper())
            return float(ticker['price'])
        except Exception as e:
            logger.error(f"Error getting market price for {symbol}: {e}")
            return None