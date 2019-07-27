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
#from sklearn.cross_validation import train_test_split
import gc
#from sklearn.preprocessing import OneHotEncoder
#from sklearn.cross_validation import StratifiedKFold
import datetime
from sklearn.model_selection import StratifiedKFold


def pair_predict(data, FeaturesPair_data, hash_label_list, label_hash_list):

    try:
        datanew = data
        
        l = datanew[36]
        l = list(set(l))
        
        datanew[36] = datanew[36].apply( lambda x:0 if  x==l[0] else 1)
        p = datanew[36]
        p = list(set(p))
        column_names = data.columns.values.tolist()
        column_names = column_names[1:-2]
        
        train_labels = datanew[36]
        train = datanew.iloc[:,1:-2]
        train_labels = train_labels.apply(lambda x:int(x))
        train_labels = np.array(train_labels, dtype=int)
        train = np.array(train,dtype=float)
        meta_train = np.zeros(shape=(len(train), Fileclass))

        from sklearn.metrics import f1_score

        def lgb_f1_score(y_hat, data):
            y_true = data.get_label()
            y_hat = np.round(y_hat) # scikits f1 doesn't like probabilities
            return 'f1', f1_score(y_true, y_hat), True
        
        test = FeaturesPair_data.iloc[:,1:-2]
        
        X_train = train
        X_train_label = train_labels
        X_test = test
        dtrain = lgb.Dataset(X_train,X_train_label) 
        deval = lgb.Dataset(X_train,
                                   label=X_train_label,
                                   reference=dtrain,
                                   )

        params = {
                'task':'train', 
                'boosting_type':'gbdt',
                'num_leaves': 15,
                'objective': 'multiclass',
                'num_class':2,
                'learning_rate': 0.05,
                'feature_fraction': 0.85,
                'subsample':0.85,
                'num_threads': 32,
                'metric':'multi_error',
                "device" : "cpu",
                'seed':100,
                'min_data':1,
                'min_data_in_bin':1,
            }
        #num_round = 200
        num_round = 10000

        model = lgb.train(params, dtrain, num_boost_round=100000, verbose_eval=100, valid_sets=deval, early_stopping_rounds = 100)
        
        pred_test = model.predict(X_test)

        pair1 =  (str(FeaturesPair_data.iloc[0:1,36].values[0]))
        pair2 =  (str(FeaturesPair_data.iloc[1:2,36].values[0]))
        
        label1 = hash_label_list[pair1.upper()]
        label2 = hash_label_list[pair2.upper()]
        if label1 == l[0]:
            label1 = 0
            label2 = 1
        else:
            label1 = 1
            label2 = 0
        print (label1,label2)

        if pred_test[0][label1] > pred_test[0][label2] and pred_test[1][label1] > pred_test[1][label2]:
##            print ('true', pair1, pair2)
            print ("Original Author:", pair1)
##            if abs(pred_test[0][label1] - pred_test[0][label2]) >= 0.1 and abs(pred_test[1][label1] - pred_test[1][label2]) >= 0.1:
##                print ('valid')
        elif pred_test[0][label1] < pred_test[0][label2] and pred_test[1][label1] < pred_test[1][label2]:  
##            print ('false', pair1, pair2)
            print ('Original Author:', pair2)
##            if abs(pred_test[0][label1] - pred_test[0][label2]) >= 0.1 and abs(pred_test[1][label1] - pred_test[1][label2]) >= 0.1:
##                print ('valid')
        else:
##            print ('unknown', pair1, pair2)
            print ('Unknown')
        print ('Similarity'+' '+str(i)+ '->'+str(i+1) )
        print (pred_test[0][label1],pred_test[0][label2])
        print ('Similarity'+' '+str(i+1)+ '->'+str(i) )
        print (pred_test[1][label1],pred_test[1][label2])
        print ('\n')
    except Exception as e:
        print (e)
        print ('error!!!!!!!!!!!!!!!!!!!!!!!!!!!!')



def main():
    
    if len(sys.argv) != 3:
        print("AppAuth must takes 2 argument.")
        print("Usage:")
        print("    $ python pariauth.py csv_path_pre csv_path_all")
        print("    ")
        print("    csv_path_pre: input the need-to-predict 2 feature vectors in 2 .csv files named with author's name.")
        print("    [dir]Features_pre---┬---[file]auth#1pre.csv--------[row]auth#1apk#1pre")
        print("                        └---[file]auth#2pre.csv--------[row]auth#2apk#1pre")
        print("    ")
        print("    csv_path_all: input all the other feature vectors in .csv files named with author's name.")
        print("    [dir]Features_all---┬---[file]auth#1all.csv---┬---[row]auth#1apk#1all")
        print("                        │                         ├---[row]auth#1apk#2all")
        print("                        │                         ├---...")
        print("                        │                         └---[row]auth#1apk#Nall")
        print("                        └---[file]auth#2all.csv---┬---[row]auth#2apk#1all")
        print("                                                   ├---[row]auth#2apk#2all")
        print("                                                   ├---...")
        print("                                                   └---[row]auth#2apk#Nall")
        exit(1)

    csv_path_pre = sys.argv[1]
    csv_path_all = sys.argv[2]
    
    if not os.path.isdir(csv_path_pre):
        print("Can NOT find directory: '%s'" % csv_path_pre)
        exit(1)

    if not os.path.isdir(csv_path_all):
        print("Can NOT find directory: '%s'" % csv_path_all)
        exit(1)

    Filepath = csv_path_all
    Fileclass = 0 #label number
    Remove_less = False #if true remove less than 2

    hash_label_list = dict()
    label_hash_list = dict()
    csvpath = Filepath + '/../all.csv'
    if(os.path.exists(csvpath)):
        os.remove(csvpath)
        print ("remove ok!")
    else:
        print ("not exists!")
        
    for i, filename in enumerate(os.listdir(Filepath)):
        if not filename.endswith('.csv'):
            continue
        Author_name = filename[0:-4]
            
        data = pd.read_csv(Filepath+'/'+filename, header=None)
        if len(data)<=2 and Remove_less==True:
            continue
        
        data['author'] = Author_name
        data['label'] = Fileclass
        hash_label_list[Author_name] = Fileclass
        label_hash_list[Fileclass] = Author_name
        
        Fileclass += 1
        
        data.to_csv(csvpath, encoding="utf_8_sig", index=False, header=False, mode='a+')

    data_pair = pd.read_csv(csvpath, header=None)

    data_pair[36] = data_pair[36].apply(lambda x :str(x).lower())

    FeaturesPair_path = csv_path_pre
    Fileclass = 0
    
    csvpath = FeaturesPair_path + '/../pair.csv'
    if(os.path.exists(csvpath)):
        os.remove(csvpath)
        print ("remove ok!")
    else:
        print ("not exists!")
        
    for i, filename in enumerate(os.listdir(Filepath)):
        if not filename.endswith('.csv'):
            continue
        Author_name = filename[0:-4]
            
        data = pd.read_csv(FeaturesPair_path+'/'+filename, header=None)
        
        data['author'] = Author_name
        data['label'] = Fileclass
        
        Fileclass += 1
        
        data.to_csv(csvpath, encoding="utf_8_sig", index=False, header=False, mode='a+')

    FeaturesPair_data = pd.read_csv(csvpath, header=None)
    FeaturesPair_data[0] = FeaturesPair_data[0].apply(lambda x :str(x).lower())

    index = ~data_pair[0].isin(FeaturesPair_data[0])

    data_all = data_pair[index]

    pair_predict(data_all, FeaturesPair_data, hash_label_list, label_hash_list)


if __name__ == '__main__':
    
    begin = time.time()
    
    main()
    
    end = time.time()
    print "Done in %d hours %d minutes %d seconds" % \
    ((end - begin) / 3600, (end - begin) / 60 % 60, (end - begin) % 60)
