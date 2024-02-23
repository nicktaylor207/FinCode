import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import time

def daily_normalized_volatility(df):
    # Ensure the 'DATE' and 'TIME_M' columns are in the correct format
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])
    df.set_index('DATETIME', inplace=True)
    
    # Calculating the NBBO Point
    df['MIDPOINT'] = (df['BID'] + df['ASK']) / 2
    
    # Eliminating single posts to understand marketmakers
    df = df.loc[(df['BID'] != 0) & (df['ASK'] != 0)]
    
    # Incremental conversion T1 (∆t = 1min)
    Mid_curves = df.resample('1T').agg({'MIDPOINT': 'last'})
    Mid_curves['PRICE_DIFF'] = Mid_curves['MIDPOINT'].diff()
    Mid_curves['SQUARED_DIFF'] = Mid_curves['PRICE_DIFF'] ** 2
    
    # Incremental conversion T15 (∆t = 15min)
    squared_diff_curves = Mid_curves.groupby(Mid_curves.index.date).resample('15T').agg({'SQUARED_DIFF': 'sum'})
    daily_vol = squared_diff_curves.groupby(squared_diff_curves.index.get_level_values(0))['SQUARED_DIFF'].sum()
    normalized_vol = squared_diff_curves['SQUARED_DIFF'] / squared_diff_curves.index.get_level_values(0).map(daily_vol)
    
    df_normalized_Vol = pd.DataFrame(normalized_vol, columns=['Normalized_Vol'])
    df_normalized_Vol.reset_index(inplace=True)
    df_normalized_Vol.set_index('DATETIME', inplace=True)
    
    # Only selecting trading days
    trading_start = time(9, 30)
    trading_end = time(16, 0)
    mask = (df_normalized_Vol.index.time >= trading_start) & (df_normalized_Vol.index.time <= trading_end)
    df_normalized_Vol_filtered = df_normalized_Vol[mask]
    
    # Plotting
    trading_start_timedelta = pd.Timedelta(hours=9, minutes=30) # Converting to mins into trading day
    df_normalized_Vol_filtered['Time_Since_930'] = (df_normalized_Vol_filtered.index - pd.to_datetime(df_normalized_Vol_filtered.index.date) - trading_start_timedelta).total_seconds() / 60.0  # Convert to minutes
    
    unique_dates = np.unique(df_normalized_Vol_filtered.index.date)
    for date in unique_dates:
        df_day = df_normalized_Vol_filtered.loc[df_normalized_Vol_filtered.index.date == date]
        plt.figure(figsize=(10, 6))
        plt.plot(df_day['Time_Since_930'], df_day['Normalized_Vol'], linestyle='-')
        
        plt.title(f'Normalized Volatility since 9:30 AM for {date}')
        plt.xlabel('Minutes since 9:30 AM')
        plt.ylabel('Normalized Volatility')
        plt.xticks(np.arange(0, max(df_day['Time_Since_930'])+1, 60), rotation=45)
        
        plt.show()




def average_normalized_volatility(df):
    # Ensure the 'DATE' and 'TIME_M' columns are in the correct format
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME_M'])
    df.set_index('DATETIME', inplace=True)
    
    # Calculating the NBBO Point
    df['MIDPOINT'] = (df['BID'] + df['ASK']) / 2
    
    # Eliminating single posts to understand marketmakers
    df = df.loc[(df['BID'] != 0) & (df['ASK'] != 0)]
    
    # Incremental conversion T1 (∆t = 1min)
    Mid_curves = df.resample('1T').agg({'MIDPOINT': 'last'})
    Mid_curves['PRICE_DIFF'] = Mid_curves['MIDPOINT'].diff()
    Mid_curves['SQUARED_DIFF'] = Mid_curves['PRICE_DIFF'] ** 2
    
    # Incremental conversion T15 (∆t = 15min)
    squared_diff_curves = Mid_curves.groupby(Mid_curves.index.date).resample('15T').agg({'SQUARED_DIFF': 'sum'})
    daily_vol = squared_diff_curves.groupby(squared_diff_curves.index.get_level_values(0))['SQUARED_DIFF'].sum()
    normalized_vol = squared_diff_curves['SQUARED_DIFF'] / squared_diff_curves.index.get_level_values(0).map(daily_vol)
    
    df_normalized_Vol = pd.DataFrame(normalized_vol, columns=['Normalized_Vol'])
    df_normalized_Vol.reset_index(inplace=True)
    df_normalized_Vol.set_index('DATETIME', inplace=True)
    
    # Only selecting trading days
    trading_start = time(9, 30)
    trading_end = time(16, 0)
    mask = (df_normalized_Vol.index.time >= trading_start) & (df_normalized_Vol.index.time <= trading_end)
    df_normalized_Vol_filtered = df_normalized_Vol[mask]

    #Calulating average volitlity at each time of every day
    average_normalized_Vol_curve = df_normalized_Vol_filtered.groupby(df_normalized_Vol_filtered.index.time)['Normalized_Vol'].mean()

    # Convert times to minutes since market open for plotting
    times = [t.hour * 60 + t.minute - 570 for t in average_normalized_Vol_curve.index]

    # Plot the average normalized volume curve
    plt.figure(figsize=(14, 7))
    plt.plot(times, average_normalized_Vol_curve.values, label='Average Normalized-Volitility Curve', color='blue', linewidth=2)

    # Formatting the plot
    plt.title('Average Normalized-Volitility Curve Across All Days')
    plt.xlabel('Time (mins since midnight)')
    plt.ylabel('Average Normalized Volitility')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to fit all elements

    # Show the plot
    plt.show()
    


