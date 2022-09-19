import os
import pandas as pd

# main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC TEST'
main = 'C:\\Users\\joaopaulo\\Desktop'
# main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'
cert = os.path.join(str(main), 'final_merge3.csv')
# cert = os.path.join(str(main), 'final_merge3_TEST.csv')
df_cert = pd.read_csv(cert)

data_dir = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\Downloads and data'
# data = os.path.join(data_dir, '03 5 - My Fare Zone', 'MyLondon_fare_zone_OA.csv')
# df_MFZ = pd.read_csv(data)

#Function to parse dataframes:
def parse_data(main_dir, sub_dir, file, encoding):
    df_os = os.path.join(main_dir, sub_dir, file)
    df = pd.read_csv(df_os, encoding=encoding)
    return df


#Function to save dataframes
def save(df_save, file_name):
    save_df = df_save.to_csv(os.path.join(main, file_name), index=False, encoding='utf-8')
    return save_df

#My Fare Zone
df_MFZ = parse_data(data_dir, '03 5 - My Fare Zone', 'MyLondon_fare_zone_OA.csv', 'utf-8')
df_MFZ = df_MFZ.rename(columns={'OA11CD': 'oa11'})
#Merge
df_cert = pd.merge(df_cert, df_MFZ, on='oa11', how='left')
#Close right dataframe:
del df_MFZ

#Deprivation index
df_dep = parse_data(data_dir, '2011 UK Townsend Deprivation Scores', 'Scores- 2011 UK LSOA.csv', 'utf-8')
df_dep = df_dep.rename(columns={'GEO_CODE': 'lsoa11', 'TDS': 'Deprivation_Index'})
df_dep.drop(columns={'ID', 'GEO_LABEL', 'quintile'}, inplace=True)
#Merge
df_cert = pd.merge(df_cert, df_dep, on='lsoa11', how='left')
#Close right dataframe:
del df_dep

#Distance from Bank Station
df_bank = parse_data(data_dir, '03 4 - Travel time to Bank Station', 'MyLondon_traveltime_to_Bank_station_OA.csv',
                     'utf-8')
df_bank = df_bank.rename(columns={'OA11CD': 'oa11'})
df_bank.drop(columns={'driving_time_mins', 'public_transport_time_mins', 'cycling_distance_miles', 'cycling_time_mins',
                     'walking_distance_miles', 'walking_time_mins'}, inplace=True)
#Merge
df_cert = pd.merge(df_cert, df_bank, on='oa11', how='left')
#Close right datafame:
del df_bank

#Average House Prices for LSOAs:
df_price = parse_data(data_dir, '02 2 - Median Housing & Sales', 'house-prices-LSOAs.csv', 'latin1')
df_price = df_price.rename(columns={'Lower Super Output Area': 'lsoa11'})
#Replace '.' Value from Median(£)-2011
df_price['Median(£)-2011'] = df_price['Median(£)-2010'].\
    where(df_price['Median(£)-2011'] == '.', other=df_price['Median(£)-2011'])
# print('nan values remaining in Median(£)-2011: ', df_price['Median(£)-2011'].str.count('.').sum())
print('nan values remaining in Median(£)-2011: ', df_price['Median(£)-2011'].isin(['.']).sum())
df_price['Median(£)-2011'] = df_price['Median(£)-2012'].\
    where(df_price['Median(£)-2011'] == '.', other=df_price['Median(£)-2011'])
print('nan values remaining in Median(£)-2011: ', df_price['Median(£)-2011'].isin(['.']).sum())
df_price.drop(df_price.columns.difference(['lsoa11', 'Median(£)-2011']), 1, inplace=True)
# df_price['Median(£)-2011'] = df_price['Median(£)-2011'].str.replace({',', ''}, regex=True).astype('float')
df_price['Median(£)-2011'] = df_price['Median(£)-2011'].str.replace(',', '')
df_price['Median(£)-2011'] = pd.to_numeric(df_price['Median(£)-2011'])
# df_price = df_price['Median(£)-2011'].convert_dtypes()
print('Data type of Median(£)-2011 column: ', df_price['Median(£)-2011'].dtypes)
print('DAta type of price_paid column: ', df_cert['price_paid'].dtypes)
# df_price = df_price[['lsoa11', 'Median(£)-2011']]
#Merge:
df_cert = pd.merge(df_cert, df_price, on='lsoa11', how='left')
del df_price

#Travel Time to Major infrastructure:
#Load Data con0111
os_con111 = os.path.join(data_dir, '03 3 - Travel Time to Major Infrastructure', 'con0111.xls')
#Read Excel, tab 'CON0111a_Summary', delete rows from 0-6 and 32490 Forward
df_con111 = pd.read_excel(os_con111, sheet_name=0)
df_con111 = df_con111[8:32490]
#Drop Columns:
df_con111.drop(df_con111.columns[[1,2,3,4,5,6,7,8,9,10,11]], axis=1, inplace=True)
df_con111.columns = ['lsoa11', 'connec_air_public', 'connec_air_car']
#Merge
df_cert = pd.merge(df_cert, df_con111, on='lsoa11', how='left')
#Close right dataframe:
del df_con111

#Load Data con0311
os_con311 = os.path.join(data_dir, '03 3 - Travel Time to Major Infrastructure', 'con0311.xls')
#Read Excel, tab 'CON0311a_Summary', delete rows from 0-6 and 32490 Forward
df_con311 = pd.read_excel(os_con311, sheet_name=0)
df_con311 = df_con311[8:32490]
#Drop Columns:
df_con311.drop(df_con311.columns[[1,2,3,4,5,6,7,8,9]], axis=1, inplace=True)
df_con311.columns = ['lsoa11','connec_road_car']
#Save temp
df_con311.to_csv(os.path.join(data_dir, '03 3 - Travel Time to Major Infrastructure', 'df_con311.csv'), index=False,
                 encoding='utf-8')
#Merge
df_cert = pd.merge(df_cert, df_con311, on='lsoa11', how='left')
#Close right dataframe:
del df_con311

#GDP data
main_qna = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\Downloads and data\\ONS GDP'
file_qna = 'qna1.csv'
qna = os.path.join(main_qna, file_qna)
qna_df = pd.read_csv(qna)
#merge
df_cert = pd.merge(df_cert, qna_df, on='quarter', how='left')

#close right dataframe
del qna_df


#Final Shape:
print('Shape of final merged dataframe with econometric data: ', df_cert.shape) #(331654, 33) -> (66482, 35)

#Save
# save(df_MFZ, 'MyFairZone.csv')
save(df_cert, 'final_merge4.csv')
# df_MFZ.to_csv(os.path.join(main, 'MyFairZone.csv'), index=False, encoding='utf-8')