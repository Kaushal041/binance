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
        price: Optional[float] = None,
        wait_for_execution: bool = True,
        timeout_seconds: float = 5
    ) -> dict[str, any]:
        """
        Place an order on Binance Futures Testnet with execution details.

        Binance Futures API returns immediately after order placement (Status: NEW)
        before the order is actually executed. This method:
        1. Places the order
        2. Waits briefly for async processing (0.5s)
        3. Fetches actual execution details
        4. For MARKET orders, polls for up to 5 seconds for execution completion

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            wait_for_execution: Wait for order to execute (default: True)
            timeout_seconds: Polling timeout for MARKET orders (default: 5)

        Returns:
            Order response data with actual execution details

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
                params["timeInForce"] = "GTC"
                params["price"] = price

            # Step 1: Place the order (returns immediately with Status: NEW)
            response = self.client.futures_create_order(**params)
            logger.info(f"Initial order response: Status={response.get('status')}, "
                       f"ExecutedQty={response.get('executedQty')}, "
                       f"AvgPrice={response.get('avgPrice')}")

            if not wait_for_execution:
                return response

            # Step 2: Wait 0.5 seconds for async processing
            time.sleep(0.5)

            # Step 3: Fetch actual execution details
            order_id = response.get("orderId")
            try:
                actual_response = self.client.futures_get_order(symbol=symbol, orderId=order_id)
                logger.info(f"Fetched order details: Status={actual_response.get('status')}, "
                           f"ExecutedQty={actual_response.get('executedQty')}, "
                           f"AvgPrice={actual_response.get('avgPrice')}")
                response = actual_response
            except (BinanceAPIException, BinanceRequestException, Exception) as e:
                logger.warning(f"Could not fetch order details: {str(e)}, using initial response")

            # Step 4: For MARKET orders, poll until execution completes
            if order_type == "MARKET" and wait_for_execution:
                response = self._wait_for_order_execution(
                    symbol=symbol,
                    order_id=order_id,
                    timeout_seconds=timeout_seconds
                )

            logger.info(f"Order completed: Status={response.get('status')}, "
                       f"ExecutedQty={response.get('executedQty')}, "
                       f"AvgPrice={response.get('avgPrice')}")
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

    def _wait_for_order_execution(
        self,
        symbol: str,
        order_id: int,
        timeout_seconds: float = 5,
        poll_interval: float = 0.5
    ) -> dict[str, any]:
        """
        Poll for MARKET order execution until completion or timeout.

        MARKET orders on Binance Futures are executed asynchronously.
        This method polls the order status repeatedly until:
        - executedQty > 0 (order has been filled)
        - status == 'FILLED' (order is fully filled)
        - timeout is reached

        Args:
            symbol: Trading pair symbol
            order_id: Order ID to monitor
            timeout_seconds: Maximum polling duration (default: 5)
            poll_interval: Time between polls in seconds (default: 0.5)

        Returns:
            Final order status data with execution details

        Raises:
            BinanceClientException: If polling fails (after retries)
        """
        start_time = time.time()
        elapsed = 0
        poll_count = 0

        while elapsed < timeout_seconds:
            try:
                poll_count += 1
                elapsed = time.time() - start_time

                order_status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
                executed_qty = float(order_status.get("executedQty", 0))
                status = order_status.get("status", "")

                logger.debug(
                    f"Poll #{poll_count} (elapsed: {elapsed:.2f}s): "
                    f"Status={status}, ExecutedQty={executed_qty}"
                )

                # Order is filled if status is FILLED or quantity was executed
                if status == "FILLED" or executed_qty > 0:
                    logger.info(
                        f"Order execution completed: "
                        f"Status={status}, ExecutedQty={executed_qty}, "
                        f"AvgPrice={order_status.get('avgPrice')}"
                    )
                    return order_status

                # Wait before next poll
                time.sleep(poll_interval)

            except (BinanceAPIException, BinanceRequestException) as e:
                logger.debug(f"Poll #{poll_count} API error: {str(e)}, retrying...")
                time.sleep(poll_interval)
            except Exception as e:
                logger.warning(f"Unexpected error during polling: {str(e)}")
                time.sleep(poll_interval)

        # Timeout reached - fetch final status and return it
        logger.warning(f"Order execution polling timed out after {timeout_seconds}s, fetching final status")
        try:
            final_order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logger.info(f"Final order status: Status={final_order.get('status')}, "
                       f"ExecutedQty={final_order.get('executedQty')}")
            return final_order
        except Exception as e:
            logger.error(f"Failed to fetch final order status: {str(e)}")
            raise BinanceClientException(f"Failed to fetch final order status: {str(e)}")

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
