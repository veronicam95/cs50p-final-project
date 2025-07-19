# CS50 final project
import pandas as pd
import datetime
import time
from tiingo import TiingoClient


config = {}
# To reuse the same HTTP Session across API calls (and have better performance), include a session key.
config['session'] = True
MY_SECRET_API_KEY = 'c179610c54a800597a57159553a6607967b35a18'
config['api_key'] = MY_SECRET_API_KEY
# Initialize
client = TiingoClient(config)

# Stocks of interest

'''
stocks_list = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "TSLA", "META", "JPM", "V",
    "UNH", "HD", "MA", "AVGO", "XOM",
    "LLY", "JNJ", "PG", "CVX", "BAC",
    "PFE", "KO", "MRK", "PEP", "ABBV",
    "T", "WMT", "CSCO", "INTC", "ADBE",
    "NFLX", "AMD", "CRM", "NKE", "MCD",
    "DIS", "QCOM", "COST", "TXN", "BA",
    "WFC", "LIN", "ABT", "AMGN", "GE",
    "CAT", "ORCL", "GS", "UPS", "TMO"
]
'''

stocks_list = ["AAPL", "AMZN", "MSFT", "NVDA", "LLY", "GOOGL"]
end = datetime.date.today()
start = end - datetime.timedelta(days=365) # 1 year back

# Get historical prices as CSV, sampled daily
def get_historical_prices(ticker, start, end):
    return client.get_ticker_price(ticker, startDate=start, endDate=end, frequency='daily') # '2017-08-31'# '2017-08-01'#AAPL
                                            
      
def main():
    all_data = {}           # For prices.csv
    indicators_list = []    # For indicators.csv

    for ticker in stocks_list:
        data = get_historical_prices(ticker, start, end) 
        df = pd.DataFrame(data)
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index)

        # Save adjClose for prices.csv
        all_data[ticker] = df["adjClose"]

        # Compute indicators
        df = calculate_50dma(df)
        df = calculate_200dma(df)
        df = get_golden_cross(df)
        df = persistent_golden_cross(df, days=5)

        # Add Ticker column
        df["Ticker"] = ticker

        # Reset index so date is a column
        df.reset_index(inplace=True)

        # Filter rows where Golden_Cross or Golden_Cross_Persist is True
        filtered = df[
            (df["Golden_Cross"]) | (df["Golden_Cross_Persist"])
        ][["date", "Ticker", "adjClose", "50_DMA", "200_DMA", "Golden_Cross", "Golden_Cross_Persist"]]

        indicators_list.append(filtered)

        time.sleep(1)

    # Save prices.csv
    price_df = pd.DataFrame(all_data)
    price_df.to_csv("prices.csv", date_format='%d.%m.%Y')
    print("Saved adjusted close prices to prices.csv")

    # Save indicators.csv
    indicators_df = pd.concat(indicators_list)
    indicators_df.to_csv("indicators.csv", index=False, date_format='%d.%m.%Y')
    print("Saved filtered indicators to indicators.csv")


# calculate 50 dma
def calculate_50dma(df, short_window=50):
    """
    Calculate 50-day moving average.
    """
    df['50_DMA'] = df['adjClose'].rolling(window=short_window).mean()
    return df

# calcualte 200 dma
def calculate_200dma(df, long_window=200):
    """
    Calculate 200-day moving average.
    """
    df['200_DMA'] = df['adjClose'].rolling(window=long_window).mean()
    return df

# find golden cross
def get_golden_cross(df):
    """
    Identify golden cross where 50 DMA crosses above 200 DMA
    """
    # Condition for golden cross
    cross = (df['50_DMA'] > df['200_DMA']) & (df['50_DMA'].shift(1) <= df['200_DMA'].shift(1))
    df['Golden_Cross'] = cross
    return df

# find persistent golden cross
def persistent_golden_cross(df, days=5): # to prove the signal is valid
    """
    Check if golden cross persists for a given number of days
    """
    df['Golden_Cross_Persist'] = df['Golden_Cross'].rolling(window=days).sum() >= days
    return df

# show excel file with all data
def show_excel_file():
    """
    Show the Excel file with all data.
    """
    df = pd.read_csv("prices.csv")
    print(df.head())  # Display first few rows of the DataFrame

if __name__ == "__main__":
    main()
