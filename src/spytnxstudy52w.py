import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


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


# Calculate 3-month percentage changes and rolling correlation
def calculate_three_month_correlation(data, spy_ticker, tnx_ticker, window=3):
    # Resample TNX to 3-month frequency (last value of each period)
    three_month_data = data.resample('3ME').last()
    # Ensure alignment of both series
    three_month_data = three_month_data.dropna()

    # Calculate 3-month percentage changes for SPY
    three_month_data[spy_ticker] = three_month_data[spy_ticker].pct_change()
    # Calculate rolling 3-month correlation between SPY changes and TNX
    correlation = three_month_data[spy_ticker].rolling(window).corr(three_month_data[tnx_ticker])
    correlation.name = "Correlation"  # Assign a name for clarity
    return three_month_data, correlation.dropna()


# Generate and save scatter plot
def plot_scatter(three_month_data, correlation, save_path="plot/scatter_plot.png"):
    common_index = three_month_data.index.intersection(correlation.index)
    interest_rate = three_month_data.loc[common_index, "^TNX"]
    correlation_values = correlation.loc[common_index]

    plt.figure(figsize=(12, 6))
    plt.scatter(interest_rate, correlation_values, alpha=0.5, color="blue", label="Correlation Data")
    plt.axvline(3, color='red', linestyle='--', label='3% Yield Threshold')

    # Highlight the red quadrant (Interest >= 3% & Negative Correlation)
    plt.axhline(0, color='gray', linestyle='--')
    plt.fill_betweenx([-1, 0], 3, max(interest_rate), color='none', edgecolor='red', linewidth=2,
                      label='High Interest & Negative Correlation')

    # Fit and plot trend line
    z = np.polyfit(interest_rate, correlation_values, 1)
    p = np.poly1d(z)
    plt.plot(interest_rate, p(interest_rate), color="orange", linewidth=2, label="Trend Line")

    plt.title("Correlation Between TNX and SPY Changes (3-Month Rolling Window)")
    plt.xlabel("TNX (%)")
    plt.ylabel("Rolling Correlation")
    plt.legend()
    plt.grid(alpha=0.3)

    # Save the plot
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Scatter plot saved to {save_path}")
    plt.show()


# Generate and save heatmap
def plot_heatmap(three_month_data, correlation, save_path="plot/heatmap.png"):
    # Ensure alignment of actual and predicted data
    common_index = three_month_data.index.intersection(correlation.index)
    interest_rate = three_month_data.loc[common_index, "^TNX"]
    correlation_values = correlation.loc[common_index]

    # Define categories
    interest_low = interest_rate < 3
    interest_high = interest_rate >= 3
    correlation_pos = correlation_values > 0
    correlation_neg = correlation_values <= 0

    # Construct matrix counts
    heatmap_data = np.array([
        [(interest_low & correlation_pos).sum(), (interest_low & correlation_neg).sum()],
        [(interest_high & correlation_pos).sum(), (interest_high & correlation_neg).sum()]
    ])

    # Define labels
    labels = ["Interest < 3%", "Interest >= 3%"]

    # Plot heatmap
    plt.figure(figsize=(6, 6))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Positive Correlation", "Negative Correlation"], yticklabels=labels)
    plt.title("Heatmap: Interest Rate vs SPY Correlation")

    # Save and show the plot
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Heatmap saved to {save_path}")
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

    # Calculate 3-month rolling correlation (3-month window)
    three_month_data, correlation = calculate_three_month_correlation(data, "SPY", "^TNX", window=3)

    # Plot scatter plot
    plot_scatter(three_month_data, correlation, "plot/scatter_plot.png")

    # Plot heatmap
    plot_heatmap(three_month_data, correlation, "plot/heatmap.png")
