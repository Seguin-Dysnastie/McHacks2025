from flask import Flask, request, jsonify
from ui import extract_date_and_close, get_company_name_and_price

app = Flask(__name__)

@app.route('/company/search', methods=['POST'])
def get_request():
    ticker = request.json["ticker"] # Get JSON data from the body of the request
    return jsonify(get_company_name_and_price(ticker)), 200

@app.route('/company/predict', methods=['POST'])
def post_request():
    data = request.json # Get JSON data from the body of the request
    companyName = data["name"]
    predictionRange = data["range"]
    interval = data["interval"]
    print(companyName, *predictionRange, interval)
    return jsonify({companyName:extract_date_and_close(companyName, *predictionRange, interval)}), 200

if __name__ == '__main__':
    app.run(debug=True)



