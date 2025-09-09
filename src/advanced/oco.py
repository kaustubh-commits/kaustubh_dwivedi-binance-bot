from binance.client import Client
from binance.exceptions import BinanceAPIException
import time
from src.market_orders import MarketOrderManager
from src.bot_logger import setup_logger
from src.validator import OrderValidator
from src.config import Config

logger = setup_logger()

class OCOOrderManager:
    """Handle OCO (One-Cancels-the-Other) orders for Binance Futures."""
    
    def __init__(self):
        self.client = Client(
            Config.API_KEY,
            Config.SECRET_KEY,
            testnet=Config.TESTNET
        )
        self.validator = OrderValidator()
        self.active_oco_orders = {}
    
    def place_oco_order(self, symbol: str, side: str, quantity: float,
                        take_profit_price: float, stop_loss_price: float) -> dict:
        """
        Place an OCO order (Take Profit + Stop Loss).
        
        Args:
            symbol: Trading symbol
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            take_profit_price: Take profit price
            stop_loss_price: Stop loss price
            
        Returns:
            dict: OCO order response
        """
        try:
            # Validate inputs
            if not all([
                self.validator.validate_symbol(symbol),
                self.validator.validate_side(side),
                self.validator.validate_quantity(quantity),
                self.validator.validate_price(take_profit_price),
                self.validator.validate_price(stop_loss_price)
            ]):
                raise ValueError("Invalid order parameters")
            
            logger.info(f"Placing OCO order: {side} {quantity} {symbol} TP:{take_profit_price} SL:{stop_loss_price}")
            
            # Place take profit order
            tp_order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side='SELL' if side.upper() == 'BUY' else 'BUY',  # Opposite side for closing
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=take_profit_price
            )
            
            # Place stop loss order
            sl_order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side='SELL' if side.upper() == 'BUY' else 'BUY',  # Opposite side for closing
                type='STOP_MARKET',
                quantity=quantity,
                stopPrice=stop_loss_price
            )
            
            # Store OCO pair
            oco_id = f"OCO_{int(time.time())}"
            self.active_oco_orders[oco_id] = {
                'tp_order_id': tp_order['orderId'],
                'sl_order_id': sl_order['orderId'],
                'symbol': symbol.upper(),
                'quantity': quantity
            }
            
            logger.info(f"OCO order placed successfully: {oco_id}")
            return {
                'success': True,
                'oco_id': oco_id,
                'tp_order': tp_order,
                'sl_order': sl_order,
                'message': f"OCO order placed: {oco_id}"
            }
            
        except Exception as e:
            error_msg = f"Error placing OCO order: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def cancel_oco_order(self, oco_id: str) -> dict:
        """Cancel an OCO order pair."""
        try:
            if oco_id not in self.active_oco_orders:
                raise ValueError(f"OCO order {oco_id} not found")
            
            oco_data = self.active_oco_orders[oco_id]
            
            # Cancel both orders
            self.client.futures_cancel_order(
                symbol=oco_data['symbol'],
                orderId=oco_data['tp_order_id']
            )
            
            self.client.futures_cancel_order(
                symbol=oco_data['symbol'],
                orderId=oco_data['sl_order_id']
            )
            
            del self.active_oco_orders[oco_id]
            
            logger.info(f"OCO order {oco_id} cancelled successfully")
            return {'success': True, 'message': f"OCO order {oco_id} cancelled"}
            
        except Exception as e:
            error_msg = f"Error cancelling OCO order {oco_id}: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}