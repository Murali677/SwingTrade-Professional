import pandas as pd

from config import (
    EMA_FAST,
    EMA_MEDIUM,
    EMA_SLOW,
    RSI_PERIOD,
    MACD_FAST,
    MACD_SLOW,
    MACD_SIGNAL,
    ATR_PERIOD,
)

from utils import get_price_series


# =====================================================
# EMA
# =====================================================

def calculate_ema(df):

    close = get_price_series(df, "Close")

    df["EMA20"] = close.ewm(span=EMA_FAST, adjust=False).mean()
    df["EMA50"] = close.ewm(span=EMA_MEDIUM, adjust=False).mean()
    df["EMA200"] = close.ewm(span=EMA_SLOW, adjust=False).mean()

    return df


# =====================================================
# RSI
# =====================================================

def calculate_rsi(df):

    close = get_price_series(df, "Close")

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=RSI_PERIOD).mean()
    avg_loss = loss.rolling(window=RSI_PERIOD).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    return df


# =====================================================
# Volume
# =====================================================

def calculate_volume(df):

    volume = get_price_series(df, "Volume")

    df["AVG_VOLUME20"] = volume.rolling(window=20).mean()

    return df


# =====================================================
# MACD
# =====================================================

def calculate_macd(df):

    close = get_price_series(df, "Close")

    ema_fast = close.ewm(span=MACD_FAST, adjust=False).mean()
    ema_slow = close.ewm(span=MACD_SLOW, adjust=False).mean()

    df["MACD"] = ema_fast - ema_slow

    df["MACD_SIGNAL"] = (
        df["MACD"]
        .ewm(span=MACD_SIGNAL, adjust=False)
        .mean()
    )

    df["MACD_HIST"] = df["MACD"] - df["MACD_SIGNAL"]

    return df


# =====================================================
# ATR
# =====================================================

def calculate_atr(df):

    high = get_price_series(df, "High")
    low = get_price_series(df, "Low")
    close = get_price_series(df, "Close")

    previous_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - previous_close).abs()
    tr3 = (low - previous_close).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1
    ).max(axis=1)

    df["ATR"] = true_range.rolling(
        window=ATR_PERIOD
    ).mean()

    return df