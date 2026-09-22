import pandas as pd

file_path = 'IR014_1data.csv'
data = pd.read_csv(file_path)
data.head()
#数据描述性统计
description = data.describe()
# 描述性统计加入偏度和峰度
additional_stats = data.agg(['skew', 'kurtosis'])
#描述性统计结果汇总
combined_description = pd.concat([description, additional_stats])

print(combined_description)