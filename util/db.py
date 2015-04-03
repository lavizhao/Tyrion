#!/usr/bin/python3
#coding: utf-8

'''
这个脚本的目的是管理mysql中的表数据
'''
import sys

#import pymysql as mysql
import mysql.connector
import logging
from .read_conf import config
import cPickle as pickle

cf = config("conf/data_dir.conf")

import random

class mydb:
    def __init__(self,host,port,user,passwd):
        self.count = 0
        #设置mysql连接
        try:
            self.conn = mysql.connector.connect(host=host,user=user,passwd=passwd,port=port)
        except Exception as err:
            logging.error(err)

        self.cache = {}
        self.cache_limit = 1000 * 600
        self.select_count = 0
        self.hit_cache = 0
        self.dump_limit = 100000

        #装载cache
        db_cache = cf["db_cache"] #获取文件名
        try :
            print "载入cache"
            f = open(db_cache,"rb")
            self.cache = pickle.load(f)
            f.close()
        except:
            self.cache = {}
            
    def create_db(self,db_name):
        try:        
            cur = self.conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8"%(db_name))
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def drop_db(self,db_name):
        try :
            cur = self.conn.cursor()
            cur.execute("drop database if exists %s;"%(db_name))
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def execute_sql(self,sql_str,db_name):
        try :
            cur = self.conn.cursor()
            cur.execute("use %s"%(db_name))
            cur.execute(sql_str)
            self.conn.commit()
        except Exception as err:
            logging.error(err)

    def insert_sql(self,sql_str,db_name,commit_num = 1):
        try :
            self.count += 1
            cur = self.conn.cursor()
            cur.execute("use %s"%(db_name))
            cur.execute(sql_str)
            if self.count % commit_num == 0:
                self.conn.commit()
                self.count = 0
        except Exception as err:
            logging.error(err)

        
    def select_sql(self,sql_str,db_name):

        self.select_count += 1
        if (self.select_count) % 3000 == 0:
            print "命中率",1.0 * self.hit_cache / self.select_count,"cache大小",len(self.cache)

        if sql_str in self.cache:
            self.hit_cache += 1
            return self.cache[sql_str]
            
        cur = self.conn.cursor()
            
        cur.execute("use %s"%(db_name))
        cur.execute(sql_str)
            
        result = cur.fetchall()

        if len(self.cache) > self.cache_limit:
            print "clean cache"
            cache_key = self.cache.keys()
            sample = random.sample(cache_key,int(0.25*self.cache_limit))
            for i in sample:
                self.cache.pop(i)
            self.cache[sql_str] = result
            print "cache大小",len(self.cache)    
        else:
            #如果cache没有到一半，直接留下
            if len(self.cache) < (0.5 * self.cache_limit):
                self.cache[sql_str] = result
            elif ( 3 * random.random()) < len(result) / 10.0:
                self.cache[sql_str] = result

        return result
            

        
    def dump_cache(self):
        print "正在存储"
        
        cache_key = self.cache.keys()
        rem_key = []
        for key in cache_key:
            if random.random() > 0.3:
                rem_key.append(key)
            else:
                pass

        for key in rem_key :
            self.cache.pop(key)

        cache_key = self.cache.keys()
        
        if len(self.cache) > self.dump_limit:
            sample = random.sample(cache_key,int(len(self.cache) - self.dump_limit))
            for i in sample :
                self.cache.pop(i)
        print "cache大小", len(self.cache)
                
        t = open(cf["db_cache"],"wb")
        pickle.dump(self.cache,t,True)
        print "存储完毕"
        
