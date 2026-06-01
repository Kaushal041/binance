# Binance Futures Trading Bot (Testnet)

A production-quality Python trading bot for Binance Futures Testnet (USDT-M) with clean architecture, comprehensive logging, and an enhanced CLI UX.

## Features

✨ **Core Features:**
- Place MARKET and LIMIT orders on Binance Futures Testnet
- Support for BUY and SELL orders
- Comprehensive input validation
- Real-time order execution and status tracking
- Detailed logging to file with log rotation
- Environment variable configuration via `.env`
- Clean, modular architecture with separation of concerns

🎨 **Enhanced CLI UX:**
- Colored output using [Rich](https://rich.readthedocs.io/)
- Beautiful formatted tables for order summary and results
- Clear validation messages with visual indicators
- Emoji feedback for user actions
- Organized error messages

🔒 **Robust Error Handling:**
- Input validation (symbol, side, type, quantity, price)
- Binance API error handling
- Network error handling (timeouts, connection errors)
- Unexpected exception handling
- Graceful error reporting to users

📊 **Logging:**
- File logging with rotation (10MB per file, 5 backup files)
- API request/response logging
- Validation error logging
- Network error logging
- Successful order logging
- Console warnings and errors

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance API client wrapper
│   ├── orders.py                # Order management logic
│   ├── validators.py            # Input validation
│   └── logging_config.py        # Logging configuration
├── logs/
│   └── trading.log              # Trading activity log (auto-generated)
├── cli.py                       # CLI entry point
├── .env                         # API credentials (not in git)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone/Setup the Project

```bash
cd trading_bot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install python-binance==1.0.17
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install rich==13.7.0
```

## Environment Setup

### Step 1: Get Binance Testnet Credentials

1. Go to [Binance Testnet](https://testnet.binancefuture.com/)
2. Create an account or login with your existing Binance account
3. Go to Account Settings → API Management
4. Create a new API key:
   - Set label: "Trading Bot"
   - Enable Futures Trading
   - **DO NOT enable Withdraw option** (for security)
   - Whitelist IP (recommended: your IP address)
5. Copy your API Key and Secret Key

### Step 2: Configure .env File

1. Open `.env` in the project root
2. Replace placeholders with your Binance Testnet credentials:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

**Security Notice:**
- Never commit `.env` to version control
- Keep your API Secret confidential
- Always use Testnet credentials for testing
- Whitelist IP addresses on the Binance side for security

## Binance Testnet Setup

### Access Testnet
- **Futures Testnet URL:** https://testnet.binancefuture.com/
- **Testnet is separate** from mainnet with different credentials
- **Test funds** are automatically provided for trading

### Key Differences from Mainnet
- Testnet uses separate credentials
- No real money involved
- Test funds reset periodically
- Lower rate limits than mainnet
- Perfect for testing and development

## How to Run

### Basic Usage

**MARKET Order Example:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**LIMIT Order Example:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 110000
```

### Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--symbol` | Yes | Trading pair symbol | `BTCUSDT`, `ETHUSDT` |
| `--side` | Yes | Order side | `BUY` or `SELL` |
| `--type` | Yes | Order type | `MARKET` or `LIMIT` |
| `--quantity` | Yes | Order quantity | `0.001`, `1.5` |
| `--price` | Only for LIMIT | Order price | `110000`, `3000.50` |

### Help

```bash
python cli.py --help
```

## Example Commands

### 1. Buy Bitcoin (MARKET Order)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### 2. Sell Ethereum (LIMIT Order)
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
```

### 3. Buy XRP (MARKET Order)
```bash
python cli.py --symbol XRPUSDT --side BUY --type MARKET --quantity 10
```

### 4. Sell Binance Coin (LIMIT Order)
```bash
python cli.py --symbol BNBUSDT --side SELL --type LIMIT --quantity 0.5 --price 700
```

## Architecture Overview

### Layer 1: CLI Interface (`cli.py`)
- Argument parsing with `argparse`
- User input handling
- Colored output with `Rich`
- Error display and user feedback

### Layer 2: Validation (`bot/validators.py`)
- Symbol validation
- Side validation (BUY/SELL)
- Order type validation (MARKET/LIMIT)
- Quantity validation (must be > 0)
- Price validation (required for LIMIT, must be > 0)
- Custom `ValidationError` exception

### Layer 3: Client (`bot/client.py`)
- Binance Futures Testnet API wrapper
- Connection testing
- Order placement
- Order status queries
- Error handling for API exceptions
- Custom `BinanceClientException` exception

### Layer 4: Order Management (`bot/orders.py`)
- Order summary creation
- API response parsing
- Result formatting and display
- Data classes: `OrderSummary`, `OrderResult`

### Layer 5: Logging (`bot/logging_config.py`)
- File logging with rotation
- Console logging for warnings/errors
- Consistent formatting
- Automatic log directory creation

## Error Handling

### Input Validation Errors
```
❌ Error: Quantity must be greater than 0, got -5
```

### API Connection Errors
```
❌ Error: Connection timeout - check your internet connection
```

### Binance API Errors
```
❌ Error: Insufficient balance or Quantity is less than the minimum allowed
```

### Missing Credentials
```
❌ Error: BINANCE_API_KEY or BINANCE_API_SECRET not found in .env file
```

## Logging Information

### Log File Location
```
trading_bot/logs/trading.log
```

### What Gets Logged

**API Requests:**
```
2026-06-01 10:30:45 - TradingBot - INFO - Placing MARKET BUY order: Symbol=BTCUSDT, Quantity=0.001, Price=None
```

**API Responses:**
```
2026-06-01 10:30:46 - TradingBot - INFO - Order placed successfully: {'orderId': 12345, 'symbol': 'BTCUSDT', ...}
```

**Validation Errors:**
```
2026-06-01 10:30:30 - TradingBot - INFO - Symbol validation passed: BTCUSDT
```

**Network Errors:**
```
2026-06-01 10:30:46 - TradingBot - ERROR - Connection timeout to Binance API
```

**Successful Orders:**
```
2026-06-01 10:30:47 - TradingBot - INFO - Order completed successfully: OrderResult(order_id=12345, ...)
```

### Log Rotation
- Maximum file size: 10 MB
- Backup files: 5
- Oldest logs are automatically rotated out

### Viewing Logs
```bash
# View entire log
cat logs/trading.log

# View last 50 lines
tail -50 logs/trading.log

# Follow log in real-time
tail -f logs/trading.log

# Search for specific orders
grep "BTCUSDT" logs/trading.log
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| python-binance | 1.0.17 | Official Binance API wrapper |
| python-dotenv | 1.0.0 | Environment variable loading |
| requests | 2.31.0 | HTTP library (dependency of binance) |
| rich | 13.7.0 | Colored terminal output |

## Code Quality

### Type Hints
All functions include type hints for better IDE support and type checking:
```python
def validate_quantity(quantity: str) -> float:
    ...
```

### Docstrings
All classes and functions have clear docstrings:
```python
"""
Validate order quantity.

Args:
    quantity: Order quantity as string

Returns:
    Validated quantity as float

Raises:
    ValidationError: If quantity is invalid
"""
```

### Modular Design
- Clear separation of concerns
- Each module has a single responsibility
- Easy to extend and test
- Reusable components

### Clean Naming
- Clear, descriptive function names
- Consistent naming conventions
- Easy to understand code intent

## Example Log Output

### MARKET Order Log Entry
```
2026-06-01 10:30:45 - TradingBot - INFO - Trading bot started
2026-06-01 10:30:45 - TradingBot - INFO - Initializing Binance Futures Testnet client
2026-06-01 10:30:45 - TradingBot - INFO - Binance Futures Testnet client initialized successfully
2026-06-01 10:30:45 - TradingBot - INFO - Testing connection to Binance API
2026-06-01 10:30:46 - TradingBot - INFO - Connection test successful
2026-06-01 10:30:46 - TradingBot - INFO - Symbol validation passed: BTCUSDT
2026-06-01 10:30:46 - TradingBot - INFO - Side validation passed: BUY
2026-06-01 10:30:46 - TradingBot - INFO - Order type validation passed: MARKET
2026-06-01 10:30:46 - TradingBot - INFO - Quantity validation passed: 0.001
2026-06-01 10:30:46 - TradingBot - INFO - Placing MARKET BUY order: Symbol=BTCUSDT, Quantity=0.001, Price=None
2026-06-01 10:30:47 - TradingBot - INFO - Order placed successfully: {'orderId': 123456789, 'symbol': 'BTCUSDT', 'status': 'FILLED', 'side': 'BUY', 'type': 'MARKET', 'executedQty': '0.001', 'avgPrice': '95000.50', ...}
2026-06-01 10:30:47 - TradingBot - INFO - Parsing order response: {...}
2026-06-01 10:30:47 - TradingBot - INFO - Order response parsed successfully: OrderResult(order_id=123456789, symbol='BTCUSDT', status='FILLED', executed_quantity=0.001, average_price=95000.5, side='BUY', order_type='MARKET')
```

### LIMIT Order Log Entry
```
2026-06-01 10:45:30 - TradingBot - INFO - Trading bot started
2026-06-01 10:45:30 - TradingBot - INFO - Initializing Binance Futures Testnet client
2026-06-01 10:45:30 - TradingBot - INFO - Binance Futures Testnet client initialized successfully
2026-06-01 10:45:30 - TradingBot - INFO - Testing connection to Binance API
2026-06-01 10:45:31 - TradingBot - INFO - Connection test successful
2026-06-01 10:45:31 - TradingBot - INFO - Symbol validation passed: ETHUSDT
2026-06-01 10:45:31 - TradingBot - INFO - Side validation passed: SELL
2026-06-01 10:45:31 - TradingBot - INFO - Order type validation passed: LIMIT
2026-06-01 10:45:31 - TradingBot - INFO - Quantity validation passed: 0.01
2026-06-01 10:45:31 - TradingBot - INFO - Price validation passed: 3500.0
2026-06-01 10:45:31 - TradingBot - INFO - Placing LIMIT SELL order: Symbol=ETHUSDT, Quantity=0.01, Price=3500.0
2026-06-01 10:45:32 - TradingBot - INFO - Order placed successfully: {'orderId': 987654321, 'symbol': 'ETHUSDT', 'status': 'NEW', 'side': 'SELL', 'type': 'LIMIT', 'executedQty': '0.0', 'avgPrice': '0', ...}
2026-06-01 10:45:32 - TradingBot - INFO - Parsing order response: {...}
2026-06-01 10:45:32 - TradingBot - INFO - Order response parsed successfully: OrderResult(order_id=987654321, symbol='ETHUSDT', status='NEW', executed_quantity=0.0, average_price=0, side='SELL', order_type='LIMIT')
```

## Troubleshooting

### Issue: "Invalid API key"
**Solution:** Verify your API credentials in `.env` are correct and copied exactly from Binance Testnet.

### Issue: "Insufficient balance"
**Solution:** Ensure you have sufficient test funds. Testnet funds are allocated automatically.

### Issue: "Quantity is less than the minimum allowed"
**Solution:** Increase the quantity. Each symbol has minimum quantity requirements.

### Issue: "Connection timeout"
**Solution:** Check your internet connection and ensure Binance API is accessible.

### Issue: "Price is required for LIMIT orders"
**Solution:** Add the `--price` parameter when placing LIMIT orders.

## Security Best Practices

1. **Never commit `.env` to Git**
   - Use `.gitignore` to exclude `.env`

2. **Whitelist IP addresses**
   - Add your IP to Binance API whitelist

3. **Use testnet first**
   - Always test with testnet credentials before using mainnet

4. **Restrict API permissions**
   - Disable Withdraw permission on the API key
   - Enable only necessary permissions

5. **Rotate credentials regularly**
   - Regenerate API keys periodically

6. **Monitor logs**
   - Review logs for suspicious activity

## Testing the Bot

### Test Scenario 1: MARKET Buy Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```
**Expected Output:** Order should be filled immediately with current market price.

### Test Scenario 2: LIMIT Sell Order
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500
```
**Expected Output:** Order should be created with NEW status, waiting for price target.

### Test Scenario 3: Invalid Input (Negative Quantity)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity -0.5
```
**Expected Output:** Validation error - "Quantity must be greater than 0"

### Test Scenario 4: Missing Price for LIMIT Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
```
**Expected Output:** Validation error - "Price is required for LIMIT orders"

## Performance Considerations

- **Connection pooling:** The client reuses connections for multiple requests
- **Log rotation:** Logs are automatically rotated to prevent disk space issues
- **Error recovery:** Graceful error handling allows recovery from transient failures
- **Minimal dependencies:** Only essential libraries are used

## Future Enhancements

Potential features for future versions:
- Position management (close positions, take profit, stop loss)
- Portfolio tracking and statistics
- Multiple simultaneous orders
- Advanced order types (stop-loss, take-profit)
- Real-time price monitoring and alerts
- Order history and trade analysis
- GUI interface (Flask/Streamlit)
- Database integration for trade history

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `logs/trading.log`
3. Verify your `.env` configuration
4. Check [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
5. Consult the [python-binance Library](https://python-binance.readthedocs.io/)

## License

This project is provided as-is for educational and trading purposes. Use at your own risk.

## Disclaimer

- This is a testnet trading bot. Always test thoroughly before using real money.
- Trading cryptocurrencies involves risk. Only trade with funds you can afford to lose.
- The author is not responsible for any financial losses.
- Past performance does not guarantee future results.

---

**Last Updated:** 2026-06-01
**Version:** 1.0.0
