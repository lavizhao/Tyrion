#coding: utf-8

'''
category查起来太慢了，重新dump一下
'''

from multiprocessing import Process,Queue
from util.db import mydb
from data import one_tran,get_conf
import time
import cPickle as pickle

#任务queue
tqueue = Queue(100000)

#结果的queue
gqueue = Queue(100000)

cf = get_conf()

def get_mydb():
    host = cf["host"]
    user = cf["user"]
    passwd = cf["passwd"]
    if passwd == "null":
        passwd = ""

    mdb = mydb(host=host,user=user,passwd=passwd,port=3306,cache_open=False)
    return mdb    


def handle(num):
    print "handle start"
    count = 0
    qsize = tqueue.qsize()

    mdb = get_mydb()

    while qsize > 0:
        category = tqueue.get()
        sql_str = 'select beh,dt from trans where category=\"%s\"'%(category)
        
        res = mdb.select_sql(sql_str,"tmall")
        gqueue.put((category,res))
        count += 1
        if count % 10 == 0:
            print "线程名",num,count

#主程序
def main():
    mdb = get_mydb()
    res = mdb.select_sql("select distinct category from trans;","tmall")
    res = [i[0] for i in res]
    for i in res:
        tqueue.put(i)

    print "开启进程"
        
    thread_num = 3
    for i in range(thread_num):
        p = Process(target=handle,args=((str(i))))
        p.start()
        
    result = {}
    current = 0
    sleep_count = 200
    count = 0
    while current <= sleep_count:
        if gqueue.qsize() > 0:
            count += 1
            res = gqueue.get()
            result[res[0]] = res[1]
            current = 0
            if count % 100 == 0:
                print "category大小",len(result)
        else:
            current += 1
            time.sleep(0.2)

    print "正在存储"
    t = open(cf["category_cache"],"wb")
    pickle.dump(result,t,True)
    
            
if __name__ == '__main__':
    main()
