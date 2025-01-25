import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Define the ETFs and interest rate data to analyze
etfs = ["XLK", "XLE", "XLF", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE", "XLC"]
start_date = "2000-01-01"
end_date = "2025-01-01"

# Initialize a dictionary to store valid ETF data
etf_data = {}

# Download historical data for ETFs
for etf in etfs:
    data = yf.download(etf, start=start_date, end=end_date)
    if not data.empty:
        # Use 'Adj Close' if available, otherwise fall back to 'Close'
        series = data.get("Adj Close", data["Close"])
        etf_data[etf] = series
    else:
        print(f"No data available for {etf}")

# Ensure all ETF data has valid and aligned indices
if etf_data:
    etf_df = pd.concat(etf_data.values(), axis=1, keys=etf_data.keys()).dropna()
else:
    print("No valid ETF data to process.")
    exit()

# Download historical data for the 10-Year Treasury Yield
rates = yf.download("^TNX", start=start_date, end=end_date)
if not rates.empty:
    rates = rates.get("Adj Close", rates["Close"])
    rates = rates.reindex(etf_df.index).dropna()  # Align rates with ETF data
else:
    print("No data available for 10-Year Treasury Yield.")
    exit()

import matplotlib.pyplot as plt

# Plot XLK and interest rates on the same graph
plt.figure(figsize=(12, 6))
plt.plot(etf_df.index, etf_df["XLK"], label="XLK (Technology ETF)", color="blue")
plt.plot(rates.index, rates, label="10-Year Treasury Yield", color="orange")
plt.title("XLK and 10-Year Treasury Yield (2000-2025)", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Value", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Define the ETFs and interest rate data to analyze
etfs = ["XLK", "XLE", "XLF", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE", "XLC"]
start_date = "2000-01-01"
end_date = "2025-01-01"

# Initialize a dictionary to store valid ETF data
etf_data = {}

# Download historical data for ETFs
for etf in etfs:
    data = yf.download(etf, start=start_date, end=end_date)
    if not data.empty:
        # Use 'Adj Close' if available, otherwise fall back to 'Close'
        series = data.get("Adj Close", data["Close"])
        etf_data[etf] = series
    else:
        print(f"No data available for {etf}")

# Ensure all ETF data has valid and aligned indices
if etf_data:
    etf_df = pd.concat(etf_data.values(), axis=1, keys=etf_data.keys()).dropna()
else:
    print("No valid ETF data to process.")
    exit()

# Download historical data for the 10-Year Treasury Yield
rates = yf.download("^TNX", start=start_date, end=end_date)
if not rates.empty:
    rates = rates.get("Adj Close", rates["Close"])
    rates = rates.reindex(etf_df.index).dropna()  # Align rates with ETF data
else:
    print("No data available for 10-Year Treasury Yield.")
    exit()

# Plot each ETF with the 10-Year Treasury Yield
for etf in etfs:
    if etf in etf_df.columns:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot ETF data on primary y-axis
        color = 'tab:blue'
        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel(f'{etf} Price ($)', fontsize=12, color=color)
        ax1.plot(etf_df.index, etf_df[etf], label=f"{etf} (ETF)", color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Create secondary y-axis for 10-Year Treasury Yield
        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('10-Year Treasury Yield (%)', fontsize=12, color=color)
        ax2.plot(rates.index, rates, label="10-Year Treasury Yield", color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Add title and grid
        plt.title(f"{etf} and 10-Year Treasury Yield (2000-2025)", fontsize=16)
        fig.tight_layout()
        plt.grid(True)
        plt.show()
    else:
        print(f"No data available for {etf}")

