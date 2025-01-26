import yfinance as yf

def get_stock_data(ticker, start_date, end_date, interval):
    """
    Fetches historical market data and company info for a given ticker symbol from Yahoo Finance.

    Parameters:
        ticker (str): The ticker symbol of the company.
        start_date (str): The start date for fetching data in the format 'YYYY-MM-DD'.
        end_date (str): The end date for fetching data in the format 'YYYY-MM-DD'.
        interval (str): The data interval (e.g., '1d', '1wk', '1mo').

    Returns:
        tuple: A tuple containing a DataFrame with historical market data and a dictionary with company info.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    # Convert DataFrame to list of lists
    data_list = data.reset_index().values.tolist()
    return data_list

def get_stock_price(ticker):
    """
    Fetches the current price of a stock.

    Parameters:
        ticker (str): The ticker symbol of the company.

    Returns:
        float: The current price of the stock.
    """
    stock = yf.Ticker(ticker)
    return stock.info['currentPrice']

def get_stock_info(ticker):
    """
    Fetches company information for a given ticker symbol.

    Parameters:
        ticker (str): The ticker symbol of the company.

    Returns:
        dict: A dictionary containing company information.
    """
    stock = yf.Ticker(ticker)
    return stock.info

def extract_date_and_close(ticker, start_date, end_date, interval):
    """
    Extracts the date and closing price from a list of lists containing stock data.

    Parameters:
    data_list (list): A list of lists containing stock data.

    Returns:
    list: A list of tuples containing the date and closing price.
    """
    data_list = get_stock_data(ticker, start_date, end_date, interval)
    result = []
    for entry in data_list:
        date = entry[0].strftime('%Y-%m-%d')  # Convert timestamp to 'YYYY-MM-DD' format
        closing_price = round(entry[4],2)  # Closing price is the 5th element in the list
        result.append((date, closing_price))
    return result

def get_company_name_and_price(ticker):
    """
    Fetches the company name and current stock price for a given ticker symbol.

    Parameters:
        ticker (str): The ticker symbol of the company.

    Returns:
        tuple: A tuple containing the company name and the current stock price.
    """
    stock = yf.Ticker(ticker)
    company_name = stock.info['shortName']
    current_price = stock.info['currentPrice']
    return (ticker, company_name, current_price)

def inverse_transform_data(transformed_data, original_data):
    """
    Transforms a list of (index, price) tuples back to (date, price) tuples.

    Parameters:
        transformed_data (list of tuples): List of (index, price) tuples.
        original_data (list of tuples): List of (date, price) tuples.

    Returns:
        list of tuples: List of (date, price) tuples.
    """
    # Create a mapping from index to date using the original data
    index_to_date = {i: date for i, (date, price) in enumerate(original_data)}

    # Transform the data back to (date, price) tuples
    inverse_transformed_data = [(index_to_date[index], price) for index, price in transformed_data]

    return inverse_transformed_data

#list_1 = get_stock_data('AAPL', '2021-01-01', '2025-01-01', '1d')
#print(extract_date_and_close(list_1))
#print(get_stock_price('AAPL'))
# Time                                                                   Open              High                Low                Close          Volume  Dividends  Stock Splits
#[Timestamp('2021-01-04 00:00:00-0500', tz='America/New_York'), 130.56318890080564, 130.65119225976613, 123.95288776509373, 126.54420471191406, 143301900,  0.0,        0.0]