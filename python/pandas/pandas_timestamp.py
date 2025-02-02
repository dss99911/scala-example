from datetime import date, datetime

import numpy as np
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
dates = pd.date_range("20130101", periods=6)
df_number = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)

# %%

#날짜 텍스트를 날짜로 변환
df_datetime_text = pd.read_csv('data/SP500_NOV2019_Hist.csv')
df_datetime = pd.to_datetime(df_datetime_text['Date']).to_frame()

# timedelta
days = (df_datetime.loc[:, "Date"] - df_datetime.loc[:, "Date"]) # 21 days 00:00:00
month_from = np.floor(days.dt.days / 30).astype(np.int64) # 21 / 30

# datetime index -> timestamp -> datetime index
df_number.index = list(map(lambda d: datetime(d.year, d.month, 1), df_number.index.tolist()))

# timestamp index
df_loc_date_index = df_number.loc['2013'] # get rows with date like
df_loc_date_index2 = df_number.sort_index().loc["2021-07-05T01:11":"2021-07-05T01:16"] # get rows with date like
df_loc_date_index3 = df_number.sort_index().loc[datetime(2021,7,5,1,11):datetime(2021,7,5,1,16)] # need `sort_index()` for range loc()

#%%

# 하나의 데이터도 Timestamp로 변환 가능
timestamp_data = pd.to_datetime("11/1/2019")

#%% long to datetime
df['time'] = pd.to_datetime(df['time'], unit='ms')

#%% datetime to str
df['year_month'] = df['event_time'].dt.strftime('%Y-%m')