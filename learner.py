#coding: utf-8

'''
这个是学习的主要文件
'''

from data import load_label,load_data,load_data_total
from scipy.sparse import csr_matrix
import numpy as np


from sklearn.naive_bayes import GaussianNB as NB
from sklearn import linear_model
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.ensemble import ExtraTreesClassifier as ET
from sklearn.ensemble import GradientBoostingClassifier as GBDT

from sklearn.metrics import f1_score
from sklearn.metrics import precision_score as pscore
from sklearn.metrics import recall_score as rscore
from data import get_conf

import sys

#先弄一下dev
def learn():

    
    clf = linear_model.SGDClassifier(penalty="l2",l1_ratio=0,alpha=0.001,class_weight={1:0.3,0:0.7},n_jobs=3)
    
    rd = 100 * 1000

    iter_num = 4
    
    for i in range(iter_num):
        print "round",i
        train = load_data("train",rd)

        train_label = load_label("train")
        train_label = np.array(train_label)

        count = 0
        for ptrain in train:
            print "partial",count
            plabel = train_label[:rd]
            train_label = train_label[rd:]
            if sum(plabel) > 0.2 * len(plabel):
                print "正例个数",sum(plabel)
                assert len(ptrain) == len(plabel)
                clf.partial_fit(ptrain,plabel,classes=[0,1])
            else :
                break
            count += 1
                
        print 100 * "="
            
    print "train_label",len(train_label)

    return clf

#试用LR、RF
def learn_total():
    
    clf = RF(n_estimators=200,max_features="auto",max_depth=8,min_samples_split=10,min_samples_leaf=2,n_jobs=3,oob_score=True,random_state=728) #max_depth = 8最好
    #clf = GBDT(n_estimators=100,max_features="auto",max_depth=8,min_samples_split=10,min_samples_leaf=2,verbose=3)
    
    rd = 500 * 1000
    
    train = load_data_total("train",rd)

    train_label = load_label("train")
    train_label = train_label[:len(train)]
    
    train_label = np.array(train_label)

    print "train_label",len(train_label),"train",len(train)
    print "train特征数",len(train[0])

    print "learn"
    
    clf.fit(train,train_label)
            


    return clf
    
    
def predict(clf):
        
    pred_test = "true"
    
    rd = 400000
    temp_dev = load_data("dev",rd)
    dev = []
    for pdev in temp_dev :
        dev.extend(pdev)
        
    dev_label = load_label("dev")
    print "dev样本大小",len(dev),len(dev_label)
    print "dev特征数",len(dev[0])

    result = clf.predict(dev)

    print "dev正样本预测数",sum(result)

    f1_s = f1_score(dev_label, result, average='binary')  * 100.0
    p_s = pscore(dev_label, result, average = 'binary') * 100.0
    r_s = rscore(dev_label, result, average = 'binary') * 100.0
    
    print "f1值", f1_s
    print "准确率",p_s
    print "召回率",r_s
    print "手算", 2 * p_s * r_s/(p_s + r_s)

    if pred_test == "false":
        sys.exit(1)

    cf = get_conf()
    
    f = open(cf["pred_dir"])
    f.readline()

    test_data = open(cf["pred129"])
    
    final = set()
    t = open(cf["final"],"w")
    t.write("user_id,item_id\n")
    
    count = 0
    rd = 200000

    ui_list = []
    for tran in test_data:
        tran = tran.split(',')
        user,item = tran[0],tran[1]
        ui_list.append("%s,%s\n"%(user,item))

    feature_list = []
    for line in f:
        sp = line.split(',')
        sp = [int(i) for i in sp]
        feature_list.append(sp)
            
        count += 1
        if count % rd == 0:
            res = clf.predict(feature_list)
            for i in range(len(res)):
                if res[i] == 1:
                    final.add(ui_list[i])
            feature_list = []
            ui_list = ui_list[rd:]        
            print count

    res = clf.predict(feature_list)
    for i in range(len(res)):
        if res[i] == 1:
            final.add(ui_list[i])
    
    print "剩余东西长度",len(res),len(ui_list)
            
    print "test预测结果",len(final)
    for i in final:
        t.write(i)
    

if __name__ == '__main__':
    clf = learn_total()
    #clf = learn()
    predict(clf)
    
