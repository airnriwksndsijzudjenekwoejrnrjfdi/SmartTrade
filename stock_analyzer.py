import yfinance as yf
import pandas as pd
import ta

def analyze_stock(ticker):
    # Download 1 year of daily stock data
    data = yf.download(ticker, period='1y', interval='1d', auto_adjust=False)

    if data.empty:
        return f"No data found for ticker '{ticker}'"

    # Ensure 'Close' is a proper 1D Series
    close_prices = pd.Series(data['Close'].values.flatten(), index=data.index)

    # Calculate indicators
    data['RSI'] = ta.momentum.RSIIndicator(close=close_prices).rsi()
    data['SMA50'] = ta.trend.SMAIndicator(close=close_prices, window=50).sma_indicator()
    data['SMA200'] = ta.trend.SMAIndicator(close=close_prices, window=200).sma_indicator()

    # Get the latest row
    latest = data.iloc[-1]

    # Extract values as scalars using .item()
    try:
        close = latest['Close'].item()
        rsi = latest['RSI'].item()
        sma50 = latest['SMA50'].item()
        sma200 = latest['SMA200'].item()
    except Exception:
        return f"Not enough indicator data for '{ticker}'. Try a different stock or longer period."

    # Check for NaNs
    if any(pd.isna(val) for val in [rsi, sma50, sma200]):
        return f"Not enough data to calculate indicators for '{ticker}'"

    # Decision logic
    if rsi < 30 and sma50 > sma200 and close > sma50:
        decision = "INVEST ✅ (RSI < 30, SMA50 > SMA200, Close > SMA50)"
    elif rsi > 70 or close < sma50:
        decision = "DON'T INVEST ❌ (RSI > 70 or Close < SMA50)"
    else:
        decision = "HOLD 🤔 (No clear signal)"

    return {
        'Ticker': ticker,
        'Close Price': round(close, 2),
        'RSI': round(rsi, 2),
        'SMA 50': round(sma50, 2),
        'SMA 200': round(sma200, 2),
        'Decision': decision
    }

if __name__ == "__main__":
    ticker = input("Enter a stock ticker (example: AAPL, TSLA): ").upper().strip()
    if ticker:
        result = analyze_stock(ticker)
        if isinstance(result, dict):
            print("\n📈 Stock Analysis Result:\n")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)
    else:
        print("No ticker entered. Please try again.")
