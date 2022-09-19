import os
import pandas as pd

# main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC TEST'
main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'

cert = os.path.join(str(main), 'London_certificates.csv')
df_cert = pd.read_csv(cert)
PP_file = os.path.join(str(main), 'pp-complete_new.csv')
df_PP = pd.read_csv(PP_file)
# merged = os.path.join(str(main), 'final_merge.csv')
# df_merged = pd.read_csv(merged)

#Check initial frame
print('Shape of certificates before timeframe: ', df_cert.shape) #(3249985, 15)
print('Shape of PPs before timeframe: ', df_PP.shape) #(3406054, 13)

#date range:
init_date = '2009-01-01'
# end_date = '2013-01-01'
end_date = '2013-12-31'

df_cert2 = df_cert[(df_cert['LODGEMENT_DATE'] > init_date)
                & (df_cert['LODGEMENT_DATE'] < end_date)]

df_PP2 = df_PP[(df_PP['deed_date'] > init_date)
                & (df_PP['deed_date'] < end_date)]

#Check shapes
print('Shape of certificates after timeframe: ', df_cert2.shape) #(1375193, 15)
print('Shape of PPs after timeframe: ', df_PP2.shape) #pps(468732, 13) -> df merged(331654, 36)