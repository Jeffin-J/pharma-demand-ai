import pandas as pd
import os

def load_and_preprocess_data():
    # Step 1: Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '../data/Sample_Pharmaceutical_Drug_Sales.csv')
    
    # Step 2: Load the dataset
    data = pd.read_csv(file_path)

    # Step 3: Handle missing values
    data.fillna({"Units Sold": 0, "Revenue": 0}, inplace=True)

    # Step 4: Standardize formats
    data['Strength'] = data['Strength'].str.lower()  # Convert to lowercase
    data['Sale Date'] = pd.to_datetime(data['Sale Date'], format='%m/%d/%Y')  # Parse dates

    # Step 5: Feature engineering
    data['Profit per Unit'] = data['Revenue'] / data['Units Sold']
    data['Days Since Sale'] = (pd.Timestamp.now() - data['Sale Date']).dt.days

    # Step 6: Encode categorical columns
    data = pd.get_dummies(data, columns=['Region', 'Customer Type'], drop_first=True)

    # Step 7: Normalize numerical columns
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    data[['Units Sold', 'Revenue']] = scaler.fit_transform(data[['Units Sold', 'Revenue']])

    return data

if __name__ == "__main__":
    # For testing and debugging
    processed_data = load_and_preprocess_data()
    print(processed_data.head())  # Print the first few rows
