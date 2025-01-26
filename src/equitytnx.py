import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Fetch historical data for 10-year bond yields (TNX) and S&P 500 (SPY)
def fetch_data(tickers, start_date, end_date):
    all_data = []
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        # Use 'Adj Close' if available, otherwise 'Close'
        if 'Adj Close' in stock_data.columns:
            series = stock_data['Adj Close']
        else:
            series = stock_data['Close']
        series.name = ticker  # Set the column name directly
        all_data.append(series)
    # Combine into a single DataFrame and align by date
    combined_data = pd.concat(all_data, axis=1)
    return combined_data


# Calculate 52-week rolling correlation between SPY and TNX
def calculate_rolling_correlation(data, ticker1, ticker2, window=252):
    return data[ticker1].rolling(window).corr(data[ticker2])


# Plot the correlation vs. bond yields
def plot_correlation_vs_yield(data, correlation, bond_ticker, equity_ticker):
    plt.figure(figsize=(12, 6))
    plt.scatter(data[bond_ticker], correlation, alpha=0.5, color="blue", label="Correlation Data")
    plt.axvline(5, color='red', linestyle='--', label='5% Yield Threshold')

    plt.title("52-week Rolling Correlation Between Yields and Equities")
    plt.xlabel(f"{bond_ticker} (%)")
    plt.ylabel(f"52-week Correlation ({bond_ticker} & {equity_ticker})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()


# Main script
if __name__ == "__main__":
    # Define parameters
    tickers = ["^TNX", "SPY"]
    start_date = "1962-01-01"
    end_date = "2025-01-01"

    # Fetch data
    data = fetch_data(tickers, start_date, end_date)

    # Drop NaN values
    data = data.dropna()

    # Calculate rolling correlation
    correlation = calculate_rolling_correlation(data, "SPY", "^TNX")

    # Plot
    plot_correlation_vs_yield(data, correlation, "^TNX", "SPY")