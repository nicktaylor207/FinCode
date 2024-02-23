from norm_volitility_curve import daily_normalized_volatility, average_normalized_volatility

import pandas as pd

# # Lesser Data
# file_path_small = '/Users/nicktaylor/Desktop/ORF_HW1/MarketCap_CSVs/Q3/XOM_2day.csv'
# df_XOM_small = pd.read_csv(file_path_small)

#XOM TAQ -- 2023 Nov 1st - Nov 30th
file_path = '/Users/nicktaylor/Desktop/ORF_HW1/MarketCap_CSVs/Q3/XOM_NOV-2023.csv'
df_XOM = pd.read_csv(file_path)




# ------------------- Plotting daily volitility curves -------------------
# #Plotting every days vol
# daily_normalized_volatility(df_XOM)


# ------------------- Plotting average volitility curves over days-------------------
average_normalized_volatility(df_XOM)
