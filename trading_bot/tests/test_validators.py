"""Test input validators."""
import pytest
from bot.validators import OrderValidator, ValidationError
from bot.enums import OrderSide, OrderType


class TestSymbolValidation:
    """Test symbol validation."""

    def test_valid_symbol(self):
        """Test valid symbol."""
        assert OrderValidator.validate_symbol("BTCUSDT") == "BTCUSDT"

    def test_lowercase_conversion(self):
        """Test symbol converted to uppercase."""
        assert OrderValidator.validate_symbol("btcusdt") == "BTCUSDT"

    def test_empty_symbol(self):
        """Test empty symbol raises error."""
        with pytest.raises(ValidationError, match="Symbol cannot be empty"):
            OrderValidator.validate_symbol("")

    def test_short_symbol(self):
        """Test too short symbol raises error."""
        with pytest.raises(ValidationError, match="at least 4 characters"):
            OrderValidator.validate_symbol("BTC")

    def test_whitespace_stripped(self):
        """Test whitespace is stripped."""
        assert OrderValidator.validate_symbol("  BTCUSDT  ") == "BTCUSDT"


class TestSideValidation:
    """Test side validation."""

    def test_valid_buy(self):
        """Test BUY side."""
        result = OrderValidator.validate_side("BUY")
        assert result == OrderSide.BUY

    def test_valid_sell(self):
        """Test SELL side."""
        result = OrderValidator.validate_side("SELL")
        assert result == OrderSide.SELL

    def test_lowercase_conversion(self):
        """Test lowercase conversion."""
        assert OrderValidator.validate_side("buy") == OrderSide.BUY

    def test_invalid_side(self):
        """Test invalid side raises error."""
        with pytest.raises(ValidationError, match="must be BUY or SELL"):
            OrderValidator.validate_side("LONG")

    def test_empty_side(self):
        """Test empty side raises error."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            OrderValidator.validate_side("")


class TestOrderTypeValidation:
    """Test order type validation."""

    def test_valid_market(self):
        """Test MARKET type."""
        result = OrderValidator.validate_order_type("MARKET")
        assert result == OrderType.MARKET

    def test_valid_limit(self):
        """Test LIMIT type."""
        result = OrderValidator.validate_order_type("LIMIT")
        assert result == OrderType.LIMIT

    def test_invalid_type(self):
        """Test invalid type raises error."""
        with pytest.raises(ValidationError, match="must be MARKET or LIMIT"):
            OrderValidator.validate_order_type("STOP")


class TestQuantityValidation:
    """Test quantity validation."""

    def test_valid_quantity(self):
        """Test valid quantity."""
        assert OrderValidator.validate_quantity("0.001") == 0.001

    def test_string_to_float(self):
        """Test string conversion to float."""
        assert OrderValidator.validate_quantity("1.5") == 1.5

    def test_negative_quantity(self):
        """Test negative quantity raises error."""
        with pytest.raises(ValidationError, match="must be greater than 0"):
            OrderValidator.validate_quantity("-0.5")

    def test_zero_quantity(self):
        """Test zero quantity raises error."""
        with pytest.raises(ValidationError, match="must be greater than 0"):
            OrderValidator.validate_quantity("0")

    def test_invalid_number(self):
        """Test invalid number raises error."""
        with pytest.raises(ValidationError, match="must be a valid number"):
            OrderValidator.validate_quantity("invalid")

    def test_min_qty_constraint(self):
        """Test minimum quantity constraint."""
        with pytest.raises(ValidationError, match="Minimum quantity"):
            OrderValidator.validate_quantity("0.0001", "BTCUSDT")

    def test_max_qty_constraint(self):
        """Test maximum quantity constraint."""
        with pytest.raises(ValidationError, match="Maximum quantity"):
            OrderValidator.validate_quantity("99999", "BTCUSDT")


class TestPriceValidation:
    """Test price validation."""

    def test_market_ignores_price(self):
        """Test MARKET orders ignore price."""
        result = OrderValidator.validate_price("95000", OrderType.MARKET)
        assert result is None

    def test_market_with_none_price(self):
        """Test MARKET order without price."""
        result = OrderValidator.validate_price(None, OrderType.MARKET)
        assert result is None

    def test_limit_requires_price(self):
        """Test LIMIT orders require price."""
        with pytest.raises(ValidationError, match="required for LIMIT"):
            OrderValidator.validate_price(None, OrderType.LIMIT)

    def test_valid_limit_price(self):
        """Test valid LIMIT price."""
        result = OrderValidator.validate_price("95000.50", OrderType.LIMIT)
        assert result == 95000.50

    def test_negative_price(self):
        """Test negative price raises error."""
        with pytest.raises(ValidationError, match="must be greater than 0"):
            OrderValidator.validate_price("-95000", OrderType.LIMIT)

    def test_zero_price(self):
        """Test zero price raises error."""
        with pytest.raises(ValidationError, match="must be greater than 0"):
            OrderValidator.validate_price("0", OrderType.LIMIT)

    def test_invalid_price(self):
        """Test invalid price raises error."""
        with pytest.raises(ValidationError, match="must be a valid number"):
            OrderValidator.validate_price("invalid", OrderType.LIMIT)


class TestCombinedValidation:
    """Test combined validation."""

    def test_valid_market_order(self):
        """Test valid MARKET order validation."""
        sym, side, typ, qty, price = OrderValidator.validate_all(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
            price=None
        )
        assert sym == "BTCUSDT"
        assert side == OrderSide.BUY
        assert typ == OrderType.MARKET
        assert qty == 0.001
        assert price is None

    def test_valid_limit_order(self):
        """Test valid LIMIT order validation."""
        sym, side, typ, qty, price = OrderValidator.validate_all(
            symbol="ETHUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity="0.01",
            price="3500.50"
        )
        assert sym == "ETHUSDT"
        assert side == OrderSide.SELL
        assert typ == OrderType.LIMIT
        assert qty == 0.01
        assert price == 3500.50

    def test_invalid_parameters(self):
        """Test invalid parameters in combined validation."""
        with pytest.raises(ValidationError):
            OrderValidator.validate_all(
                symbol="",
                side="BUY",
                order_type="MARKET",
                quantity="0.001",
                price=None
            )
