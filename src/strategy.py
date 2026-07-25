from utils import get_price_series
import math


def evaluate_stock(symbol, df):

    # ---------------------------------
    # Need enough candles
    # ---------------------------------

    if len(df) < 220:
        return None

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # ---------------------------------
    # Price Data
    # ---------------------------------

    close = float(get_price_series(df, "Close").iloc[-1])
    high = float(get_price_series(df, "High").iloc[-1])
    volume = float(get_price_series(df, "Volume").iloc[-1])

    # Previous day's high (Breakout)
    previous_high = float(get_price_series(df, "High").iloc[-2])

    # ---------------------------------
    # Indicators
    # ---------------------------------

    ema20 = float(latest["EMA20"])
    ema50 = float(latest["EMA50"])
    ema200 = float(latest["EMA200"])

    rsi = float(latest["RSI"])

    macd = float(latest["MACD"])
    macd_signal = float(latest["MACD_SIGNAL"])

    avg_volume = float(latest["AVG_VOLUME20"])

    atr = float(latest["ATR"])

    # ---------------------------------
    # Validate Data
    # ---------------------------------

    values = [
        ema20,
        ema50,
        ema200,
        rsi,
        macd,
        macd_signal,
        avg_volume,
        atr,
    ]

    if any(math.isnan(v) for v in values):
        return None

    # ---------------------------------
    # Score
    # ---------------------------------

    score = 0
    reasons = []

# ---------------------------------
# Trend Score
# ---------------------------------

    # EMA20 above EMA50
    if ema20 > ema50:
        score += 20
        reasons.append("EMA20 > EMA50")

    # EMA50 above EMA200 and rising 
    if (
    ema50 > ema200
    and ema50 > float(prev["EMA50"])
):
        score += 20
        reasons.append("Strong Trend")

    # Price above EMA20
    distance = ((close - ema20) / ema20) * 100

    if close > ema20 and distance < 5:
        score += 20
        reasons.append("Near EMA20")

    # RSI Sweet Spot
    if 55 <= rsi <= 65:
        score += 15
        reasons.append("RSI")

    # MACD
    if macd > macd_signal:
        score += 15
        reasons.append("MACD")

    # Volume
    if volume > avg_volume * 1.5:
        score += 15
        reasons.append(" Strong Volume")
    else:
        return None

    # ---------------------------------
    # Signal
    # ---------------------------------

    if score >= 90:
        signal = "Strong Buy"

    elif score >= 80:
        signal = "Buy"

    elif score >= 70:
        signal = "Watch"

    else:
        signal = "Ignore"

    # ---------------------------------
    # Trade Levels
    # ---------------------------------

    cmp_price = round(close, 2)

    # Buy Zone
    entry = round(previous_high * 1.002, 2)

    buy_zone_low = round(entry - (atr * 0.30), 2)
    buy_zone_high = round(entry + (atr * 0.30), 2)

    # ATR Stop
    stoploss = round(entry - (1.5 * atr), 2)

    risk = entry - stoploss

    # 1 : 2 Risk Reward
    target = round(entry + (risk * 2), 2)

    stock = symbol.replace(".NS", "")

    tradingview = f"https://www.tradingview.com/chart/?symbol=NSE:{stock}"
    screener = f"https://www.screener.in/company/{stock}/"

    return {
        "Rank": 0,
        "Symbol": stock,
        "CMP": cmp_price,

        "Entry": entry,
        "Buy Zone": f"₹{buy_zone_low} - ₹{buy_zone_high}",

        "Target": target,
        "StopLoss": stoploss,
        "Score": score,
        "Signal": signal,
        "Reasons": " + ".join(reasons),
        "TradingView": tradingview,
        "Screener": screener,
    }