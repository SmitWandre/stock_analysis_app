# Stock Analysis Dashboard

This project is a comprehensive Stock Analysis Dashboard built using Python. It allows users to analyze stock data, calculate various technical indicators, and visualize the data in an intuitive way. The app is developed using `yfinance` for data retrieval, `pandas` for data manipulation, `matplotlib` for visualization, and `streamlit` for the user interface.

## Features
- Fetch historical stock data from Yahoo Finance.
- Compute technical indicators such as:
  - Moving Averages (7-day and 30-day)
  - Relative Strength Index (RSI)
  - Stochastic RSI
  - Moving Average Convergence Divergence (MACD)
  - Bollinger Bands
  - Average Daily Percentage Change
  - Profit/Loss Percentage
- Visualize:
  - Stock prices and moving averages
  - RSI with overbought/oversold levels
  - MACD with signal line and histogram
  - Stochastic RSI with overbought/oversold levels
  - Bollinger Bands
- Streamlit-based interactive UI to input stock ticker, date range, and analysis interval.

## Installation
### Prerequisites
- Python 3.7+
- `pip` for package management

### Install Required Packages
```bash
pip install yfinance pandas matplotlib streamlit
```

## Usage
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the URL provided by Streamlit (usually `http://localhost:8501`).
4. Enter a stock ticker (e.g., `AAPL`), select a date range and interval, then click "Analyze Stock."

## Project Structure
```
├── app.py              # Main application file
├── README.md           # Project documentation
└── requirements.txt    # List of dependencies
```

## Technical Indicators Explained
- **Moving Averages (MA):** Shows the average price of a stock over a set period.
- **Relative Strength Index (RSI):** Indicates whether a stock is overbought or oversold.
- **Stochastic RSI:** A normalized RSI to provide overbought/oversold signals.
- **MACD:** Highlights the trend direction and momentum of the stock.
- **Bollinger Bands:** Represents volatility and potential price breakouts.
- **Average Daily Percentage Change:** Average daily movement of stock prices in percentage.
- **Profit/Loss Percentage:** Measures the change in stock price over the selected timeframe.

## Example
Example usage to analyze `AAPL` stock from January 1, 2023, to December 31, 2023, with daily intervals:

1. Input `AAPL` as the stock ticker.
2. Select the date range and interval in the sidebar.
3. Click "Analyze Stock" to view the summary and visualizations.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue to discuss improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [Yahoo Finance API](https://pypi.org/project/yfinance/) for stock data.
- [Streamlit](https://streamlit.io/) for building an interactive dashboard.

---

Enjoy analyzing your stocks!
