import numpy as np
import pandas as pd
import os

main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\Downloads and data'

sub_econ_dir = 'ONS GDP'
file_econ = 'qna.csv'
qna = os.path.join(main, sub_econ_dir, file_econ)
qna_df = pd.read_csv(qna, header=0)

#select only quarterly rows (Starting from [1946 Q1]
qna_df = qna_df.drop(qna_df.index[0:81])

#Convert [YEAR Q#] to [YEAR Q#], eliminating spaces.
qna_df['Title'] = qna_df['Title'].str.replace(' ', '')

#Select columns of most interest:
qna_df = qna_df[['Title', 'Gross Domestic Product: Quarter on Quarter growth: CVM SA %',
                 'Construction, cont Q on Q yr ago', 'Real Estate Activities (period on period growth) %:CVM']]

#Rename 'Title' Column to 'quarter'
qna_df.rename(columns={'Title': 'quarter'}, inplace=True)

#save econ:
# qna_df.to_csv(os.path.join(main, 'qna1.csv'), index=False, encoding='utf-8')

#Median house prices for LSOAs DATASET 47

sub_prices_dir = '02 2 - Median Housing & Sales'
file_prices = 'HPSSA Dataset 47 - Mean price paid for residential properties by LSOA.xls'
df_med_prices = pd.read_excel(os.path.join(main, sub_prices_dir, file_prices), sheet_name='Data')
df_med_prices = df_med_prices.iloc[4: , :106]
df_med_prices.drop(df_med_prices.iloc[:, 4:61], axis=1, inplace=True)
df_med_prices.replace(':', np.NaN, inplace=True)
print(df_med_prices.describe())


#save median prices dataframe:
df_med_prices.to_csv(os.path.join(main, sub_prices_dir, 'Mean Residential Prices by LSOA - Dataset47.csv'))
