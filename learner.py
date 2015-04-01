#coding: utf-8

'''
这个是学习的主要文件
'''

from data import load_label,load_data
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.naive_bayes import GaussianNB as NB
from sklearn import linear_model
from sklearn.metrics import f1_score
from data import get_conf



#先弄一下dev
def main():
    clf = linear_model.SGDClassifier(penalty="l2",l1_ratio=0,alpha=0.0001,class_weight={1:0.9,0:0.1})
    
    rd = 100 * 1000

    iter_num = 3
    
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

    rd = 200000
    temp_dev = load_data("dev",rd)
    dev = []
    for pdev in temp_dev :
        dev.extend(pdev)
        
    dev_label = load_label("dev")
    print len(dev),len(dev_label)

    result = clf.predict(dev)

    print sum(result)

    print f1_score(dev_label, result, average='macro')  
    print f1_score(dev_label, result, average='micro')
    print f1_score(dev_label, result)

    cf = get_conf()
    
    f = open(cf["pred_dir"])
    f.readline()

    test_data = open(cf["pred129"])
    
    final = set()
    t = open(cf["final"],"w")
    t.write("user_id,item_id\n")
    
    count = 0
    for line in f:
        tran = test_data.readline()
        tran = tran.split(',')
        user,item = tran[0],tran[1]
        
        sp = line.split(',')
        sp = [int(i) for i in sp]
        res = clf.predict(sp)[0]
        if int(res) == 1:
            final.add("%s,%s\n"%(user,item))
            
        count += 1
        if count % 10000 == 0:
            print count

    print len(final)
    for i in final:
        t.write(i)
    

if __name__ == '__main__':
    main()
    
