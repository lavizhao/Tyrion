#coding: utf-8

'''
自己封了一个，主要是能用就行
'''

from copy import deepcopy
import unittest
import math

class sparse_vector:
    def __init__(self,input_dict={}):
        self.data = deepcopy(input_dict)

    def keys(self):
        return set(self.data.keys())

    def values(self):
        return self.data.values()

    def __getitem__(self,key):
        return self.data.get(key,0)

    def __setitem__(self,key,value):
        self.data[key] = value
        
    def __eq__(self,other):
        if isinstance(other, type(self)):
            result = (self.data == other.data)
        elif isinstance(other, type(self.data)):
            result = (self.data == other)
        else:
            result = NotImplemented
        return result

    def __add__(self,x):
        d1 = self.data
        d2 = x.data
        temp_d = {}
        all_keys = self.keys() | (x.keys())

        for key in all_keys:
            v_self = d1.get(key)
            v_x = d2.get(key)
            if v_self is None:
                temp_d[key] = v_x
            elif v_x is None:
                temp_d[key] = v_self
            else:
                temp_d[key] = v_self + v_x

        return self.__class__(temp_d)

    def __str__(self):
        return self.data.__str__()

    def __repr(self):
        return self.data.__repr__()
        
    def __len__(self):
        return len(self.data)

    def __mul__(self,r):
        return self.__class__({k: v*r for k, v in self.data.items()})

    def __sub__(self,other):
        #如果都是向量    
        if isinstance(other,type(self)):
            return self + other*(-1)

        elif type(other) == type(1):
            return self.__class__({k: v-other for k, v in self.data.items()})

    def __rmul__(self,r):
        return self.__class__({k: r*v for k, v in self.data.items()})

    def __ne__(self,other):
        eq_result = self.__eq__(other)
        if eq_result is NotImplemented:
            result = eq_result
        else:
            result = not eq_result
        return result

    def dot(self,other):
        temp_d = {}
        for key in self.data:
            v_o = other.data.get(key)
            if v_o == None:
                pass
            else :
                v_self = self.data.get(key)
                temp_d[key] = v_self * v_o
        
        return self.__class__(temp_d)

    def sum(self):
        #print self.data.values()
        return sum(self.data.values())

    def norm(self):
        n = self.dot(self)    
        return math.sqrt(n.sum())    
        
class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testInit(self):
        sp1 = sparse_vector({1:2})
        self.assertEqual(sp1.data,{1:2})

    def testGetitem(self):
        sp1 = sparse_vector({'a':2,'b':4})
        self.assertEqual(sp1['a'],2)
        self.assertEqual(sp1['b'],4)
        self.assertEqual(sp1['c'],0)

    def testEq(self):
        sp1 = sparse_vector({'a':2,'b':4})
        sp2 = sparse_vector({'a':2,'b':4})
        sp3 = sparse_vector({'a':2,'b':3})
        
        self.assertEqual(sp1==sp2,True)
        self.assertEqual(sp1==sp3,False)

    def testAdd(self):
        sp1 = sparse_vector({'a':2,'b':4})
        sp2 = sparse_vector({'a':2,'b':4})
        sp3 = sparse_vector({'c':2,'b':3})

        self.assertEqual(sp1+sp2,{'a':4,'b':8})
        self.assertEqual(sp1+sp3,{'a':2,'b':7,'c':2})

    def testMul(self):
        sp1 = sparse_vector({'a':2,'b':4})
        
        self.assertEqual(sp1*2,{'a':4,'b':8})

    def testSub(self):
        sp1 = sparse_vector({'a':2,'b':4})
        sp2 = sparse_vector({'a':3,'c':1})

        self.assertEqual(sp1-2,{'a':0,'b':2})
        self.assertEqual(sp1-sp2,{'a':-1,'b':4,'c':-1})

    def testRmul(self):
        sp1 = sparse_vector({'a':2,'b':4})
        
        self.assertEqual(2*sp1,{'a':4,'b':8})

    def testNe(self):
        sp1 = sparse_vector({'a':2,'b':4})
        sp2 = sparse_vector({'a':1,'b':4})
        sp3 = sparse_vector({'a':2,'b':4})

        self.assertEqual(sp1!=sp2,True)
        self.assertEqual(sp1!=sp3,False)

    def testDot(self):
        sp1 = sparse_vector({'a':2,'b':4})
        sp2 = sparse_vector({'a':1,'b':4})
        sp3 = sparse_vector({'a':2,'c':4})
        
        self.assertEqual(sp1.dot(sp2),{'a':2,'b':16})
        self.assertEqual(sp1.dot(sp3),{'a':4})

    def testNorm(self):
        sp1 = sparse_vector({'a':2,'b':4})

        self.assertEqual(sp1.norm(),math.sqrt(2*2+4*4))

    def testFuck(self):
        sp1 = sparse_vector({'a':2,'b':4})
        sp1[2] = 4
        print(sp1)
        
if __name__ == '__main__':
    unittest.main()
