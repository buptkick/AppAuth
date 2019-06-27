# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 17:50:58 2018

@author: softsec-zcp
"""


import os, sys, time
import lightgbm as lgb
import pandas as pd
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
#from sklearn.cross_validation import train_test_split
import gc
from sklearn.preprocessing import OneHotEncoder
#from sklearn.cross_validation import StratifiedKFold
import datetime

all_feature = True


def cross_validation(data, auth_num):

    data = data.reset_index(drop=True)

    fileclass = auth_num
    column_names = data.columns.values.tolist()
    print (column_names[0:5])
    column_names = column_names[1:-2]
    print (len(column_names))
    train_labels = data[36]
    train_apk = data[0]

    if all_feature:
        train = data.iloc[:,1:-2]
    else:
        train = data.iloc[:,21:-2]
        
    train_labels = train_labels.apply(lambda x:int(x))
    train_labels = np.array(train_labels, dtype=int)
    train = np.array(train, dtype=float)
    meta_train = np.zeros(shape=(len(train), fileclass))
    from sklearn.metrics import f1_score
    def lgb_f1_score(y_hat, data):
        y_true = data.get_label()
        y_hat = np.round(y_hat) # scikits f1 doesn't like probabilities
        return 'f1', f1_score(y_true, y_hat), True

    X_train = train
    X_train_label = train_labels
    dtrain = lgb.Dataset(X_train, X_train_label) 
    #dval   = lgb.Dataset(X_val, X_val_label, reference = dtrain)   
    params = {
            'task':'train', 
            'boosting_type':'gbdt',
            'num_leaves': 15,
            'objective': 'multiclass',
            'num_class':fileclass,
            'learning_rate': 0.05,
            'feature_fraction': 0.5,
            'subsample':0.5,
            'num_threads': 32,
            'metric':'multi_error',
            'seed':100,
            'min_data':1,
            'min_data_in_bin':1,
        }
    num_round = 10000
    lgb.cv(params, dtrain, num_round, nfold=5, early_stopping_rounds=50)


def main():

    if len(sys.argv) > 2:
        print("AppAuth must takes less than 1 argument.")
        print("Usage:")
        print("    $ python crossval.py [op]csv_path")
        print("    ")
        print("    [op]csv_path: input the feature vectors in .csv files named with author's name.")
        exit(1)

    if len(sys.argv) == 2:
        Filepath = sys.argv[1]
    else:
        Filepath = os.path.dirname(os.path.realpath(__file__)) + '/Features'
    
    if not os.path.isdir(Filepath):
        print("Can NOT find directory: '%s'" % Filepath)
        exit(1)
        
    Fileclass = 0
    filecount = 0
    Remove_less = False
    csvpath = Filepath + '/../all.csv'
    if(os.path.exists(csvpath)):
        os.remove(csvpath)
        print ("remove ok!")
    else:
        print ("not exists!")
    for i,filename in enumerate(os.listdir(Filepath)):
        if not filename.endswith('.csv'):
            continue
        
        Author_name = filename[0:-4]

        try:
            data = pd.read_csv(Filepath + '/' + filename, header=None)
        except:
            print ('error', Author_name)
            continue
        if len(data)<=2 and Remove_less ==True:
            continue
        

        data['label'] = Fileclass
        data['author'] = Author_name
        
        Fileclass += 1
        filecount = filecount + len(data)
        
        data.to_csv(csvpath, encoding="utf_8_sig", index=False, header=False, mode='a+')

    data_all = pd.read_csv(csvpath, header=None)
    data_all = data_all.dropna(axis=0)

    data_all[0] = data_all[0].apply(lambda x:str(x).upper())

    cross_validation(data_all, Fileclass)
    

if __name__ == '__main__':
    
    begin = time.time()
    
    main()
    
    end = time.time()
    print "Done in %d hours %d minutes %d seconds" % \
    ((end - begin) / 3600, (end - begin) / 60 % 60, (end - begin) % 60)

