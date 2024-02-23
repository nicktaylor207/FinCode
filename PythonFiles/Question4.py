from trade_vs_NBBO import  analyze_trade_vs_nbbo, plotting_trade_vs_nbbo

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt





file_path_CLNE_Quotes = '/Users/nicktaylor/Desktop/ORF_HW1/CLNE_TAQ/CLNE_Quotes.csv'
file_path_CLNE_Trades = '/Users/nicktaylor/Desktop/ORF_HW1/CLNE_TAQ/CLNE_Trades.csv'

analyze_trade_vs_nbbo(file_path_CLNE_Quotes, file_path_CLNE_Trades)
plotting_trade_vs_nbbo(file_path_CLNE_Quotes, file_path_CLNE_Trades)






