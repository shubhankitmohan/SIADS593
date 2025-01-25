import os
import pandas as pd
import yfinance as yf

# Define the ETFs and interest rate data to analyze
etfs = ["XLK", "XLE", "XLF", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE", "XLC"]
start_date = "2000-01-01"
end_date = "2025-01-01"

# Create a folder to store the data
os.makedirs("data", exist_ok=True)

# Initialize a dictionary to store valid ETF data
etf_data = {}

# Download historical data for ETFs
for etf in etfs:
    data = yf.download(etf, start=start_date, end=end_date)
    if not data.empty:
        # Use 'Adj Close' if available, otherwise fall back to 'Close'
        series = data.get("Adj Close", data["Close"])
        etf_data[etf] = series

        # Save the data to CSV
        data.to_csv(f"data/{etf}.csv")
    else:
        print(f"No data available for {etf}")

# Ensure all ETF data has valid and aligned indices
if etf_data:
    etf_df = pd.concat(etf_data.values(), axis=1, keys=etf_data.keys()).dropna()
    etf_df.to_csv("data/all_etfs.csv")  # Save combined ETF data
else:
    print("No valid ETF data to process.")
    exit()

# Download historical data for the 10-Year Treasury Yield
rates = yf.download("^TNX", start=start_date, end=end_date)
if not rates.empty:
    rates = rates.get("Adj Close", rates["Close"])
    rates = rates.reindex(etf_df.index).dropna()  # Align rates with ETF data

    # Save the data to CSV
    rates.to_csv("data/10_year_treasury_yield.csv")
else:
    print("No data available for 10-Year Treasury Yield.")
    exit()
