#!/usr/bin/env python3
"""
CLI interface for the Binance Futures Trading Bot.
Provides command-line argument parsing and user interaction.
"""

from __future__ import annotations

import argparse
import sys
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot import (
    setup_logging,
    OrderValidator,
    ValidationError,
    BinanceClient,
    BinanceClientException,
    OrderManager,
)


# Initialize Rich console for colored output
console = Console()

# Load environment variables
load_dotenv()


def setup_argparse() -> argparse.ArgumentParser:
    """
    Set up argument parser for CLI.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Binance Futures Trading Bot (Testnet)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a MARKET BUY order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Place a LIMIT SELL order
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 110000

  # Place an ETH order
  python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.01
        """
    )

    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
    )

    parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )

    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT"
    )

    parser.add_argument(
        "--quantity",
        type=str,
        required=True,
        help="Order quantity (must be greater than 0)"
    )

    parser.add_argument(
        "--price",
        type=str,
        required=False,
        default=None,
        help="Order price (required for LIMIT orders)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate order without actually placing it"
    )

    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompt (use with caution)"
    )

    return parser


def display_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float]
) -> None:
    """
    Display order summary in a formatted table.

    Args:
        symbol: Trading pair symbol
        side: Order side
        order_type: Order type
        quantity: Order quantity
        price: Order price
    """
    summary_table = Table(title="Order Summary", show_header=False, box=None)
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="green")

    summary_table.add_row("Symbol", symbol)
    summary_table.add_row("Side", side)
    summary_table.add_row("Type", order_type)
    summary_table.add_row("Quantity", OrderManager.format_quantity(quantity))
    summary_table.add_row("Price", OrderManager.format_price(price))

    console.print()
    console.print(Panel(summary_table, border_style="blue"))
    console.print()


def display_order_result(order_id: int, status: str, executed_qty: float, avg_price: float) -> None:
    """
    Display order result in a formatted table.

    Args:
        order_id: Order ID
        status: Order status
        executed_qty: Executed quantity
        avg_price: Average price
    """
    result_table = Table(title="Order Result", show_header=False, box=None)
    result_table.add_column("Parameter", style="cyan")
    result_table.add_column("Value", style="green")

    result_table.add_row("Order ID", str(order_id))
    result_table.add_row("Status", status)
    result_table.add_row("Executed Quantity", OrderManager.format_quantity(executed_qty))
    result_table.add_row("Average Price", OrderManager.format_price(avg_price))

    console.print()
    console.print(Panel(result_table, border_style="green"))
    console.print()


def display_error(message: str) -> None:
    """
    Display error message in red.

    Args:
        message: Error message to display
    """
    console.print(f"[bold red][ERROR] {message}[/bold red]")


def display_success(message: str) -> None:
    """
    Display success message in green.

    Args:
        message: Success message to display
    """
    console.print(f"[bold green][OK] {message}[/bold green]")


def display_info(message: str) -> None:
    """
    Display info message in cyan.

    Args:
        message: Info message to display
    """
    console.print(f"[bold cyan][INFO] {message}[/bold cyan]")


def validate_arguments(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str]
) -> tuple:
    """
    Validate all command-line arguments.

    Args:
        symbol: Trading pair symbol
        side: Order side
        order_type: Order type
        quantity: Order quantity
        price: Order price

    Returns:
        Tuple of validated parameters

    Raises:
        ValidationError: If any parameter is invalid
    """
    display_info("Validating input parameters...")

    try:
        validated = OrderValidator.validate_all(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        display_success("All parameters validated successfully!")
        return validated
    except ValidationError as e:
        display_error(str(e))
        raise


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Setup logging
        logger = setup_logging()
        logger.info("Trading bot started")

        # Parse arguments
        parser = setup_argparse()
        args = parser.parse_args()

        # Validate arguments
        try:
            symbol, side, order_type, quantity, price = validate_arguments(
                symbol=args.symbol,
                side=args.side,
                order_type=args.type,
                quantity=args.quantity,
                price=args.price
            )
        except ValidationError:
            logger.error("Argument validation failed")
            return 1

        # Display order summary
        display_order_summary(symbol, side, order_type, quantity, price)

        # Get API credentials
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            display_error("BINANCE_API_KEY or BINANCE_API_SECRET not found in .env file")
            logger.error("Missing API credentials in .env file")
            return 1

        # Initialize Binance client
        try:
            display_info("Initializing Binance Futures Testnet client...")
            client = BinanceClient(api_key, api_secret)
            display_success("Client initialized successfully!")
        except BinanceClientException as e:
            display_error(str(e))
            logger.error(f"Failed to initialize client: {str(e)}")
            return 1

        # Test connection
        try:
            display_info("Testing connection to Binance API...")
            client.test_connection()
            display_success("Connection test passed!")
        except BinanceClientException as e:
            display_error(str(e))
            logger.error(f"Connection test failed: {str(e)}")
            return 1

        # Ask for confirmation (unless --confirm flag used)
        if not args.confirm:
            console.print()
            console.print("[bold yellow]IMPORTANT: Please review above order details[/bold yellow]")
            confirm_input = console.input(
                "[bold cyan]Continue with order? (yes/no): [/bold cyan]"
            ).lower().strip()

            if confirm_input != 'yes':
                logger.info("Order cancelled by user")
                console.print("[yellow]Order cancelled[/yellow]")
                return 0

        # DRY RUN mode
        if args.dry_run:
            console.print()
            console.print("[bold cyan][DRY RUN] Order would be placed (no API call)[/bold cyan]")
            logger.info(
                f"DRY RUN: Would place {side} {order_type} order - "
                f"Symbol={symbol}, Qty={quantity}, Price={price}"
            )

            # Simulate response
            fake_response = {
                'orderId': 999999999,
                'symbol': symbol,
                'status': 'FILLED' if args.type == 'MARKET' else 'NEW',
                'side': side,
                'type': order_type,
                'executedQty': str(quantity) if args.type == 'MARKET' else '0',
                'avgPrice': str(price or 0),
            }
            display_success("Simulated order placed successfully (DRY RUN)!")
            display_order_result(
                order_id=fake_response['orderId'],
                status=fake_response['status'],
                executed_qty=float(fake_response['executedQty']),
                avg_price=float(fake_response['avgPrice'])
            )
            return 0

        # Place order
        try:
            display_info(f"Placing {order_type} {side} order...")
            response = client.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )

            # Validate and parse response
            OrderManager.validate_response(response)
            order_result = OrderManager.parse_order_response(response)

            # Display result
            display_success(f"Order placed successfully! Order ID: {order_result.order_id}")
            display_order_result(
                order_id=order_result.order_id,
                status=order_result.status,
                executed_qty=order_result.executed_quantity,
                avg_price=order_result.average_price
            )

            logger.info(f"Order completed successfully: {order_result}")
            return 0

        except BinanceClientException as e:
            display_error(str(e))
            logger.error(f"Order placement failed: {str(e)}")
            return 1
        except ValueError as e:
            display_error(f"Failed to parse order response: {str(e)}")
            logger.error(f"Response parsing error: {str(e)}")
            return 1

    except KeyboardInterrupt:
        logger.warning("Trading bot interrupted by user")
        console.print("\n[yellow]Bot interrupted by user[/yellow]")
        return 130
    except Exception as e:
        logger.critical(f"Unexpected error in main: {str(e)}")
        display_error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
