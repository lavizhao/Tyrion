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

#配置文件存储位置
cfdir = "conf/data_dir.conf"
conf = config(cfdir)

def get_conf():
    return  conf

#返回一条数据，这个具体用在统计数据等其他地方
def one_tran(tp="tran"):
    f = open(conf["user_dir"])
    reader = csv.reader(f)

    count = 0
    
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
