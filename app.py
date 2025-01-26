from flask import Flask, request, jsonify
from ui import extract_date_and_close, get_company_name_and_price
from prediction import predict

app = Flask(__name__)

@app.route('/company/search', methods=['POST'])
def get_request():
    ticker = request.json["ticker"] # Get JSON data from the body of the request
    return jsonify(get_company_name_and_price(ticker)), 200

@app.route('/company/predict', methods=['POST'])
def post_request():
    data = request.json # Get JSON data from the body of the request
    ticker = data["ticker"]
    predictionRange = data["range"]
    interval = data["interval"]
    prediction = predict(extract_date_and_close(ticker, *predictionRange, interval), 
            extract_date_and_close(ticker, predictionRange[1], "2025-01-01", interval), 
            300)
    
    return jsonify(prediction), 200

if __name__ == '__main__':
    app.run(debug=True)



