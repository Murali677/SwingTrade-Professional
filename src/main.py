from scanner import download_market
from dashboard import update_dashboard
from backtest import run_backtest
from indicators import (
    calculate_ema,
    calculate_rsi,
    calculate_volume,
    calculate_macd,
    calculate_atr,
)
from strategy import evaluate_stock
from report import create_html_report
from email_report import send_email

import webbrowser
import os


# =====================================================
# Download Market Data
# =====================================================

print("\nDownloading market data...\n")

market = download_market()

print(f"\nDownloaded {len(market)} stocks\n")

results = []


# =====================================================
# Process Each Stock
# =====================================================

for symbol, df in market.items():

    try:

        df = calculate_ema(df)
        df = calculate_rsi(df)
        df = calculate_volume(df)
        df = calculate_macd(df)
        df = calculate_atr(df)

        print(f"Processing {symbol}")

        result = evaluate_stock(symbol, df)

        if result is not None:
            results.append(result)

        print(f"Done {symbol}")

    except Exception as e:
        print(f"{symbol}: {e}")


# =====================================================
# Sort Results
# =====================================================

results = sorted(
    results,
    key=lambda x: x["Score"],
    reverse=True
)


# =====================================================
# Run Backtest
# =====================================================

print("\nRunning Backtest...\n")

backtest_results = run_backtest(
    market,
    evaluate_stock
)

print(backtest_results)


# =====================================================
# Update Dashboard
# =====================================================

update_dashboard(
    results,
    backtest_results
)


# =====================================================
# Filter Report
# =====================================================

strong_buy = [
    r for r in results
    if r["Signal"] == "Strong Buy"
]

buy = [
    r for r in results
    if r["Signal"] == "Buy"
][:3]

watch = [
    r for r in results
    if r["Signal"] == "Watch"
][:3]

report_data = strong_buy + buy + watch


# =====================================================
# Console Summary
# =====================================================

print("\n")
print("=" * 75)
print("SWING TRADE SUMMARY")
print("=" * 75)

print(f"Stocks Scanned : {len(results)}")
print(f"Strong Buy     : {len(strong_buy)}")
print(f"Buy            : {len(buy)}")
print(f"Watch          : {len(watch)}")

print("=" * 75)

print("\nTOP PICKS\n")

for i, stock in enumerate(report_data, start=1):

    stock["Rank"] = i

    print(
        f"{i:2}. "
        f"{stock['Symbol']:15}"
        f"{stock['Signal']:12}"
        f"Score: {stock['Score']}"
    )


# =====================================================
# Create HTML Report
# =====================================================

report_file = create_html_report(report_data)

print("\nHTML Report Created")
print(report_file)

print("\nReport Data:")
print(report_data)
print(f"Total stocks in report: {len(report_data)}")


# =====================================================
# Open HTML Report
# =====================================================

webbrowser.open(
    "file://" + os.path.abspath(report_file)
)


# =====================================================
# Send Email
# =====================================================

send_email(
    report_data,
    report_file
)

print("\nEmail sent successfully.\n")