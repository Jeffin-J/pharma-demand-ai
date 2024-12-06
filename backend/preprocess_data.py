import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

def load_and_preprocess_data():
    # Step 1: Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '../data/Sample_Pharmaceutical_Drug_Sales.csv')
    
    # Step 2: Load the dataset
    data = pd.read_csv(file_path)

    # Step 3: Handle missing values
    data.fillna({"Units Sold": 0, "Revenue": 0}, inplace=True)

    # Step 4: Convert columns to appropriate data types
    data['Revenue'] = pd.to_numeric(data['Revenue'], errors='coerce')
    data['Units Sold'] = pd.to_numeric(data['Units Sold'], errors='coerce')
    data['Sale Date'] = pd.to_datetime(data['Sale Date'], format='%m/%d/%Y', errors='coerce')

    # Handle missing or invalid values after conversion
    data.fillna({"Revenue": 0, "Units Sold": 1}, inplace=True)

    # Step 5: Feature engineering
    data['Profit per Unit'] = data['Revenue'] / data['Units Sold']
    data['Days Since Sale'] = (pd.Timestamp.now() - data['Sale Date']).dt.days

    # Step 6: Encode categorical columns
    data = pd.get_dummies(data, columns=['Region', 'Customer Type'], drop_first=True)

    # Step 7: Normalize numerical columns
    scaler = MinMaxScaler()
    data[['Units Sold', 'Revenue']] = scaler.fit_transform(data[['Units Sold', 'Revenue']])

    # Step 8: Analyze trends (example of seasonal analysis)
    data['Month'] = data['Sale Date'].dt.month
    monthly_sales = data.groupby('Month')['Units Sold'].sum()

    print("Monthly sales trends:")
    print(monthly_sales)

    return data

def analyze_trends(data):
    # Seasonal trends: Group by month
    data['Month'] = data['Sale Date'].dt.month
    seasonal_demand = data.groupby('Month')['Units Sold'].sum()
    print("Seasonal Demand Trends:")
    print(seasonal_demand)

    # Critical stock analysis: Identify medicines frequently understocked
    understocked = data[data['Units Sold'] < 0.2]  # Threshold for critical stock
    print("Understocked Medicines:")
    print(understocked['Drug Name'].value_counts())

    return seasonal_demand, understocked


data = load_and_preprocess_data()  # Ensure data is defined by loading it first

# Call this in load_and_preprocess_data
seasonal_demand, understocked = analyze_trends(data)




if __name__ == "__main__":
    # For testing and debugging
    processed_data = load_and_preprocess_data()
    print(processed_data.head())  # Display the first few rows for verification










