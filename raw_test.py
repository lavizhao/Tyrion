#coding: utf-8

'''
抽取出候选的测试集
'''

from data import get_conf

cf = get_conf()

#毛候选文件
idir = cf["item_dir"]

from gen_feature import get_mydb

mdb = get_mydb()

def main():
    f = open(idir)
    f.readline()

    t = open(cf["pred129"],"w")

    item_set = set()

    count = 0
    for line in f:
        line = line.strip()
        item,geo,category = line.split(',')
        
        sql_str = 'select distinct user from trans where item = \"%s\"'%(item)
        
        sql_res = mdb.select_sql(sql_str,"tmall")

        for i in sql_res:
            user = i[0]

            beh = 0
            geo = "ns"
            date = "2014-12-19"
            tm = "12"
            tw = "%s,%s,%s,%s,%s,%s %s\n"%(user,item,beh,geo,category,date,tm)
            t.write(tw)

            count += 1
            if count % 1000 == 0:
                print count / 10000.0 , "万"

if __name__ == '__main__':
    main()
