#coding: utf-8

'''
用来创建数据库和删除数据库，插入表等操作
'''

import mysql.connector
import sys
import logging

from data import one_tran,get_conf

cf = get_conf()

host = cf["host"]
user = cf["user"]
passwd = cf["passwd"]
if passwd == "null":
    passwd = ""

conn = mysql.connector.connect(host=host,user=user,passwd=passwd)

def create():
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8"%("tmall"))

    cur.execute("use tmall")
    cur.execute("CREATE table trans (user char(13),item char(13),beh tinyint,geo char(10),category char(10),dt date,tm tinyint, \
    index ind1(user(8)),index ind2(item(8)),index ind3(geo),index ind4(category),index ind5(dt))")
    conn.commit()

    #写数据库
    ot = one_tran()
    count = 0
    for tran in ot:
        cur.execute(tran.sql_str())
        
        count += 1
        if count % 10000 == 0:
            print count/1000000.0,"M"
            conn.commit()

    conn.commit()

def deld():
    cur = conn.cursor()
    cur.execute("drop database if exists tmall")
    conn.commit()
    

if __name__ == '__main__':
    opt = sys.argv[1]
    if opt not in ['create','del']:
        logging.error('option not right')
        sys.exit(1)

    elif opt == "create":
        create()

    else:
        deld()

    
