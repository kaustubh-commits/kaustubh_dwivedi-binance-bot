import re
from typing import Optional, Union
from decimal import Decimal, InvalidOperation

class OrderValidator:
    """Validator for trading orders with comprehensive validation rules."""
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_TYPES = ['MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET']
    VALID_TIME_IN_FORCE = ['GTC', 'IOC', 'FOK']
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Validate trading symbol format."""
        if not symbol or not isinstance(symbol, str):
            return False
        
        # Check if symbol follows USDT-M futures format (ends with USDT)
        pattern = r'^[A-Z0-9]+USDT$'
        return bool(re.match(pattern, symbol.upper()))
    
    @staticmethod
    def validate_quantity(quantity: Union[str, float, int]) -> bool:
        """Validate order quantity."""
        try:
            qty = Decimal(str(quantity))
            return qty > 0
        except (InvalidOperation, TypeError, ValueError):
            return False
    
    @staticmethod
    def validate_price(price: Union[str, float, int]) -> bool:
        """Validate order price."""
        try:
            p = Decimal(str(price))
            return p > 0
        except (InvalidOperation, TypeError, ValueError):
            return False
    
    @staticmethod
    def validate_side(side: str) -> bool:
        """Validate order side."""
        return side.upper() in OrderValidator.VALID_SIDES
    
    @staticmethod
    def validate_order_type(order_type: str) -> bool:
        """Validate order type."""
        return order_type.upper() in OrderValidator.VALID_TYPES
    
    @staticmethod
    def validate_time_in_force(tif: str) -> bool:
        """Validate time in force."""
        return tif.upper() in OrderValidator.VALID_TIME_IN_FORCE