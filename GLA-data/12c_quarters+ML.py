import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

# init_quarter = '2010Q1'
# end_quarter = '2021Q4'
init_quarter = '2010-01-01'
end_quarter = '2021-09-30'

# Q_range = pd.date_range(pd.to_datetime(init_quarter), pd.to_datetime(end_quarter), freq='Q').to_period('Q')
# range = pd.date_range(pd.to_datetime(init_quarter), pd.to_datetime(end_quarter), freq='Q').tolist()
Q_range = pd.date_range(pd.to_datetime(init_quarter), pd.to_datetime(end_quarter), freq='Q')
print('Type of Q_range: ', type(Q_range))
print('dtype of Q_range: ', Q_range.dtype)
print('Shape of Q_range: ', Q_range.shape)
print(Q_range)
print()

# Q_array = np.array(item[1] for item in Q_range)
# Q_array = Q_range.to_numpy()
# # Q_array = [item(0) for item in Q_array]
# print('Type of Q_array: ', type(Q_array))
# # print('dtype of Q_array: ', Q_array.dtype)
# # print('Shape of Q_array: ', Q_array.shape)
# print(Q_array)
# print()

print('range_list: ')
range_list = []
# for i in range(len(Q_range)):
for i in Q_range:
    I = i.to_period('d')
    print(I, type(I), str(I))
    #print(i, type(i), str(i))
    range_list.append(str(I))
print(len(range_list))
print(type(range_list))
print(range_list)
print()

range_array = np.array(range_list)
# print('range_array START: ')
# print(len(range_array))
# print(type(range_array))
# print(range_array)
# print('range_array END: ')
# print()

# quarters_range = np.arange(init_quarter, end_quarter, 3, dtype = 'period[Q-DEC]')
# range = np.arange(init_quarter, end_quarter, 3, dtype= 'datetime64[M]')
# print('Type of range: ', type(range))
# print('dtype of range: ', range.dtype)
# print('Shape of range: ', range.shape)
# print(range)
# print()


print('def array(range_q, lag):')
def array(range_q, lag):
    quarters = list()
    #Function will repeat from 2010Q1 to last quarter in list of quarters.
    #for lag+1
    # print('range_q[lag+1: ]: ')
    # print(range_q[lag+1: ])
    # print('len of range_q[lag+1: ]: ', len(range_q[lag+1: ]))
    # print('range_q[lag+1: ] END ')
    #
    # #Same for lag:
    # print('range_q[lag: ]: ')
    # print(range_q[lag:])
    # print('len of range_q[lag: ]: ', len(range_q[lag:]))
    # print('range_q[lag: ] END ')
    for i in range_q[lag: ]: #Last element here is included, use range_q[lag: ]
    #for i in range_q[-40:]:
        #Convert datetime64[M] to an indexable format
        print('i: ', i)
        #qs = range_q[int(np.where(range_q == i)[0]) - lag - 1 : int(np.where(range_q == i)[0])]
        qs = range_q[int(np.where(range_q == i)[0]) - lag: int(np.where(range_q == i)[0]) +1]
        # qs = range_q[int(np.where(range_q == i)[0]) - lag - 1: int(np.where(range_q == i)[0] + 1)]
        # qs = range_q[int(np.where(range_q == i)[0]) - lag - 1: ]
        quarters.append(qs)
    print('len of quarters: ', len(quarters))
    print(quarters)
    return quarters

lag = 8
# print(range_array[lag+1: ].shape)
# print(range_array[lag+1: ].dtype)
# print(type(range_array[lag+1: ]))
# print(range_array[lag+1: ])
print()
print('Passing Array function: ')
array(range_array, lag)     #UNMUTE!
print()

#Test converting to time object:
time_array = array(range_array, lag)    #UNMUTE!
# time_array_object = pd.to_datetime(time_array)
# print('Convert datetime object START')
# print(time_array_object)
# print('Convert datetime object END')
# print()

# for i in time_array:
#     print(i[0], type(i[0]), type(pd.to_datetime(i[0])))


# for i in range_array[lag+1: ]:
#     print(type(np.where(range_array == i)), int(np.where(range_array == i)[0]),i, type(i))
#     qs = range_array[int(np.where(range_array == i)[0]) : int(np.where(range_array == i)[0]) + 5]
#     print(qs)

#This is why it is crashing: i is a string. I need to get the index fro each i to pass along.

#SECOND STEP: DEFINE ML FUNCTION
def ML(X_train, X_test, y_train, y_test):
    rf = RandomForestRegressor(n_estimators=100, max_depth=None, bootstrap=True, max_features='sqrt', n_jobs=5,
                               criterion='mse')
    rf.fit(X_train, y_train)
    prediction_test = rf.predict(X = X_test)
    print('Training accuracy score is: ', rf.score(X_train, y_train))
    print('Testing accuracy score is: ', rf.score(X_test, y_test))


#THIRD STEP: Parse the arrays to build index for X_train, X_test, y_train, y_test.
def X_y(time_array, dataframe):
    df_X = dataframe.drop('price_paid', axis=1)
    df_y = dataframe[['quarter', 'price_paid']]
    for i in time_array:
        df_X_train = df_X[(i[0] <= df_X['quarter'] <= i[-2])]
        df_X_train = df_X_train.sample(frac=0.1, replace=False, random_state=1) #Sampling: DELETE THIS LATER!
        df_X_train = df_X_train.drop('quarter', axis=1)
        X_train_values = df_X_train.values
        X_train = np.array(X_train_values)

        df_X_test = df_X[(df_X['quarter'] == i[-1])]
        df_X_test = df_X_test.sample(frac=0.2, replace=False, random_state=1)  #Sampling: DELETE THIS LATER!
        df_X_test = df_X_test.drop('quarter', axis=1)
        X_test_values = df_X_test.values
        X_test = np.array(X_test_values)

        df_y_train = df_y[(i[0] <= df_y['quarter'] <= i[-2])]
        df_y_train = df_y_train.sample(frac=0.1, replace=False, random_state=1)  #Sampling: DELETE THIS LATER!
        y_train_values = df_y_train['price_paid'].values
        y_train = np.array(y_train_values)

        df_y_test = df_y[df_y['quarter'] == i[-1]]
        df_y_test = df_y_test.sample(frac=0.2, replace=False, random_state=1)  #Sampling: DELETE THIS LATER!
        y_test_values = df_y_test['prices_paid'].values
        y_test = np.array(y_test_values)

        del df_X_train, X_train_values, df_X_test, X_test_values, df_y_train, y_train_values, df_y_test, y_test_values
        #print('Element time array: ', i)
        print('Range train dataset: {0} to {1}'.format(i[0], i[-2]))
        print('Test dataset: ', i[-1])
        ML(X_train, X_test, y_train, y_test)
    #return X_train, X_test, y_train, y_test
    print()
    print('Len of time_array: ', len(time_array))


# X_y(array(range_array, lag))