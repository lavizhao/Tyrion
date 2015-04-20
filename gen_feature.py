#coding: utf-8

'''
feature抽取
'''
import mysql.connector
import sys
import logging,time

from data import one_tran,get_conf
from util.db import mydb #mysql db的意思
from util.ds import Tran
import datetime

import csv,sys
import itertools

cf = get_conf()

def get_mydb():
    host = cf["host"]
    user = cf["user"]
    passwd = cf["passwd"]
    if passwd == "null":
        passwd = ""

    mdb = mydb(host=host,user=user,passwd=passwd,port=3306)
    return mdb    

max_day = 32

#单线程的先这么写着
mdb = get_mydb()

last_day = datetime.date(2014,12,18)
day129 = datetime.date(2014,12,19)
print "last day is ",last_day

#将day转化成datetime.date
def turn_day(dt):
    sp = dt.split('-')
    sp = [int(i) for i in sp]
    return datetime.date(sp[0],sp[1],sp[2])

def day_tim_beh():
    day = ["day%s"%(i) for i in range(1,max_day)]
    beh = ["beh%s"%(i) for i in range(1,5)]

    result = list(itertools.product(day,beh))
    result = ["%s_%s"%(i,j) for i,j in result]

    return set(result)
    
#抽象类
class abstract_f:
    def set_type(self,date_set):
        self.date_set = date_set

    def get_type(self):
        return self.date_set
        
    #获取类的名字，用来做特征的名字
    def get_name(self):
        return self.__class__.__name__

    #生成候选特征名字，例如beh1_day2这种
    def get_cand(self):
        pass

    #抽取特征，这个也很好理解，get_cand函数就是在这里用的，然后返回的是个字典
    #{feature1:value1,.....}这种
    def extract(self,tran):
        pass

    #讲特征名转成类名+特征的字典
    def transform(self,udict):
        result = {"%s_%s"%(self.get_name(),i):udict[i] for i in udict}
        return result

    def filed_names(self):
        cand = self.get_cand()
        return ["%s_%s"%(self.get_name(),i) for i in cand]


class feature_time_beh(abstract_f):
    def __init__(self):
        pass

    def get_cand(self):
        return day_tim_beh()

    def get_sql(self,tran):
        return "haha"
        
    def extract(self,tran):
        assert isinstance(tran,Tran)==True

        td = tran.date
        if self.get_type() == "train":
            td = turn_day(td)
        elif self.get_type() == "dev":
            td = last_day
        elif self.get_type() == "test":
            td = day129
        else:
            td = last_day

        sql_str = self.get_sql(tran)
        sql_result = mdb.select_sql(sql_str,"tmall")

        result = dict.fromkeys(self.get_cand(),0)
        
        #对于每一条数据，第一位是行为，第二位是日期
        for msql in sql_result:
            dt = msql[1]
            timed = (td-dt).days #日期间隔
            beh = msql[0]

            #得到特征字符串
            fstr = "day%s_beh%s"%(timed,beh)
            if fstr in result:
                result[fstr] += 1

        res = self.transform(result)

        return res

        
        
#用户在过去n天（n可以为0,1,2...35天，取的比较多的原因是怕最后维度不一样）
#内，的beh次数        
class user_item_shopping_beh(feature_time_beh):
    def get_sql(self,tran):
        item = tran.item_id
        user = tran.user_id
        return 'select beh,dt from trans where item=\"%s\" and user=\"%s\"'%(item,user)
        

#用户在过去n天beh过多少次商品
class user_shopping_beh(feature_time_beh):
    def get_sql(self,tran):
        user = tran.user_id
        return 'select beh,dt from trans where user=\"%s\"'%(user)

    
#商品n天内被beh过多少次
class item_shopping_beh(feature_time_beh):
    def get_sql(self,tran):
        item = tran.item_id
        return 'select beh,dt from trans where item=\"%s\"'%(item)

#商品所在种类n天内被beh过多少次
class category_shopping_beh(feature_time_beh):
    def get_sql(self,tran):
        category = tran.item_category
        return 'select beh,dt from trans where category=\"%s\"'%(category)


        
#这两个字典是这个文件最重要的部分，经过上一轮的迭代
#如果特征不变，那么放在normal_list中
#如果特征更改、增加那么放在append_list中
#如果特征删除，那么放在哪里都不放。。。
#normal_list = [user_item_shopping_beh]
#append_list = [user_shopping_beh,item_shopping_beh,category_shopping_beh]
normal_list = []
append_list = [user_item_shopping_beh,user_shopping_beh,item_shopping_beh]

def main(data_set):

    #根据数据集打开文件
    ot = one_tran(dt=data_set)

    #这是这些类的实例化
    normal_ins = [i() for i in normal_list]
    append_ins = [i() for i in append_list]

    normal_name = [i.get_name() for i in normal_ins]
    append_name = [i.get_name() for i in append_ins]

    #用来记录现有的不需要改变特征的特征名
    normal_cands = []
    for i in normal_ins:
        normal_cands.extend(i.filed_names())

    normal_cands = set(normal_cands)
    
    #设定这些类的数据集类型，主要是给他们制定日期是哪一天
    for i in normal_ins:
        i.set_type(data_set)
    for i in append_ins:
        i.set_type(data_set)

    #fileds是csv文件的列名
    fileds = []
    for norm in normal_ins:
        fileds.extend(norm.filed_names())
    for app in append_ins:
        fileds.extend(app.filed_names())

    #开文件，这里的文件主要作用是留住那些不变的
    try :    
        if data_set == "train":
            f = open(cf["train_dir"])
        elif data_set == "dev":
            f = open(cf["dev_dir"])
        elif data_set == "test":
            f = open(cf["pred_dir"])
        else:
            print "有问题"
            sys.exit(1)

    except :
        f = None

    if f != None:
        reader = csv.DictReader(f)
        
    #临时文件
    temp_file = open(cf["temp_file"],"w")
    writer = csv.DictWriter(temp_file,fileds)

    first = {i:i for i in fileds}
    writer.writerow(first)

    count = 0
    
    for tran in ot:
        
        #抽取现有特征的当前行
        if f != None:
            line = reader.next()
            
        final = {}

        #抽需要改变的
        for i in append_ins:
            res = i.extract(tran)
            final = dict(final,**res) #字典合并

        if f != None:
            #抽取不需要改变的
            for key in line:
                if key in normal_cands:
                    final[key] = line[key]

        writer.writerow(final)

        count += 1
        if count % 1000 == 0:
            print count

    try : 
        f.close()
        temp_file.close()
    except:
        print "呵呵"
    temp_file = open(cf["temp_file"])

    if data_set == "train":
        f = open(cf["train_dir"],"w")
    elif data_set == "dev":
        f = open(cf["dev_dir"],"w")
    elif data_set == "test":
        f = open(cf["pred_dir"],"w")
    else:
        print "有问题"
        sys.exit(1)


    for line in temp_file:
        f.write(line)    
    
from optparse import OptionParser 
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-d", "--data", dest="data",help="选择数据集，训练还是测试")

    (options, args) = parser.parse_args()

    if options.data == "train":
        print "训练集"
        main("train")

    elif options.data == "dev":
        print "验证集合"
        main("dev")
        
    elif options.data == "test":
        print "测试集合"
        main("test")
        
    else :
        print "error,没有符合的数据集"
        sys.exit(1)

    mdb.dump_cache()
