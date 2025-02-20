import pandas as pd
def preprocess_data(data):
    # Define column mapping to standardize column names
    column_mapping = {
        'date': 'Date',
        'category': 'Category',
        'subcategory': 'SubCategory',
        'sub-category': 'SubCategory',
        'region': 'Region',
        'city': 'City',
        'sales': 'Sales',
        'quantity': 'Quantity',
        'profit': 'Profit'
    }
    
    # Rename columns using mapping (case insensitive)
    data.columns = [column_mapping.get(col.lower(), col) for col in data.columns]
    
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Handle invalid dates gracefully

    # Drop rows with invalid dates (NaT) after conversion
    data = data.dropna(subset=['Date'])

    # Convert the 'Date' column to a proper format (e.g., YYYY-MM-DD)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    # Extract year and month from the 'Date' column
    data['Year'] = pd.to_datetime(data['Date']).dt.year.astype(int)
    data['Month'] = pd.to_datetime(data['Date']).dt.month.astype(int)

    # Fill missing values in other columns with 0
    data = data.fillna(0)
    return data
