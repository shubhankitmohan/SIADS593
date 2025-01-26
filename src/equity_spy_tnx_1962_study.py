import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


# Calculate weekly percentage changes and rolling correlation
def calculate_weekly_correlation(data, spy_ticker, tnx_ticker, window=52):
    # Resample TNX to weekly frequency (last value of each week)
    weekly_data = data.resample('W').last()
    # Calculate weekly percentage changes for SPY
    weekly_data[spy_ticker] = weekly_data[spy_ticker].pct_change()
    # Calculate rolling correlation between SPY weekly changes and TNX
    correlation = weekly_data[spy_ticker].rolling(window).corr(weekly_data[tnx_ticker])
    correlation.name = "Correlation"  # Assign a name for clarity
    return weekly_data, correlation


# Plot the correlation vs. bond yields and save the plot
def plot_correlation_vs_yield(weekly_data, correlation, bond_ticker, equity_ticker, save_path="plot/correlation_plot.png"):
    # Drop NaN values and align data
    combined = pd.concat([weekly_data[bond_ticker], correlation], axis=1).dropna()
    aligned_tnx = combined[bond_ticker]
    aligned_correlation = combined["Correlation"]

    plt.figure(figsize=(12, 6))

    # Scatter plot
    plt.scatter(aligned_tnx, aligned_correlation, alpha=0.45, color="blue", label="Correlation Data")
    plt.axvline(5, color='red', linestyle='--', label='4.5% Yield Threshold')

    # Fit and plot trend line
    z = np.polyfit(aligned_tnx, aligned_correlation, 1)
    p = np.poly1d(z)
    plt.plot(aligned_tnx, p(aligned_tnx), color="orange", linewidth=2, label="Trend Line")

    plt.title("Correlation Between TNX and Weekly SPY Changes (Since 1962)")
    plt.xlabel(f"{bond_ticker} (%)")
    plt.ylabel(f"Rolling Correlation ({bond_ticker} & Weekly {equity_ticker} Changes)")
    plt.legend()
    plt.grid(alpha=0.3)

    # Save the plot to a file
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Plot saved to {save_path}")

    # Show the plot
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

    # Calculate weekly rolling correlation
    weekly_data, correlation = calculate_weekly_correlation(data, "SPY", "^TNX")

    # Plot
    plot_correlation_vs_yield(weekly_data, correlation, "^TNX", "SPY")
