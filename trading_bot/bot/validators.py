"""
Input validation module for trading orders.
Validates user input for order parameters.
"""

import logging
from typing import Optional
from bot.enums import OrderSide, OrderType
from bot.constraints import SYMBOL_CONSTRAINTS

logger = logging.getLogger("TradingBot")


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class OrderValidator:
    """Validates order parameters."""

    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)

        Returns:
            Validated symbol in uppercase

        Raises:
            ValidationError: If symbol is invalid

        Examples:
            >>> OrderValidator.validate_symbol("btcusdt")
            'BTCUSDT'
            >>> OrderValidator.validate_symbol("")
            Traceback (most recent call last):
                ...
            bot.validators.ValidationError: Symbol cannot be empty
        """
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol cannot be empty")

        symbol = symbol.upper().strip()

        if len(symbol) < 4:
            raise ValidationError("Symbol must be at least 4 characters long (e.g., BTCUSDT)")

        logger.info(f"Symbol validation passed: {symbol}")
        return symbol

    @staticmethod
    def validate_side(side: str) -> OrderSide:
        """
        Validate order side (BUY/SELL).

        Args:
            side: Order side (BUY or SELL)

        Returns:
            Validated OrderSide enum

        Raises:
            ValidationError: If side is invalid

        Examples:
            >>> OrderValidator.validate_side("buy")
            <OrderSide.BUY: 'BUY'>
            >>> OrderValidator.validate_side("LONG")
            Traceback (most recent call last):
                ...
            bot.validators.ValidationError: Side must be BUY or SELL
        """
        if not side or not isinstance(side, str):
            raise ValidationError("Side cannot be empty")

        try:
            side_enum = OrderSide(side.upper().strip())
            logger.info(f"Side validation passed: {side_enum.value}")
            return side_enum
        except ValueError:
            raise ValidationError(f"Side must be BUY or SELL, got {side}")

    @staticmethod
    def validate_order_type(order_type: str) -> OrderType:
        """
        Validate order type (MARKET/LIMIT).

        Args:
            order_type: Order type (MARKET or LIMIT)

        Returns:
            Validated OrderType enum

        Raises:
            ValidationError: If order type is invalid

        Examples:
            >>> OrderValidator.validate_order_type("market")
            <OrderType.MARKET: 'MARKET'>
            >>> OrderValidator.validate_order_type("STOP")
            Traceback (most recent call last):
                ...
            bot.validators.ValidationError: Order type must be MARKET or LIMIT
        """
        if not order_type or not isinstance(order_type, str):
            raise ValidationError("Order type cannot be empty")

        try:
            type_enum = OrderType(order_type.upper().strip())
            logger.info(f"Order type validation passed: {type_enum.value}")
            return type_enum
        except ValueError:
            raise ValidationError(f"Order type must be MARKET or LIMIT, got {order_type}")

    @staticmethod
    def validate_quantity(quantity: str, symbol: str = "") -> float:
        """
        Validate order quantity with symbol constraints.

        Args:
            quantity: Order quantity as string
            symbol: Trading symbol (optional, for constraint checking)

        Returns:
            Validated quantity as float

        Raises:
            ValidationError: If quantity is invalid

        Examples:
            >>> OrderValidator.validate_quantity("0.001")
            0.001
            >>> OrderValidator.validate_quantity("-0.5")
            Traceback (most recent call last):
                ...
            bot.validators.ValidationError: Quantity must be greater than 0
        """
        try:
            qty = float(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Quantity must be a valid number, got {quantity}")

        if qty <= 0:
            raise ValidationError(f"Quantity must be greater than 0, got {qty}")

        # Check symbol constraints if available
        if symbol and symbol in SYMBOL_CONSTRAINTS:
            constraints = SYMBOL_CONSTRAINTS[symbol]
            if qty < constraints['min_qty']:
                raise ValidationError(
                    f"Minimum quantity for {symbol} is {constraints['min_qty']}"
                )
            if qty > constraints['max_qty']:
                raise ValidationError(
                    f"Maximum quantity for {symbol} is {constraints['max_qty']}"
                )

            # Check precision
            qty_str = str(qty)
            if '.' in qty_str:
                decimals = len(qty_str.split('.')[1])
                if decimals > constraints['qty_precision']:
                    raise ValidationError(
                        f"{symbol} allows max {constraints['qty_precision']} "
                        f"decimal places, got {decimals}"
                    )

        logger.info(f"Quantity validation passed: {qty}")
        return qty

    @staticmethod
    def validate_price(
        price: Optional[str],
        order_type: OrderType,
        symbol: str = ""
    ) -> Optional[float]:
        """
        Validate order price with symbol constraints.

        Args:
            price: Order price as string (required for LIMIT orders)
            order_type: Order type (MARKET or LIMIT)
            symbol: Trading symbol (optional, for constraint checking)

        Returns:
            Validated price as float, or None for MARKET orders

        Raises:
            ValidationError: If price is invalid

        Examples:
            >>> OrderValidator.validate_price(None, OrderType.MARKET)

            >>> OrderValidator.validate_price("95000.50", OrderType.LIMIT)
            95000.5
            >>> OrderValidator.validate_price(None, OrderType.LIMIT)
            Traceback (most recent call last):
                ...
            bot.validators.ValidationError: Price required for LIMIT orders
        """
        if order_type == OrderType.MARKET:
            if price is not None:
                logger.warning("Price provided for MARKET order, will be ignored")
            return None

        if order_type == OrderType.LIMIT:
            if price is None:
                raise ValidationError("Price required for LIMIT orders")

            try:
                p = float(price)
            except (ValueError, TypeError):
                raise ValidationError(f"Price must be a valid number, got {price}")

            if p <= 0:
                raise ValidationError(f"Price must be greater than 0, got {p}")

            # Check symbol constraints if available
            if symbol and symbol in SYMBOL_CONSTRAINTS:
                constraints = SYMBOL_CONSTRAINTS[symbol]

                # Check precision
                price_str = str(p)
                if '.' in price_str:
                    decimals = len(price_str.split('.')[1])
                    if decimals > constraints['price_precision']:
                        raise ValidationError(
                            f"{symbol} allows max {constraints['price_precision']} "
                            f"decimal places for price, got {decimals}"
                        )

            logger.info(f"Price validation passed: {p}")
            return p

        return None

    @staticmethod
    def validate_all(
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: Optional[str] = None
    ) -> tuple[str, OrderSide, OrderType, float, Optional[float]]:
        """
        Validate all order parameters.

        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (optional, required for LIMIT)

        Returns:
            Tuple of validated parameters

        Raises:
            ValidationError: If any parameter is invalid

        Examples:
            >>> sym, s, t, qty, p = OrderValidator.validate_all(
            ...     "BTCUSDT", "BUY", "MARKET", "0.001", None
            ... )
            >>> sym
            'BTCUSDT'
            >>> qty
            0.001
        """
        validated_symbol = OrderValidator.validate_symbol(symbol)
        validated_side = OrderValidator.validate_side(side)
        validated_order_type = OrderValidator.validate_order_type(order_type)
        validated_quantity = OrderValidator.validate_quantity(quantity, validated_symbol)
        validated_price = OrderValidator.validate_price(price, validated_order_type, validated_symbol)

        return (
            validated_symbol,
            validated_side,
            validated_order_type,
            validated_quantity,
            validated_price
        )

