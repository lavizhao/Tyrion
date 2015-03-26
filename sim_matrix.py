#coding: utf-8

'''
存储并计算用户相似度矩阵
'''

import time
from data import get_conf,one_tran
from multiprocessing import Process,Queue
from util.ds import user_vector
from util.sim_function import user_beh_cos_sim as Ubcs
from util.sim_function import user_time_sim as Uts
from util.sim_function import user_shopping_sim as Uss
from util.sim_function import user_sim as Us

#这个队列是进程队列，用户名都放在了里面
gqueue = Queue()

#这个队列的作用是文件结果都放在这里,最后取出来然后写
oqueue = Queue()

cf = get_conf()

#每个进程执行的函数
def handle(umatrix):
    print("process start")
    count = 0
    us = Us()
    while gqueue.qsize() > 0:
        user = gqueue.get()
        users = umatrix.keys()
        
        print "进程执行进度",count
        
        user_vec = umatrix[user]
        
        for u1 in users:
            if user < u1:
                sim = us.sim(user_vec,umatrix[u1])
                rs = "%s,%s %s\n"%(user,u1,sim)
                oqueue.put(rs)
            
        count += 1
            
#计算用户-用户的相似度
def uumat():
    #得到每一行的数据
    ot = one_tran()
    
    result = {}
    t = open(cf["usim_matrix"],"w")

    count = 0
    for tran in ot:
        user = tran.user_id
        item = tran.item_id
        beh = tran.behavior_type

        result.setdefault(user,user_vector(user))

        #1. 用户浏览记录
        result[user].beh_vec[item] = max(int(beh),result[user].beh_vec[item])

        #2. 用户时间字典
        result[user].time_vec[tran.time] += 1

        #3. 浏览日期字典
        result[user].date_vec[tran.date] += 1

        #4. 购买次数字典
        result[user].shopping_vec[tran.behavior_type] += 1

        #5. 用户出现地理位置
        result[user].geo_vec[tran.user_geohash] += 1
        
        count += 1
        if count % 1000000 ==0:
            print count/1000000.0,"M"


    for u in result.keys():
        gqueue.put(u)        
            
    num = 4
    for i in range(num):
        p = Process(target=handle,args=(result,))
        p.start()
            
    ct = 0
    mct = 10000 * 10000 / 2
    while 1:
        if oqueue.qsize() >0:
            if ct % 10000 == 0:
                print "写文件进度",ct
                
            rs = oqueue.get()
            t.write(rs)
            mct -= 1
            ct += 1
        else:
            if mct == 0:
                break
            else:
                time.sleep(0.1)
    
if __name__ == '__main__':
    uumat()
