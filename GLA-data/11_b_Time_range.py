import os
import pandas as pd
import datetime

# main = 'C:\\Users\\joaopaulo\\Desktop'
main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'
merged = os.path.join(str(main), 'final_merge1.csv')
df_merged = pd.read_csv(merged)

#Check initial instances
print('Shape of initial df: ', df_merged.shape) #(5243, 35) -> (2888739, 35) -> (2888739, 39) -> (1147948, 41)
print('Type of initial df[deed_date]: ', type(df_merged['deed_date'])) #object
print('Type of initial df[LODGEMENT_DATE]: ', type(df_merged['LODGEMENT_DATE'])) #object

#filter by dates
df_merged['deed_date'] = pd.to_datetime(df_merged['deed_date'])
# df_merged['deed_date'] = pd.to_datetime(df_merged['deed_date'], format='%d%m%y')
print('Type of converted df[deed_date]: ', df_merged['deed_date'].dtypes) #datetime64[ns]

df_merged['LODGEMENT_DATE'] = pd.to_datetime(df_merged['LODGEMENT_DATE'])
print('Type of converted df[LODGEMENT_DATE]: ', df_merged['LODGEMENT_DATE'].dtypes) #datetime64[ns]

#date range:
# init_date = '2009-01-01'
# end_date = '2013-12-31'
#First ML attempt was with this range: 2010 -> 2012
# init_date = '2010-01-01'
# end_date = '2012-12-31'
#Second attempt with 2011y only
# init_date = '2011-01-01'
# end_date = '2011-12-31'
#Third attempt with 2y-span and 2011 in the middle (6m+2011+6m)
# init_date = '2010-06-01'
# end_date = '2012-06-01'
#Fourth attempt: 3y! - Accuracy decreased
# init_date = '2010-01-01'
# end_date = '2012-12-31'

#Third attempt considering quarters (approximation of Third attempt - 6m+2011+6m)
# init_date = '2010-07-01'
# end_date = '2012-06-30'
#Time-series attempt: From 2010Q1 to last dates in 2021.
init_date = '2010-01-01'

# df2 = df_merged[(df_merged['deed_date'] >= init_date)
#                 & (df_merged['deed_date'] <= end_date)]
df2 = df_merged[(df_merged['deed_date'] >= init_date)]

#Check remaining instances
print('Type of final df2: ', df2.shape)#(203855, 41) -> (1147948, 41) -> (875262, 36)
print('Type of converted df[deed_date]: ', df2['deed_date'].dtypes) #datetime64[ns]
print('Type of final df2[LODGEMENT_DATE]: ', df2['LODGEMENT_DATE'].dtypes) #datetime64[ns]
#print(df2.loc[50,:])

#save
df2.to_csv(os.path.join(main, 'final_merge2.csv'), index=False, encoding='utf-8')