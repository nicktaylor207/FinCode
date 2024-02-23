import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

import os


def plot_daily_normalized_volume(df, save_path=None):
    """
    Takes a DataFrame with trade data, filters by trading hours, and plots the
    normalized volume for each day within those hours.
    
    Parameters:
    - df: DataFrame containing columns 'DATE', 'TIME_M', and 'SIZE'.
    """
    # Combine 'DATE' and 'TIME_M' into a 'DATETIME' and set it as the index
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])
    df.set_index('DATETIME', inplace=True)

    trading_start = datetime.time(9, 30)
    trading_end = datetime.time(16, 0)

    # Create a mask that selects only the times within trading hours
    mask = (df.index.time >= trading_start) & (df.index.time <= trading_end)
    df = df[mask]

    # Calculate volume curves and daily volumes
    volume_curves = df.groupby(df.index.date).resample('15T').agg({'SIZE': 'sum'})
    daily_volumes = df.groupby(df.index.date)['SIZE'].sum()

    # Normalize the volume curves by the daily volumes
    normalized_volume = volume_curves['SIZE'] / volume_curves.index.get_level_values(0).map(daily_volumes)

    # Extract unique days for plotting
    unique_days = normalized_volume.index.get_level_values(0).unique()

    # Set up the plot
    num_plots = len(unique_days)
    num_cols = 2
    num_rows = num_plots // num_cols + (num_plots % num_cols > 0)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, num_rows * 3), squeeze=False)
    axes = axes.flatten()

    # Plot normalized volume for each day
    for i, day in enumerate(unique_days):
        day_data = normalized_volume.xs(day)
        times_str = [time.strftime('%H:%M') for time in day_data.index]
        axes[i].plot(times_str, day_data.values, label=f'Normalized Volume {day}')
        axes[i].set_title(f'Normalized Volume on {day}')
        axes[i].set_xlabel('Time')
        axes[i].set_ylabel('Normalized Volume')
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].legend()

    plt.tight_layout()

    # Save the plot to a file if a save_path is provided
    if save_path:
        plt.savefig(save_path)

    plt.show()



def plot_average_normalized_volume(df, save_path=None):
    """
    Processes a DataFrame to filter by trading hours, normalize the volume,
    calculate the average normalized volume across all days, and plot the result.

    Parameters:
    - df: DataFrame containing columns 'DATE', 'TIME_M', and 'SIZE'.
    """
    # Parse 'DATETIME' and set as index
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])
    df.set_index('DATETIME', inplace=True)

    # Define trading hours
    trading_start = datetime.time(9, 30)
    trading_end = datetime.time(16, 0)

    # Filter by trading hours
    mask = (df.index.time >= trading_start) & (df.index.time <= trading_end)
    df_filtered = df[mask]

    # Calculate the volume for each 15-minute bin
    volume_curves = df_filtered.groupby(df_filtered.index.date).resample('15T').agg({'SIZE': 'sum'})

    # Calculate daily volumes
    daily_volumes = df_filtered.groupby(df_filtered.index.date)['SIZE'].sum()

    # Normalize the volume curves by the daily volumes
    normalized_volume = volume_curves['SIZE'] / volume_curves.index.get_level_values(0).map(daily_volumes)


    df_normalized_volume = normalized_volume.to_frame(name='Normalized_Volume')
    df_normalized_volume.reset_index(inplace=True)
    df_normalized_volume.set_index('DATETIME', inplace=True)


    average_curve = df_normalized_volume.groupby(df_normalized_volume.index.time)['Normalized_Volume'].mean()

    # Convert times to minutes since midnight for plotting
    times = [t.hour * 60 + t.minute for t in average_curve.index]

    # Plot the average normalized volume curve
    plt.figure(figsize=(14, 7))
    plt.plot(times, average_curve.values, label='Average Normalized-Volume Curve', color='blue', linewidth=2)

    # Formatting the plot
    plt.title('Average Normalized-Volume Curve Across All Days')
    plt.xlabel('Time (mins since midnight)')
    plt.ylabel('Average Normalized Volume')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to fit all elements


    # Save the plot to a file if a save_path is provided
    if save_path:
        plt.savefig(save_path)

    # Show the plot
    plt.show()





