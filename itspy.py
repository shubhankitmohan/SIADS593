import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

# File paths
sp500_file = "/Users/shubhankit/PycharmProjects/SIADS593/src/data/data.csv"
fedfunds_file = "/Users/shubhankit/PycharmProjects/SIADS593/src/data/FEDFUNDS.csv"

# Load S&P 500 Data and keep only yearly values
sp500_data = pd.read_csv(sp500_file, parse_dates=['Date'])
sp500_data = sp500_data.set_index('Date').resample('Y').last().reset_index()
sp500_data.dropna(inplace=True)  # Drop missing values

# Load Federal Funds Rate Data and keep only yearly values
fedfunds_data = pd.read_csv(fedfunds_file, parse_dates=['observation_date'])
fedfunds_data.rename(columns={'observation_date': 'Date', 'FEDFUNDS': 'Fed Funds Rate'}, inplace=True)
fedfunds_data = fedfunds_data.set_index('Date').resample('Y').last().reset_index()
fedfunds_data.dropna(inplace=True)  # Drop missing values

# Merge datasets on Date
merged_data = pd.merge(sp500_data, fedfunds_data, on='Date', how='inner')

# Separate data before and after 2020 for different smoothing strategies
pre_2020 = merged_data[merged_data['Date'] < "2020-01-01"].copy()
post_2020 = merged_data[merged_data['Date'] >= "2020-01-01"].copy()

# Apply Gaussian Smoothing only to pre-2020 data
pre_2020['SP500 Smoothed'] = gaussian_filter1d(pre_2020['SP500'], sigma=5)

# Combine back the exact post-2020 values
merged_data['SP500 Smoothed'] = pd.concat([pre_2020['SP500 Smoothed'], post_2020['SP500']])

# Key historical events with **custom vertical offsets**
events = {
    "1970 Penn Central Bank Collapse": ("1970-01-01", 210),
    "1974 Bear Market": ("1974-01-01", 150),
    "1982 Latin American Debt Crisis": ("1982-01-01", 220),
    "1987 Crash": ("1987-01-01", 250),
    "S&L Crisis": ("1989-01-01", 180),
    "Long-Term Capital Collapse": ("1998-01-01", 170),
    "Dot-Com Crash": ("2000-01-01", 190),
    "Financial Crisis": ("2008-01-01", 220),
    "COVID Stimulus & Fed QE": ("2020-01-01", 20),
    "Fed Taper Tantrum": ("2013-01-01", 20)
}

# Convert event dates to datetime
event_dates = {event: (pd.to_datetime(date), offset) for event, (date, offset) in events.items()}

# Plotting
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot S&P 500 (smoothed for pre-2020, exact for post-2020)
ax1.plot(merged_data['Date'], merged_data['SP500 Smoothed'], color='black', label='S&P 500 Index (till 2023)', linewidth=2)
ax1.set_xlabel('Year')
ax1.set_ylabel('S&P 500 Index', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Ensure 6000 is labeled on the y-axis
ax1.set_yticks(np.arange(0, 6000, 1000))  # Labels every 1000 up to 6000

# Create a second y-axis for the Federal Funds Rate
ax2 = ax1.twinx()
ax2.plot(merged_data['Date'], merged_data['Fed Funds Rate'], color='blue', linestyle='dashed', label='Federal Funds Rate')
ax2.set_ylabel('Federal Funds Rate (%)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Mark Key Events with custom vertical offsets
for event, (date, offset) in event_dates.items():
    closest_date = merged_data.iloc[(merged_data['Date'] - date).abs().argsort()[:1]]
    sp_value = closest_date['SP500 Smoothed'].values[0]
    ax1.annotate(event, (date, sp_value), textcoords="offset points", xytext=(0, offset), ha='center', fontsize=9,
                 color='red', arrowprops=dict(arrowstyle="->", color='red'))

# Title and Legends
plt.title('S&P 500 Index vs. Federal Funds Effective Rate with Key Events')
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Save plot as PNG
plt.savefig("sp500_vs_fedfunds.png", dpi=300, bbox_inches="tight")

# Show plot
plt.show()
