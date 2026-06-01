"""Order enums for type safety."""
from enum import Enum


class OrderSide(str, Enum):
    """Order side enumeration."""
    BUY = "BUY"
    SELL = "SELL"

    def __str__(self) -> str:
        return self.value


class OrderType(str, Enum):
    """Order type enumeration."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"

    def __str__(self) -> str:
        return self.value


class OrderStatus(str, Enum):
    """Order status enumeration."""
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    PENDING_CANCEL = "PENDING_CANCEL"

    def __str__(self) -> str:
        return self.value
