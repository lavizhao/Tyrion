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

    mu,mi = 0,0
    mgeo = ""
    mcat = ""

    count = 0
    for tran in ot:
        uset.add(tran.user_id)
        iset.add(tran.item_id)
        geo.add(tran.user_geohash)
        dates.add(tran.date)

        mu = max(mu,tran.user_id)
        mi = max(mi,tran.item_id)

        if len(tran.user_geohash) > len(mgeo):
            mgeo = tran.user_geohash

        if len(tran.item_category) > len(mcat):
            mcat = tran.item_category
            

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
    print "最大用户",mu
    print "最大物品",mi
    print "最大地理位置",mgeo
    print "最大物品种类",mcat

    for dt in beh:
        print "日期",dt,"行为",beh[dt]
    

if __name__ == '__main__':
    stat()        
