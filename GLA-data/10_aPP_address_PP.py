import os
import pandas as pd

PP_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\LAND REGISTRY DATA'
PP_file = os.path.join(str(PP_folder), 'pp-complete1.csv')
df_PP = pd.read_csv(PP_file)

dest = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'

#Count empty values in ead address column:
print('Shape of PRICES PAID dataframe: ', df_PP.shape) #(3406054, 12)
paon_null = df_PP['paon'].isnull().sum()
saon_null = df_PP['saon'].isnull().sum()
st_null = df_PP['street'].isnull().sum()
print('Null instances of paon: ', paon_null) #51
print('Null instances of saon: ', saon_null) #2307672
print('Null instances of street: ', st_null) #2375

#New dataframe to performe concatenation
df_PP2 = df_PP.drop(df_PP.columns.difference(['saon', 'paon', 'street']), 1)
print('Shape of dataframe df_pp2 without columns: ', df_PP2.shape) #(3406054, 3)

#Address form: paon, saon, street
# df_PP['address'] = df_PP[['paon', 'saon', 'street']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_PP2['address'] = df_PP2.stack().groupby(level=0, sort=False).agg(', '.join).values
print('Shape of dataframe df_pp2 after parsing address: ', df_PP2.shape) #(3406054, 4)

#Append address
address = df_PP2['address']
df_PP = df_PP.join(address)
print('Shape of dataframe df_pp after parsing address: ', df_PP.shape) #(3406054, 13)

#organise columns
df_PP = df_PP[['saon', 'paon', 'street', 'address', 'postcode', 'district', 'county', 'price_paid', 'deed_date',
               'property_type', 'new_build', 'duration', 'category']]

#save both dataframes to the final folder
df_PP.to_csv(os.path.join(dest, 'pp-complete2.csv'), index=False, encoding='utf-8')