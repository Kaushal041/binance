# Binance Futures Trading Bot - Quick Start & Explanation

## 🚀 Quick Start

### 1. Installation (One-Time Setup)

```bash
# Navigate to project directory
cd trading_bot

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `.env` file with your Binance Testnet credentials:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

### 3. Run the Bot

#### Market Buy Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Limit Sell Order
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500
```

---

## 📊 How the Code Works

### Architecture Overview

```
User Input (CLI)
       ↓
   cli.py (Argument Parsing)
       ↓
   validators.py (Input Validation)
       ↓
   BinanceClient (API Communication)
       ↓
   orders.py (Response Parsing)
       ↓
   logging_config.py (Logging)
       ↓
    User Output
```

### Module Breakdown

#### 1. **cli.py** - Entry Point
**Purpose:** Handles command-line interface and user interaction

**Key Functions:**
- `setup_argparse()`: Parses command-line arguments
- `validate_arguments()`: Validates all input parameters
- `main()`: Main execution flow
- Display functions: `display_order_summary()`, `display_order_result()`, etc.

**Flow:**
1. Parse user arguments
2. Validate input parameters
3. Initialize Binance client
4. Test API connection
5. Place order
6. Parse and display results
7. Log all activities

**Example Input:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Processing:**
- Symbol: `BTCUSDT` → validated
- Side: `BUY` → validated
- Type: `MARKET` → validated
- Quantity: `0.001` → converted to float and validated

#### 2. **bot/validators.py** - Input Validation
**Purpose:** Ensures all user input is valid before API calls

**Classes:**
- `ValidationError`: Custom exception for validation failures
- `OrderValidator`: Validates individual and combined parameters

**Validation Rules:**

| Parameter | Rule | Example |
|-----------|------|---------|
| Symbol | Not empty, min 4 chars | BTCUSDT ✓, BTC ✗ |
| Side | BUY or SELL only | BUY ✓, LONG ✗ |
| Order Type | MARKET or LIMIT only | MARKET ✓, STOP ✗ |
| Quantity | Must be > 0 | 0.001 ✓, -0.5 ✗ |
| Price | Required for LIMIT, must be > 0 | 95000 ✓ (for LIMIT) |

**Example Validation Flow:**
```python
# User input: --quantity -5
OrderValidator.validate_quantity("-5")
# → ValidationError: "Quantity must be greater than 0, got -5"
```

**Code Location:** `bot/validators.py`

#### 3. **bot/client.py** - Binance API Client
**Purpose:** Handles all communication with Binance Futures Testnet API

**Key Methods:**
- `__init__()`: Initialize client with API credentials
- `test_connection()`: Verify API connectivity
- `place_order()`: Send order to exchange
- `get_order_status()`: Query order status
- `cancel_order()`: Cancel an order

**Connection Details:**
```python
# Testnet endpoint
TESTNET_BASE_URL = "https://testnet.binancefuture.com"

# Client uses UMFutures (Unified Margin Futures)
client = UMFutures(
    key=api_key,
    secret=api_secret,
    base_url="https://testnet.binancefuture.com"
)
```

**Order Placement Flow:**
```
1. Validate credentials
2. Create request parameters
3. Send to Binance API
4. Receive response
5. Log request/response
6. Handle errors
7. Return result
```

**Example:**
```python
client = BinanceClient(api_key, api_secret)
response = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.001,
    price=None  # Not used for MARKET orders
)
# Response:
# {
#   'orderId': 123456789,
#   'symbol': 'BTCUSDT',
#   'status': 'FILLED',
#   'executedQty': '0.001',
#   'avgPrice': '95000.50',
#   ...
# }
```

**Error Handling:**
- `BinanceAPIException`: API-level errors (invalid symbol, insufficient balance)
- `BinanceConnectTimeout`: Network timeouts
- `BinanceRequestException`: Request errors
- Custom `BinanceClientException`: Wrapper for all client errors

#### 4. **bot/orders.py** - Order Management
**Purpose:** Parse API responses and format order data

**Data Classes:**
```python
@dataclass
class OrderSummary:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]

@dataclass
class OrderResult:
    order_id: int
    symbol: str
    status: str
    executed_quantity: float
    average_price: float
    side: str
    order_type: str
```

**Key Methods:**
- `parse_order_response()`: Convert Binance API response to OrderResult
- `validate_response()`: Check response has all required fields
- `format_price()`: Format price for display
- `format_quantity()`: Format quantity for display

**Example Response Parsing:**
```python
# Raw Binance response
response = {
    'orderId': 123456789,
    'symbol': 'BTCUSDT',
    'status': 'FILLED',
    'side': 'BUY',
    'type': 'MARKET',
    'executedQty': '0.001',
    'avgPrice': '95000.50'
}

# Parsed result
order_result = OrderManager.parse_order_response(response)
# OrderResult(
#     order_id=123456789,
#     symbol='BTCUSDT',
#     status='FILLED',
#     executed_quantity=0.001,
#     average_price=95000.5,
#     side='BUY',
#     order_type='MARKET'
# )
```

#### 5. **bot/logging_config.py** - Logging Setup
**Purpose:** Configure file and console logging

**Configuration:**
- **File Handler**: Logs to `logs/trading.log`
  - Max size: 10 MB
  - Backup files: 5 (automatic rotation)
- **Console Handler**: Shows warnings and errors only
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

**Usage:**
```python
logger = setup_logging()
logger.info("Order placed successfully")
logger.error("Connection failed")
```

**Log Levels:**
- `INFO`: Normal operation (API calls, successful orders)
- `WARNING`: Non-critical issues
- `ERROR`: Recoverable errors (API failures, validation errors)
- `CRITICAL`: Unexpected errors

---

## 🔄 Complete Execution Flow

### Scenario 1: Successful MARKET Order

```
User Input:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

↓ Parse Arguments
symbol="BTCUSDT", side="BUY", type="MARKET", quantity="0.001", price=None

↓ Validate Input
OrderValidator.validate_all()
- symbol: BTCUSDT ✓
- side: BUY ✓
- type: MARKET ✓
- quantity: 0.001 ✓
- price: None ✓ (not required for MARKET)

↓ Initialize Client
BinanceClient(api_key, api_secret)

↓ Test Connection
client.test_connection() → Success ✓

↓ Place Order
client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.001,
    price=None
)

↓ Binance API Response
{
    'orderId': 123456789,
    'symbol': 'BTCUSDT',
    'status': 'FILLED',
    'side': 'BUY',
    'type': 'MARKET',
    'executedQty': '0.001',
    'avgPrice': '95000.50'
}

↓ Parse Response
OrderResult(
    order_id=123456789,
    symbol='BTCUSDT',
    status='FILLED',
    executed_quantity=0.001,
    average_price=95000.5,
    side='BUY',
    order_type='MARKET'
)

↓ Display Results
Order Summary:
- Symbol: BTCUSDT
- Side: BUY
- Type: MARKET
- Quantity: 0.0010
- Price: N/A

Order Result:
- Order ID: 123456789
- Status: FILLED
- Executed Quantity: 0.0010
- Average Price: 95,000.50

↓ Logging
All steps logged to logs/trading.log

Exit Code: 0 (Success)
```

### Scenario 2: LIMIT Order with Validation Error

```
User Input:
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
(Missing --price parameter)

↓ Parse Arguments
symbol="BTCUSDT", side="BUY", type="LIMIT", quantity="0.001", price=None

↓ Validate Input
OrderValidator.validate_all()
- symbol: BTCUSDT ✓
- side: BUY ✓
- type: LIMIT ✓
- quantity: 0.001 ✓
- price: None ✗ VALIDATION ERROR!

↓ Validation Error
ValidationError: "Price is required for LIMIT orders"

↓ Error Handling
Display: ❌ Error: Price is required for LIMIT orders
Log to file

Exit Code: 1 (Failure)
```

---

## 📝 Run Commands Reference

### Basic Commands

```bash
# MARKET Buy Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# MARKET Sell Order
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01

# LIMIT Buy Order
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 94000

# LIMIT Sell Order
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500

# Help
python cli.py --help
```

### Common Symbols

```bash
# Bitcoin
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Ethereum
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.01

# Binance Coin
python cli.py --symbol BNBUSDT --side BUY --type MARKET --quantity 0.1

# XRP
python cli.py --symbol XRPUSDT --side BUY --type MARKET --quantity 10

# Solana
python cli.py --symbol SOLUSDT --side BUY --type MARKET --quantity 0.5

# Cardano
python cli.py --symbol ADAUSDT --side BUY --type MARKET --quantity 50
```

### Test Scenarios

```bash
# Test 1: Valid MARKET order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Test 2: Valid LIMIT order
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500

# Test 3: Invalid quantity (negative)
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity -0.5
# Expected: Error - Quantity must be greater than 0

# Test 4: Invalid side
python cli.py --symbol BTCUSDT --side LONG --type MARKET --quantity 0.001
# Expected: Error - Side must be one of ['BUY', 'SELL']

# Test 5: LIMIT without price
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
# Expected: Error - Price is required for LIMIT orders

# Test 6: Invalid symbol (too short)
python cli.py --symbol BTC --side BUY --type MARKET --quantity 0.001
# Expected: Error - Symbol must be at least 4 characters

# Test 7: Zero quantity
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0
# Expected: Error - Quantity must be greater than 0
```

---

## 🔧 How to Debug

### View Logs

```bash
# View entire log file
cat logs/trading.log

# View last 50 lines
tail -50 logs/trading.log

# Follow logs in real-time
tail -f logs/trading.log

# Search for specific symbol
grep "BTCUSDT" logs/trading.log

# Search for errors
grep "ERROR" logs/trading.log

# Count orders by symbol
grep "Placing" logs/trading.log | wc -l
```

### Common Issues & Solutions

**Issue 1: "BINANCE_API_KEY or BINANCE_API_SECRET not found"**
- Check `.env` file exists and is not empty
- Verify file path is correct
- Ensure credentials are not enclosed in quotes

**Issue 2: "Connection timeout"**
- Check internet connection
- Verify Binance API is accessible
- Try again after a moment

**Issue 3: "Invalid API key"**
- Verify API key is copied correctly
- Ensure you're using TESTNET credentials, not mainnet
- Check IP whitelist on Binance

**Issue 4: "Insufficient balance"**
- You don't have enough test funds
- Deposit more test funds on testnet
- Testnet funds refresh periodically

---

## 🎯 Order Status Meanings

| Status | Meaning | Action |
|--------|---------|--------|
| FILLED | Order fully executed | No action needed |
| PARTIALLY_FILLED | Part of order executed | Can wait or cancel |
| NEW | Order placed but not executed | Waiting for conditions |
| CANCELED | Order was cancelled | Needs new order |
| EXPIRED | Order expired | Needs new order |
| PENDING_CANCEL | Cancellation in progress | Wait for completion |

---

## 💡 Key Concepts

### MARKET Order
- Executes immediately at current market price
- No price specified
- Guaranteed execution
- Fast settlement

### LIMIT Order
- Executes at specific price or better
- Price must be specified
- Waits for price condition
- May not execute if price never reached

### GTC (Good-Till-Cancelled)
- LIMIT orders use GTC time-in-force
- Order stays open until filled or manually cancelled
- Can remain open for days/weeks

### Average Price
- For MARKET orders: price paid per unit
- For partially filled LIMIT orders: average of all executed portions
- Useful for calculating profit/loss

---

## 📊 Example Workflow

### Complete Trading Session

```bash
# 1. Start - Place a buy order
$ python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
✓ Order placed successfully! Order ID: 123456789
Status: FILLED
Executed Quantity: 0.0010
Average Price: 95,000.50

# 2. Check logs
$ tail -20 logs/trading.log
2026-06-01 10:15:32 - TradingBot - INFO - Order placed successfully
2026-06-01 10:15:32 - TradingBot - INFO - Order completed successfully

# 3. Later - Place a sell limit order
$ python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000
✓ Order placed successfully! Order ID: 987654321
Status: NEW
Executed Quantity: 0.0000
Average Price: 0.00

# 4. Order waits for price to reach 100,000
# When price reaches 100,000, order auto-fills

# 5. View all trading activity
$ grep "Order placed" logs/trading.log
```

---

## 🔐 Security Checklist

Before running in production:
- [ ] Store API keys in `.env` only (not in code)
- [ ] Don't commit `.env` to Git
- [ ] Use testnet first to verify functionality
- [ ] Whitelist your IP on Binance
- [ ] Disable Withdraw permission on API key
- [ ] Rotate API keys regularly
- [ ] Monitor logs for suspicious activity
- [ ] Test with small quantities first
- [ ] Review all code before running
- [ ] Keep bot running on secure server

---

## 📈 Performance Metrics

From the logs you can calculate:
- Number of orders placed
- Success rate (successful / total)
- Average execution time
- Most traded symbols
- Buy vs Sell ratio
- Times of highest trading activity

---

## 🎓 Learning Resources

**Binance Documentation:**
- [Binance Futures API Docs](https://binance-docs.github.io/apidocs/futures/en/)
- [Testnet Guide](https://testnet.binancefuture.com/)

**Python Libraries:**
- [python-binance Docs](https://python-binance.readthedocs.io/)
- [Rich Console Docs](https://rich.readthedocs.io/)

**Trading Concepts:**
- Market orders vs Limit orders
- Time-in-force options (GTC, IOC, FOK)
- Order status lifecycle
- Position management

---

## 🚨 Important Notes

1. **Testnet Only**: This bot connects to testnet by default - no real funds at risk
2. **Paper Trading**: Use testnet to practice strategies without risk
3. **API Rate Limits**: Binance has rate limits - don't spam requests
4. **Error Recovery**: The bot handles errors gracefully and logs everything
5. **Logging**: All activity is logged - useful for debugging and auditing

---

## 📞 Support

If you encounter issues:
1. Check the logs in `logs/trading.log`
2. Review error messages carefully
3. Verify `.env` configuration
4. Check internet connection
5. Test with simple MARKET orders first
6. Consult Binance API documentation

---

**Version:** 1.0.0
**Last Updated:** 2026-06-01
**Status:** Production Ready ✅
