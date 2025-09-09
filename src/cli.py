import click
from colorama import Fore, Style, init
from src.market_orders import MarketOrderManager
from src.limit_orders import LimitOrderManager
from src.advanced.oco  import OCOOrderManager
from src.advanced.twap import TWAPOrderManager
from src.advanced.grid import GridOrderManager
from src.bot_logger import setup_logger

# Initialize colorama for colored output
init(autoreset=True)
logger = setup_logger()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Binance Futures Trading Bot - CLI Interface"""
    click.echo(f"{Fore.CYAN}{'='*50}")
    click.echo(f"{Fore.CYAN}🚀 Binance Futures Trading Bot")
    click.echo(f"{Fore.CYAN}{'='*50}")

@cli.group()
def market():
    """Market order operations"""
    pass

@cli.group()
def limit():
    """Limit order operations"""
    pass

@cli.group()
def advanced():
    """Advanced order operations"""
    pass

# Market order commands
@market.command('buy')
@click.argument('symbol')
@click.argument('quantity', type=float)
def market_buy(symbol, quantity):
    """Place a market buy order"""
    manager = MarketOrderManager()
    result = manager.place_market_order(symbol, 'BUY', quantity)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

@market.command('sell')
@click.argument('symbol')
@click.argument('quantity', type=float)
def market_sell(symbol, quantity):
    """Place a market sell order"""
    manager = MarketOrderManager()
    result = manager.place_market_order(symbol, 'SELL', quantity)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

# Limit order commands
@limit.command('buy')
@click.argument('symbol')
@click.argument('quantity', type=float)
@click.argument('price', type=float)
@click.option('--tif', default='GTC', help='Time in force (GTC/IOC/FOK)')
def limit_buy(symbol, quantity, price, tif):
    """Place a limit buy order"""
    manager = LimitOrderManager()
    result = manager.place_limit_order(symbol, 'BUY', quantity, price, tif)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

@limit.command('sell')
@click.argument('symbol')
@click.argument('quantity', type=float)
@click.argument('price', type=float)
@click.option('--tif', default='GTC', help='Time in force (GTC/IOC/FOK)')
def limit_sell(symbol, quantity, price, tif):
    """Place a limit sell order"""
    manager = LimitOrderManager()
    result = manager.place_limit_order(symbol, 'SELL', quantity, price, tif)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

@limit.command('cancel')
@click.argument('symbol')
@click.argument('order_id', type=int)
def limit_cancel(symbol, order_id):
    """Cancel a pending limit order"""
    manager = LimitOrderManager()
    result = manager.cancel_order(symbol, order_id)

    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

# Advanced order commands
@advanced.command('oco')
@click.argument('symbol')
@click.argument('side')
@click.argument('quantity', type=float)
@click.argument('take_profit_price', type=float)
@click.argument('stop_loss_price', type=float)
def place_oco(symbol, side, quantity, take_profit_price, stop_loss_price):
    """Place an OCO (Take Profit + Stop Loss) order pair"""
    manager = OCOOrderManager()
    result = manager.place_oco_order(symbol, side, quantity, take_profit_price, stop_loss_price)

    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
        click.echo(f"{Fore.GREEN}   TP Order ID: {result['tp_order']['orderId']}")
        click.echo(f"{Fore.GREEN}   SL Order ID: {result['sl_order']['orderId']}")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

@advanced.command('twap')
@click.argument('symbol')
@click.argument('side')
@click.argument('total_quantity', type=float)
@click.argument('duration_minutes', type=int)
@click.option('--interval', default=60, type=int, help='Interval between orders in seconds')
def place_twap(symbol, side, total_quantity, duration_minutes, interval):
    """Place a TWAP (Time-Weighted Average Price) order"""
    manager = TWAPOrderManager()
    result = manager.place_twap_order(symbol, side, total_quantity, duration_minutes, interval)

    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
        click.echo(f"{Fore.YELLOW}   Will place {result['total_intervals']} orders of {result['quantity_per_order']:.4f} each.")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

@advanced.command('grid')
@click.argument('symbol')
@click.argument('lower_price', type=float)
@click.argument('upper_price', type=float)
@click.argument('grid_levels', type=int)
@click.argument('quantity_per_level', type=float)
def place_grid(symbol, lower_price, upper_price, grid_levels, quantity_per_level):
    """Create a grid trading strategy"""
    manager = GridOrderManager()
    result = manager.create_grid_orders(symbol, lower_price, upper_price, grid_levels, quantity_per_level)

    if result['success']:
        click.echo(f"{Fore.GREEN}✅ {result['message']}")
        click.echo(f"{Fore.GREEN}   Created {result['buy_orders_count']} buy orders and {result['sell_orders_count']} sell orders.")
    else:
        click.echo(f"{Fore.RED}❌ {result['error']}")

if __name__ == "__main__":
    import sys
    print("DEBUG: cli.py is running with args:", sys.argv)  # Debug check
    cli()