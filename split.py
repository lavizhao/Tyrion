#coding: utf-8

'''
分割数据，暂定留最后四天的数据,也就是12月15,16,17,18
'''

from data import one_tran,get_conf
import csv

cf = get_conf()

target = set(["2014-12-17","2014-12-18"])

#分割函数
def spt():
    ot = one_tran("tran,list")
    train = open(cf["usplit_train"],"w")
    test = open(cf["usplit_test"],"w")

    train = csv.writer(train)
    test = csv.writer(test)

    count = 0
    for tran,line in ot:
        if tran.date in target:
            test.writerow(line)
        else:
            train.writerow(line)

        count += 1
        if count % 1000000 == 0:
            print("进度%sM"%(count/1000000.0))

if __name__ == '__main__':
    spt()
