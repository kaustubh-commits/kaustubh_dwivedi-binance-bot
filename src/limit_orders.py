from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from src.validator import OrderValidator
from src.bot_logger import setup_logger
from src.config import Config

logger = setup_logger()

class LimitOrderManager:
    """Handle limit order operations for Binance Futures."""
    
    def __init__(self):
        self.client = Client(
            Config.API_KEY,
            Config.SECRET_KEY,
            testnet=Config.TESTNET
        )
        self.validator = OrderValidator()
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                          price: float, time_in_force: str = 'GTC') -> dict:
        """
        Place a limit order.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            time_in_force: 'GTC', 'IOC', or 'FOK'
            
        Returns:
            dict: Order response or error details
        """
        try:
            # Validate inputs
            if not self.validator.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if not self.validator.validate_side(side):
                raise ValueError(f"Invalid side: {side}")
            
            if not self.validator.validate_quantity(quantity):
                raise ValueError(f"Invalid quantity: {quantity}")
                
            if not self.validator.validate_price(price):
                raise ValueError(f"Invalid price: {price}")
                
            if not self.validator.validate_time_in_force(time_in_force):
                raise ValueError(f"Invalid time in force: {time_in_force}")
            
            logger.info(f"Placing limit order: {side} {quantity} {symbol} @ {price}")
            
            # Place the order
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                timeInForce=time_in_force.upper(),
                quantity=quantity,
                price=price
            )
            
            logger.info(f"Limit order placed successfully: {order['orderId']}")
            return {
                'success': True,
                'order': order,
                'message': f"Limit order placed: {order['orderId']}"
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
    
    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancel a limit order."""
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
            logger.info(f"Order {order_id} cancelled successfully")
            return {'success': True, 'result': result}
        except Exception as e:
            error_msg = f"Error cancelling order {order_id}: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}