"""
Binance Futures client wrapper for testnet trading.
Handles API communication with Binance Futures Testnet.
"""

import logging
import time
from typing import Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.retry import retry_with_backoff

logger = logging.getLogger("TradingBot")


class BinanceClientException(Exception):
    """Custom exception for Binance client errors."""
    pass


class BinanceClient:
    """
    Wrapper for Binance Futures Testnet API.
    Simplifies interaction with the exchange.
    """

    TESTNET_BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Binance Futures Testnet client.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret

        Raises:
            BinanceClientException: If credentials are invalid
        """
        if not api_key or not api_secret:
            raise BinanceClientException("API key and secret cannot be empty")

        logger.info("Initializing Binance Futures Testnet client")

        try:
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=True
            )
            logger.info("Binance Futures Testnet client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise BinanceClientException(f"Failed to initialize client: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test connection to Binance API.

        Returns:
            True if connection is successful

        Raises:
            BinanceClientException: If connection fails
        """
        try:
            logger.info("Testing connection to Binance API")
            self.client.futures_time()
            logger.info("Connection test successful")
            return True
        except BinanceAPIException as e:
            logger.error(f"Binance API error during connection test: {e.status_code} - {e.message}")
            raise BinanceClientException(f"API Error: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
            raise BinanceClientException(f"Connection test failed: {str(e)}")

    def get_balance(self) -> dict[str, any]:
        """
        Get account balance information.

        Returns:
            Account balance data

        Raises:
            BinanceClientException: If API call fails
        """
        try:
            logger.info("Fetching account balance")
            balance = self.client.balance()
            logger.info(f"Account balance fetched successfully: {balance}")
            return balance
        except BinanceAPIException as e:
            logger.error(f"Binance API error fetching balance: {e.status_code} - {e.message}")
            raise BinanceClientException(f"Failed to fetch balance: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error fetching balance: {str(e)}")
            raise BinanceClientException(f"Balance fetch failed: {str(e)}")

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> dict[str, any]:
        """
        Place an order on Binance Futures Testnet.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)

        Returns:
            Order response data

        Raises:
            BinanceClientException: If order placement fails
        """
        try:
            logger.info(
                f"Placing {order_type} {side} order: "
                f"Symbol={symbol}, Quantity={quantity}, Price={price}"
            )

            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
            }

            if order_type == "LIMIT" and price is not None:
                params["timeInForce"] = "GTC"  # Good-til-cancelled
                params["price"] = price

            response = self.client.futures_create_order(**params)

            logger.info(f"Order placed successfully: {response}")
            return response

        except BinanceAPIException as e:
            logger.error(
                f"Binance API error placing order: {e.status_code} - {e.message}"
            )
            raise BinanceClientException(f"Order placement failed: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise BinanceClientException(f"Request error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error placing order: {str(e)}")
            raise BinanceClientException(f"Order placement failed: {str(e)}")

    def get_order_status(self, symbol: str, order_id: int) -> dict[str, any]:
        """
        Get the status of an order.

        Args:
            symbol: Trading pair symbol
            order_id: Order ID

        Returns:
            Order status data

        Raises:
            BinanceClientException: If API call fails
        """
        try:
            logger.info(f"Fetching order status: Symbol={symbol}, OrderID={order_id}")
            status = self.client.query_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order status retrieved: {status}")
            return status
        except BinanceAPIException as e:
            logger.error(f"Binance API error fetching order status: {e.status_code} - {e.message}")
            raise BinanceClientException(f"Failed to fetch order status: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error fetching order status: {str(e)}")
            raise BinanceClientException(f"Order status fetch failed: {str(e)}")

    def cancel_order(self, symbol: str, order_id: int) -> dict[str, any]:
        """
        Cancel an open order.

        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel

        Returns:
            Cancellation response data

        Raises:
            BinanceClientException: If cancellation fails
        """
        try:
            logger.info(f"Cancelling order: Symbol={symbol}, OrderID={order_id}")
            response = self.client.cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order cancelled successfully: {response}")
            return response
        except BinanceAPIException as e:
            logger.error(f"Binance API error cancelling order: {e.status_code} - {e.message}")
            raise BinanceClientException(f"Order cancellation failed: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error cancelling order: {str(e)}")
            raise BinanceClientException(f"Order cancellation failed: {str(e)}")
