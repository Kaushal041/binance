"""Setup configuration for Binance Trading Bot."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="binance-trading-bot",
    version="2.0.0",
    author="Senior Technical Team",
    description="Production-grade Binance Futures Testnet trading bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/binance-trading-bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-binance==1.0.17",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "rich==13.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "pylint>=2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "trading-bot=cli:main",
        ],
    },
)
