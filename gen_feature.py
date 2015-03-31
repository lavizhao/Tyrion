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

max_day = 36

#单线程的先这么写着
mdb = get_mydb()

last_day = datetime.date(2014,12,18)
print "last day is ",last_day
    
#抽象类
class abstract_f:
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

        
#用户在过去n天（n可以为0,1,2...35天，取的比较多的原因是怕最后维度不一样）
#内，的beh次数        
class user_item_shopping_beh(abstract_f):
    def __init__(self):
        pass

    def get_cand(self):
        day = ["day%s"%(i) for i in range(1,max_day)]
        beh = ["beh%s"%(i) for i in range(0,5)]

        result = list(itertools.product(day,beh))
        result = ["%s_%s"%(i,j) for i,j in result]

        return set(result)

    def extract(self,tran):
        assert isinstance(tran,Tran)==True

        user = tran.user_id
        item = tran.item_id

        sql_str = 'select beh,dt from trans where item=\"%s\" and user=\"%s\"'%(item,user)
        sql_result = mdb.select_sql(sql_str,"tmall")

        result = dict.fromkeys(self.get_cand(),0)
        
        #对于每一条数据，第一位是行为，第二位是日期
        for msql in sql_result:
            dt = msql[1]
            timed = (last_day-dt).days #日期间隔
            beh = msql[0]

            #得到特征字符串
            fstr = "day%s_beh%s"%(timed,beh)
            if fstr in result:
                result[fstr] += 1

        res = self.transform(result)
        return res


#用户在过去n天beh过多少次商品
class user_shopping_beh(abstract_f):
    def __init__(self):
        pass

    def get_cand(self):
        day = ["day%s"%(i) for i in range(1,max_day)]
        beh = ["beh%s"%(i) for i in range(0,5)]

        result = list(itertools.product(day,beh))
        result = ["%s_%s"%(i,j) for i,j in result]

        return set(result)

    def extract(self,tran):
        assert isinstance(tran,Tran)==True

        user = tran.user_id
        item = tran.item_id

        sql_str = 'select beh,dt from trans where user=\"%s\"'%(user)
        sql_result = mdb.select_sql(sql_str,"tmall")

        result = dict.fromkeys(self.get_cand(),0)
        
        #对于每一条数据，第一位是行为，第二位是日期
        for msql in sql_result:
            dt = msql[1]
            timed = (last_day-dt).days #日期间隔
            beh = msql[0]

            #得到特征字符串
            fstr = "day%s_beh%s"%(timed,beh)
            if fstr in result:
                result[fstr] += 1

        res = self.transform(result)

        return res

    
#商品n天内被beh过多少次
class item_shopping_beh(abstract_f):
    def __init__(self):
        pass

    def get_cand(self):
        day = ["day%s"%(i) for i in range(1,max_day)]
        beh = ["beh%s"%(i) for i in range(0,5)]

        result = list(itertools.product(day,beh))
        result = ["%s_%s"%(i,j) for i,j in result]

        return set(result)

    def extract(self,tran):
        assert isinstance(tran,Tran)==True

        user = tran.user_id
        item = tran.item_id

        sql_str = 'select beh,dt from trans where item=\"%s\"'%(item)
        sql_result = mdb.select_sql(sql_str,"tmall")

        result = dict.fromkeys(self.get_cand(),0)
        
        #对于每一条数据，第一位是行为，第二位是日期
        for msql in sql_result:
            dt = msql[1]
            timed = (last_day-dt).days #日期间隔
            beh = msql[0]

            #得到特征字符串
            fstr = "day%s_beh%s"%(timed,beh)
            if fstr in result:
                result[fstr] += 1

        res = self.transform(result)
        
        return res


#商品所在种类n天内被beh过多少次
class category_shopping_beh(abstract_f):
    def __init__(self):
        pass

    def get_cand(self):
        day = ["day%s"%(i) for i in range(1,max_day)]
        beh = ["beh%s"%(i) for i in range(0,5)]

        result = list(itertools.product(day,beh))
        result = ["%s_%s"%(i,j) for i,j in result]

        return set(result)

    def extract(self,tran):
        assert isinstance(tran,Tran)==True

        user = tran.user_id
        item = tran.item_id
        category = tran.item_category

        sql_str = 'select beh,dt from trans where category=\"%s\"'%(category)
        sql_result = mdb.select_sql(sql_str,"tmall")

        result = dict.fromkeys(self.get_cand(),0)
        
        #对于每一条数据，第一位是行为，第二位是日期
        for msql in sql_result:
            dt = msql[1]
            timed = (last_day-dt).days #日期间隔
            beh = msql[0]

            #得到特征字符串
            fstr = "day%s_beh%s"%(timed,beh)
            if fstr in result:
                result[fstr] += 1

        res = self.transform(result)

        return res


        
#这两个字典是这个文件最重要的部分，经过上一轮的迭代
#如果特征不变，那么放在normal_list中
#如果特征更改、增加那么放在append_list中
#如果特征删除，那么放在哪里都不放。。。
normal_list = []
append_list = [user_item_shopping_beh,user_shopping_beh,item_shopping_beh,category_shopping_beh]

def main():
    ot = one_tran(dt="test128")
    #ot = one_tran()
    count = 0

    #这是这些类的实例化
    normal_ins = [i() for i in normal_list]
    append_ins = [i() for i in append_list]

    #写入文件
    fileds = []
    for norm in normal_ins:
        fileds.extend(norm.filed_names())
    for app in append_ins:
        fileds.extend(app.filed_names())

    t = open(cf["train_dir"],"w")
    writer = csv.DictWriter(t,fileds)

    first = {i:i for i in fileds}
    
    writer.writerow(first)
    
    for tran in ot:
        final = {}
        for i in append_ins:
            res = i.extract(tran)
            final = dict(final,**res) #字典合并

        writer.writerow(final)
            
        count += 1
        if count % 10 == 0:
            print count

    mdb.dump_cache()
            
if __name__ == '__main__':
    main()
