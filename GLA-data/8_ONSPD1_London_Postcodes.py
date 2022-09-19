import os
import pandas as pd

PC_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\GEOCODING\\' \
            'NSPL_Aug_2011\\Data'
PC_file = os.path.join(str(PC_folder), 'NSPL_AUG_2021_UK.csv')
df = pd.read_csv(PC_file)

#Checking df BEFORE:
print('Shape of dataframe BEFORE: ', df.shape) #(2665236, 41)

#Delete cols except: 'pcds', 'rgn', 'lat', 'long',:
df.drop(df.columns.difference(['pcds', 'rgn', 'lat', 'long', 'oa11', 'lsoa11', 'msoa11']), 1, inplace=True)
print('Shape of dataframe without columns: ', df.shape) #(2665236, 7)

#Extracting GLA -> rgn:E12000007
df = df[df['rgn'] == 'E12000007']

#Change 'pcds' to 'POSTCODES' in df_PC
df = df.rename(columns={'pcds': 'POSTCODE'})
PC_heads = df.head()
print(PC_heads)

#Check df AFTER:
print('Shape of final dataframe: ', df.shape) #(325247, 7)

#save
df.to_csv(os.path.join(PC_folder, 'NSPL_AUG_2021_GLA.csv'), index=False, encoding='utf-8')