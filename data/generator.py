import yfinance as yf
import pandas as pd

# Download historical data
df = yf.download("AAPL", start="2015-01-01", end="2021-01-01")

# Check structure
print("DF type:", type(df))
print("Columns:", df.columns)
print("Head:\n", df.head())

# Just to be extra safe: ensure columns are flat
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(-1)

# Save to CSV in clean format
df.to_csv("historical_data.csv", index=True)
