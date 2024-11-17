# -*- coding: utf-8 -*-
"""
AutoSmartAPI Package
This package contains modules for interacting with the SmartAPI, fetching historical data,
trading sessions, and other financial data.

Author: Mahesh Kumar
Email: maheshrajbhar90@gmail.com
Version: 0.0.0.1
"""

# Import the main classes and functions that should be accessible when the package is imported
from .main import TechnicalAnalysis  # Assuming your main class is in a file named 'smartapi.py'

# You can also define version number here if needed
__version__ = '0.0.0.1'
import logging
logging.basicConfig(level=logging.INFO)
logging.info("TechnicalAnalysis package loaded successfully!")

