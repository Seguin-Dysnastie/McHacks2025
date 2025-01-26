from flask import Flask, render_template, request, jsonify
from datetime import date, timedelta
from ui import get_company_name_and_price, extract_date_and_close
from prediction import predict

app = Flask(__name__)

def build_daily_data(start_date, end_date, user_prices):
    """
    Builds daily data from start_date to end_date (inclusive),
    pairing each date with one corresponding price from user_prices.

    user_prices must have exactly the same length as
    the number of days in [start_date..end_date].

    Returns (dates, prices):
      - dates: list of "YYYY-MM-DD" strings
      - prices: list of floats
    """
    dates = []
    prices = []

    total_days = (end_date - start_date).days + 1
    if len(user_prices) != total_days:
        raise ValueError(
            f"Number of prices ({len(user_prices)}) does not match number of days ({total_days})."
        )

    current = start_date
    idx = 0
    while current <= end_date:
        dates.append(current.strftime('%Y-%m-%d'))
        prices.append(user_prices[idx])

        current += timedelta(days=1)
        idx += 1

    return dates, prices

def get_manual_data():
    """
    Example: 
      - Real data: 2023-01-01 to 2023-01-05
      - Predicted data: 2023-01-01 to 2023-01-05
      (You can adjust these dates and the corresponding price lists as you wish.)
    """

    # (A) Real data definition
    start_real = date(2023, 1, 1)
    end_real   = date(2023, 1, 5)
    real_prices_list = [100, 101.5, 102, 102.5, 103.0]  # 5 prices for 5 days
    realDates, realPrices = build_daily_data(start_real, end_real, real_prices_list)

    # (B) Predicted data definition
    start_pred = date(2023, 1, 1)
    end_pred   = date(2023, 1, 5)
    pred_prices_list = [95, 96.2, 98, 99.9, 100.5]      # 5 prices for 5 days
    predDates, predPrices = build_daily_data(start_pred, end_pred, pred_prices_list)

    return {
        "company": "xyz",
        "realDates": realDates,
        "realPrices": realPrices,
        "predDates": predDates,
        "predPrices": predPrices
    }

@app.route('/graph',methods=['POST'])
def show_graph():
    # Get your "manual" data (no random or increments)
    ticker = request.form.get('company')
    predictionRange = ["2010-01-01","2023-12-31"]
    interval = "1d"

    prediction = predict(extract_date_and_close(ticker, *predictionRange, interval), 
            extract_date_and_close(ticker, predictionRange[1], "2025-01-01", interval), 
            200, ticker)
    
    
    return render_template('graph.html', data=prediction)

    #return render_template('graph.html', data=prediction)

if __name__ == "__main__":
    app.run(debug=True)
