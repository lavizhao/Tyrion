#coding: utf-8

'''
feature抽取
'''
import mysql.connector
import sys
import logging


from data import one_tran,get_conf
import csv

cf = get_conf()

host = cf["host"]
user = cf["user"]
passwd = cf["passwd"]
if passwd == "null":
    passwd = ""

conn = mysql.connector.connect(host=host,user=user,passwd=passwd)
cur = conn.cursor()
cur.execute("use tmall")


f = open(cf["item_dir"])

reader = csv.reader(f)

count = 0
he = 0

for line in reader:
    if count == 0:
        count += 1
        continue

        
    item = line[0]
    cur.execute("select * from trans where item = \"%s\" "%(item))
    result = cur.fetchall()
    for i in result:
        print i

    print 100 * "="

    he += len(result)
    count += 1
    if count % 100 == 0:
        print count
    
    
print "总共多少项",count
print "平均多少",he * 1.0 / count
