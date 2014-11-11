#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     15.09.2014
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

global basicTolerantD

basicTolerantD  =  5

class point:
    def __init__(self):
            self.x = 0
            self.y = 0

    def getPoint(self, x_pos, y_pos):

            self.x = x_pos
            self.y = y_pos



class subLink:
    def __init__(self):
            self.startP = point()
            self.endP = point()
            self.footPoint = point()
            self.onSubLink = False
            self.subLinkLength = 0
            self.relativePosOnSub = 0
            self.tolerantD= 5

    def getStartP(self, x_pos, y_pos):

            self.startP.x = x_pos
            self.startP.y = y_pos

    def getEndP(self, x_pos, y_pos):

            self.endP.x = x_pos
            self.endP.y = y_pos
    def calSubLinkLenth(self):

            self.subLinkLength = math.sqrt((self.startP.x - self.endP.x)*(self.startP.x - self.endP.x)*1.0+(self.startP.y - self.endP.y)*(self.startP.y - self.endP.y)*1.0)

    def deftolerantD(self,linkCapacity):

        self.tolerantD = basicTolerantD + (linkCapacity*3.5/2)
        print 'tolerantD is :',self.tolerantD

    def checkPointOnSub(self, vehPostion_act,vehPostion_pre):
        #vehPostion_pre = startP, vehPostion_act = endP, A ist gradient

         A = 1.0*(self.startP.y - self.endP.y)/(self.startP.x - self.endP.x)
         print 'A:',A
         B = -1*1.0
         C = self.startP.y - A*self.startP.x
         print 'a b c', A,B,C

         distance = math.fabs(A*vehPostion_act.x + B*vehPostion_act.y +C)/math.sqrt(A*A+B*B)
         print 'distance:',distance

         if distance <= self.tolerantD:

            self.onSubLink = True
            print 'vehicle position within tolerant area!'
            if vehPostion_pre !=[]:
                #Gradient of vehicle trajectory
                 AforVeh = (vehPostion_pre.y - vehPostion_act.y)/(vehPostion_pre.x - vehPostion_act.x)

                 if A*AforVeh < 0:#different direction
                    self.onSubLink = False
                    print 'vehicle direction doesnt match link direction!'
                 else:
                    #x = (  B*B*x0  -  A*B*y0  -  A*C  ) / ( A*A + B*B );
                    #y  =  ( -A*B*x0 + A*A*y0 - B*C  ) / ( A*A + B*B );
                    self.footPoint.x = (B*B*vehPostion_act.x - A*B*vehPostion_act.y - A*C)/( A*A + B*B )
                    self.footPoint.y = (-A*B*vehPostion_act.x + A*A*vehPostion_act.y - B*C)/( A*A + B*B )
                    print 'self.footPoint.x,self.footPoint.y',self.footPoint.x,self.footPoint.y
                    distanceToStart = math.sqrt((self.startP.x - self.footPoint.x)*(self.startP.x - self.footPoint.x)+(self.startP.y - self.footPoint.y)*(self.startP.y - self.footPoint.y))
                    distanceToEnd = math.sqrt((self.endP.x - self.footPoint.x)*(self.endP.x - self.footPoint.x)+(self.endP.y - self.footPoint.y)*(self.endP.y - self.footPoint.y))
                    #to make sure the foot point is between start and end point
                    maxDistance = max(distanceToStart,distanceToEnd)
                    print 'maxDistance',maxDistance
                    print 'self.subLinkLength',self.subLinkLength
                    if maxDistance < self.subLinkLength:
                        print 'vehicle direction matches link direction!'
                        self.relativePosOnSub = distanceToStart/self.subLinkLength
                        print 'relavant position on sublink:',self.relativePosOnSub
                    else:
                        self.onSubLink = False
                        print 'Foot point is out of link range!'



class link():
    #coordinatesForLink[[12,11][12,10][10,11][12,13]]
        def __init__(self,coordinatesForLink):
            self.points = [0]*len(coordinatesForLink)
            self.subLinks = [0]*(len(coordinatesForLink)-1)
            self.onLink = False
            self.onSublinkNo = 0
            self.linkLength = 0
            self.relativePosOnLink = 0
            for i in range(len(self.points)):
                self.points[i] = point()
                #coordinatesForLink[i] two dimention,[12,11]
                self.points[i].getPoint(coordinatesForLink[i][0],coordinatesForLink[i][1])
##                print 'points[i].x:',self.points[i].x
##                print 'points[i].y:',self.points[i].y

        def checkPointOnLink(self,linkCapacity,vehPostion_act,vehPostion_pre):

            for i in range(len(self.subLinks)):
                self.subLinks[i] = subLink()
                self.subLinks[i].startP = self.points[i]
                self.subLinks[i].endP = self.points[i+1]
                print 'startP.x:',self.subLinks[i].startP.x
                print 'startP.y:',self.subLinks[i].startP.y
                self.subLinks[i].calSubLinkLenth()
                self.linkLength = self.linkLength + self.subLinks[i].subLinkLength
            for i in range(len(self.subLinks)):
                self.subLinks[i].deftolerantD(linkCapacity)
                self.subLinks[i].checkPointOnSub(vehPostion_act,vehPostion_pre)
                if self.subLinks[i].onSubLink == True:
                    self.onSublinkNo = i
                    tempLength = 0
                    for j in range(i):
                        tempLength = tempLength + self.subLinks[j].subLinkLength
                    tempLength = tempLength + self.subLinks[i].relativePosOnSub *self.subLinks[i].subLinkLength

                    self.relativePosOnLink = tempLength/self.linkLength
                    print 'relavant position on link:',self.relativePosOnLink
                    break


def positionMatching(coordinatesForLink,linkCapacity, vehPostion_act,vehPostion_pre):

    linkToMatch = link(coordinatesForLink)
    linkToMatch.checkPointOnLink(linkCapacity,vehPostion_act,vehPostion_pre)
    return linkToMatch.onLink, linkToMatch.relativePosOnLink

if __name__ == '__main__':
    #only used to test,
    coordinatesForLink = [[-40,0],[0,30],[30,70]]
    linkCapacity = 2
    vehPostion_act = point()
    vehPostion_pre = point()
    vehPostion_act.getPoint(5,30)
    vehPostion_pre.getPoint(-25,18)
    positionMatching(coordinatesForLink,linkCapacity,vehPostion_act,vehPostion_pre)


