import os
import pandas as pd
import datetime

main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'
merged = os.path.join(main, 'final_merge.csv')
df_merged = pd.read_csv(merged)

#check initial instances
print('Shape of intial df: ', df_merged.shape) #(2775294, 39) -> (875262, 36)
print('Type of original df[deed_date]: ', type(df_merged['deed_date'])) #<class 'pandas.core.series.Series'>
print('dtype of original df[deed_date]: ', df_merged['deed_date'].dtype) #Object

#Convert ['deed_date'] to datetime format
df_merged['deed_date'] = pd.to_datetime(df_merged['deed_date'])
print('dtype of converted df[deed_date]: ', df_merged['deed_date'].dtype) #datetime64[ns]
print('type of')

#Eliminate old dates:
limit_date = '2010-01-01'
df_merged = df_merged[(df_merged['deed_date'] >= limit_date)]

#Create year column:
df_merged['year'] = df_merged['deed_date'].dt.year
print(df_merged.head(10))
print('dtype of [year] column: ', df_merged['year'].dtype) #int64

#Create Quarter column:
df_merged['quarter'] = df_merged['deed_date'].dt.to_period('Q')
print(df_merged.head(10))
print('dtype of [quarter] column: ', df_merged['quarter'].dtype) #period[Q-DEC]

#save
df_merged.to_csv(os.path.join(main, 'final_merge1.csv'), index=False, encoding='utf-8')