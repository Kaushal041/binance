# Installation & Setup Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection
- Binance Testnet account

## Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should output: Python 3.x.x
```

## Step 2: Clone/Setup Project

Navigate to the project directory:

```bash
cd trading_bot
```

## Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `python-binance`: Binance API wrapper
- `python-dotenv`: Environment variable management
- `requests`: HTTP library
- `rich`: Colored terminal output

Verify installation:
```bash
pip list
```

## Step 5: Get Binance Testnet Credentials

### Create Account
1. Go to [Binance Testnet](https://testnet.binancefuture.com/)
2. Sign up or login with existing Binance account
3. Email verification (if required)

### Create API Key
1. Login to Binance Testnet
2. Click on Profile icon (top right)
3. Select "API Management"
4. Click "Create API Key"
5. Label: "Trading Bot"
6. Click "Create"

### Configure API Key
1. In API Management, click "Edit Restrictions"
2. Enable: "Futures Trading"
3. Disable: "Withdraw" (for security)
4. (Optional) Add IP whitelist
5. Save

### Copy Credentials
1. Copy your API Key
2. Copy your Secret Key
3. Keep them safe!

## Step 6: Configure .env File

1. Open `.env` in the project root
2. Replace placeholders:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

**⚠️ Important:**
- Never share your Secret Key
- Never commit `.env` to Git
- Keep keys confidential

## Step 7: Test Installation

```bash
# Run help to verify installation
python cli.py --help

# Should display:
# usage: cli.py [-h] --symbol SYMBOL --side {BUY,SELL} --type {MARKET,LIMIT} --quantity QUANTITY [--price PRICE]
```

## Step 8: Test Connection

```bash
# Try a simple market order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Expected output:
```
ℹ Validating input parameters...
✓ All parameters validated successfully!

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      Order Summary             ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Symbol      │ BTCUSDT           ┃
┃ Side        │ BUY               ┃
┃ Type        │ MARKET            ┃
┃ Quantity    │ 0.0010            ┃
┃ Price       │ N/A               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

ℹ Initializing Binance Futures Testnet client...
✓ Client initialized successfully!
ℹ Testing connection to Binance API...
✓ Connection test passed!
ℹ Placing MARKET BUY order...
✓ Order placed successfully! Order ID: 123456789

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      Order Result              ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Order ID    │ 123456789         ┃
┃ Status      │ FILLED            ┃
┃ Exec. Qty   │ 0.0010            ┃
┃ Avg. Price  │ 95,000.50         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Troubleshooting Installation

### Issue: "Python not found"
**Solution:** 
- Install Python from [python.org](https://www.python.org/)
- Add Python to PATH
- Restart terminal

### Issue: "No module named 'binance'"
**Solution:**
```bash
pip install python-binance==1.0.17
```

### Issue: ".env file not found"
**Solution:**
- Ensure `.env` exists in project root
- Create it if missing
- Add credentials

### Issue: "BINANCE_API_KEY not found"
**Solution:**
- Check `.env` file exists
- Verify credentials are added
- Check file is in project root
- Reload terminal if recently edited

### Issue: "Connection timeout"
**Solution:**
- Check internet connection
- Verify Binance API is accessible
- Try using a VPN if regional restrictions
- Wait a moment and retry

### Issue: "Invalid API key"
**Solution:**
- Verify API key is correct
- Ensure using TESTNET credentials (not mainnet)
- Check for extra spaces in `.env`
- Regenerate API key if needed

## File Permissions

Ensure proper file permissions:

```bash
# Make cli.py executable (macOS/Linux)
chmod +x cli.py

# Make sure .env is readable
chmod 600 .env
```

## Virtual Environment Management

### Activate
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate
```bash
deactivate
```

### Delete (if needed)
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

## Update Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated
```

## Uninstall

```bash
# Remove all dependencies
pip uninstall -r requirements.txt -y

# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv
```

## Docker Installation (Optional)

For containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "cli.py"]
```

Build and run:
```bash
docker build -t trading-bot .
docker run --env-file .env trading-bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## Next Steps

1. ✅ Installation complete
2. Read README.md for detailed documentation
3. Check QUICKSTART.md for usage examples
4. Review SUMMARY.md for architecture overview
5. Start trading!

## Support

If you encounter issues:
1. Check logs: `tail -f logs/trading.log`
2. Verify `.env` configuration
3. Check internet connection
4. Review error messages
5. Consult Binance API docs

---

Last Updated: 2026-06-01
