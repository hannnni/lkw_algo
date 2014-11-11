#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     28.05.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import os
import string
import random
import csv
import numpy# as np
import scipy
import TrafficModels

global NoOfIntersections, NoOfCycles, NoOfSignalProgramms

NoOfIntersections = 2
NoOfCycles = 3
NoOfSignalProgramms = 4

global path
path = 'C:\Users\ga78bip\Desktop\Johannes\SP'

global NameofIntersection
NameOfIntersections = {0:'56-1',1:'56-02',2:'56-03',3:'55-7'}#only one example

class signalProgramm:
    #genome part
        def __init__(self):
             self.Ix = 0
             self.intersection = []
             self.cycleTime = 0
             self.sgList = []
             self.signalPlans = []
             self.biCode = []
        def getSgList(self, sgListName):
            with open(sgListName, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                #i = 0
                for row in spamreader:
                    rowlist = row[0].split(';')
                    #print 'rowList length', len(rowlist)
                    for i in range(len(rowlist)):
                        self.sgList.append(rowlist[i])
                    #i=i+1
                #print 'sgList: ',self.sgList

        def getSignalplans(self,getSignalplansName):
            with open(getSignalplansName, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                #l = 0
                #for row in spamreader:
                    #l=l+1

                self.signalPlans = [0]*len(self.sgList)
                for l in range(len(self.signalPlans)):
                    self.signalPlans[l] = []

                i = 0
                for row in spamreader:
                    rowlist = row[0].split(';')
                    for j in range(len(rowlist)):
                        self.signalPlans[j].append(int(rowlist[j]))
                    i=i+1
                #print 'signal plans:', self.signalPlans


def genAllPos():
    IndLen = int(round(math.sqrt(NoOfSignalProgramms)))*NoOfCycles*NoOfIntersections
    Ind = []
    Ind = [0]*IndLen
    allP = []
    for j in range(2**IndLen):
        for i in range(len(Ind)):
            if Ind[i]+1 <=1:
                Ind[i] = Ind[i]+1
                allP.append(Ind[:])
                break
            else:
                Ind[i] = Ind[i]-1
                #print i
        #allP[j] = Ind

    #print allP
    return allP

def readSig():
    overallSignalProgramms = [0]*NoOfIntersections

    for i in range(NoOfIntersections):
        signalProgrammForIntersection = [0]*NoOfSignalProgramms
        for j in range(NoOfSignalProgramms):
            #the path should be also include at the beginning
            oderPosition = path + '\intersection' + str(i) + '\SignalProgramm' + str(j)
            fileName_sgList = oderPosition + '\sgList.csv'
            fileName_signalPlans =oderPosition + '\signalPlans.csv'
            #print 'fileName_sgList:'
            #print fileName_sgList
            sp = signalProgramm()
            sp.getSgList(fileName_sgList)
            sp.getSignalplans(fileName_signalPlans)
            sp.Ix = j
            sp.intersection = NameOfIntersections[i]
            #print 'signal plans', sp.signalPlans
            signalProgrammForIntersection[j]= sp
            #print 'signal programm j:', signalProgrammForIntersection[j].signalPlans
            #print 'signal programms No.:', len(signalProgrammForIntersection)
        overallSignalProgramms[i] = signalProgrammForIntersection
    return(overallSignalProgramms)

class genome:
        def __init__(self):

            length = int(math.sqrt(NoOfSignalProgramms))*NoOfIntersections*NoOfCycles
            self.fitness = 0
            self.bits = []
            self.spIxs = []
            self.tobeEvaluatedSps = []

            for i in range(length):
                self.bits.append(random.randint(0, 1))

        def bin2int(self, lists):#convert binaral to int
                 m = 1
                 r = 0
                 lists.reverse()
                 for i in range(len(lists)):
                         r = r + m * lists[i]
                         m = m * 2
                 lists.reverse()
                 return r

        def decode(self,overallSignalProgramms):#translate to signal plans
            #x = self.bin2int(gen)
            #exec(self.expr)
            #return y #here actually calculate the fitness value
            gensection = self.bits
            sectionLength = int(math.sqrt(NoOfSignalProgramms))
            noOfOverallSps = int(len(gensection)/sectionLength)
            spIxs = []
            #print 'gen', gen
            for i in range(noOfOverallSps):
                biSection = gensection[i*2:i*2+sectionLength]
                spIxs.append(self.bin2int(biSection))
            #print 'Signal Plan No. :', spIxs
            self.spIxs = spIxs
            #print'  '
            #print'  '
            # Translation
            #self.tobeEvaluatedSps = [0]*NoOfIntersections
            self.tobeEvaluatedSps = []
            #print 'NoOfIntersections:',NoOfIntersections
            #print 'overallSignalProgramms', len(overallSignalProgramms)
            #print 'overallSignalProgramms[-1]', overallSignalProgramms[3][0].signalPlans
            for i in range(NoOfIntersections):
                spIxsforThisIntersection = \
                spIxs[i*NoOfCycles:i*NoOfCycles+NoOfCycles]
                spForThisIntersection = overallSignalProgramms[i]
                #print 'No of Intersections: ', i
                #print 'spIxsforThisIntersection', spIxsforThisIntersection

                tobeEvaluatedSpsForThisInter = [0]*len(spForThisIntersection[0].sgList)
                for x in range(len(tobeEvaluatedSpsForThisInter)):
                    tobeEvaluatedSpsForThisInter[x] = []
                for j in range(len(spIxsforThisIntersection)):
                    spIx = spIxsforThisIntersection[j]
                    #print 'spIx', spIx
                    sp = spForThisIntersection[spIx]
                    #print 'sp.signalPlans', sp.signalPlans
                    for h in range(len(sp.sgList)):
                        tobeEvaluatedSpsForThisInter[h]= tobeEvaluatedSpsForThisInter[h]+ sp.signalPlans[h]
                    #print 'signal plans ', sp.signalPlans
                #print 'Intersection No.: ', i
                #print 'tobeEvaluatedSpsForThisInter:', tobeEvaluatedSpsForThisInter
                self.tobeEvaluatedSps = self.tobeEvaluatedSps + tobeEvaluatedSpsForThisInter
                #print 'tobeEvaluatedSpsForThisInter:', tobeEvaluatedSpsForThisInter
                #print 'self.tobeEvaluatedSps[i]', self.tobeEvaluatedSps[i]
            #print 'tobeEvaluatedSps: ', self.tobeEvaluatedSps
            #print 'length:', len(self.tobeEvaluatedSps)
            #print 'self.tobeEvaluatedSps[3]', self.tobeEvaluatedSps[3]
            return self.tobeEvaluatedSps#pass to traffic model

        def getFitness(self, overallSignalProgramms,vehcleInputs,HGVInputs):
            #x = self.bin2int(self.bits)
            #print 'x', x
            #exec(expr)
            #self.fitness = y
            #print 'y', y
            weightFactorForWaitingTime = 0
            weightFactorForStops = 1
            self.decode(overallSignalProgramms)
            #print 'call Traffic Models>>'
            (overallWaitingTime, overallStops) = TrafficModels.maintest(self.tobeEvaluatedSps,vehcleInputs,HGVInputs)
            self.fitness = -overallWaitingTime*weightFactorForWaitingTime - weightFactorForStops*overallStops



def mainTest(vehcleInputs,HGVInputs):
    allP = genAllPos()
    overallSignalProgramms = readSig()
    allPNo = [0] * len(allP)
    allFitnessV = [0] * len(allP)
    maxFitness = 0
    bestSig = []
    for i in range(len(allP)):
        gen = genome()
        gen.bits = allP[i]
        gen.decode(overallSignalProgramms)
        allPNo[i] = gen.spIxs[:]

        gen.getFitness(overallSignalProgramms,vehcleInputs,HGVInputs)
        allFitnessV[i] = gen.fitness

    #print allFitnessV
    #print 'all signal plans combination:'
    #print allPNo
    maxFitness = max(allFitnessV)
    bestSig = allPNo[allFitnessV.index(max(allFitnessV))]
    print '--------------------------------------------------------'
    print 'all fitness value:'
    print allFitnessV
    print '--------------------------------------------------------'

    print 'the best Individual is:'
    print bestSig
    print 'the best fitness value is:'
    print maxFitness

if __name__ == '__main__':
    mainTestest(vehcleInputs,HGVInputs)
