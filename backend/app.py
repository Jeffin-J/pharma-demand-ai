from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

@app.route('/')
def home():
    return jsonify(message="Welcome to the Pharma Demand AI backend!")

@app.route('/submit-data', methods=['POST'])
def submit_data():
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

if __name__ == '__main__':
    app.run(debug=True)









