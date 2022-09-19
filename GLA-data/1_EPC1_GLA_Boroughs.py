import os
import zipfile
from glob import glob
import shutil

#33 boroughs
#Brentwood is not London borough
boroughs = ['City-of-London','Barking-and-Dagenham','Barnet','Bexley','Brent','Bromley',
            'Camden','Croydon','Ealing','Enfield','Greenwich','Hackney','Hammersmith-and-Fulham',
            'Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington',
            'Kensington-and-Chelsea','Kingston-upon-Thames','Lambeth','Lewisham',
            'Merton','Newham','Redbridge','Richmond-upon-Thames','Southwark','Sutton',
            'Tower-Hamlets','Waltham-Forest','Wandsworth','Westminster']

#new attempt
EPC_dir = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\EPC DATA'
main = os.path.join(EPC_dir, 'all-domestic-certificates')
dest = os.path.join(EPC_dir, 'London_certificates')
# EPC_extr_dirs = glob(str(main + '\\*\\'))
EPC_extr_dirs = glob('C:\\Users\\joaopaulo\\Desktop\\'
                'Gla_data\\EPC DATA\\all-domestic-certificates\\*\\')

#Creating folders
# try:
#     os.mkdir(main)
# except OSError:
#     print('Creation of directory all-domestic-certificates failed')
# else:
#     print('Successfuly created the directory all-domestic-certificates')
#
# try:
#     os.mkdir(dest)
# except OSError:
#     print('Creation of directory London_certificates failed')
# else:
#     print('Successfuly created the directory London_certificates')

#Extracting Zip file (Last atempt)
# zip = os.path.join(str(EPC_dir), 'all-domestic-certificates.zip')
# with zipfile.ZipFile(zip, 'r') as zip_ref:
#     zip_ref.extractall(main)

#Extracting Zip file (New atempt) #Also unpacking in a temp folder.
# zip = os.path.join(str(EPC_dir), 'all-domestic-certificates.zip')
# shutil.unpack_archive(zip, extract_dir=main)

#Control the len of all boroughs. Should be 34 (removing Brentwood later = 33)
print(len(boroughs))
print(len(EPC_extr_dirs))
print('listing all_EPCs Before')
epc2 = os.listdir(main)
print(len(epc2))

def get_EPCbrgs(EPC_list):
    full_list = EPC_extr_dirs
    final_list = [x for y in EPC_list for x in full_list if y in x]
    return final_list


#Moving directories to another folder (You will have to amnually remove Brentwood)
dir_move = get_EPCbrgs(boroughs)
for sub_dir in dir_move:
    shutil.move(sub_dir, dest)

print('Length of dir AFTER')
print(len(get_EPCbrgs(boroughs)))
epc_dest = os.listdir(dest)
print(len(epc_dest))


#Delete remaining directories
# shutil.rmtree(main)

#Delete Brentwood
# brentwood_dir = os.path.join(dest, 'domestic-E07000068-Brentwood')
# shutil.rmtree(brentwood_dir)