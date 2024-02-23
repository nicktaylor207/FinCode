from market_Cap import calculating_market_cap
from vol_curves import read_csv_files_into_dataframes, plot_daily_volume_curves, plot_average_volume_curve
from norm_volume_curve import plot_daily_normalized_volume, plot_average_normalized_volume

import matplotlib.pyplot as plt
import pandas as pd





# ---------------------------------- (A) Market Cap Dataframes----------------------------------

# # Define the folder path
# folder_path_marketCap = '/Users/nicktaylor/Desktop/ORF_HW1/MarketCap_CSVs/Q2'
# dfs_marketCap = calculating_market_cap(folder_path_marketCap)

# # Defining Market-Cap dataframes
# df_PSX_marketCap = dfs_marketCap['PSX']
# df_MPC_marketCap = dfs_marketCap['MPC']
# df_VLO_marketCap = dfs_marketCap['VLO']
# df_XOM_marketCap = dfs_marketCap['XOM']
# df_CVX_marketCap = dfs_marketCap['CVX']
# df_EOG_marketCap = dfs_marketCap['EOG']
# df_COP_marketCap = dfs_marketCap['COP']
# df_PXD_marketCap = dfs_marketCap['PXD']
# df_WMB_marketCap = dfs_marketCap['WMB']
# df_SLB_marketCap = dfs_marketCap['SLB']


# def calculate_average_market_cap_per_company(dfs_marketCap):
#     """
#     Calculates the average market cap for each company based on the values stored in each DataFrame.

#     Parameters:
#     - dfs_marketCap: dict. A dictionary where keys are stock symbols and values are DataFrames containing 'MarketCap'.

#     Returns:
#     - dict: A dictionary with stock symbols as keys and their average market cap as values.
#     """
#     average_market_caps = {}

#     for stock_symbol, df in dfs_marketCap.items():
#         # Calculate the mean of the 'MarketCap' column for each DataFrame
#         average_market_caps[stock_symbol] = df['MarketCap'].mean()

#     return average_market_caps


# # Example usage:
# # Assuming dfs_marketCap is a dictionary with your DataFrames keyed by stock symbols
# average_market_cap = calculate_average_market_cap_per_company({
#     'PSX': df_PSX_marketCap,
#     'MPC': df_MPC_marketCap,
#     'VLO': df_VLO_marketCap,
#     'XOM': df_XOM_marketCap,
#     'CVX': df_CVX_marketCap,
#     'EOG': df_EOG_marketCap,
#     'COP': df_COP_marketCap,
#     'PXD': df_PXD_marketCap,
#     'WMB': df_WMB_marketCap,
#     'SLB': df_SLB_marketCap,
# })


# print(average_market_cap)


# ---------------------------------- (B) Volume Curve Dataframes----------------------------------

#Define the foler path
folder_path_TAQ = '/Users/nicktaylor/Desktop/ORF_HW1/TAQ_CSVs/Q2'
dfs_TAQ = read_csv_files_into_dataframes(folder_path_TAQ)

# Defining TAQ dataframes
df_CVX_TAQ = dfs_TAQ['df_CVX_TAQ']
df_WMB_TAQ = dfs_TAQ['df_WMB_TAQ']
df_MPC_TAQ = dfs_TAQ['df_MPC_TAQ']
df_EOG_TAQ = dfs_TAQ['df_EOG_TAQ']
df_COP_TAQ = dfs_TAQ['df_COP_TAQ']
df_XOM_TAQ = dfs_TAQ['df_XOM_TAQ']
df_VLO_TAQ = dfs_TAQ['df_VLO_TAQ']
df_SLB_TAQ = dfs_TAQ['df_SLB_TAQ']
df_PSX_TAQ = dfs_TAQ['df_PSX_TAQ']
df_PXD_TAQ = dfs_TAQ['df_PXD_TAQ']

# # Plots daily volume curve for 2023 November
# plot_daily_volume_curves(df_CVX_TAQ, title_prefix='CVX')

# # Plots the month average volume for 2023 November
# plot_average_volume_curve(df_CVX_TAQ)




# ---------------------------------- (C) Normalized-Volume Curve Dataframes----------------------------------


# # Plot the daily normalized Volume for XOM
# plot_daily_normalized_volume(df_XOM_TAQ, save_path='/Users/nicktaylor/Desktop/normalized_volume_plot.png')


plot_average_normalized_volume(df_CVX_TAQ, save_path='/Users/nicktaylor/Desktop/average_normalized_volume_plot.png')






