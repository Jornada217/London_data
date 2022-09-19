import os
import pandas as pd
from glob import glob
import shutil

boroughs = ['City-of-London','Barking-and-Dagenham','Barnet','Bexley','Brent','Bromley',
            'Camden','Croydon','Ealing','Enfield','Greenwich','Hackney','Hammersmith-and-Fulham',
            'Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington',
            'Kensington-and-Chelsea','Kingston-upon-Thames','Lambeth','Lewisham',
            'Merton','Newham','Redbridge','Richmond-upon-Thames','Southwark','Sutton',
            'Tower-Hamlets','Waltham-Forest','Wandsworth','Westminster']

dir_EPC = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\EPC DATA\\London_certificates'

EPC_sub = os.listdir(dir_EPC)
print(len(EPC_sub))
print(EPC_sub)
print()

#You have to unquote each step, from 1 , (2a and 2b), to 3, and run in sequence.

#1 - Check all files in each folder. -
# OK, two files on each folder and none on root folder.
# for (dirpath, dirnames, files) in os.walk(dir_EPC):
#     print(len(files))

#2a - Function to delete each 'recommendations.csv'
def del_rec(folder):
    rec = os.path.join(str(folder), 'recommendations.csv')
    os.remove(rec)

# #2b - Loop to check dirs and parse function to delete recommendations.csv
for f in glob(str(dir_EPC) + '\\*\\'):
    del_rec(f)

#3 - Check the files on each folder again.
for (dirpath, dirnames, files) in os.walk(dir_EPC):
    print(dirpath)
    print(dirnames)
    print(len(files))
    print(files)
    # cert = os.path.join(dirpath, files)
    # print(cert)
    #df = %%%
    # print('Number of rows in dataframe: ', len(df.index))