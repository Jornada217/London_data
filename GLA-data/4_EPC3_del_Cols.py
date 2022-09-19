import os
import pandas as pd
from glob import glob

LdnEPC_folder = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\EPC DATA'
LdnEPC_file = 'certificates_combined1.csv'
LdnEPC_file_dest = 'certificates_combined2.csv'

def drop_cols(folder, file, dest_file):
    cert = os.path.join(str(folder), str(file))
    df = pd.read_csv(cert)
    print('Initial shape is:', df.shape) #(3249985, 90) - 2.9GB
    df.drop(columns={'LMK_KEY', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'BUILDING_REFERENCE_NUMBER',
                       'POTENTIAL_ENERGY_RATING', 'CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY',
                       'LOCAL_AUTHORITY', 'CONSTITUENCY', 'COUNTY', 'INSPECTION_DATE', 'TRANSACTION_TYPE',
                       'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL', 'ENERGY_CONSUMPTION_CURRENT',
                       'ENERGY_CONSUMPTION_POTENTIAL',
                       'CO2_EMISSIONS_CURRENT', 'CO2_EMISSIONS_POTENTIAL', 'CO2_EMISS_CURR_PER_FLOOR_AREA',
                       'LIGHTING_COST_CURRENT', 'LIGHTING_COST_POTENTIAL', 'HEATING_COST_CURRENT',
                       'HEATING_COST_POTENTIAL', 'HOT_WATER_COST_CURRENT', 'HOT_WATER_COST_POTENTIAL', 'ENERGY_TARIFF',
                       'MAINS_GAS_FLAG', 'FLOOR_LEVEL', 'FLAT_TOP_STOREY', 'FLAT_STOREY_COUNT', 'MAIN_HEATING_CONTROLS',
                       'GLAZED_TYPE', 'GLAZED_AREA', 'EXTENSION_COUNT', 'LOW_ENERGY_LIGHTING',
                       'NUMBER_OPEN_FIREPLACES', 'HOTWATER_DESCRIPTION', 'HOT_WATER_ENERGY_EFF', 'HOT_WATER_ENV_EFF',
                       'FLOOR_DESCRIPTION', 'FLOOR_ENERGY_EFF', 'FLOOR_ENV_EFF', 'WINDOWS_ENERGY_EFF',
                       'WINDOWS_ENV_EFF',  'CONSTRUCTION_AGE_BAND', 'FLOOR_HEIGHT',#'PROPERTY_TYPE', 'BUILT_FORM',
                       'WALLS_DESCRIPTION', 'WALLS_ENERGY_EFF', 'WALLS_ENV_EFF', 'SECONDHEAT_DESCRIPTION',
                       'SHEATING_ENERGY_EFF', 'SHEATING_ENV_EFF', 'ROOF_DESCRIPTION', 'ROOF_ENERGY_EFF', 'ROOF_ENV_EFF',
                       'MAINHEAT_DESCRIPTION', 'MAINHEAT_ENERGY_EFF', 'MAINHEAT_ENV_EFF', 'MAINHEATCONT_DESCRIPTION',
                       'MAINHEATC_ENERGY_EFF', 'MAINHEATC_ENV_EFF', 'LIGHTING_DESCRIPTION', 'LIGHTING_ENERGY_EFF',
                       'LIGHTING_ENV_EFF', 'MAIN_FUEL', 'WIND_TURBINE_COUNT', 'HEAT_LOSS_CORRIDOR',
                       'UNHEATED_CORRIDOR_LENGTH', 'PHOTO_SUPPLY', 'SOLAR_WATER_HEATING_FLAG',
                       'MECHANICAL_VENTILATION', 'CONSTITUENCY_LABEL', 'POSTTOWN',
                       'LODGEMENT_DATETIME', 'TENURE', 'FIXED_LIGHTING_OUTLETS_COUNT', 'LOW_ENERGY_FIXED_LIGHT_COUNT'},
              inplace=True)
    print('Final shape is:', df.shape) #(3249985, 10) - 315MB -> (3249985, 14) 464MB
    df.to_csv(os.path.join(folder, str(dest_file)), index=False, encoding='utf-8')

#Reindex columns:
def re_index(folder, file, dest_file):
    cert = os.path.join(str(folder), str(file))
    df = pd.read_csv(cert)
    df = df[['ADDRESS', 'POSTCODE', 'LOCAL_AUTHORITY_LABEL', 'LODGEMENT_DATE', 'CURRENT_ENERGY_RATING',
             'TOTAL_FLOOR_AREA', 'NUMBER_HABITABLE_ROOMS', 'NUMBER_HEATED_ROOMS', 'MULTI_GLAZE_PROPORTION',
             'WINDOWS_DESCRIPTION', 'PROPERTY_TYPE', 'BUILT_FORM']]
    df.to_csv(os.path.join(folder, str(dest_file)), index=False, encoding='utf-8')

#This is the test for the file on DESKTOP
drop_cols(LdnEPC_folder, LdnEPC_file, LdnEPC_file_dest)
re_index(LdnEPC_folder, LdnEPC_file, LdnEPC_file_dest)
