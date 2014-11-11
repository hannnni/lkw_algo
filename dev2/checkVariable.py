#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     05.02.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cPickle as pickle
import random
import os

class link:
    a = ''
    b = ''
    c = ''


def check(link):

    link.a = [1,2,3,4,5,5,6]
    link.b = [2]
    link.c = link.a[1:6]
    return link

if __name__ == '__main__':
    testCheck = link()
    check(testCheck)
    ss = [[[1,2],'smart1'],[[2,2],'smart2']]
    try: os.remove("tmp.txt")
    except: pass

    pickle.dump(ss, open("tmp.txt", "w"))



# ? tmp.txt ?????? obj ??
    obj2 = pickle.load(open("tmp.txt", "r"))

    print obj2
    print obj2[1]
    #print 'obj2.a',obj2.a
    for i in range(0):
        print 'jjjjj'
    print testCheck.a
    print 'sum:',sum(testCheck.a)
    print 'max:',max(testCheck.a)
    print 'maxpos:',testCheck.a.index(max(testCheck.a))
    print testCheck.b
    print testCheck.c
####    x = []
####    try:kk = x.index(5)
####    except:kk = -1
####    print 'kk',kk
##    x.append(1)
##    print x
    te = 0.002345
    te = round(te,3)
    print 'te',te

