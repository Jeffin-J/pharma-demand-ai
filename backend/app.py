'''
SOURCES:
https://pypi.org/project/Flask-Cors/
https://flask.palletsprojects.com/en/stable/api/

'''


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from preprocess_data import load_and_preprocess_data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Define the static folder for serving the favicon
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')

# Load and preprocess data
data = load_and_preprocess_data()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Pharma Demand AI backend!"})

@app.route('/get-processed-data', methods=['GET'])
def get_processed_data():
    try:
        return data.to_json(orient='records')
    except Exception as e:
        return jsonify({"error": f"Failed to load processed data: {str(e)}"}), 500

@app.route('/get-stock-alerts', methods=['GET'])
def get_stock_alerts():
    try:
        threshold = int(request.args.get('threshold', 50))  # Default threshold is 50 units
        alerts = []
        for _, row in data.iterrows():
            if row['Units Sold'] < threshold:  # Example alert logic
                alerts.append({
                    "name": row['Drug Name'],
                    "current_stock": row['Units Sold'],
                    "alert_message": "Stock critically low!",
                })
        return jsonify(alerts)
    except Exception as e:
        return jsonify({"error": f"Failed to generate alerts: {str(e)}"}), 500

@app.route('/get-stock-recommendations', methods=['POST'])
def get_stock_recommendations():
    try:
        # Receive current stock data from frontend
        current_stock = request.json.get('current_stock', {})
        recommendations = a_star_algorithm(current_stock)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": f"Failed to generate stock recommendations: {str(e)}"}), 500

@app.route('/favicon.ico')
def favicon():
    # Serve the favicon from the static directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/submit-data', methods=['POST', 'GET'])
def submit_data():
    if request.method == 'GET':
        # Inform users they need to use POST
        return jsonify({"error": "Method not allowed. Please use POST to submit data."}), 405
    try:
        data = request.json  # Retrieve JSON data from the request
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid data format. Expected a list of medicines."}), 400

        # Validate each medicine entry
        for medicine in data:
            if not all(key in medicine for key in ("name", "stock", "demand")):
                return jsonify({"error": f"Missing fields in one or more medicines: {medicine}"}), 400

        print("Received data from frontend:", data)  # Log received data for debugging
        return jsonify({"message": "Data received successfully!", "received_data": data})
    except Exception as e:
        print("Error processing data:", e)  # Log the error for debugging
        return jsonify({"error": "An error occurred while processing the data."}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed. Please use the correct HTTP method."}), 405



def a_star_algorithm(current_stock):
    recommendations = []
    for drug, stock in current_stock.items():
        # Retrieve seasonal demand trend (or default to average demand)
        heuristic = data[data['Drug Name'] == drug]['Units Sold'].mean()
        month = pd.Timestamp.now().month
        seasonal_demand = data[(data['Drug Name'] == drug) & (data['Month'] == month)]['Units Sold'].mean()
        estimated_demand = seasonal_demand if not pd.isna(seasonal_demand) else heuristic

        # Critical threshold
        critical_threshold = 30  # Default or use custom logic
        if stock < critical_threshold:
            recommendations.append({
                "drug": drug,
                "current_stock": stock,
                "recommendation": f"Reorder soon. Estimated demand: {estimated_demand:.2f} units.",
            })
    return recommendations




if __name__ == "__main__":
    app.run(debug=True)


