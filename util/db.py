#!/usr/bin/python3
#coding: utf-8

'''
这个脚本的目的是管理mysql中的表数据
'''
import sys

#import pymysql as mysql
import mysql.connector
import logging

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
        self.cache_limit = 20000
        self.select_count = 0
        self.hit_cache = 0
            
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
        try:
            self.select_count += 1
            if (self.select_count) % 300 == 0:
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
                cache_key = cache.keys()
                sample = cache_key.random(cache_key,0.25*self.cache_limit)
                for i in sample:
                    self.cache.pop(i)
                self.cache[sql_str] = result
            else:
                if random.random() < len(result) / 200.0:
                    self.cache[sql_str] = result

            return result
            
        except Exception as err:
            logging.error(err)
            logging.error("select error")

