import requests
import pandas as pd

API_KEY = "WFH3LLY3IZFFKFCS"
SYMBOL = "RELIANCE.BSE"   # Indian stock
FUNCTION = "TIME_SERIES_DAILY"

url = f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&apikey={API_KEY}&outputsize=compact"

response = requests.get(url)
data = response.json()

# Convert JSON to DataFrame
time_series = data["Time Series (Daily)"]
df = pd.DataFrame.from_dict(time_series, orient="index")
df.reset_index(inplace=True)

# Rename columns
df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

# Convert datatypes
df["Date"] = pd.to_datetime(df["Date"])
df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

# Add Stock Name
df["Symbol"] = SYMBOL

print(df.head())



import requests
import pandas as pd
import time

API_KEY = "WFH3LLY3IZFFKFCS"
symbols = ["RELIANCE.BSE", "TCS.BSE", "INFY.BSE"]

final_df = pd.DataFrame()

for symbol in symbols:
    print(f"Fetching {symbol}...")
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # SAFETY CHECK
    if "Time Series (Daily)" not in data:
        print("API limit hit. Waiting...")
        time.sleep(60)
        continue
    
    ts = data["Time Series (Daily)"]
    temp_df = pd.DataFrame.from_dict(ts, orient="index")
    temp_df.reset_index(inplace=True)
    temp_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    temp_df = temp_df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": float})
    temp_df["Symbol"] = symbol
    
    final_df = pd.concat([final_df, temp_df])
    
    time.sleep(15)  # VERY IMPORTANT

print(final_df.head())


import sqlite3

# Create SQLite DB
conn = sqlite3.connect("stock_market.db")

# Rename columns for consistency
final_df.rename(columns={
    "Date": "trade_date",
    "Open": "open_price",
    "High": "high_price",
    "Low": "low_price",
    "Close": "close_price",
    "Volume": "volume",
    "Symbol": "symbol"
}, inplace=True)

# Save to SQLite
final_df.to_sql(
    name="stock_prices",
    con=conn,
    if_exists="append",
    index=False
)

conn.close()

print("✅ Data stored in SQLite successfully")