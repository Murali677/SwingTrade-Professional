import yfinance as yf
from config import PERIOD, INTERVAL


def load_symbols():
    with open("../stocks.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]


def download_market():
    symbols = load_symbols()
    market = {}

    for i, symbol in enumerate(symbols, start=1):

        print(f"[{i}/{len(symbols)}] Downloading {symbol}")

        df = yf.download(
            symbol,
            period=PERIOD,
            interval=INTERVAL,
            auto_adjust=True,
            progress=False,
        )

        if df.empty:
            continue

        # ----------------------------
        # Flatten MultiIndex columns
        # ----------------------------
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        market[symbol] = df

    return market