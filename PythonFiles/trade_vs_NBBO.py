import pandas as pd
import numpy as np
import matplotlib.pyplot as plt





def analyze_trade_vs_nbbo(file_path_quotes, file_path_trades):
    # Load the data
    df_CLNE_Q = pd.read_csv(file_path_quotes)
    df_CLNE_T = pd.read_csv(file_path_trades)

    # Calculate total records per exchange and filter out unreasonable exchanges
    threshold_BID = df_CLNE_Q.groupby('EX')['BIDSIZ'].sum().quantile(0.50)
    threshold_ASK = df_CLNE_Q.groupby('EX')['ASKSIZ'].sum().quantile(0.50)
    reasonable_exchanges = df_CLNE_Q.groupby('EX').filter(lambda x: (x['BIDSIZ'].sum() > threshold_BID) & (x['ASKSIZ'].sum() > threshold_ASK) and 'D' not in x['EX'].unique())['EX'].unique()

    # Filter df_quotes and df_trades to only include reasonable exchanges
    df_CLNE_Q = df_CLNE_Q[df_CLNE_Q['EX'].isin(reasonable_exchanges)]
    df_CLNE_T = df_CLNE_T[df_CLNE_T['EX'].isin(reasonable_exchanges)]

    # Convert TIME_M to seconds since midnight for filtering by market hours
    df_CLNE_T['Seconds_Since_Midnight'] = pd.to_timedelta(df_CLNE_T['TIME_M']).dt.total_seconds()
    df_CLNE_Q['Seconds_Since_Midnight'] = pd.to_timedelta(df_CLNE_Q['TIME_M']).dt.total_seconds()

    # Define market hours in seconds since midnight
    market_start_seconds = 9 * 3600 + 30 * 60  # 9:30 AM
    market_end_seconds = 16 * 3600  # 4:00 PM

    # Filter by market hours
    df_CLNE_T_MH = df_CLNE_T[(df_CLNE_T['Seconds_Since_Midnight'] >= market_start_seconds) & (df_CLNE_T['Seconds_Since_Midnight'] <= market_end_seconds)]
    df_CLNE_Q_MH = df_CLNE_Q[(df_CLNE_Q['Seconds_Since_Midnight'] >= market_start_seconds) & (df_CLNE_Q['Seconds_Since_Midnight'] <= market_end_seconds)]

    # Set TIME_M as index and sort
    df_CLNE_T_MH.set_index('TIME_M', inplace=True)
    df_CLNE_Q_MH.set_index('TIME_M', inplace=True)
    df_CLNE_T_MH.sort_index(inplace=True)
    df_CLNE_Q_MH.sort_index(inplace=True)

    # Forward fill NBBO Bid and Ask
    df_CLNE_T_MH['NBBO_Bid'] = df_CLNE_Q_MH['BID'].reindex(df_CLNE_T_MH.index, method='ffill')
    df_CLNE_T_MH['NBBO_Ask'] = df_CLNE_Q_MH['ASK'].reindex(df_CLNE_T_MH.index, method='ffill')

    # Classify each trade's relation to NBBO
    df_CLNE_T_MH['Below_Bid'] = df_CLNE_T_MH['PRICE'] < df_CLNE_T_MH['NBBO_Bid']
    df_CLNE_T_MH['At_Bid'] = df_CLNE_T_MH['PRICE'] == df_CLNE_T_MH['NBBO_Bid']
    df_CLNE_T_MH['In_Spread'] = (df_CLNE_T_MH['PRICE'] > df_CLNE_T_MH['NBBO_Bid']) & (df_CLNE_T_MH['PRICE'] < df_CLNE_T_MH['NBBO_Ask'])
    df_CLNE_T_MH['At_Ask'] = df_CLNE_T_MH['PRICE'] == df_CLNE_T_MH['NBBO_Ask']
    df_CLNE_T_MH['Above_Ask'] = df_CLNE_T_MH['PRICE'] > df_CLNE_T_MH['NBBO_Ask']

    # Calculate fractions
    fraction_below_bid = df_CLNE_T_MH['Below_Bid'].mean()
    fraction_at_bid = df_CLNE_T_MH['At_Bid'].mean()
    fraction_in_spread = df_CLNE_T_MH['In_Spread'].mean()
    fraction_at_ask = df_CLNE_T_MH['At_Ask'].mean()
    fraction_above_ask = df_CLNE_T_MH['Above_Ask'].mean()

    # Print results
    print("Fraction of trades in relation to NBBO:")
    print(f"Below the Bid: {fraction_below_bid}")
    print(f"At the Bid: {fraction_at_bid}")
    print(f"In the Spread: {fraction_in_spread}")
    print(f"At the Ask: {fraction_at_ask}")
    print(f"Above the Ask: {fraction_above_ask}")






def plotting_trade_vs_nbbo(file_path_quotes, file_path_trades):
    # Load the data
    df_CLNE_Q = pd.read_csv(file_path_quotes)
    df_CLNE_T = pd.read_csv(file_path_trades)

    # Calculate total records per exchange and filter out unreasonable exchanges
    threshold_BID = df_CLNE_Q.groupby('EX')['BIDSIZ'].sum().quantile(0.50)
    threshold_ASK = df_CLNE_Q.groupby('EX')['ASKSIZ'].sum().quantile(0.50)
    reasonable_exchanges = df_CLNE_Q.groupby('EX').filter(lambda x: (x['BIDSIZ'].sum() > threshold_BID) & (x['ASKSIZ'].sum() > threshold_ASK) and 'D' not in x['EX'].unique())['EX'].unique()

    # Filter df_quotes and df_trades to only include reasonable exchanges
    df_CLNE_Q = df_CLNE_Q[df_CLNE_Q['EX'].isin(reasonable_exchanges)]
    df_CLNE_T = df_CLNE_T[df_CLNE_T['EX'].isin(reasonable_exchanges)]

    # Convert TIME_M to seconds since midnight for filtering by market hours
    df_CLNE_T['Seconds_Since_Midnight'] = pd.to_timedelta(df_CLNE_T['TIME_M']).dt.total_seconds()
    df_CLNE_Q['Seconds_Since_Midnight'] = pd.to_timedelta(df_CLNE_Q['TIME_M']).dt.total_seconds()

    # Define market hours in seconds since midnight
    market_start_seconds = 9 * 3600 + 30 * 60  # 9:30 AM
    market_end_seconds = 16 * 3600  # 4:00 PM

    # Filter by market hours
    df_CLNE_T_MH = df_CLNE_T[(df_CLNE_T['Seconds_Since_Midnight'] >= market_start_seconds) & (df_CLNE_T['Seconds_Since_Midnight'] <= market_end_seconds)]
    df_CLNE_Q_MH = df_CLNE_Q[(df_CLNE_Q['Seconds_Since_Midnight'] >= market_start_seconds) & (df_CLNE_Q['Seconds_Since_Midnight'] <= market_end_seconds)]

    # Set TIME_M as index and sort
    df_CLNE_T_MH.set_index('TIME_M', inplace=True)
    df_CLNE_Q_MH.set_index('TIME_M', inplace=True)
    df_CLNE_T_MH.sort_index(inplace=True)
    df_CLNE_Q_MH.sort_index(inplace=True)

    # Forward fill NBBO Bid and Ask
    df_CLNE_T_MH['NBBO_Bid'] = df_CLNE_Q_MH['BID'].reindex(df_CLNE_T_MH.index, method='ffill')
    df_CLNE_T_MH['NBBO_Ask'] = df_CLNE_Q_MH['ASK'].reindex(df_CLNE_T_MH.index, method='ffill')

    # --------------------------------- Plotting ---------------------------------
    plt.figure(figsize=(60, 40))  # Adjust the figure size as needed
    # Plot 'NBBO_Bid'
    plt.plot(df_CLNE_T_MH.index, df_CLNE_T_MH['NBBO_Bid'], label='NBBO Bid', linestyle='-', marker='', color='blue')
    # Plot 'NBBO_Ask'
    plt.plot(df_CLNE_T_MH.index, df_CLNE_T_MH['NBBO_Ask'], label='NBBO Ask', linestyle='-', marker='', color='red')
    # Plot 'PRICE'
    plt.plot(df_CLNE_T_MH.index, df_CLNE_T_MH['PRICE'], label='Trade Price', marker='x', color='green')

    # Labeling
    plt.title('NBBO Bid/Ask and Trade Price Over Time')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()

    plt.show()