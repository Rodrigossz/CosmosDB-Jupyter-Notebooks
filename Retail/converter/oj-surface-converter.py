# This code converts the orignal Orange Juice dataset into Surface Seles data.
# It will create 2 files, json and csv. They are equivalent. 


import csv
import json
import pandas as pd
import uuid # to create an unique id for each data point
import datetime
from datetime import timedelta
import numpy as np

from pandas.tseries.frequencies import to_offset
from numpy.ma.testutils import assert_array_equal

csv_file = 'oj-AutoML.csv'
json_file_new = 'SurfaceSales.json'
csv_file_new = 'SurfaceSales.csv'
time_column_name = 'WeekStarting'


DS_FREQ = 'W-THU'
data = pd.read_csv(csv_file, parse_dates=[time_column_name])
data[time_column_name] = pd.to_datetime(data[time_column_name])
new_start = pd.Timestamp('2017.01.01')
dfs = []
for grain, df in data.groupby(['Store', 'Brand']):
    start = df[time_column_name].min()
    df['ix'] = df.index.values
    index = pd.DataFrame({
        time_column_name: pd.date_range(start, end=df[time_column_name].max(), freq=DS_FREQ),
        'empty': 0
    })
    df = index.merge(df, on=time_column_name, how='left')
    df['new_date'] = (pd.date_range(start + 27 * to_offset('YS') + start.week * to_offset(DS_FREQ), freq=DS_FREQ, periods = len(df))).strftime("%m-%d-%Y")
    df.dropna(subset=['ix'], inplace=True)
    df.drop(['ix', 'empty'], inplace=True, axis=1)
    dfs.append(df)
data = pd.concat(dfs)
#data['new_date'] = [new_start + dt.week * to_offset('W-MON')  for dt in data[time_column_name]]
#Sanity check
assert data.duplicated(subset=[time_column_name, 'Store', 'Brand']).sum() == 0
#weeks_before = np.array([dt.week for dt in data[time_column_name]])
#weeks_after = np.array([dt.week for dt in data['new_date']])
#assert_array_equal(weeks_before, weeks_after)

 

data.drop(time_column_name, axis=1, inplace=True)
data.rename({'new_date': time_column_name}, axis=1, inplace=True)


# Final  fixies
data['Quantity']= (data.Quantity/100).astype('int')
data['Price']= (data.Price*100.00)
data['Advert']= (data.Advert).astype('int')
data['Store']= (data.Store).astype('int')
data.rename({'Large HH': 'largeHH'}, axis=1, inplace=True)
data.rename({'Store': 'storeId'}, axis=1, inplace=True)
data.rename({'Quantity': 'quantity'}, axis=1, inplace=True)
data.rename({'Brand': 'productCode'}, axis=1, inplace=True)
data.rename({'Price': 'price'}, axis=1, inplace=True)
data.rename({'Advert': 'advertising'}, axis=1, inplace=True)
data.rename({'COLLEGE': 'collegeRatio'}, axis=1, inplace=True)
data.rename({'INCOME': 'income'}, axis=1, inplace=True)
data.rename({'Hincome150': 'highIncome150Ratio'}, axis=1, inplace=True)
data.rename({'CPWVOL5': 'salesNearest5StoresRatio'}, axis=1, inplace=True)
data.rename({'CPDIST5': 'avgDistanceNearest5Supermarkets'}, axis=1, inplace=True)
data.rename({'SSTRVOL': 'salesNearestWarehousesRatio'}, axis=1, inplace=True)
data.rename({'SSTRDIST': 'distanceNearestWarehouse'}, axis=1, inplace=True)
data.rename({'WorkingWoman': 'more1FullTimeEmployeeRatio'}, axis=1, inplace=True)
data.rename({'Minorities': 'minoritiesRatio'}, axis=1, inplace=True)
data.rename({'WeekStarting': 'weekStarting'}, axis=1, inplace=True)
data.rename({'Age60': 'ratioAge60'}, axis=1, inplace=True)


# #renaming the products
rename_dt = {'dominicks': 'surface.go', 'minute.maid': 'surface.pro7', 'tropicana': 'surface.laptop3'}
data['productCode'] = data.apply(lambda x: rename_dt[x['productCode']], axis=1)


#ids to string
data['id'] = [str(uuid.uuid4()) for _ in range(len(data))]


data.to_json(json_file_new, orient = "records",double_precision = 4,lines=True)
data.to_csv(csv_file_new)


data.head()