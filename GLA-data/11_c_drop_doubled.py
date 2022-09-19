import os
import pandas as pd

# main = 'C:\\Users\\joaopaulo\\Desktop'
main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'
merged = os.path.join(str(main), 'final_merge2.csv')
# merged = os.path.join(str(main), 'Final Merge RecordLinkage TESTE.csv')
df_merged = pd.read_csv(merged)

#Check initial instances
print('Shape of original df_merged: ', df_merged.shape) #(999, 35) -> (509722, 35) -> (1147948, 41)

#All dates must be converted before you work with them
df_merged['deed_date'] = pd.to_datetime(df_merged['deed_date'])
df_merged['LODGEMENT_DATE'] = pd.to_datetime(df_merged['LODGEMENT_DATE'])
print('Type of initial df[deed_date]: ', df_merged['deed_date'].dtypes) #datetime64[ns]
print('Type of initial df[LODGEMENT_DATE]: ', df_merged['LODGEMENT_DATE'].dtypes) #datetime64[ns]

#Eliminate if LODGEMENT_DATE > deed_date
df_merged = df_merged[df_merged['LODGEMENT_DATE'] <= df_merged['deed_date']].reset_index()
print('Shape of df_merged after removing LODGEMENT_DATE > deed_date: ', df_merged.shape) #(361914, 36) -> (977246, 42)

#Maximum threshold was determined by previous step.
#Select the largest LODGEMENT_DATE by each deed_date from each groupby

#Select single instances in a dataset (largest LODGEMENT_DATE cannot be dropped from single instances)
df_single = df_merged.groupby(['address2', 'deed_date']).filter(lambda x: len(x['deed_date']) == 1)
print('Shape of df_single with groupby == 1: ', df_single.shape) #(637, 36) -> (303718, 36) -> (735555, 42)

#Select double instances in a dataset. -> Keep only the largest date on doubled groups.
df_double = df_merged.groupby(['address2', 'deed_date']).filter(lambda x: len(x['deed_date']) > 1)
print('Shape of df_merged after grouping only > 1: ', df_double.shape) #(147, 36) -> (58196, 36) -> (241691, 42)

#THIS IS TAKING WAY TOO LONG!
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-view-versus-copy
#selecting the MAX dete
# df_double = df_double.loc[df_double.groupby(['address2_y', 'deed_date'])['LODGEMENT_DATE'].idxmax()]
df_double = df_double.groupby(['address2', 'deed_date']).\
    apply(lambda group: group.nlargest(1, columns='LODGEMENT_DATE'))
print('Shape of df_double after grouping only > 1 and keeping max LODGEMENT_DATE: ', df_double.shape) #(27936, 36) -> (113368, 42)

#APPEND doubled groups and single groups to one dataset
df_merged = df_double.append(df_single)
# df_merged = df_merged[~(df_merged['LODGEMENT_DATE'] == df_double)]
print('Shape of df_merged FINAL: ', df_merged.shape) #(707, 36) -> (331654, 36) -> (848923, 42)
#(784, 34) by keeping MAX in df_double
#(784, 34) by keeping MIN in df_double

df_merged.drop(columns={'address2', 'Score', 'saon', 'paon', 'street', 'address', 'postcode_y',
                        'ADDRESS2', 'LOCAL_AUTHORITY_LABEL'}, inplace = True)

df_merged = df_merged[['index', 'level_0', 'level_1', 'county', 'district', 'oa11', 'lsoa11', 'msoa11',
                       'POSTCODE', 'address2_y', 'ADDRESS',
                       'lat', 'long', 'property_type', 'new_build', 'duration', 'category',
                       'CURRENT_ENERGY_RATING', 'TOTAL_FLOOR_AREA', 'NUMBER_HABITABLE_ROOMS', 'NUMBER_HEATED_ROOMS',
                       'MULTI_GLAZE_PROPORTION', 'WINDOWS_DESCRIPTION', 'PROPERTY_TYPE', 'BUILT_FORM',
                       #'FLOOR_HEIGHT', 'CONSTRUCTION_AGE_BAND',
                       'LODGEMENT_DATE', 'deed_date', 'year', 'quarter', 'price_paid']]

#Save
df_merged.to_csv(os.path.join(main, 'final_merge3.csv'), index=False, encoding='utf-8')