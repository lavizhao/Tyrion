#!/usr/bin/python
#coding: utf-8

'''
生成统计信息
'''

from data import one_tran

def stat():
    ot = one_tran()

    #用户
    uset = set()
    #商品
    iset = set()
    #地理
    geo = set()

    #日期
    dates = set()

    beh = {}
    

    count = 0
    for tran in ot:
        uset.add(tran.user_id)
        iset.add(tran.item_id)
        geo.add(tran.user_geohash)
        dates.add(tran.date)

        beh.setdefault(tran.date,{})
        beh[tran.date].setdefault(tran.behavior_type,0)

        beh[tran.date][tran.behavior_type] += 1
            
        count += 1
        if count % 1000000 == 0:
            print("进度%sM"%(count/1000000.0))

    print "用户个数",len(uset)
    print "商品个数",len(iset)
    print "地理位置",len(geo)
    print "日期",dates

    for dt in beh:
        print "日期",dt,"行为",beh[dt]
    

if __name__ == '__main__':
    stat()        
