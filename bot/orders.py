"""
Order management module for trading operations.
Handles order execution and result formatting.
"""

from __future__ import annotations

import logging
from typing import Optional, Any
from dataclasses import dataclass

logger = logging.getLogger("TradingBot")


@dataclass
class OrderSummary:
    """Represents an order summary."""
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "symbol": self.symbol,
            "side": self.side,
            "order_type": self.order_type,
            "quantity": self.quantity,
            "price": self.price,
        }


@dataclass
class OrderResult:
    """Represents an order result from the API."""
    order_id: int
    symbol: str
    status: str
    executed_quantity: float
    average_price: float
    side: str
    order_type: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "status": self.status,
            "executed_quantity": self.executed_quantity,
            "average_price": self.average_price,
            "side": self.side,
            "order_type": self.order_type,
        }


class OrderManager:
    """Manages order operations and formatting."""

    @staticmethod
    def create_summary(
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> OrderSummary:
        """
        Create an order summary.

        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (optional)

        Returns:
            OrderSummary object
        """
        logger.info(f"Creating order summary: {symbol} {side} {order_type}")
        return OrderSummary(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

    @staticmethod
    def parse_order_response(response: dict[str, any]) -> OrderResult:
        """
        Parse Binance API order response.

        Args:
            response: Order response from Binance API

        Returns:
            OrderResult object

        Raises:
            ValueError: If response format is invalid
        """
        try:
            logger.info(f"Parsing order response: {response}")

            # Validate required fields
            required_fields = ['orderId', 'symbol', 'status', 'side', 'type', 'executedQty', 'avgPrice']
            for field in required_fields:
                if field not in response:
                    raise KeyError(f"Missing required field: {field}")

            executed_qty = float(response.get("executedQty", 0))
            average_price = float(response.get("avgPrice", 0))

            result = OrderResult(
                order_id=response.get("orderId"),
                symbol=response.get("symbol"),
                status=response.get("status"),
                executed_quantity=executed_qty,
                average_price=average_price,
                side=response.get("side"),
                order_type=response.get("type"),
            )

            logger.info(f"Order response parsed successfully: {result}")
            return result

        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing order response: {str(e)}")
            raise ValueError(f"Invalid order response format: {str(e)}")

    @staticmethod
    def validate_response(response: dict[str, Any]) -> bool:
        """
        Validate order response from Binance.

        Args:
            response: Order response data

        Returns:
            True if response is valid

        Raises:
            ValueError: If response is invalid
        """
        required_fields = ["orderId", "symbol", "status", "side", "type"]

        for field in required_fields:
            if field not in response:
                raise ValueError(f"Missing required field in response: {field}")

        logger.info("Order response validation passed")
        return True

    @staticmethod
    def format_price(price: Optional[float]) -> str:
        """
        Format price for display.

        Args:
            price: Price value

        Returns:
            Formatted price string
        """
        if price is None:
            return "N/A"
        return f"{price:,.2f}"

    @staticmethod
    def format_quantity(quantity: float) -> str:
        """
        Format quantity for display.

        Args:
            quantity: Quantity value

        Returns:
            Formatted quantity string
        """
        return f"{quantity:.4f}"
