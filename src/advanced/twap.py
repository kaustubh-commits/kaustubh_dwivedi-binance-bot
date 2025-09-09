import time
import threading
from datetime import datetime, timedelta
from src.market_orders import MarketOrderManager
from src.bot_logger import setup_logger
from src.validator import OrderValidator

logger = setup_logger()

class TWAPOrderManager:
    """Handle TWAP (Time-Weighted Average Price) orders."""
    
    def __init__(self):
        self.market_manager = MarketOrderManager()
        self.validator = OrderValidator()
        self.active_twap_orders = {}
    
    def place_twap_order(self, symbol: str, side: str, total_quantity: float,
                         duration_minutes: int, interval_seconds: int = 60) -> dict:
        """
        Place a TWAP order that splits large orders into smaller chunks over time.
        
        Args:
            symbol: Trading symbol
            side: 'BUY' or 'SELL'
            total_quantity: Total quantity to trade
            duration_minutes: Duration over which to execute the order
            interval_seconds: Interval between each order execution
            
        Returns:
            dict: TWAP order response
        """
        try:
            # Validate inputs
            if not all([
                self.validator.validate_symbol(symbol),
                self.validator.validate_side(side),
                self.validator.validate_quantity(total_quantity)
            ]):
                raise ValueError("Invalid TWAP parameters")
            
            if duration_minutes <= 0 or interval_seconds <= 0:
                raise ValueError("Duration and interval must be positive")
            
            # Calculate order parameters
            total_intervals = (duration_minutes * 60) // interval_seconds
            quantity_per_order = total_quantity / total_intervals
            
            twap_id = f"TWAP_{int(time.time())}"
            
            logger.info(f"Starting TWAP order: {twap_id} - {side} {total_quantity} {symbol} over {duration_minutes}m")
            
            # Store TWAP data
            self.active_twap_orders[twap_id] = {
                'symbol': symbol,
                'side': side,
                'total_quantity': total_quantity,
                'quantity_per_order': quantity_per_order,
                'total_intervals': total_intervals,
                'interval_seconds': interval_seconds,
                'executed_quantity': 0,
                'executed_orders': 0,
                'active': True,
                'start_time': datetime.now()
            }
            
            # Start TWAP execution in a separate thread
            thread = threading.Thread(
                target=self._execute_twap,
                args=(twap_id,),
                daemon=True
            )
            thread.start()
            
            return {
                'success': True,
                'twap_id': twap_id,
                'message': f"TWAP order started: {twap_id}",
                'total_intervals': total_intervals,
                'quantity_per_order': quantity_per_order
            }
            
        except Exception as e:
            error_msg = f"Error placing TWAP order: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def _execute_twap(self, twap_id: str):
        """Execute TWAP order in intervals."""
        twap_data = self.active_twap_orders[twap_id]
        
        try:
            while twap_data['active'] and twap_data['executed_orders'] < twap_data['total_intervals']:
                # Place market order for this interval
                result = self.market_manager.place_market_order(
                    symbol=twap_data['symbol'],
                    side=twap_data['side'],
                    quantity=twap_data['quantity_per_order']
                )
                
                if result['success']:
                    twap_data['executed_quantity'] += twap_data['quantity_per_order']
                    twap_data['executed_orders'] += 1
                    
                    logger.info(f"TWAP {twap_id} - Executed order {twap_data['executed_orders']}/{twap_data['total_intervals']}")
                else:
                    logger.error(f"TWAP {twap_id} - Failed to execute order: {result['error']}")
                
                # Wait for next interval
                if twap_data['executed_orders'] < twap_data['total_intervals']:
                    time.sleep(twap_data['interval_seconds'])
            
            logger.info(f"TWAP {twap_id} completed - Executed {twap_data['executed_quantity']} total")
            twap_data['active'] = False
            
        except Exception as e:
            logger.error(f"Error in TWAP execution {twap_id}: {e}")
            twap_data['active'] = False
    
    def cancel_twap_order(self, twap_id: str) -> dict:
        """Cancel an active TWAP order."""
        try:
            if twap_id not in self.active_twap_orders:
                raise ValueError(f"TWAP order {twap_id} not found")
            
            self.active_twap_orders[twap_id]['active'] = False
            
            logger.info(f"TWAP order {twap_id} cancelled")
            return {'success': True, 'message': f"TWAP order {twap_id} cancelled"}
            
        except Exception as e:
            error_msg = f"Error cancelling TWAP order {twap_id}: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_twap_status(self, twap_id: str) -> dict:
        """Get status of a TWAP order."""
        if twap_id not in self.active_twap_orders:
            return {'success': False, 'error': f"TWAP order {twap_id} not found"}
        
        twap_data = self.active_twap_orders[twap_id]
        return {
            'success': True,
            'twap_id': twap_id,
            'status': twap_data
        }