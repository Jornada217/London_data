import pandas as pd
import os
import recordlinkage

EPC_main = 'EPC'
PP_main = 'PP'
PP_col = 'district'
EPC_col = 'LOCAL_AUTHORITY_LABEL'

main = 'C:\\Users\\joaopaulo\\Desktop\\Gla_data\\PP EPC FULL'
EPC_file = os.path.join(main, 'certificates_combined4.csv')
df_EPC = pd.read_csv(EPC_file)
# print(type(df_EPC))
df_EPC['ADDRESS2'] = df_EPC['ADDRESS']
df_EPC['ADDRESS2'] = df_EPC['ADDRESS2'].str.lower()
df_EPC['ADDRESS2'] = df_EPC['ADDRESS2'].str.replace(',', '')

PP_file = os.path.join(main, 'pp-complete2.csv')
df_PP = pd.read_csv(PP_file)
df_PP[PP_col] = df_PP[PP_col].replace('CITY OF WESTMINSTER', 'WESTMINSTER')
df_PP['address2'] = df_PP['address']
df_PP['address2'] = df_PP['address2'].str.lower()
df_PP['address2'] = df_PP['address2'].str.replace(',', '')

boroughs_GLA = ['City of London','Barking and Dagenham','Barnet','Bexley','Brent','Bromley',
            'Camden','Croydon','Ealing','Enfield','Greenwich','Hackney','Hammersmith and Fulham',
            'Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington',
            'Kensington and Chelsea','Kingston upon Thames','Lambeth','Lewisham',
            'Merton','Newham','Redbridge','Richmond upon Thames','Southwark','Sutton',
            'Tower Hamlets','Waltham Forest','Wandsworth','Westminster']

# boroughs_GLA = ['City of London','Barking and Dagenham']
# boroughs_GLA = ['City of London']

#Checking df BEFORE
print('Shape of EPC dataframe BEFORE: ', df_EPC.shape) #(3249985, 15) 16?
print('Shape of PP dataframe BEFORE: ', df_PP.shape) #(3406054, 13) 14?


def parse(col, dir, sub_dir, df, boroughs):
    df2 = df[df[col].str.lower() == str(boroughs).lower()]
    df2.to_csv(os.path.join(dir, sub_dir, '{}.csv'.format(boroughs)))
    return df2

shapes_list = []
shapes_cols = ['Borough', 'EPC Shape Before', 'PP Shape Before', 'PP Len Before', 'Candidates', 'Final Shape',
               'Final Len', 'Loss']
df_statistics = pd.DataFrame(columns=shapes_cols)

df_merged_final = pd.DataFrame()

for i in boroughs_GLA:
    df2EPC = parse(EPC_col, main, EPC_main, df_EPC, i)
    # print(type(df2EPC))
    df2PP = parse(PP_col, main, PP_main, df_PP, i)
    EPC_before = df2EPC.shape
    PP_before = df2PP.shape
    print('Shape of EPC for {}: '.format(i), EPC_before)
    print('Shape of PP for {}: '.format(i), PP_before)
    # recordlinkage candidates
    indexer = recordlinkage.Index()
    indexer.block(left_on='postcode', right_on='POSTCODE')
    candidates = indexer.index(df2PP, df2EPC)
    candidates_len = len(candidates)
    # print('Len of blocked candidates in {}: '.format(i), candidates_len)
    # Compare
    compare = recordlinkage.Compare()
    compare.exact('postcode', 'POSTCODE', label='postcode')
    compare.string('address2', 'ADDRESS2', method='jarowinkler', threshold=0.996, label='address2')
    features = compare.compute(candidates, df2PP, df2EPC)
    # Quality of the matches:
    quality = features.sum(axis=1).value_counts().sort_index(ascending=False)
    print('Quality in {}'.format(i))
    print(quality)
    # Potential matches:
    potential_matches = features[features.sum(axis=1) >= 2].reset_index()
    potential_matches['Score'] = potential_matches.loc[:, 'postcode':'address2'].sum(axis=1)
    # print(potential_matches)
    # MERGE
    account_merge = potential_matches.merge(df2PP, left_on=['level_0'], how='left', right_index=True)
    final_merge = account_merge.merge(df2EPC, left_on=['level_1'], how='left', right_index=True)
    # Drop if ADDRESS2 != address2
    # It is renaming 'address2' to 'address2_y', do not know why.
    final_merge = final_merge[final_merge['address2_y'] == final_merge['ADDRESS2']]
    final_shape = final_merge.shape
    df_statistics = df_statistics.append({'Borough': str(i), 'EPC Shape Before': EPC_before,
                                          'PP Shape Before': PP_before, 'PP Len Before':PP_before[0],
                                          'Candidates': candidates_len, 'Final Shape': final_shape,
                                          'Final Len': final_shape[0], 'Loss': (1-(final_shape[0]/PP_before[0]))},
                                         ignore_index=True)
    df_merged_final = df_merged_final.append(final_merge, ignore_index=True)
    print(type(df_merged_final))
    print(len(df_merged_final))
    del account_merge, df2PP, df2EPC
    print('Shape after keeping address2 == ADDRESS2 in {}: '. format(i), final_shape)
    # save
    # final_merge.to_csv(os.path.join(main, 'Merged', 'Merged {}.csv'.format(i)), index=False, encoding='utf-8')


df_statistics.to_csv(os.path.join(main, 'Statistics.csv'), index=False, encoding='utf-8')
print('Shape of final merged daframe: ', df_merged_final.shape)
df_merged_final.to_csv(os.path.join(main, 'final_merge.csv'), index=False, encoding='utf-8')