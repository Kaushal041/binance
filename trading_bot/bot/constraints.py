"""Order constraints for Binance Futures."""

# Symbol-specific constraints (simplified - real app fetches dynamically)
SYMBOL_CONSTRAINTS: dict[str, dict] = {
    'BTCUSDT': {
        'min_qty': 0.001,
        'max_qty': 10000,
        'qty_precision': 4,
        'price_precision': 2,
        'min_notional': 5,
    },
    'ETHUSDT': {
        'min_qty': 0.01,
        'max_qty': 10000,
        'qty_precision': 3,
        'price_precision': 2,
        'min_notional': 5,
    },
    'BNBUSDT': {
        'min_qty': 0.01,
        'max_qty': 10000,
        'qty_precision': 3,
        'price_precision': 2,
        'min_notional': 5,
    },
    'XRPUSDT': {
        'min_qty': 0.1,
        'max_qty': 100000,
        'qty_precision': 1,
        'price_precision': 5,
        'min_notional': 5,
    },
    'SOLUSDT': {
        'min_qty': 0.01,
        'max_qty': 10000,
        'qty_precision': 3,
        'price_precision': 2,
        'min_notional': 5,
    },
}
