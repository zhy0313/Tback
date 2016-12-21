# -*- coding: utf-8 -*-

"""
TradingStrategy
__author__ = ‘Administrator‘
__mtime__ = 2016/12/19
"""

import pandas
mydata = [{'subid' : 'A', 'Close_date_wk': 25, 'week_diff':3},
          {'subid' : 'B', 'Close_date_wk': 26, 'week_diff':2},
          {'subid' : 'C', 'Close_date_wk': 27, 'week_diff':2},]
df = pandas.DataFrame(mydata)

for index, row in df.iterrows():
    i = 0
    # print index
    print row
    max_range = row['Close_date_wk']
    min_range = int(row['Close_date_wk'] - row['week_diff'])
    for i in range(min_range,max_range):
        col_head = 'job_week_'  +  str(i)
        row[col_head] = 1