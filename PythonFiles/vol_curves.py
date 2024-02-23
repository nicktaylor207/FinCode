import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

import os



def read_csv_files_into_dataframes(folder_path):
    # Dictionary to hold your dataframes with 'df_' + file name (without extension) as keys
    dataframes_dict = {}

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):  # Check if the file is a CSV
            # Extracting file name without the '.csv' extension
            file_name_without_extension = os.path.splitext(filename)[0]

            # Construct the key by adding 'df_' prefix
            dataframe_key = 'df_' + file_name_without_extension

            # Full path to the file
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file into a DataFrame and add it to the dictionary
            dataframes_dict[dataframe_key] = pd.read_csv(file_path)

            print(f"{filename} has been read into a dataframe named '{dataframe_key}'.")

    return dataframes_dict




def plot_daily_volume_curves(df, title_prefix=''):
    """
    Plots volume curves for the DataFrame provided, within trading hours, 
    grouped by day with 15-minute bins.

    Parameters:
    - df: DataFrame. The DataFrame containing the trade data.
    - title_prefix: str. A prefix for the plot titles (usually the stock symbol).
    """
    # Create 'DATETIME' column and set it as index
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])
    df.set_index('DATETIME', inplace=True)

    # Define trading hours
    trading_start = datetime.time(9, 30)
    trading_end = datetime.time(16, 0)

    # Filter out trades outside of trading hours
    mask = (df.index.time >= trading_start) & (df.index.time <= trading_end)
    df = df[mask]

    # Calculate volume curves
    volume_curves = df.groupby(df.index.date).resample('15T').agg({'SIZE': 'sum'})
    volume_curves.reset_index(inplace=True)
    volume_curves['level_0'] = pd.to_datetime(volume_curves['level_0'])
    volume_curves.set_index('DATETIME', inplace=True)

    # Group by 'level_0' (the day)
    grouped = volume_curves.groupby('level_0')

    # Calculate the number of rows needed for subplots (5 plots per row)
    num_days = len(grouped)
    num_rows = (num_days + 4) // 5

    # Create a figure with a grid of subplots
    fig, axes = plt.subplots(num_rows, 5, figsize=(20, num_rows * 4), constrained_layout=True)
    axes = axes.flatten()

    # Plot each day's volume curve
    for ax, (name, group) in zip(axes, grouped):
        group['SIZE'].plot(ax=ax)
        ax.set_title(f"{title_prefix} {name.date()}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Volume')

    # Turn off any unused subplots
    for i in range(num_days, num_rows * 5):
        axes[i].axis('off')

    plt.show()




def plot_average_volume_curve(df):
    """
    Plots the average volume curve across all days for the given DataFrame within specified trading hours.

    Parameters:
    - df: DataFrame. The DataFrame containing the trade data with 'DATE' and 'TIME_M' columns.
    """


    # Create 'DATETIME' column and set it as index
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])
    df.set_index('DATETIME', inplace=True)

    # Define trading hours
    trading_start = datetime.time(9, 30)
    trading_end = datetime.time(16, 0)

    # Create a mask that selects only the times within trading hours
    mask = (df.index.time >= trading_start) & (df.index.time <= trading_end)
    df = df[mask]

    # Group by date and resample into 15-minute bins
    volume_curves = df.groupby(df.index.date).resample('15T').agg({'SIZE': 'sum'})
    volume_curves.reset_index(inplace=True, drop=False)

    # Group by the time to calculate the average volume for each 15-minute bin across all days
    average_curve = volume_curves.groupby(volume_curves['DATETIME'].dt.time)['SIZE'].mean()

    # Convert times to minutes since midnight for plotting
    times = [t.hour * 60 + t.minute for t in average_curve.index]
    
    # Plot the average curve
    plt.figure(figsize=(14, 7))
    plt.plot(times, average_curve.values, label='Average Volume Curve', color='blue', linewidth=2)

    # Formatting the plot
    plt.title('Average Volume Curve Across All Days')
    plt.xlabel('Time (mins since midnight)')
    plt.ylabel('Average Volume')
    plt.legend()
    plt.grid(True)
    # Set x-ticks to be more meaningful (every 60 minutes)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to fit all elements

    # Show the plot
    plt.show()


