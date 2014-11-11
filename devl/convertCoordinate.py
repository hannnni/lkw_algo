#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     05.09.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import string
import random
import csv
import numpy# as np
import scipy
import math

global semiMajorAxis, firstEccSquar

semiMajorAxis = 6378137
firstEccSquar = 0.00669437999






class point:
    def __init__(self):
        self.geodCoord_la = 0
        self.geodCoord_lo = 0
        self.geodCoord_el = 0
        self.ECEFCoord_x = 0
        self.ECEFCoord_y = 0
        self.ECEFCoord_z = 0
        self.ENuCoord_e = 0
        self.ENuCoord_n = 0
        self.ENuCoord_u = 0

    def getGeodCoord(self,la,lo,el):
        self.geodCoord_la = la
        self.geodCoord_lo = lo
        self.geodCoord_el = el

    def convertGeod2ECEF(self):

        Normal = semiMajorAxis/math.sqrt(1-firstEccSquar*math.sin(self.geodCoord_la)*math.sin(self.geodCoord_la))

        self.ECEFCoord_x = (Normal + self.geodCoord_el)*math.cos(self.geodCoord_la)*math.cos(self.geodCoord_lo)
        self.ECEFCoord_y = (Normal + self.geodCoord_el)*math.cos(self.geodCoord_la)*math.sin(self.geodCoord_lo)
        self.ECEFCoord_z = (Normal*(1-firstEccSquar)+ self.geodCoord_el)*math.sin(self.geodCoord_la)

    def convertECEF2ENU(self,refPoint):

        self.ENuCoord_e = -math.sin(self.geodCoord_lo)*(self.ECEFCoord_x-refPoint.ECEFCoord_x)\
        + math.cos(self.geodCoord_lo)*(self.ECEFCoord_y-refPoint.ECEFCoord_y)

        self.ENuCoord_n = -math.sin(self.geodCoord_la)*math.cos(self.geodCoord_lo)*(self.ECEFCoord_x-refPoint.ECEFCoord_x)\
        + math.sin(self.geodCoord_lo)*math.sin(self.geodCoord_la)*(self.ECEFCoord_y-refPoint.ECEFCoord_y)\
        + math.cos(self.geodCoord_la)*(self.ECEFCoord_z-refPoint.ECEFCoord_z)

        self.ENuCoord_u = math.cos(self.geodCoord_la)*math.cos(self.geodCoord_lo)*(self.ECEFCoord_x-refPoint.ECEFCoord_x)\
        + math.cos(self.geodCoord_lo)*math.sin(self.geodCoord_la)*(self.ECEFCoord_y-refPoint.ECEFCoord_y)\
        + math.sin(self.geodCoord_la)*(self.ECEFCoord_z-refPoint.ECEFCoord_z)







def main():
    r_la = 51.200312
    r_lo = 6.757542
    r_el = 6300137
    refPoint = point()
    refPoint.getGeodCoord(r_la,r_lo,r_el)
    refPoint.convertGeod2ECEF()

    la = 51.200689
    lo = 6.752532
    el = 6300137
    calPoint = point()
    calPoint.getGeodCoord(la,lo,el)
    calPoint.convertGeod2ECEF()
    calPoint.convertECEF2ENU(refPoint)

    print 'calPoint.ENuCoord_e:',calPoint.ENuCoord_e
    print 'calPoint.ENuCoord_n:',calPoint.ENuCoord_n
    print 'calPoint.ENuCoord_u:',calPoint.ENuCoord_u


if __name__ == '__main__':
    main()
