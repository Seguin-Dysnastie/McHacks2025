import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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


liste_2 = extract_date_and_close('AAPL', '1980-01-01', '2025-01-01', '1mo')

def transform_data(data):
    """
    Transforms a list of (time, price) tuples into (position, price) tuples.
    
    Parameters:
    data (list of tuples): List of (time, price) tuples.
    
    Returns:
    list of tuples: List of (position, price) tuples.
    """
    new_data = []
    for element in data:
        new_data.append((data.index(element), element[1]))
    return new_data

input_graph = transform_data(liste_2)

def fit_polynomial_degree_5(data, tolerance=1e-5, max_iterations=10000):
    """
    Fits a polynomial regression model of degree 5 to the given data and refines it iteratively.

    Parameters:
        data (list of tuples): A list of tuples where each tuple contains (x, y) values.
        tolerance (float): The tolerance for the difference between the points and the function.
        max_iterations (int): The maximum number of iterations for refining the model.

    Returns:
        np.poly1d: The refined polynomial function of degree 5.
    """
    # Extract x and y values from the data
    x = np.array([point[0] for point in data])
    y = np.array([point[1] for point in data])

    # Initial fit of a polynomial regression model of degree 5
    coefficients = np.polyfit(x, y, 10)
    polynomial = np.poly1d(coefficients)

    # Iteratively refine the model
    for _ in range(max_iterations):
        y_fit = polynomial(x)
        error = np.mean((y - y_fit) ** 2)
        if error < tolerance:
            break
        coefficients = np.polyfit(x, y, 10)
        polynomial = np.poly1d(coefficients)

    # Generate values for the fitted polynomial curve
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = polynomial(x_fit)
    return polynomial

def comparison_of_polynomial_functions(data, degree):
    """
    Fits polynomial regression models of varying degrees to the given data and compares their performance.

    Parameters:
        data (list of tuples): A list of tuples where each tuple contains (x, y) values.
        degree (int): The maximum degree of the polynomial regression models to fit.

    Returns:
        dict: A dictionary containing the polynomial functions and their performance metrics.
    """
    # Extract x and y values from the data
    x = np.array([point[0] for point in data])
    y = np.array([point[1] for point in data])

    # Fit polynomial regression models of varying degrees
    polynomial_functions = {}
    performance_metrics = {}
    for d in range(1, degree + 1):
        coefficients = np.polyfit(x, y, d)
        polynomial = np.poly1d(coefficients)
        polynomial_functions[d] = polynomial

        # Calculate performance metrics
        mse = mean_squared_error(y, polynomial(x))
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y, polynomial(x))
        r2 = r2_score(y, polynomial(x))
        performance_metrics[d] = {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R^2': r2}

    return polynomial_functions, performance_metrics

def compare_polynomials(function_1, function_2, x_values):
    # Calculate the y values for both functions
    y1 = function_1(x_values)
    y2 = function_2(x_values)

    # Calculate performance metrics
    mse = mean_squared_error(y1, y2)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y1, y2)
    r2 = r2_score(y1, y2)

    return {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R^2': r2}

def btw_2_function(function_1, function_2, x_values):
    metrics_1 = compare_polynomials(function_1, function_2, x_values)
    metrics_2 = compare_polynomials(function_2, function_1, x_values)

    # Compare based on Mean Squared Error (MSE)
    if metrics_1['MSE'] < metrics_2['MSE']:
        return function_1
    else:
        return function_2

def find_the_best_sublist(data, sublist_length):
    # Create the reference sublist from the last sublist of the list
    reference_sublist = data[-sublist_length:]
    reference_polynomial = fit_polynomial_degree_5(reference_sublist)

    best_sublist = None
    best_polynomial = None
    best_mse = float('inf')

    # Iterate over the data to create sublists with a step of 10
    for i in range(0, len(data) - (sublist_length * 2) + 1, 10):
        sublist = data[i:i + sublist_length]
        sublist_polynomial = fit_polynomial_degree_5(sublist)

        # Compare the current sublist polynomial with the reference polynomial
        x_values = np.array([point[0] for point in sublist])
        mse = mean_squared_error(reference_polynomial(x_values), sublist_polynomial(x_values))

        if mse < best_mse:
            best_mse = mse
            best_sublist = sublist
            best_polynomial = sublist_polynomial

    return best_sublist

x = find_the_best_sublist(input_graph, 40)
print(x)

def adjust_and_plot(data1, data2):  

    """
    Adjusts two lists of tuples to start at the same height by removing the constant term
    and displays them on the same graph.

    Parameters:
        data1 (list of tuples): The first list of tuples where each tuple contains (x, y) values.
        data2 (list of tuples): The second list of tuples where each tuple contains (x, y) values.
    """
    # Extract x and y values from the data
    x1, y1 = zip(*data1)
    x2, y2 = zip(*data2)

    # Convert to numpy arrays
    x1 = np.array(x1)
    y1 = np.array(y1)
    x2 = np.array(x2)
    y2 = np.array(y2)

    # Remove the constant term (first y value) from both y values
    y1_adjusted = y1 - y1[0]
    y2_adjusted = y2 - y2[0]

    # Create a common x-axis starting from 0 with the same interval
    common_x = np.arange(len(y1))

    # Plot the adjusted data
    plt.plot(common_x, y1_adjusted, label='Data 1')
    plt.plot(common_x, y2_adjusted, label='Data 2')
    plt.xlabel('X')
    plt.ylabel('Y (Adjusted)')
    plt.title('Adjusted Data Plot')
    plt.legend()
    plt.show()

adjust_and_plot(input_graph[-40:], x)




