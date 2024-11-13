# Import necessary modules
from flask import Flask, jsonify, request
import heapq  # For optimizing the priority queue used in the A* algorithm

# Initialize the Flask app
app = Flask(__name__)

# Home route
# This is a basic route that gives a welcome message when you visit the home page
@app.route('/')
def home():
    return jsonify(message="Welcome to the Pharma Demand AI backend!")


# Sample medicine data
medicines = [
    {"name": "Aspirin", "current_stock": 200, "daily_demand": 20, "scenario": "flu season"},
    {"name": "Ibuprofen", "current_stock": 150, "daily_demand": 10, "scenario": "regular"},
    {"name": "Antibiotics", "current_stock": 50, "daily_demand": 15, "scenario": "flu season"},
]

# Optimized A* algorithm implementation
def a_star_search(start, goal, graph):
    open_list = []
    closed_list = set()
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node == goal:
            return construct_path(current_node)

        closed_list.add(current_node)

        for neighbor, cost in graph.get(current_node, {}).items():
            if neighbor in closed_list:
                continue

            tentative_g_score = g_score[current_node] + cost
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [node for _, node in open_list]:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found

# Simple heuristic function (customize as needed)
def heuristic(node, goal):
    return abs(goal - node)

# Function to construct the path (example placeholder)
def construct_path(node):
    return [node]  # Replace with full path reconstruction logic as needed

# Define test scenarios for A* algorithm
test_scenarios = [
    {
        "name": "Simple Path",
        "graph": {
            0: {1: 1, 2: 4},
            1: {2: 2, 3: 5},
            2: {3: 1},
            3: {}
        },
        "start": 0,
        "goal": 3
    },
    {
        "name": "Complex Path with Obstacles",
        "graph": {
            0: {1: 1, 2: 4},
            1: {2: 2},
            2: {3: 5, 4: 2},
            3: {4: 1},
            4: {}
        },
        "start": 0,
        "goal": 4
    },
    {
        "name": "Disconnected Graph",
        "graph": {
            0: {1: 1},
            1: {},
            2: {3: 2},
            3: {}
        },
        "start": 0,
        "goal": 3
    }
]

# Route to test the A* algorithm with multiple scenarios
@app.route('/test-a-star')
def test_a_star_scenarios():
    results = []
    for scenario in test_scenarios:
        start = scenario["start"]
        goal = scenario["goal"]
        graph = scenario["graph"]
        result = a_star_search(start, goal, graph)
        results.append({
            "scenario": scenario["name"],
            "start": start,
            "goal": goal,
            "result": result if result else "No path found"
        })
    return jsonify(results)

# Function to determine priority of each medicine
def prioritize_medicine(medicine):
    if medicine["daily_demand"] > 15 and "flu" in medicine["scenario"]:
        return "high"
    elif medicine["daily_demand"] > 10:
        return "medium"
    else:
        return "low"

# Route to get the priority levels of all medicines
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
def estimate_days_until_stockout(medicine):
    if medicine["daily_demand"] == 0:
        return float('inf')  # If there's no demand, the stock lasts forever
    return medicine["current_stock"] / medicine["daily_demand"]

# Route to get stock predictions for all medicines
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

# Function for rule-based stock recommendations
def recommend_stock_action(medicine, delivery_days, storage_limit):
    days_left = estimate_days_until_stockout(medicine)
    if days_left < delivery_days:
        return f"Order immediately, stock will run out in {days_left:.1f} days."
    elif medicine["current_stock"] > storage_limit:
        return "Order less frequently due to storage constraints."
    elif days_left < delivery_days * 2:
        return "Consider ordering soon to avoid stockouts."
    else:
        return "Stock level is sufficient for now."

# Route to get stock recommendations based on rules
@app.route('/stock-recommendations')
def get_stock_recommendations():
    recommendations = []
    delivery_days = 3
    storage_limit = 200
    for medicine in medicines:
        action = recommend_stock_action(medicine, delivery_days, storage_limit)
        recommendations.append({
            "name": medicine["name"],
            "recommendation": action
        })
    return jsonify(recommendations)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)





















# # Import necessary modules
# from flask import Flask, jsonify  # Flask is the framework, and jsonify helps us return data in JSON format

# # Initialize the Flask app
# app = Flask(__name__)

# # Home route
# # This is a basic route that gives a welcome message when you visit the home page
# @app.route('/')
# def home():
#     return jsonify(message="Welcome to the Pharma Demand AI backend!")

# # Sample medicine data
# # This list contains sample data for different medicines with fields like name, current stock, daily demand, and a scenario
# medicines = [
#     {"name": "Aspirin", "current_stock": 200, "daily_demand": 20, "scenario": "flu season"},
#     {"name": "Ibuprofen", "current_stock": 150, "daily_demand": 10, "scenario": "regular"},
#     {"name": "Antibiotics", "current_stock": 50, "daily_demand": 15, "scenario": "flu season"},
# ]

# # Function to determine priority of each medicine
# # This function checks each medicine's daily demand and scenario to assign it a priority level (high, medium, or low)
# def prioritize_medicine(medicine):
#     if medicine["daily_demand"] > 15 and "flu" in medicine["scenario"]:
#         return "high"  # High priority if demand is high and it's flu season
#     elif medicine["daily_demand"] > 10:
#         return "medium"  # Medium priority for moderate demand
#     else:
#         return "low"  # Low priority for low demand

# # Route to get the priority levels of all medicines
# # This route goes through each medicine, assigns it a priority, and returns the list of priorities as JSON
# @app.route('/priorities')
# def get_priorities():
#     prioritized_medicines = []
#     for medicine in medicines:
#         priority = prioritize_medicine(medicine)
#         prioritized_medicines.append({
#             "name": medicine["name"],
#             "priority": priority
#         })
#     return jsonify(prioritized_medicines)

# # Function to estimate how many days each medicine will last
# # This function calculates the days remaining until stock runs out based on current stock and daily demand
# def estimate_days_until_stockout(medicine):
#     if medicine["daily_demand"] == 0:
#         return float('inf')  # If there's no demand, the stock lasts forever
#     return medicine["current_stock"] / medicine["daily_demand"]

# # Route to get stock predictions for all medicines
# # This route calculates how many days of stock are left for each medicine and returns the results as JSON
# @app.route('/stock-predictions')
# def get_stock_predictions():
#     stock_predictions = []
#     for medicine in medicines:
#         days_left = estimate_days_until_stockout(medicine)
#         stock_predictions.append({
#             "name": medicine["name"],
#             "days_left": days_left
#         })
#     return jsonify(stock_predictions)

# # Function for rule-based stock recommendations
# # This function takes delivery time and storage limit into account to suggest actions for each medicine
# def recommend_stock_action(medicine, delivery_days, storage_limit):
#     # Estimate days left for stock
#     days_left = estimate_days_until_stockout(medicine)
    
#     # Apply rule-based reasoning
#     if days_left < delivery_days:
#         return f"Order immediately, stock will run out in {days_left:.1f} days."
#     elif medicine["current_stock"] > storage_limit:
#         return "Order less frequently due to storage constraints."
#     elif days_left < delivery_days * 2:
#         return "Consider ordering soon to avoid stockouts."
#     else:
#         return "Stock level is sufficient for now."

# # Route to get stock recommendations based on rules
# # This route provides stock recommendations for each medicine by applying rule-based logic
# @app.route('/stock-recommendations')
# def get_stock_recommendations():
#     recommendations = []
#     delivery_days = 3  # Example: Assume delivery takes 3 days
#     storage_limit = 200  # Example: Set a storage limit of 200 units for each item

#     for medicine in medicines:
#         action = recommend_stock_action(medicine, delivery_days, storage_limit)
#         recommendations.append({
#             "name": medicine["name"],
#             "recommendation": action
#         })
#     return jsonify(recommendations)

# # Run the app
# # This checks if the file is being run directly and, if so, starts the Flask server in debug mode for easy testing
# if __name__ == '__main__':
#     app.run(debug=True)
