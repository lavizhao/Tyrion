#coding: utf-8

'''
主要是定义相似度函数，因为相似度函数在某些情况下的作用非常关键
'''

import logging
from abc import ABCMeta, abstractmethod

#因为相似度这玩意其实不好衡量，所以在这里面统一的，1是最大，0是最小。越大越相似

#相似度函数的抽象类
class abstract_sim:
    __metaclass__ = ABCMeta

    #计算两个向量的相似度
    @abstractmethod
    def sim(self):
        pass


#只用浏览记录来计算两个物品的相似度
class user_beh_cos_sim(abstract_sim):
    def sim(self,u1,u2):
        if type(u1) != type(u2):
            logging.ERROR("在计算相似度函数user_beh_cossim中，u1和u2的type不等")
        else:
            beh1 = u1.beh_vec
            beh2 = u2.beh_vec

            norm1 = beh1.norm()
            norm2 = beh2.norm()

            dotsum = beh1.dot(beh2)
            #print "用户行为",dotsum

            return dotsum.sum() / norm1 / norm2

#只用用户浏览时间计算两个物品的相似度
class user_time_sim(abstract_sim):
    def sim(self,u1,u2):
        if type(u1) != type(u2):
            logging.ERROR("在计算相似度函数user_time_sim中，u1和u2的type不等")
            
        else:
            tim1 = u1.time_vec
            tim2 = u2.time_vec

            jiao = (tim1.keys()) & (tim2.keys())
            bing = (tim1.keys()) | (tim2.keys())
            
            #print "浏览时间",jiao
            return len(jiao) * 1.0 / len(bing) 

#购买次数相似度
class user_shopping_sim(abstract_sim):
    def sim(self,u1,u2):
        if type(u1) != type(u2):
            logging.ERROR("在计算相似度函数user_shopping_sim中，u1和u2的type不等")
            
        else:
            shop1 = u1.shopping_vec
            shop2 = u2.shopping_vec

            sh3 = shop1 - shop2

            #下面纯规则写了
            
            #买东西的个数
            buy4 = abs(sh3[4])
            buy3 = abs(sh3[3])
            buy2 = abs(sh3[2])
            buy1 = abs(sh3[1])

            #如果买东西差的太多，那么肯定不相同
            if buy4 > 10:
                return 0
            elif buy4 > 5 and (buy3 + buy2) > 5:
                return 0.25
            elif buy1 > 100:
                return 0.75
            else:
                return 1
            
class user_geo_sim(abstract_sim):
    def sim(self,u1,u2):
        if type(u1) != type(u2):
            logging.ERROR("在计算相似度函数user_geo_sim中，u1和u2的type不等")
            
        else:
            geo1 = u1.geo_vec
            geo2 = u2.geo_vec

            jiao = (geo1.keys()) & (geo2.keys())
            bing = (geo1.keys()) | (geo2.keys())

            #最后一个是惩罚项，如果两个都是空的话，那么即使两个用户都是空，相似度也不是1
            return len(jiao) * 1.0 / len(bing)/(1+1.0/(len(jiao)+1))

            
#总的相似度
class user_sim(abstract_sim):
    def __init__(self):
        self.ubcs = user_beh_cos_sim()
        self.uts = user_time_sim()
        self.uss = user_shopping_sim()
        self.ugs = user_geo_sim()

    def sim(self,u1,u2):
        if type(u1) != type(u2):
            logging.ERROR("在计算相似度函数user_sim中，u1和u2的type不等")
            
        else:
            beh_sim = self.ubcs.sim(u1,u2)
            tim_sim = self.uts.sim(u1,u2)
            sho_sim = self.uss.sim(u1,u2)
            geo_sim = self.ugs.sim(u1,u2)

            #下面是权值
            beh_w = 2.0
            tim_w = 2.0
            sho_w = 3.0
            geo_w = 2.0
            return (beh_sim*beh_w + tim_sim*tim_w + sho_sim*sho_w + geo_sim*geo_w)/\
                (beh_w + tim_w + sho_w + geo_w)
