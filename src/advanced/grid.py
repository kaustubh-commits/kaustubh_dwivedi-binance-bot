import time
from decimal import Decimal
from src.market_orders import MarketOrderManager
from src.bot_logger import setup_logger
from src.validator import OrderValidator
from src.limit_orders import LimitOrderManager

logger = setup_logger()

class GridOrderManager:
    """Handle Grid trading orders for automated buy-low/sell-high within a price range."""
    
    def __init__(self):
        self.limit_manager = LimitOrderManager()
        self.validator = OrderValidator()
        self.active_grids = {}
    
    def create_grid_orders(self, symbol: str, lower_price: float, upper_price: float,
                          grid_levels: int, quantity_per_level: float) -> dict:
        """
        Create grid orders within a specified price range.
        
        Args:
            symbol: Trading symbol
            lower_price: Lower boundary of the grid
            upper_price: Upper boundary of the grid
            grid_levels: Number of price levels in the grid
            quantity_per_level: Quantity for each grid level
            
        Returns:
            dict: Grid creation response
        """
        try:
            # Validate inputs
            if not all([
                self.validator.validate_symbol(symbol),
                self.validator.validate_price(lower_price),
                self.validator.validate_price(upper_price),
                self.validator.validate_quantity(quantity_per_level)
            ]):
                raise ValueError("Invalid grid parameters")
            
            if lower_price >= upper_price:
                raise ValueError("Lower price must be less than upper price")
            
            if grid_levels < 2:
                raise ValueError("Grid levels must be at least 2")
            
            grid_id = f"GRID_{int(time.time())}"
            
            # Calculate price step
            price_step = (upper_price - lower_price) / (grid_levels - 1)
            
            logger.info(f"Creating grid {grid_id}: {symbol} from {lower_price} to {upper_price} with {grid_levels} levels")
            
            buy_orders = []
            sell_orders = []
            
            # Create buy orders (lower half of the grid)
            for i in range(grid_levels // 2):
                price = lower_price + (i * price_step)
                result = self.limit_manager.place_limit_order(
                    symbol=symbol,
                    side='BUY',
                    quantity=quantity_per_level,
                    price=price
                )
                
                if result['success']:
                    buy_orders.append({
                        'order_id': result['order']['orderId'],
                        'price': price,
                        'quantity': quantity_per_level
                    })
                    logger.info(f"Grid buy order placed at {price}")
            
            # Create sell orders (upper half of the grid)
            for i in range(grid_levels // 2, grid_levels):
                price = lower_price + (i * price_step)
                result = self.limit_manager.place_limit_order(
                    symbol=symbol,
                    side='SELL',
                    quantity=quantity_per_level,
                    price=price
                )
                
                if result['success']:
                    sell_orders.append({
                        'order_id': result['order']['orderId'],
                        'price': price,
                        'quantity': quantity_per_level
                    })
                    logger.info(f"Grid sell order placed at {price}")
            
            # Store grid data
            self.active_grids[grid_id] = {
                'symbol': symbol,
                'lower_price': lower_price,
                'upper_price': upper_price,
                'grid_levels': grid_levels,
                'quantity_per_level': quantity_per_level,
                'price_step': price_step,
                'buy_orders': buy_orders,
                'sell_orders': sell_orders,
                'active': True,
                'created_at': time.time()
            }
            
            logger.info(f"Grid {grid_id} created successfully with {len(buy_orders)} buy and {len(sell_orders)} sell orders")
            
            return {
                'success': True,
                'grid_id': grid_id,
                'buy_orders_count': len(buy_orders),
                'sell_orders_count': len(sell_orders),
                'message': f"Grid {grid_id} created successfully"
            }
            
        except Exception as e:
            error_msg = f"Error creating grid orders: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def cancel_grid_orders(self, grid_id: str) -> dict:
        """Cancel all orders in a grid."""
        try:
            if grid_id not in self.active_grids:
                raise ValueError(f"Grid {grid_id} not found")
            
            grid_data = self.active_grids[grid_id]
            cancelled_orders = 0
            
            # Cancel buy orders
            for order in grid_data['buy_orders']:
                result = self.limit_manager.cancel_order(
                    symbol=grid_data['symbol'],
                    order_id=order['order_id']
                )
                if result['success']:
                    cancelled_orders += 1
            
            # Cancel sell orders
            for order in grid_data['sell_orders']:
                result = self.limit_manager.cancel_order(
                    symbol=grid_data['symbol'],
                    order_id=order['order_id']
                )
                if result['success']:
                    cancelled_orders += 1
            
            grid_data['active'] = False
            
            logger.info(f"Grid {grid_id} cancelled - {cancelled_orders} orders cancelled")
            return {
                'success': True,
                'cancelled_orders': cancelled_orders,
                'message': f"Grid {grid_id} cancelled"
            }
            
        except Exception as e:
            error_msg = f"Error cancelling grid {grid_id}: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def get_grid_status(self, grid_id: str) -> dict:
        """Get status of a grid."""
        if grid_id not in self.active_grids:
            return {'success': False, 'error': f"Grid {grid_id} not found"}
        
        return {
            'success': True,
            'grid_id': grid_id,
            'status': self.active_grids[grid_id]
        }