# config.py

# Yahoo Finance Settings
PERIOD = "1y"
INTERVAL = "1d"

# Technical Indicators
EMA_FAST = 20
EMA_MEDIUM = 50
EMA_SLOW = 200

RSI_PERIOD = 14

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

VOLUME_PERIOD = 20
ATR_PERIOD = 14

# Scanner
MIN_SCORE = 80

# Reports
OUTPUT_FOLDER = "../reports"


# -----------------------------
# Email Settings
# -----------------------------

import os
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Backtest
LOOK_FORWARD_DAYS = 20
TARGET_RR = 2
