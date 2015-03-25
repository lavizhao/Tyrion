#coding: utf-8

'''
基本的数据结构封装
user和item文件的字段保持跟比赛题目中完全一致
'''

import datetime

#Tran对应user，即数据说明第一部分，字段完全一致，可直接访问,usergeo可以没有
class Tran:
    __slots__ = ['user_id', 'item_id', 'behavior_type','user_geohash','item_category','time']
    
    def __init__(self,uid,iid,betype,itemcat,time,usergeo=None):
        self.user_id = uid
        self.item_id = iid
        self.behavior_type = betype
        self.user_geohash = usergeo
        self.item_category = itemcat
        #self.time = datetime.datetime(time)
        time = time.split()
        self.date = time[0]
        self.time = time[1]

    def __str__(self):
        s = "用户标识:%s || 商品标识:%s || 用户对商品行为类型:%s \
用户空间标识:%s || 商品分类标识: %s || 行为时间:%s\n"\
        %(self.user_id,self.item_id,self.behavior_type,\
          self.user_geohash,self.item_category,self.time)

        return s

    def __getstate__(self):
        return (self.user_id,self.item_id,self.behavior_type,self.user_geohash,self.item_category,self.time)

    def __setstate__(self,slots):
        self.user_id = slots[0]
        self.item_id = slots[1]
        self.behavior_type = slots[2]
        self.user_geohash = slots[3]
        self.item_category = slots[4]
        self.time = slots[5]

