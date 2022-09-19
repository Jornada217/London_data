import os
import pandas as pd

LdnEPC_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\EPC DATA'
cert = os.path.join(str(LdnEPC_folder), 'certificates_combined3.csv')
df = pd.read_csv(cert)

#Create Area/habitable and Area/heated
df['Area/Habitable'] = df['TOTAL_FLOOR_AREA'] / df['NUMBER_HABITABLE_ROOMS']
df['Area/Heated'] = df['TOTAL_FLOOR_AREA'] / df['NUMBER_HEATED_ROOMS']

#Statistics:
print('Shape of dataframe: ', df.shape) #(3249985, 12)
area_null = df['TOTAL_FLOOR_AREA'].isnull().sum()
print('NULL instances of TOTAL_FLOOR_AREA: ', area_null) #0
total_area = df['TOTAL_FLOOR_AREA'].count()
area_ZERO = df['TOTAL_FLOOR_AREA'][df['TOTAL_FLOOR_AREA'] == 0].count()
print('Total Floor Area Instances: ', total_area) #3249985
print('Instances with ZERO Floor Area: ', area_ZERO) #11670
print('Instances with ZERO Floor Area: ', (area_ZERO/total_area)*100, '%') #0.3590785803626786 %

total_number_hab = df['NUMBER_HABITABLE_ROOMS'].sum()
hab_null = df['NUMBER_HABITABLE_ROOMS'].isnull().sum()
print('NULL instances of HABITABLE ROOMS: ', hab_null) #421558
print('NULL instances of HABITABLE ROOMS: ', (hab_null/total_number_hab)*100, '%') #4.109827961800919 %

min_room = 5.8
total_hab = df['Area/Habitable'].count()
hab = df['Area/Habitable'][df['Area/Habitable'] < min_room].count()
# print(hab/total_hab)
print('Habitable rooms smaller that minimum: ', (hab/total_hab)*100, '%') #0.041401103864444795 % -> 11.00~% ????
total_heat = df['Area/Heated'].count()
heat = df['Area/Heated'][df['Area/Heated'] < min_room].count()
# print(heat/total_heat)
print('Heated rooms smaller that minimum: ', (heat/total_heat)*100, '%') #0.03542605129989213 % -> -> 11.00~% ????

# df.to_csv(os.path.join(LdnEPC_folder, 'certificates_combined.csv'), index=False, encoding='utf-8')

