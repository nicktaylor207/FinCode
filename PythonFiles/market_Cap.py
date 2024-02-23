import pandas as pd
import os

def calculating_market_cap(folder_path):
    """
    Reads all CSV files in the specified folder into pandas DataFrames, computes MarketCap,
    and returns a dictionary of DataFrames.

    Parameters:
    - folder_path: str. The path to the folder containing the CSV files.

    Returns:
    - dataframes_dict: dict. A dictionary where each key is a file name and each value is a pandas DataFrame.
    """
    # Dictionary to hold your dataframes with file names as keys
    dataframes_dict = {}

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):  # Check if the file is a CSV
            # Extracting file name without the '.csv' extension
            file_name_without_extension = os.path.splitext(filename)[0]

            file_path = os.path.join(folder_path, filename)  # Full path to the file
            df = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
            
            # Calculate 'MarketCap' by multiplying 'SHROUT' and 'PRC'
            df['MarketCap'] = df['SHROUT'] * df['PRC']
            
            # Adding the DataFrame to the dictionary with the file name as the key
            dataframes_dict[file_name_without_extension] = df

    return dataframes_dict