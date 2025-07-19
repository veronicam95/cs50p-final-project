# S&P 500 Golden Cross Stock Scanner

#### Video Demo: https://www.youtube.com/watch?v=Nux_gDBdheE
#### Description:

This is my final project for **CS50’s Introduction to Programming with Python**. I built a Python program that analyzes real stock price data and detects a technical trading signal called the **Golden Cross** — this happens when a stock’s 50-day moving average (50 DMA) crosses above its 200-day moving average (200 DMA). This signal is often used by traders to identify potential long-term uptrends.

The project uses the **Tiingo API** to pull 1 year of daily adjusted closing prices for a list of selected stocks (e.g., AAPL, MSFT, AMZN, NVDA). Then, it calculates moving averages, detects golden crosses, and checks if the golden cross signal persisted for at least 5 days. The final results are saved in two CSV files:
- `prices.csv`: Contains adjusted closing prices for all selected stocks.
- `indicators.csv`: Contains rows where a Golden Cross or Persistent Golden Cross was detected, along with moving average values.

---

### How it works:

When you run the script:
1. It loops through each stock in `stocks_list` (defined in `project.py`).
2. For each stock:
   - It downloads 1 year of daily adjusted close prices from Tiingo.
   - It calculates the 50-day and 200-day moving averages.
   - It identifies Golden Cross signals where the 50 DMA crosses above the 200 DMA.
   - It checks if the Golden Cross signal has persisted for at least 5 days.
3. It saves:
   - `prices.csv`: Contains the daily adjusted close prices for all stocks.
   - `indicators.csv`: Contains dates, ticker symbols, adjusted close prices, 50 DMA, 200 DMA, and Golden Cross signal info for rows where a Golden Cross or Persistent Golden Cross was found.

---

### Files included:

- `project.py`: The main program that:
  - Connects to Tiingo API
  - Downloads stock data
  - Calculates moving averages
  - Detects golden cross signals
  - Saves output CSV files
- `test_project.py`: Contains test functions (using `pytest`) that check key functions like moving average calculations and Golden Cross detection.
- `requirements.txt`: Lists required Python packages: `pandas`, `tiingo`.
- `prices.csv`: Contains the raw adjusted close price data.
- `indicators.csv`: Contains filtered signal data for Golden Cross and Persistent Golden Cross events.

---

### Design choices:

- I chose the **Tiingo API** for reliable stock data and clear rate limits.
- To avoid exceeding free API limits, I limited the stock list to a few tickers (e.g., AAPL, AMZN, MSFT, NVDA) and added a `time.sleep(1)` pause between requests.
- I kept the output simple with two clean CSV files — one for prices, one for signal data.
- The code is organized into functions (`calculate_50dma`, `calculate_200dma`, `get_golden_cross`, `persistent_golden_cross`) so it’s easier to test and extend.

---

### How to run:

1. Get a free API key from [https://www.tiingo.com](https://www.tiingo.com) and paste it into the `MY_SECRET_API_KEY` variable inside `project.py`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
