"""
Trading bot package.

A production-grade Binance Futures Testnet trading bot with
validation, error handling, and logging.
"""

from bot.logging_config import setup_logging
from bot.validators import OrderValidator, ValidationError
from bot.client import BinanceClient, BinanceClientException
from bot.orders import OrderManager, OrderSummary, OrderResult
from bot.enums import OrderSide, OrderType, OrderStatus
from bot.constraints import SYMBOL_CONSTRAINTS
from bot.retry import retry_with_backoff

__all__ = [
    "setup_logging",
    "OrderValidator",
    "ValidationError",
    "BinanceClient",
    "BinanceClientException",
    "OrderManager",
    "OrderSummary",
    "OrderResult",
    "OrderSide",
    "OrderType",
    "OrderStatus",
    "SYMBOL_CONSTRAINTS",
    "retry_with_backoff",
]

__version__ = "2.0.0"
__author__ = "Senior Technical Team"

