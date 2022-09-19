import os
import pandas as pd
#16 September 2021 (Prices paid data may change)

PP_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\LAND REGISTRY DATA'
cert = os.path.join(str(PP_folder), 'pp-complete.csv')
df = pd.read_csv(cert)

#Checking df BEFORE
print('Shape of dataframe BEFORE: ', df.shape) #(26321784, 16)
#4.495GB


#Adding Heads to the file
df.columns = ['unique_id', 'price_paid', 'deed_date', 'postcode', 'property_type', 'new_build', 'duration', 'paon',
              'saon', 'street', 'locality', 'town', 'district', 'county', 'category', 'status']
print('Heads added...')

#Delete cols: unique_id, locality, town
df.drop(columns={'unique_id', 'locality', 'town', 'status'}, inplace=True)
print('Cols deleted...')

#Extracting GLA -> 'county' / 14 column
df = df[df['county'] == 'GREATER LONDON']
print('Number of rows of GLA: ', len(df)) #3406054
print('Earliest deed date: ', df['deed_date'].min()) #1995-01-01 00:00


#Reorganise columns:
df = df[['saon', 'paon', 'street', 'postcode', 'district', 'county', 'price_paid', 'deed_date', 'property_type',
         'new_build', 'duration', 'category']]
print('Columns reorganised...')

#Adpting Scores:
print('Unique values in property_type: ', df['property_type'].unique())
df['property_type'] = df['property_type'].replace(['D', 'S', 'T', 'F', 'O'], [5, 4, 1, 3, 2])
df['new_build'] = df['new_build'].replace(['Y', 'N'], [1, 0])
df['duration'] = df['duration'].replace(['F', 'L'], [1, 0])
df['category'] = df['category'].replace(['A', 'B'], [1, 0])
print('Scores changed...')

#Checking df AFTER
print('Shape of new dataframe: ', df.shape) #(3406054, 12) after deleting non GLAs
print('Sum of null Instances of dataframe: ', df.isnull().sum())
#Count As and Bs from dataset:
print('Number of As and Bs in the category column: ', df['category'].value_counts())
# A    3260527
# B     145527 -> 0.0427 (4.27%)
#Drop Bs from the dataset:
df = df[df.category != 0]
print('shape of dataframe for category A: ', df.shape)

#Is there any non GLA District?
districts = df['district'].value_counts(ascending=True)
print('The type of districts: ', type(districts)) #<class 'pandas.core.series.Series'>
print('The len of districts: ', len(districts)) #33
print(districts) #33 boroughs
print('Shape of FINAL dataframe: ', df.shape) #(3406054, 12)
#302.8MB

#Saving
df.to_csv(os.path.join(PP_folder, 'pp-complete1.csv'), index=False, encoding='utf-8')


