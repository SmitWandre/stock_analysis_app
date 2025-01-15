import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to get stock data with timeframe
def get_stock_data(ticker, start_date, end_date, interval):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return stock_data

# Function to get moving averages
def get_moving_averages(stock_data):
    stock_data['7-Day MA'] = stock_data['Close'].rolling(window=7).mean()
    stock_data['30-Day MA'] = stock_data['Close'].rolling(window=30).mean()
    return stock_data

# Function to get RSI
def get_rsi(stock_data, window=14):
    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    return stock_data

# Function to get MACD
def get_macd(stock_data, fast_period=12, slow_period=26, signal_period=9):
    stock_data['12-Day EMA'] = stock_data['Close'].ewm(span=fast_period, adjust=False).mean()
    stock_data['26-Day EMA'] = stock_data['Close'].ewm(span=slow_period, adjust=False).mean()
    stock_data['MACD_Line'] = stock_data['12-Day EMA'] - stock_data['26-Day EMA']
    stock_data['Signal_Line'] = stock_data['MACD_Line'].ewm(span=signal_period, adjust=False).mean()
    stock_data['MACD_Histogram'] = stock_data['MACD_Line'] - stock_data['Signal_Line']
    return stock_data

# Function to get Stochastic RSI
def get_stoch_rsi(stock_data, window=14):
    if 'RSI' not in stock_data.columns or stock_data['RSI'].isnull().all():
        raise ValueError("RSI values are missing. Ensure RSI is calculated before Stochastic RSI.")
    lowest_rsi = stock_data['RSI'].rolling(window=window).min()
    highest_rsi = stock_data['RSI'].rolling(window=window).max()
    stoch_rsi = (stock_data['RSI'] - lowest_rsi) / (highest_rsi - lowest_rsi)
    stock_data['Stoch_RSI'] = stoch_rsi
    return stock_data

# Function to calculate Bollinger Bands
def get_bollinger_bands(stock_data, window=20, multiplier=2):
    stock_data['SMA'] = stock_data['Close'].rolling(window=window).mean()
    stock_data['STD'] = stock_data['Close'].rolling(window=window).std()
    stock_data['Upper Band'] = stock_data['SMA'] + (multiplier * stock_data['STD'])
    stock_data['Lower Band'] = stock_data['SMA'] - (multiplier * stock_data['STD'])
    return stock_data

# Function to calculate average daily percentage change
def get_avg_pct_change(stock_data):
    stock_data['Daily % Change'] = stock_data['Close'].pct_change() * 100
    avg_pct_change = stock_data['Daily % Change'].mean()
    return avg_pct_change

# Function to calculate profit/loss percentage
def get_profit_loss_percentage(stock_data):
    if stock_data.empty:
        return None
    start_price = stock_data['Close'].iloc[0]
    end_price = stock_data['Close'].iloc[-1]
    profit_loss = ((end_price - start_price) / start_price) * 100
    return float(profit_loss)

# Function to plot stock data
def plot_stock_data(stock_data, ticker, interval):
    plt.figure(figsize=(20, 18))

    # Price and Moving Averages
    plt.subplot(5, 1, 1)
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
    plt.plot(stock_data.index, stock_data['7-Day MA'], label='7-Day MA', color='orange')
    plt.plot(stock_data.index, stock_data['30-Day MA'], label='30-Day MA', color='green')
    plt.title(f"{ticker} Stock Price and Moving Averages ({interval} Interval)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    # RSI Plot
    plt.subplot(5, 1, 2)
    plt.plot(stock_data.index, stock_data['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought')
    plt.axhline(30, color='green', linestyle='--', label='Oversold')
    plt.title(f"{ticker} Relative Strength Index (RSI) ({interval} Interval)")
    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.legend()
    plt.grid()

    # MACD Plot
    plt.subplot(5, 1, 3)
    plt.plot(stock_data.index, stock_data['MACD_Line'], label='MACD Line', color='blue')
    plt.plot(stock_data.index, stock_data['Signal_Line'], label='Signal Line', color='orange')
    plt.bar(stock_data.index, stock_data['MACD_Histogram'], label='MACD Histogram', color='grey', alpha=0.5)
    plt.title(f"{ticker} MACD ({interval} Interval)")
    plt.xlabel("Date")
    plt.ylabel('MACD Value')
    plt.legend()
    plt.grid()

    # Stochastic RSI Plot
    plt.subplot(5, 1, 4)
    plt.plot(stock_data.index, stock_data['Stoch_RSI'], label='Stoch_RSI', color='blue')
    plt.axhline(0.8, linestyle='--', label='Overbought (80%)', color='red')
    plt.axhline(0.2, linestyle='--', label='Oversold (20%)', color='green')
    plt.title(f"{ticker} Stochastic RSI ({interval} Interval)")
    plt.xlabel("Date")
    plt.ylabel("Stoch RSI Value")
    plt.legend()
    plt.grid()

    # Bollinger Bands
    plt.subplot(5,1,5)
    plt.plot(stock_data.index, stock_data['Upper Band'], label='Upper Bollinger Band', color='red', linestyle='--')
    plt.plot(stock_data.index, stock_data['Lower Band'], label='Lower Bollinger Band', color='purple', linestyle='--')
    plt.fill_between(stock_data.index, stock_data['Upper Band'], stock_data['Lower Band'], color='grey', alpha=0.2)
    plt.title(f"{ticker} Bollinger Bands ({interval} Interval)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    return plt

# Streamlit App
if __name__ == "__main__":
    st.title("Stock Analysis Dashboard")
    st.sidebar.header("User Input")

    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))
    interval = st.sidebar.selectbox("Select Timeframe", options=["1m", "5m", "15m", "1h", "4h", "1d"], index=5)

    if st.sidebar.button("Analyze Stock"):
        data = get_stock_data(ticker, start_date, end_date, interval)

        if data.empty:
            st.error("No data available for the selected interval and date range.")
        else:
            data = get_moving_averages(data)
            data = get_rsi(data)
            data = get_stoch_rsi(data)
            data = get_macd(data)
            data = get_bollinger_bands(data)
            avg_percentage_change = get_avg_pct_change(data)
            profit_loss_percentage = get_profit_loss_percentage(data)

            st.subheader(f"{ticker} Stock Analysis Summary")
            st.write(f"**Overall Average Daily Percentage Change:** {avg_percentage_change:.2f}%")
            st.write(f"**Profit/Loss Over Timeframe:** {profit_loss_percentage:.2f}%")

            st.subheader("Raw Data")
            st.dataframe(data[['Close', '7-Day MA', '30-Day MA', 'RSI', 'Daily % Change']].tail())

            st.subheader(f"{ticker} Stock Charts")
            st.pyplot(plot_stock_data(data, ticker, interval))
