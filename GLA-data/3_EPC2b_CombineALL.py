import os
import pandas as pd
from glob import glob
import shutil

EPC_dir = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\EPC DATA'
LdnEPC_folder = os.path.join(EPC_dir, 'London_certificates')

sub_folders = glob(str(LdnEPC_folder) + '\\*\\')

def EPC_files(folder):
    cert = os.path.join(str(folder), 'certificates.csv')
    return cert

#Calculate rows of combined file:
all_EPCfiles = [EPC_files(i) for i in sub_folders]
print(all_EPCfiles)
combined_EPC = pd.concat([pd.read_csv(f) for f in all_EPCfiles])
print('Sum of total rows in combined file: ', len(combined_EPC.index)) #3249985
print('Shape of the combined file: ', combined_EPC.shape) #(3249985, 90)

# Save to 'certificates.csv' file
combined_EPC.to_csv(os.path.join(EPC_dir, 'certificates_combined1.csv'), index=False, encoding='utf-8')

#Delete Folder and subfolders -> Manually for now
# shutil.rmtree(LdnEPC_folder)