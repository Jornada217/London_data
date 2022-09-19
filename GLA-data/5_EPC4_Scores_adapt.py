import os
import pandas as pd
import numpy as np

LdnEPC_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\EPC DATA'
cert = os.path.join(str(LdnEPC_folder), 'certificates_combined2.csv')
df = pd.read_csv(cert)


#CURRENT_ENERGY_RATING
en_values = df['CURRENT_ENERGY_RATING'].value_counts(ascending=True)
print('Len of CURRENT_ENERGY_RATING: ', len(en_values)) #8
print('Type of CURRENT_ENERGY_RATING: ', type(en_values)) #<class 'pandas.core.series.Series'>
# print(en_values)
del en_values
print()
df['CURRENT_ENERGY_RATING'] = df['CURRENT_ENERGY_RATING'].replace(['A','B','C','D','E','F','G', 'INVALID!'],\
                                [7, 6, 5, 4, 3, 2, 1, 4])

#Convert instances of 'WINDOWS_DESCRIPTION' to  1->100
wd_values = df['WINDOWS_DESCRIPTION'].value_counts(ascending=True)
print('Len WINDOWS_DESCRIPTION: ', len(wd_values)) #62
print('Type WINDOWS_DESCRIPTION: ', type(wd_values)) #<class 'pandas.core.series.Series'>
del wd_values

df['WINDOWS_DESCRIPTION'] = df['WINDOWS_DESCRIPTION'].\
    replace(['Some triple glazing','Single glazedtriple glazing','Some multiple glazing','Mostly  double glazing', #1
             'double glazing','Single and multiple glazing','Secondary glazing','Multiple glazing throughout ', #2
             'Single glazedsecondary glazing','Mostly triple glazing','Partial triple glazing','Fully secondary glazed', #3
             'Full triple glazing','Mostly multiple glazing','Fully secondary glazing','Single glazeddouble glazing', #4
             'Partial multiple glazing','Fully double glazed|Gwydrau dwbl llawn', #5
             'High performance glazing|Ffenestri perfformiad uchel','Multiple glazing throughout', #6
             'Mostly secondary glazing','Some secondary glazing','Fully triple glazed','SAP05:Windows', #7
             'Partial secondary glazing','Full secondary glazing','Some double glazing','Mostly double glazing', #8
             'Partial double glazing','Single glazed','High performance glazing','Fully double glazed', #9
             'Full triple glazed','Fully', 'Fully double glazing', 'Fully triple glazing', 'Mostly  multiple glazing', #10
             'Mostly  secondary glazing', 'Multiple glazing throughout|Gwydrau lluosog ym mhobman', #11
             'Partial double glazed', 'Partial double glazingdouble glazing', 'Single glazedSingle glazing', #12
             'Single glazed|Gwydrau sengl', 'Some  double glazing', 'Some  multiple glazing', #13
             'Unknown complex glazing regime', 'secondary glazing', '(other premises below)', 'Gwydrau dwbl llawn', #14
             'Some', 'Multiple glazing throughout double glazing', 'Some  secondary glazing', 'Mostly', #15
             'Gwydrau dwbl gan mwyaf', 'Multiple glazing throught', 'Rhai gwydrau dwbl', 'Fully Triple glazed', #16
             'Ffenestri perfformiad uchel', 'Fully double glazeddouble glazing', 'Gwydrau sengl', #17
             'Partial double glazing|Gwydrau dwbl rhannol', 'Mostly  triple glazing'], #18
            [25, 0, 25, 75, #1
             100, 50, 100, 100, #2
             0, 75, 50, 100, #3
             100, 75, 100, 0, #4
             75, 100, #5
             100, 100, #6
             75, 50, 100, 100, #7
             50, 100, 50, 75, #8
             50, 0, 100, 100, #9
             100, 100, 100, 100, 75, #10
             75, 100, #11
             75, 75, 0, #12
             0, 50, 50, #13
             50, 100, 50, 100, #14
             50, 100, 50, 75, #15
             75, 100, 50, 100, #16
             100, 100, 0, #17
             50, 80]) #18


#Checking Null instances:
print('sum of null WINDOWS_DESCRIPTION instances BEFORE: ', df['WINDOWS_DESCRIPTION'].isnull().sum()) #1135
# print(wd_values)
print('Sum of null MULTI_GLAZE_PROPORTION instances BEFORE: ', df['MULTI_GLAZE_PROPORTION'].isnull().sum()) #425111
print('Sum of null Habitable Rooms BEFORE: ', df['NUMBER_HABITABLE_ROOMS'].isnull().sum()) #421558
print('Sum of null Heated Rooms BEFORE: ', df['NUMBER_HEATED_ROOMS'].isnull().sum()) #421558


#Replace missing values from WINDOWS_DESCRIPTION with 50 (For now)
df['WINDOWS_DESCRIPTION'].fillna(50, inplace=True)

# Replace missing values in MULTI_GLAZE_PROPORTION and WINDOWS_DESCRIPTION
mg_values = df['MULTI_GLAZE_PROPORTION'].value_counts(ascending=True, bins=5)
# print('Len MULTI_GLAZE_PROPORTION', len(mg_values))
# print('Type MULTI_GLAZE_PROPORTION', type(mg_values))
# print(mg_values)
del mg_values

df['MULTI_GLAZE_PROPORTION'].fillna(df['WINDOWS_DESCRIPTION'], inplace=True)

#Replace missing values from Habitable Rooms with (mode of floor area / mode of habitable rooms)

# print('Mean of Floor Area: ', df['TOTAL_FLOOR_AREA'].mean())
# print('Median of Floor Area: ', df['TOTAL_FLOOR_AREA'].median())
print('Mode of Floor Area: ', df['TOTAL_FLOOR_AREA'].mode()) #50
print('Median of Habitable Rooms: ', df['NUMBER_HABITABLE_ROOMS'].median()) #3.0
count = (df['TOTAL_FLOOR_AREA'].mode()/df['NUMBER_HABITABLE_ROOMS'].mode())
print(type(count))
print('Division of medians - Area / Habitable Rooms: ', count) #16.666667
del count

# df['NUMBER_HABITABLE_ROOMS'].fillna((df['TOTAL_FLOOR_AREA'].mode()/df['NUMBER_HABITABLE_ROOMS'].mode()),
#                                     inplace=True)
# df['NUMBER_HEATED_ROOMS'].fillna((df['TOTAL_FLOOR_AREA'].mode()/df['NUMBER_HABITABLE_ROOMS'].mode()),
#                                  inplace=True)

df['NUMBER_HABITABLE_ROOMS'].fillna(16.67, inplace=True)
df['NUMBER_HEATED_ROOMS'].fillna(16.67, inplace=True)

#Replacing PROPERTY_TYPE and BUILT_FORM
df['PROPERTY_TYPE'] = df['PROPERTY_TYPE'].replace(['House', 'Flat', 'Maisonette', 'Bungalow', 'Park Home', 'Park home'],
                                                  [5, 4, 3, 2, 1, 1])
df['BUILT_FORM'] = df['BUILT_FORM'].replace(['Detached', 'Semi-Detached', 'Enclosed End-Terrace',
                                             'Enclosed Mid-Terrace','End-Terrace', 'Mid-Terrace', 'NO DATA!'],
                                            [5, 4, 2, 1, 3, 1, 0])
df['BUILT_FORM'].fillna(2, inplace=True)

#Checking Null instances AFTER:
print()

print('Unique Values of CURRENT_ENERGY_RATING: ', df['CURRENT_ENERGY_RATING'].unique())
print('Sum of null CURRENT_ENERGY_RATING instances AFTER: ', df['CURRENT_ENERGY_RATING'].isnull().sum()) #0
print('Unique Values of WINDOWS_DESCRIPTION: ', df['WINDOWS_DESCRIPTION'].unique())
print('Sum of null WINDOWS_DESCRIPTION instances AFTER: ', df['WINDOWS_DESCRIPTION'].isnull().sum()) #0
print('Unique Values of MULTI_GLAZE_PROPORTION: ', df['MULTI_GLAZE_PROPORTION'].unique())
print('Sum of null MULTI_GLAZE_PROPORTION instances AFTER: ', df['MULTI_GLAZE_PROPORTION'].isnull().sum()) #0
print('Unique Values of NUMBER_HABITABLE_ROOMS: ', df['NUMBER_HABITABLE_ROOMS'].unique())
print('Sum of null NUMBER_HABITABLE_ROOMS AFTER: ', df['NUMBER_HABITABLE_ROOMS'].isnull().sum()) #0
print('Unique Values of NUMBER_HEATED_ROOMS: ', df['NUMBER_HEATED_ROOMS'].unique())
print('Sum of null NUMBER_HEATED_ROOMS AFTER: ', df['NUMBER_HEATED_ROOMS'].isnull().sum()) #0
print('Unique Values of PROPERTY_TYPE: ', df['PROPERTY_TYPE'].unique())
print('Sum of null PROPERTY_TYPE AFTER: ', df['PROPERTY_TYPE'].isnull().sum()) #0
print('Unique Values of BUILT_FORM: ', df['BUILT_FORM'].unique())
print('Sum of null BUILT_FORM AFTER: ', df['BUILT_FORM'].isnull().sum()) #0

#Save to 'certificates.csv' file
df.to_csv(os.path.join(LdnEPC_folder, 'certificates_combined3.csv'), index=False, encoding='utf-8')


