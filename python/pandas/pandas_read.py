from datetime import date, datetime

import numpy as np
import pandas as pd
from pandas import DataFrame
#%% parquet


df_from_parquet = pd.read_parquet("path")

#%% csv
adult_columns = [
    "Age",
    "Workclass",
]
pd.read_csv("adult.test",
            names=adult_columns,  # columns
            sep=r"\s*,\s*", engine="python",  # for using sep, engine should be python. default is 'c'
            na_values="?",
            skiprows=1)  # skip first row
df_from_csv = pd.read_csv("path")

#%% excel
# pip install -U openpyxl
df_from_excel: DataFrame = pd.read_excel("path", index_col=0, sheet_name='Sheet3')

#%% set index
df_index = pd.read_csv("data/SP500_NOV2019_Hist.csv", index_col=0)

#%% parse datetime
df_date = pd.read_csv("data/SP500_NOV2019_Hist.csv", index_col=0, parse_dates=True)