#!/usr/bin/python
#coding: utf-8

'''
掌管数据存储和载入的文件
'''

import csv
from util.read_conf import config
from util.ds import Tran
from optparse import OptionParser
#import cPickle as pickle
import pickle
import sys

#配置文件存储位置
cfdir = "conf/data_dir.conf"
conf = config(cfdir)

def get_conf():
    return  conf

#返回一条数据，这个具体用在统计数据等其他地方
def one_tran(dt="total",tp="tran"):
    if dt == "total":
        f = open(conf["user_dir"])
    elif dt == "dev":
        f = open(conf["test128"])
    elif dt == "train":
        f = open(conf["train70"])
    elif dt == "test":
        f = open(conf["pred129"])
    else:
        print "未定义文件名%s"%(dt)
        sys.exit(1)
    
    reader = csv.reader(f)

    count = 0
    if dt == "test":
        count += 1
    
    for line in reader:
        if count == 0:
            count += 1
            continue

        ud,iid,bt,ug,ic,tm = int(line[0]),int(line[1]),int(line[2]),line[3],line[4],line[5]
        tran = Tran(ud,iid,bt,ic,tm,ug)
        count += 1
        if tp == "tran":
            yield tran
        elif tp == "list":
            yield line
        elif tp == "list,tran" or tp == "tran,list":
            yield [tran,line]
        else:
            yield ','.join(line)

#存储user文件
def dump_user():
    #user文件，开文件
    f = open(conf["user_dir"])
    reader = csv.reader(f)

    t = open(conf["udump_dir"],"wb")

    result = []
    
    count = 0
    for line in reader:
        if count == 0:
            count += 1
            continue
            
        ud,iid,bt,ug,ic,tm = int(line[0]),int(line[1]),int(line[2]),line[3],line[4],line[5]
        tran = Tran(ud,iid,bt,ic,tm,ug)
        result.append(tran)
        
        count += 1
        if count % 1000000 == 0:
            print("进度%sM"%(count/1000000))

    print("正在存储")
    pickle.dump(result,t,True)
        
def load_user():
    f = open(conf["udump_dir"],"rb")
    trans = pickle.load(f)

    for tran in trans:
        print(tran)

#存储label
def dump_label(data_set):
    print data_set
    ot = one_tran(data_set)
    t = ""
    if data_set == "train":
        t = open(conf["train_label"],"w")
    elif data_set == "dev":
        t = open(conf["dev_label"],"w")
    else:
        print "没做"
        sys.exit(1)

    count = 0
        
    for tran in ot:
        beh = tran.behavior_type
        lb = -1
        if beh == 1:
            lb = 0
        elif beh == 4:
            lb = 1
        else:
            print "err"
            sys.exit(1)

        t.write("%s\n"%(lb))
        count += 1
        if count % 10000 == 0:
            print count
            
    print "done"

def load_label(data_set):
    if data_set == "train":
        f = open(conf["train_label"])
    elif data_set == "dev":
        f = open(conf["dev_label"])
    else:
        print "没做"
        sys.exit(1)

    result = f.readlines()
    result = [int(i) for i in result]
    return result

def load_data(data_set,rd):
    if data_set == "train":
        f = open(conf["train_dir"])
    elif data_set == "dev":
        f = open(conf["dev_dir"])
    else:
        print "没做"
        sys.exit(1)

    result = []
    f.readline()
    if data_set == "train":
        count = 0
        for line in f:
            sp = line.split(',')
            sp = [int(i) for i in sp]
            result.append(sp)
            count += 1
            if count % rd == 0:
                yield result
                result = []
    else:
        count = 0
        for line in f:
            sp = line.split(',')
            sp = [int(i) for i in sp]
            result.append(sp)
            count += 1
            if count % 20000 == 0:
                print count
        yield result
    
if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-d","--data",dest="data",action="store",\
                      help=u"存储数据种类",type="string")
    parser.add_option("-a","--action",dest="action",action="store",\
                      help=u"选择动作是存储还是装载装载用来测试",type="string")
    (options, args) = parser.parse_args()

    if options.action == "dump":
        if options.data == "user":
            dump_user()

    elif options.action == "load":
        if options.data == "user":
            load_user()

    if options.action == "label":
        dump_label(options.data)
