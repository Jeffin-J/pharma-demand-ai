from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Define the static folder for serving the favicon
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')

@app.route('/')
def home():
    return jsonify(message="Welcome to the Pharma Demand AI backend!")

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




# Preventing GET on POST-only routes
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed. Please use the correct HTTP method."}), 405


if __name__ == '__main__':
    app.run(debug=True)

