import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import yfinance as yf
from ui import get_company_name_and_price


def plot(data1, data2):
    x1,y1 = zip(*data1)
    x2,y2 = zip(*data2)

    x1 = np.array(x1)
    y1 = np.array(y1)
    x2 = np.array(x2)
    y2 = np.array(y2)

    y1_adjusted = y1 - y1[0]
    y2_adjusted = y2 - y2[0]

    common_x = np.arange(len(y1))

    plt.plot(common_x, y1_adjusted, label='Data 1')
    plt.plot(common_x, y2_adjusted, label='Data 2')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Comparison of Two Data Sets')
    plt.legend()
    plt.show()

def get_prediction(indexes, length, points):
    values = []
    for i in range(length//5):
        mean = 0
        for index in indexes:
            mean += points[index+1+i][1] - points[index][1]

        values.append((mean/len(indexes))*3)
    
    return values


def predict(pts, futurePts, length, ticker):

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


    def fit_poly(data, tolerance=1e-5, max_iterations=10000):
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
        x = np.array([nb for nb in range(len(data))])
        y = np.array([point[1]-data[0][1] for point in data])

        # Initial fit of a polynomial regression model of degree 5
        coefficients = np.polyfit(x, y, length//4)
        polynomial = np.poly1d(coefficients)

        # Iteratively refine the model
        for _ in range(max_iterations):
            y_fit = polynomial(x)
            error = np.mean((y - y_fit) ** 2)
            if error < tolerance:
                break
            coefficients = np.polyfit(x, y, length//4)
            polynomial = np.poly1d(coefficients)

        # Generate values for the fitted polynomial curve
        x_fit = np.linspace(min(x), max(x), 100)
        y_fit = polynomial(x_fit)
        
        # Calculate performance metrics
        mse = mean_squared_error(y, polynomial(x))
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y, polynomial(x))
        r2 = r2_score(y, polynomial(x))

        return (mse, rmse, mae, r2, polynomial)


    input_graph = transform_data(pts)[-length:]
    
    polynomial_function = fit_poly(transform_data(input_graph))

    bestPattern = []
    for i in range(0,len(pts[:-2*length]),30):
        x = np.array([nb for nb in range(length)])
        y = np.array([point[1]-pts[i][1] for point in pts[i:i+length]])

        mae = mean_absolute_error(y, polynomial_function[-1](x))
        mse = mean_squared_error(y, polynomial_function[-1](x))
        
        bestPattern.append((mae,mse,i))

    bestPattern = sorted(bestPattern, key=lambda x:(x[0]+x[1]))[:10]
    predictionIndex = [pattern[2] for pattern in bestPattern]
    
    real = [pts[-1]] + futurePts[:length//5]

    prediction = get_prediction(predictionIndex, length, pts)
    predictionPoints = [pts[-1]]
    for (i,diff) in enumerate(prediction):
        predictionPoints.append([real[i+1][0],pts[-1][1]+diff])


    return (pts[-length//2:],real,predictionPoints, get_company_name_and_price(ticker))
