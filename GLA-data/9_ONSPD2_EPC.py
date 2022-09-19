import os
import pandas as pd

LdnEPC_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\' \
                'EPC DATA'
cert = os.path.join(str(LdnEPC_folder), 'certificates_combined3.csv')
df_EPC = pd.read_csv(cert)

PC_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\GEOCODING\\' \
            'NSPL_Aug_2011\\Data'
PC_file = os.path.join(str(PC_folder), 'NSPL_AUG_2021_GLA.csv')
df_PC = pd.read_csv(PC_file)

dest = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'

#EPC dataframe BEFORE:
print('Shape of EPC dataframe BEFORE merging: ', df_EPC.shape) #(3249985, 10)
print()
print('Shape of POSTCODES dataframe BEFORE merging: ', df_PC.shape) #(325245, 7)??
print()
# PC_heads = df_PC.head()
# print(PC_heads)

#Keep only 'POSTCODE', 'lat', 'long' columns.
# df_PC.drop(df_PC.columns.difference(['POSTCODE', 'lat', 'long']), 1, inplace=True)
#Drop 'rgn'
df_PC.drop(columns={'rgn'}, inplace=True)

#Merge with left join
df_EPC = pd.merge(df_EPC, df_PC, on='POSTCODE', how='left')
print('Merging Accomplished')

#Check if there are empty lat and long in df_EPC:
print('Shape of EPC dataframe after MERGE: ', df_EPC.shape) # (3249985, 10) -> (3249985, 15) -> (3249985, 19)
lat_null = df_EPC['lat'].isnull().sum()
long_null = df_EPC['long'].isnull().sum()
print('Number of empty LATITUDE rows in EPC: ', lat_null) #3447
print('Number of empty LONGITUDE rows in EPC: ', long_null) #3447

#Save to the final folder
df_EPC.to_csv(os.path.join(dest, 'certificates_combined4.csv'), index=False, encoding='utf-8')