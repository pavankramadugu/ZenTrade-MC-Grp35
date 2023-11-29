
import yfinance as yf
import pandas as pd
from niftystocks import ns
from datetime import datetime, timedelta
from pytickersymbols import PyTickerSymbols

def get_date_range(frequency):
    """
    Get the date range based on the specified frequency.

    Parameters:
    - frequency (str): Frequency of data (e.g., 'Weekly', 'Monthly').

    Returns:
    - tuple: Start date and end date.
    """
    end_date = datetime.now()
    if frequency == 'Weekly':
        start_date = end_date - timedelta(days=30)
    elif frequency == 'Monthly':
        start_date = end_date - timedelta(days=90)
    elif frequency == 'Quarterly':
        start_date = end_date - timedelta(days=180)
    elif frequency == 'Semi-Annually':
        start_date = end_date - timedelta(days=365)
    elif frequency == 'Annually':
        start_date = end_date - timedelta(days=730)
    else:
        raise ValueError("Invalid frequency")
    return start_date, end_date

def get_weights(risk_appetite):
    """
    Get weights based on the specified risk appetite.

    Parameters:
    - risk_appetite (str): Risk appetite level ('Low', 'Medium', 'High').

    Returns:
    - dict: Weights for different metrics.
    """
    if risk_appetite == 'Low':
        return {'Monthly Returns': 0.1, 'Volatility': 0.6, 'Momentum': 0.1, 'Sharpe Ratio': 0.2}
    elif risk_appetite == 'Medium':
        return {'Monthly Returns': 0.3, 'Volatility': 0.2, 'Momentum': 0.3, 'Sharpe Ratio': 0.2}
    elif risk_appetite == 'High':
        return {'Monthly Returns': 0.4, 'Volatility': 0.1, 'Momentum': 0.4, 'Sharpe Ratio': 0.1}
    else:
        raise ValueError("Invalid risk appetite")

def fetch_stock_data(tickers, start_date, end_date):
    """
    Fetch stock data for the given tickers and date range.

    Parameters:
    - tickers (list): List of stock tickers.
    - start_date (datetime): Start date for data.
    - end_date (datetime): End date for data.

    Returns:
    - pd.DataFrame: Concatenated stock data.
    """
    data_list = []
    successful_tickers = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                successful_tickers.append(ticker)
                data_list.append(data['Adj Close'].rename(ticker))
            else:
                print(f"No data found for ticker: {ticker}")
        except Exception as e:
            print(f"Error fetching data for ticker {ticker}: {e}")

    all_data = pd.concat(data_list, axis=1)
    return all_data

def calculate_metrics(data):
    """
    Calculate financial metrics based on the stock data.

    Parameters:
    - data (pd.DataFrame): Stock data.

    Returns:
    - pd.DataFrame: Calculated metrics.
    """
    metrics = pd.DataFrame(index=data.columns)
    monthly_returns = data.resample('M').ffill().pct_change().mean()
    metrics['Monthly Returns'] = monthly_returns
    daily_volatility = data.pct_change().std()
    metrics['Volatility'] = daily_volatility
    momentum = data.pct_change(periods=len(data) // 4).iloc[-1]
    metrics['Momentum'] = momentum
    sharpe_ratio = monthly_returns / daily_volatility
    metrics['Sharpe Ratio'] = sharpe_ratio
    return metrics

def select_stocks(stock_metrics, weights, num_stocks=15):
    """
    Select top stocks based on calculated metrics and weights.

    Parameters:
    - stock_metrics (pd.DataFrame): Calculated metrics for stocks.
    - weights (dict): Weights for different metrics.
    - num_stocks (int): Number of top stocks to select.

    Returns:
    - pd.Series: Ranked stocks.
    """
    ranked_stocks = stock_metrics.dot(pd.Series(weights)).sort_values(ascending=False)
    return ranked_stocks.head(num_stocks)

def get_tickers(countries):
    """
    Get stock tickers based on specified countries.

    Parameters:
    - countries (list): List of countries.

    Returns:
    - list: Stock tickers.
    """
    sd = PyTickerSymbols()
    germany_tickers = sd.get_dax_frankfurt_yahoo_tickers()
    us_tickers = sd.get_sp_100_nyc_yahoo_tickers()
    india_tickers = ns.get_nifty50_with_ns()
    yf_tickers = {
        'Germany': germany_tickers + ['SDEU.L'],
        'USA': us_tickers + ['TLT'],
        'India': india_tickers + ['EBBETF0431.NS'],
        'China': ['CNYB.MI',
                  "600010.SS", "600028.SS", "600030.SS", "600031.SS", "600036.SS", "600048.SS",
                  "600050.SS", "600089.SS", "600104.SS", "600111.SS", "600196.SS", "600276.SS",
                  "600309.SS", "600406.SS", "600436.SS", "600438.SS", "600519.SS", "600690.SS",
                  "600745.SS", "600809.SS", "600887.SS", "600893.SS", "600900.SS", "600905.SS",
                  "601012.SS", "601066.SS", "601088.SS", "601166.SS", "601225.SS", "601288.SS",
                  "601318.SS", "601390.SS", "601398.SS", "601628.SS", "601633.SS", "601668.SS",
                  "601669.SS", "601728.SS", "601857.SS", "601888.SS", "601899.SS", "601919.SS",
                  "603259.SS", "603260.SS", "603288.SS", "603501.SS", "603799.SS", "603986.SS",
                  "688111.SS", "688599.SS"
                  ]
    }

    final_tickers = ['GLD']

    for country in countries:
        final_tickers.extend(yf_tickers.get(country, []))

    return final_tickers

if __name__ == '__main__':
    frequency = 'Annually'
    risk_appetite = 'Low'

    # Example: Fetch stock data for Chinese stocks based on low risk appetite
    tickers = get_tickers(['China'])
    start_date, end_date = get_date_range(frequency)
    weights = get_weights(risk_appetite)

    stock_data = fetch_stock_data(tickers, start_date, end_date)
    stock_metrics = calculate_metrics(stock_data)
    top_stocks = list(select_stocks(stock_metrics, weights).keys())

    final_names = []

    for stock in top_stocks:
        final_names.append(yf.Ticker(stock).info['shortName'])

    print(final_names)
