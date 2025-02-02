
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html

# https://en.wikipedia.org/wiki/Misleading_graph

df = pd.DataFrame({
    'num': np.arange(3) + 2,
    'years': ['2018', '2019', '2020'],
    'values': [1, 2, 3],

})
df.plot()  # 직선. x: index, y: all numeric columns
df.plot(kind='bar')  # bar
df.plot(x="years", y="values", # x, y column
        kind='bar',
        figsize=(10, 5),
        rot=0  # x label rotation
        )
ax = df.plot.bar(figsize=(4, 4), legend=False)  # pie차트는 어떠한 경우에도 권장되지 않는다고..
ax.set_xlabel('Cause of delay')
ax.set_ylabel('Count')

plt.show()

#%%
import matplotlib.pyplot as plt
ax = df.hist(column='num', bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
plt.show()
