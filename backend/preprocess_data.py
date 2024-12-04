import pandas as pd
import os

def load_and_preprocess_data():
    # Step 1: Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '../data/Sample_Pharmaceutical_Drug_Sales.csv')
    
    # Step 2: Load the dataset
    data = pd.read_csv(file_path)

    # Step 3: Convert columns to numeric
    data['Revenue'] = pd.to_numeric(data['Revenue'], errors='coerce')  # Convert Revenue to numeric
    data['Units Sold'] = pd.to_numeric(data['Units Sold'], errors='coerce')  # Convert Units Sold to numeric

    # Step 4: Handle missing or invalid values
    data.fillna({"Revenue": 0, "Units Sold": 1}, inplace=True)  # Replace NaN with default values

    # Step 5: Calculate derived columns
    data['Profit per Unit'] = data['Revenue'] / data['Units Sold']  # Calculate profit per unit
    data['Sale Date'] = pd.to_datetime(data['Sale Date'], format='%m/%d/%Y', errors='coerce')  # Parse Sale Date
    data['Days Since Sale'] = (pd.Timestamp.now() - data['Sale Date']).dt.days  # Calculate days since sale
    data['Days Since Sale'].fillna(0, inplace=True)  # Replace NaN in Days Since Sale with 0

    # Step 6: Encode categorical columns
    data = pd.get_dummies(data, columns=['Region', 'Customer Type'], drop_first=True)

    # Step 7: Ensure there are no missing values after encoding
    data.fillna(0, inplace=True)

    return data

if __name__ == "__main__":
    # For testing and debugging
    processed_data = load_and_preprocess_data()
    print(processed_data.head())  # Print the first few rows of processed data



