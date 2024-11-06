# Import necessary modules
from flask import Flask, jsonify  # Flask is the framework, and jsonify helps us return data in JSON format

# Initialize the Flask app
app = Flask(__name__)

# Home route
# This is a basic route that gives a welcome message when you visit the home page
@app.route('/')
def home():
    return jsonify(message="Welcome to the Pharma Demand AI backend!")

# Sample medicine data
# This list contains sample data for different medicines with fields like name, current stock, daily demand, and a scenario
medicines = [
    {"name": "Aspirin", "current_stock": 200, "daily_demand": 20, "scenario": "flu season"},
    {"name": "Ibuprofen", "current_stock": 150, "daily_demand": 10, "scenario": "regular"},
    {"name": "Antibiotics", "current_stock": 50, "daily_demand": 15, "scenario": "flu season"},
]

# Function to determine priority of each medicine
# This function checks each medicine's daily demand and scenario to assign it a priority level (high, medium, or low)
def prioritize_medicine(medicine):
    if medicine["daily_demand"] > 15 and "flu" in medicine["scenario"]:
        return "high"  # High priority if demand is high and it's flu season
    elif medicine["daily_demand"] > 10:
        return "medium"  # Medium priority for moderate demand
    else:
        return "low"  # Low priority for low demand

# Route to get the priority levels of all medicines
# This route goes through each medicine, assigns it a priority, and returns the list of priorities as JSON
@app.route('/priorities')
def get_priorities():
    prioritized_medicines = []
    for medicine in medicines:
        priority = prioritize_medicine(medicine)
        prioritized_medicines.append({
            "name": medicine["name"],
            "priority": priority
        })
    return jsonify(prioritized_medicines)

# Function to estimate how many days each medicine will last
# This function calculates the days remaining until stock runs out based on current stock and daily demand
def estimate_days_until_stockout(medicine):
    if medicine["daily_demand"] == 0:
        return float('inf')  # If there's no demand, the stock lasts forever
    return medicine["current_stock"] / medicine["daily_demand"]

# Route to get stock predictions for all medicines
# This route calculates how many days of stock are left for each medicine and returns the results as JSON
@app.route('/stock-predictions')
def get_stock_predictions():
    stock_predictions = []
    for medicine in medicines:
        days_left = estimate_days_until_stockout(medicine)
        stock_predictions.append({
            "name": medicine["name"],
            "days_left": days_left
        })
    return jsonify(stock_predictions)

# Run the app
# This checks if the file is being run directly and, if so, starts the Flask server in debug mode for easy testing
if __name__ == '__main__':
    app.run(debug=True)
