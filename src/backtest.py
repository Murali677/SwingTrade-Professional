import math
from config import LOOK_FORWARD_DAYS


def run_backtest(market, strategy_function):

    total_trades = 0
    winners = 0
    losers = 0

    gains = []
    losses = []

    for symbol, df in market.items():

        # Need enough history for EMA200 + ATR
        if len(df) < LOOK_FORWARD_DAYS + 200:
            continue

        # Walk through historical candles
        for i in range(200, len(df) - LOOK_FORWARD_DAYS):

            history = df.iloc[: i + 1].copy()

            try:
                result = strategy_function(symbol, history)
            except Exception:
                continue

            # Skip if strategy returned nothing
            if result is None:
                continue

            # Only backtest Buy signals
            if result["Signal"] not in ("Buy", "Strong Buy"):
                continue

            entry = result["Entry"]
            target = result["Target"]
            stop = result["StopLoss"]

            # Ignore invalid values
            if any(math.isnan(x) for x in [entry, target, stop]):
                continue

            total_trades += 1

            future = df.iloc[i + 1 : i + 1 + LOOK_FORWARD_DAYS]

            trade_closed = False

            for _, candle in future.iterrows():

                high = float(candle["High"])
                low = float(candle["Low"])

                # Target Hit
                if high >= target:

                    gain = ((target - entry) / entry) * 100

                    if not math.isnan(gain):
                        gains.append(gain)

                    winners += 1
                    trade_closed = True
                    break

                # Stop Hit
                if low <= stop:

                    loss = ((stop - entry) / entry) * 100

                    if not math.isnan(loss):
                        losses.append(loss)

                    losers += 1
                    trade_closed = True
                    break

            # Exit after holding period
            if not trade_closed:

                close = float(future.iloc[-1]["Close"])

                pnl = ((close - entry) / entry) * 100

                if math.isnan(pnl):
                    continue

                if pnl >= 0:
                    winners += 1
                    gains.append(pnl)
                else:
                    winners += 0
                    losers += 1
                    losses.append(pnl)

    # Remove NaN values
    gains = [g for g in gains if not math.isnan(g)]
    losses = [l for l in losses if not math.isnan(l)]

    avg_gain = round(sum(gains) / len(gains), 2) if gains else 0
    avg_loss = round(sum(losses) / len(losses), 2) if losses else 0

    win_rate = (
        round((winners / total_trades) * 100, 2)
        if total_trades
        else 0
    )

    total_gain = sum(gains)
    total_loss = abs(sum(losses))

    profit_factor = (
        round(total_gain / total_loss, 2)
        if total_loss > 0
        else 0
    )

    # Placeholder (we'll improve later)
    max_drawdown = 0

    print("\n========== BACKTEST ==========")
    print(f"Total Trades : {total_trades}")
    print(f"Winners      : {winners}")
    print(f"Losers       : {losers}")
    print(f"Win Rate     : {win_rate}%")
    print(f"Avg Gain     : {avg_gain}%")
    print(f"Avg Loss     : {avg_loss}%")
    print(f"ProfitFactor : {profit_factor}")
    print("==============================\n")

    return {
        "Total Trades": total_trades,
        "Winners": winners,
        "Losers": losers,
        "Win Rate": win_rate,
        "Avg Gain": avg_gain,
        "Avg Loss": avg_loss,
        "Profit Factor": profit_factor,
        "Max Drawdown": max_drawdown,
    }