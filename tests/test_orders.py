"""Test order management."""
import pytest
from bot.orders import OrderManager, OrderResult


class TestOrderParsing:
    """Test order response parsing."""

    def test_parse_valid_response(self):
        """Test parsing valid order response."""
        response = {
            'orderId': 123456,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'side': 'BUY',
            'type': 'MARKET',
            'executedQty': '0.001',
            'avgPrice': '95000.50'
        }
        result = OrderManager.parse_order_response(response)

        assert result.order_id == 123456
        assert result.symbol == 'BTCUSDT'
        assert result.status == 'FILLED'
        assert result.executed_quantity == 0.001
        assert result.average_price == 95000.50

    def test_parse_missing_field(self):
        """Test parsing with missing required field."""
        response = {
            'orderId': 123456,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'side': 'BUY',
            'type': 'MARKET',
            # Missing 'executedQty' and 'avgPrice'
        }
        with pytest.raises(ValueError):
            OrderManager.parse_order_response(response)

    def test_parse_invalid_quantity(self):
        """Test parsing with invalid quantity."""
        response = {
            'orderId': 123456,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'side': 'BUY',
            'type': 'MARKET',
            'executedQty': 'invalid',
            'avgPrice': '95000.50'
        }
        with pytest.raises(ValueError):
            OrderManager.parse_order_response(response)


class TestResponseValidation:
    """Test response validation."""

    def test_valid_response(self):
        """Test valid response validation."""
        response = {
            'orderId': 123456,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'side': 'BUY',
            'type': 'MARKET'
        }
        assert OrderManager.validate_response(response) is True

    def test_missing_field_validation(self):
        """Test validation with missing field."""
        response = {
            'orderId': 123456,
            'symbol': 'BTCUSDT',
            # Missing 'status'
        }
        with pytest.raises(ValueError, match="Missing required field"):
            OrderManager.validate_response(response)


class TestFormatting:
    """Test output formatting."""

    def test_format_price_valid(self):
        """Test price formatting."""
        assert OrderManager.format_price(95000.5) == "95,000.50"

    def test_format_price_none(self):
        """Test None price formatting."""
        assert OrderManager.format_price(None) == "N/A"

    def test_format_quantity(self):
        """Test quantity formatting."""
        assert OrderManager.format_quantity(0.001) == "0.0010"
        assert OrderManager.format_quantity(1.5) == "1.5000"
