#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     25.02.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import string
import random
import csv
import numpy# as np
import scipy
import pygame

global filename
#filename = 'networkTest.csv'
filename = 'networkTest2.csv'
"""
Should predefine link Number or should be read from the excle sheet?
"""
global NumberOfLinks
NumberOfLinks = 38#or can be readed from excel tables????, wenn constant , then need to be checked!!!

global simulationCycle, cycleTime, simulationTime
simulationCycle = 3
cycleTime = 60
simulationTime = simulationCycle*cycleTime


class linkInfor:
    def __init__(self):
        self.linkID = []
        self.linkLength = []
        self.linkCapacity = []
        self.isTurning = []
        self.isInLink = []
        self.isOutLink = []
        self.isSignalized = []
        self.mergeFrom = []
        self.divergeTo = []
        self.extraDivergeTo = []
    #just in case that all the variables dont get the initial empty value!!!!!mabe not needed
    def init_Link(self):
        self.linkID = []
        self.linkLength = []
        self.linkCapacity = []
        self.isTurning = []
        self.isInLink = []
        self.isOutLink = []
        self.isSignalized = []
        self.mergeFrom = []
        self.divergeTo = []
        self.extraDivergeTo = []

class CellTransmissionModel:
    def __init__(self):
            self.linkIDs = []
            self.linkCapacitys = []
            self.linkMaxFlows = []
            self.currentStatuses = []
            self.previousStatuses = []
            self.currentFlows = []
            self.previousFlows = []
            #maybe not need if a list of sublist is used
            #self.linkIndexForStatus = []
            #self.linkIndexForFlow = []
#ID Index:
            self.mergeFromIds = []
            self.divergeToIds = []
            self.extraDivergeToIds =[]
            self.mergeFromIdsList = []
            self.divergeToIdsList = []
            self.extraDivergeToIdsList =[]
#IX Index:
            self.mergeFromIxs = []
            self.divergeToIxs = []
            self.extraDivergeToIxs =[]
            self.mergeFromIxsList = []
            self.divergeToIxsList = []
            self.extraDivergeToIxsList =[]

            self.isTurning = []
            self.isInLink = []
            self.isOutLink = []
            self.isSignalized = []

            self.turningRatiosDiverge = []
            self.turningRatiosExtraDiverge = []

            self.networkLinks =[]
    def readNetwork(self, excelFile):
            with open(filename, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                self.networkLinks = range(NumberOfLinks)
                for Ix in range(NumberOfLinks):
                    self.networkLinks[Ix] = linkInfor()

                i = 0
                for row in spamreader:
                    rowlist = row[0].split(';')

                    self.networkLinks[i].init_Link()
                    self.networkLinks[i].linkID = int(rowlist[0])
                    #print self.networkLinks[i].linkID
                    self.networkLinks[i].linkLength = int(rowlist[1])
                    #print self.networkLinks[i].linkLength
                    self.networkLinks[i].linkCapacity = int(rowlist[2])
                    print 'No.of Link ' ,i
                    print self.networkLinks[i].linkCapacity
                    self.networkLinks[i].isTurning = int(rowlist[3])
                    #print self.networkLinks[i].isTurning
                    self.networkLinks[i].isInLink = int(rowlist[4])
                    #print self.networkLinks[i].isInLink
                    self.networkLinks[i].isOutLink = int(rowlist[5])
                    #print self.networkLinks[i].isOutLink
                    self.networkLinks[i].isSignalized = int(rowlist[6])
                    #print self.networkLinks[i].isSignalized
                    mergeFromList = rowlist[7].split('|')
                    #print mergeFromList
                    self.networkLinks[i].mergeFrom = []
                    #print len(mergeFromList)
                    if mergeFromList[0]!= '':
                        for mergeLink in mergeFromList:
                            self.networkLinks[i].mergeFrom.append(int(mergeLink))
                    #print self.networkLinks[i].mergeFrom

                    divergeToList = rowlist[8].split('|')
                    self.networkLinks[i].divergeTo=[]
                    if divergeToList[0]!= '':
                        for divergeLink in divergeToList:
                            self.networkLinks[i].divergeTo.append(int(divergeLink))
                    #print self.networkLinks[i].divergeTo

                    extraDivergeToList = rowlist[9].split('|')
                    self.networkLinks[i].extraDivergeTo = []
                    if extraDivergeToList[0]!= '':
                        for exstraDivergeLink in extraDivergeToList:
                            self.networkLinks[i].extraDivergeTo.append(int(exstraDivergeLink))
                    #print self.networkLinks[i].extraDivergeTo
                    #
                    i = i+1
                print 'the No. of the link ',i
            #return self.networkLinks # x, y = return(a, b), return more than 1 values


    def buildCTM(self):
        #print '_____________________________________________________________________________'
        networkForCTM = self.networkLinks
        #i = 0
        for networkLink in networkForCTM:
            self.linkIDs.append(networkLink.linkID)
            #print i
            #i = i +1
            #print networkLink.linkCapacity
            self.linkCapacitys.append((networkLink.linkCapacity)*1.6)
            self.linkMaxFlows.append((networkLink.linkCapacity)*0.5)
            self.isTurning.append(networkLink.isTurning)
            self.isInLink.append(networkLink.isInLink)
            self.isOutLink.append(networkLink.isOutLink)
            self.isSignalized.append(networkLink.isSignalized)
            if networkLink.linkID >= 500:
                travelSpeed = 5 #speed at turning links
            else:
                travelSpeed = 12.5 # speed at normal links
            travelTime = round(networkLink.linkLength/travelSpeed)
            cellNumber = int(travelTime + 2) #include 2 vitual cells
            #self.linkIndexForStatus.append(overallLengthStatus)
            #overallLengthStatus = cellNumber + overallLengthStatus
            currentLinkStatus = []
            for cell in range(0,cellNumber):
                currentLinkStatus.append(0.0)
            self.currentStatuses.append(currentLinkStatus)

            #self.linkIndexForFlow.append(overallLengthFlow)
            #overallLengthFlow = cellNumber + overallLengthFlow - 1
            currentLinkFlow = []
            for FlowNumber in range(0,cellNumber-1):
                currentLinkFlow.append(0.0)
            self.currentFlows.append(currentLinkFlow)

            #need Ixs instead of  IDs
            if len(networkLink.mergeFrom) != 0:
                self.mergeFromIds.append(networkLink.linkID)
                self.mergeFromIdsList.append(networkLink.mergeFrom)
            if len(networkLink.divergeTo) != 0:
                self.divergeToIds.append(networkLink.linkID)
                self.divergeToIdsList.append(networkLink.divergeTo)
                #temporary calculation of turning ratia, should be readed from the file
                turningRatioDiverge = []
                NumberOfDivergeLinks = len(networkLink.divergeTo)
                turningRatioDiverge = [1/float(NumberOfDivergeLinks) for linksnumber in range(NumberOfDivergeLinks)]
                self.turningRatiosDiverge.append(turningRatioDiverge)

            if len(networkLink.extraDivergeTo) != 0:
                self.extraDivergeToIds.append(networkLink.linkID)
                self.extraDivergeToIdsList.append(networkLink.extraDivergeTo)
                #temporary calculation of turning ratia, should be readed from the file
                turningRatioExtraDiverge = []
                NumberOfExtraDivergeLinks = len(networkLink.extraDivergeTo)
                turningRatioExtraDiverge = [1/float(NumberOfExtraDivergeLinks) for linksnumber in range(NumberOfExtraDivergeLinks)]
                self.turningRatiosExtraDiverge.append(turningRatioExtraDiverge)

#convert link id to link ix in oder to find links easily!!!!
        for ml in range(len(self.mergeFromIds)):
            linkIx = self.linkIDs.index(self.mergeFromIds[ml])
            self.mergeFromIxs.append(linkIx)

            MIdsTemp = self.mergeFromIdsList[ml]
            MIxTemp = [0]*len(self.mergeFromIdsList[ml])
            for mln in range(len(MIxTemp)):
                MIxTemp[mln] = self.linkIDs.index(MIdsTemp[mln])
            self.mergeFromIxsList.append(MIxTemp)

        for dl in range(len(self.divergeToIds)):
            linkIx = self.linkIDs.index(self.divergeToIds[dl])
            self.divergeToIxs.append(linkIx)

            DIdsTemp = self.divergeToIdsList[dl]
            DIxTemp = [0]*len(self.divergeToIdsList[dl])
            for dln in range(len(DIxTemp)):
                DIxTemp[dln] = self.linkIDs.index(DIdsTemp[dln])
            self.divergeToIxsList.append(DIxTemp)

        for el in range(len(self.extraDivergeToIds)):
            linkIx = self.linkIDs.index(self.extraDivergeToIds[el])
            self.extraDivergeToIxs.append(linkIx)

            EIdsTemp = self.extraDivergeToIdsList[el]
            EIxTemp = [0]*len(self.extraDivergeToIdsList[el])
            for eln in range(len(EIxTemp)):
                EIxTemp[eln] = self.linkIDs.index(EIdsTemp[eln])
            self.extraDivergeToIxsList.append(EIxTemp)

#the first link is extra link, need to check the network.......!!!!
        #print '_____________________________________________________________________________'
        #print 'Merge Ixs:'
        #print self.mergeFromIxs
        #print 'Diverge Ixs:'
        #print self.divergeToIxs
        #print 'Extradiverge Ixs:'
        #print self.extraDivergeToIxs
        #print 'Merge IxsList:'
        #print self.mergeFromIxsList
        #print 'Diverge IxsList:'
        #print self.divergeToIxsList
        #print 'turning ratios for diverge links'
        #print self.turningRatiosDiverge
        #print 'Extradiverge IxsList:'
        #print self.extraDivergeToIxsList
        #print 'turning ratios for extra diverge links'
        #print self.turningRatiosExtraDiverge


    def flowModel(self):
        #new empty list for currenflow and status, think about it, which model will be calculated at the very beginning , initialize should be there
        currentStatuses = [0]*len(self.currentStatuses)
        currentFlows = [0]*len(self.currentFlows)
        for nl in range(len(self.currentStatuses)):
            currentStatuses[nl] = [0.0]*len(self.currentStatuses[nl])
            currentFlows[nl] = [0.0]*len(self.currentFlows[nl])

        previousStatuses = self.currentStatuses
        previousFlows = self.currentFlows
        linkCapacitys = self.linkCapacitys
        linkMaxFlows = self.linkMaxFlows
        #linkIndexForStatus = self.linkIndexForStatus
        #linkIndexForFlow = self.linkIndexForFlow
    #check the linkIndexForStatus ?= linkIndexForFlow

        for l in range(len(self.currentStatuses)):
            capacity = linkCapacitys[l]
            maxFlow = linkMaxFlows[l]
            previousStatus = previousStatuses[l]
            previousFlow = previousFlows[l]
            #startPositionForStatus = linkIndexForStatus[l]
            #endPositionForStatus = linkIndexForStatus[l+1]-1
            cellNumber = len(currentStatuses[l])
    #calculate flows
            for c in range(cellNumber-1):
                if previousStatus[c]>maxFlow:
                    sigma = 0.45 # proprotion between backwavespeed and freeflow speed
                else:
                    sigma = 1.0
    ##            print currentFlows
    ##            print linkIndexForFlow[l]+c
                currentFlows[l][c] = \
                min(previousStatus[c], maxFlow, \
                sigma*(capacity-previousStatus[c+1]))
    #update
            for c2 in range(1,cellNumber-1):
                currentStatuses[l][c2] = \
                previousStatus[c2] + \
                currentFlows[l][c2-1] - currentFlows[l][c2]

        self.currentStatuses = currentStatuses
        self.currentFlows = currentFlows

        self.previousFlows = previousFlows
        self.previousStatuses = previousStatuses
        #print ' Status after flow model are:'
        #print self.currentStatuses
        #print self.currentFlows
#________________________________________________________________________________

    def initFlow(self):
        for i in range(len(self.isInLink)):
            if self.isInLink[i] == 1:
                self.currentStatuses[i][1] = 0.1 # assume evrery inlink get 0.1 flow every second
                #need to be assigned according to the detector data for all the inlinks
#________________________________________________________________________________

    def mergeModel(self):
        currentStatuses = self.currentStatuses
        #currentFlow = self.currentFlow
        previousStatuses = self.previousStatuses
        #previousFlow = self.previousFlow
        linkCapacitys = self.linkCapacitys
        linkMaxFlows = self.linkMaxFlows
        #linkIndexForStatus = self.linkIndexForStatus
        #linkIndexForFlow = self.linkIndexForFlow
        linkIDs = self.linkIDs

        mergeFromIxs = self.mergeFromIxs
        #print 'merge from links: ',mergeFromIxs
        mergeFromIxsList = self.mergeFromIxsList
        #print 'merge from linkslist: ',mergeFromIxsList


        for ml in range(len(mergeFromIxs)):

            mergeToLinkIx = mergeFromIxs[ml]

            CapacityForMergeTo = linkCapacitys[mergeToLinkIx]
            toBeDistributedLinks = mergeFromIxsList[ml][:]
            receivingCapacity = CapacityForMergeTo - previousStatuses[mergeToLinkIx][1]
            receivingMaxflow = linkMaxFlows[mergeToLinkIx]
            restOfReceivingCapacity = max(receivingCapacity,receivingMaxflow)

            for step in range(len(mergeFromIxsList)-1):
    #Step 1 : calculation of weighting factors for tobedistributed links
                weightFactors = []
                totalCapacity = 0.0 #float take care 0.0, not 0
                for tbl in range(len(toBeDistributedLinks)):
                    #print 'toBeDistributedLinks is:'
                    #print toBeDistributedLinks
                    toBeDistributedLinkIx = toBeDistributedLinks[tbl]
                    totalCapacity = totalCapacity + linkCapacitys[toBeDistributedLinkIx]
                for tbl in range(len(toBeDistributedLinks)):
                    toBeDistributedLinkIx = toBeDistributedLinks[tbl]
                    weightFactors.append(linkCapacitys[toBeDistributedLinkIx]/totalCapacity)
                #print 'weightfactors: ', weightFactors

    #step 2  actually previousToBeDistributedLinks and toBeDistributedLinks are the same, one changes another also!!!!!
    #have to use [:], then only get the value of it

                previousNoLinks = len(toBeDistributedLinks)
                toStayLinks = []

                for tbl in range(previousNoLinks):
                    #print 'tbl', tbl
                    #print 'length of toBeDistributedLinks', toBeDistributedLinks
                    toBeDistributedLinkIx = toBeDistributedLinks[tbl]
                    toBeDistributedVolume = restOfReceivingCapacity * weightFactors[tbl]
                    #get value from the last second cell
                    toBesendVolume = previousStatuses[toBeDistributedLinkIx][-2]

                    #print 'to be send value: ',toBesendVolume

                    if toBeDistributedVolume >= toBesendVolume:
                        currentStatuses[toBeDistributedLinkIx][-1] = \
                        linkCapacitys[toBeDistributedLinkIx] - toBesendVolume
                        restOfReceivingCapacity = restOfReceivingCapacity - toBesendVolume
                        #del toBeDistributedLinks[tbl]
                        #toBedelLinks.append(toBeDistributedLinks[tbl])
                        #currentNoLinks = len(toBeDistributedLinks)
                        #print 'build virual cell for merge from links:', currentStatuses[toBeDistributedLinkIx][-1]
                    else:
                        toStayLinks.append(toBeDistributedLinks[tbl])


                toBeDistributedLinks = toStayLinks
                currentNoLinks = len(toBeDistributedLinks)


                if currentNoLinks == previousNoLinks:
                    for tbl in range(len(toBeDistributedLinks)):
                        toBeDistributedLinkIx = toBeDistributedLinks[tbl]
                        toBeDistributedVolume = restOfReceivingCapacity * weightFactors[tbl]
                        currentStatuses[toBeDistributedLinkIx][-1] = \
                        linkCapacitys[toBeDistributedLinkIx] -toBeDistributedVolume

                    currentStatuses[mergeToLinkIx][0] = CapacityForMergeTo - previousStatuses[mergeToLinkIx][1]
                    break


    #step 3
    #current, previous........take care
    #decide the receiving value,
                if toBeDistributedLinks ==[]:
                    for tbl in range(len(mergeFromIxsList[ml])):# this is already changed.....!!!!!
                        toBeDistributedLinkIx = mergeFromIxsList[ml][tbl]
                        currentStatuses[mergeToLinkIx][0]  = currentStatuses[mergeToLinkIx][0]  + \
                        previousStatuses[toBeDistributedLinkIx][-2]
                        #print 'Merge linkIx:', mergeFromIxs[ml]
                        #print 'currentStatuses[ml][0] a ', currentStatuses[mergeToLinkIx][0]
                    break
                else:
                    currentStatuses[mergeToLinkIx][0]  = max(CapacityForMergeTo - previousStatuses[mergeToLinkIx][1], receivingMaxflow)
                    #print 'currentStatuses[ml][0] b ', currentStatuses[mergeToLinkIx][0]

        self.currentStatuses = currentStatuses
##        print '______________________________________________check______________'
##        print mergeFromIxs[0]
##        print mergeFromIxsList[0][0]
##        print self.currentStatuses[mergeFromIxs[0]]
##        print self.currentStatuses[mergeFromIxsList[0][0]]


    def divergeModel(self):
        currentStatuses = self.currentStatuses
        #currentFlow = self.currentFlow
        previousStatuses = self.previousStatuses
        linkMaxFlows = self.linkMaxFlows
        #previousFlow = self.previousFlow
        linkCapacitys = self.linkCapacitys# still Number of Lanes
        #linkIndexForStatus = self.linkIndexForStatus
        #linkIndexForFlow = self.linkIndexForFlow
        linkIDs = self.linkIDs
##
##            self.mergeFromIxs = []
##            self.divergeToIxs = []
##            self.extraDivergeToIxs =[]
##            self.mergeFromIxsList = []
##            self.divergeToIxsList = []
##            self.extraDivergeToIxsList =[]

        divergeToIxs = self.divergeToIxs
        divergeToIxsList = self.divergeToIxsList

        turningRatiosList = self.turningRatiosDiverge


        for dl in range(len(divergeToIxs)):

            divergeFromLinkIx = divergeToIxs[dl]
            CapacityOfDivergeFrom = linkCapacitys[divergeFromLinkIx]
            MaximalFlowofDivergeFrom = linkMaxFlows[divergeFromLinkIx]
            turningRatios = turningRatiosList[dl]
            #print 'check point ______________'
            #print 'divergeFromLinkIx', divergeFromLinkIx
            #print 'turningRatios', turningRatios

            toBeDistributedLinks = divergeToIxsList[dl]
            #print 'toBeDistributedLinks', toBeDistributedLinks
            restrictedSendingByOutgoings = MaximalFlowofDivergeFrom
    #define the sending ability,
            for ogl in range(len(toBeDistributedLinks)):

                divergeToLinkIx = toBeDistributedLinks[ogl]
                CapacityOfDivergeTo = linkCapacitys[divergeToLinkIx]
                MaximalFlowofDivergeTo = linkMaxFlows[divergeToLinkIx]
##                print 'check point ______________'
##                print 'length of tobe diverged links', len(toBeDistributedLinks)
##                print divergeToLinkIx
##                print 'previousStatuses[divergeToLinkIx]'
##                print previousStatuses[divergeToLinkIx]
##                print 'turningRatios'
##                print turningRatios
##                print 'ogl'
##                print ogl

                restrictedSendingByOutgoings = restrictedSendingByOutgoings - \
                max(MaximalFlowofDivergeTo - \
                (CapacityOfDivergeTo - previousStatuses[divergeToLinkIx][1])/turningRatios[ogl], 0)
    #build the virtual cell for incoming / diverge from links

            overallsendingAbility = min(previousStatuses[divergeFromLinkIx][-2], max(restrictedSendingByOutgoings,0))
            currentStatuses[divergeFromLinkIx][-1] = CapacityOfDivergeFrom - overallsendingAbility

    #build the virtual cell for outgoing / diverge to links
            for ogl in range(len(toBeDistributedLinks)):

                divergeToLinkIx = toBeDistributedLinks[ogl]
                CapacityOfDivergeTo = linkCapacitys[divergeToLinkIx]
                MaximalFlowofDivergeTo = linkMaxFlows[divergeToLinkIx]

                currentStatuses[divergeToLinkIx][0] = \
                min(turningRatios[ogl]*overallsendingAbility,\
                 MaximalFlowofDivergeTo, \
                 CapacityOfDivergeTo - previousStatuses[divergeToLinkIx][1])

        self.currentStatuses = currentStatuses


    def ExtraDivergeModel(self):
        currentStatuses = self.currentStatuses
        #currentFlow = self.currentFlow
        previousStatuses = self.previousStatuses
        linkMaxFlows = self.linkMaxFlows
        #previousFlow = self.previousFlow
        linkCapacitys = self.linkCapacitys# still Number of Lanes
        #linkIndexForStatus = self.linkIndexForStatus
        #linkIndexForFlow = self.linkIndexForFlow
        #linkIDs = self.linkIDs
##
##            self.mergeFromIxs = []
##            self.extraDivergeToIxs = []
##            self.extraDivergeToIxs =[]
##            self.mergeFromIxsList = []
##            self.extraDivergeToIxsList = []
##            self.extraDivergeToIxsList =[]

        extraDivergeToIxs = self.extraDivergeToIxs
        extraDivergeToIxsList = self.extraDivergeToIxsList

        turningRatiosList = self.turningRatiosExtraDiverge


        for dl in range(len(extraDivergeToIxs)):

            divergeFromLinkIx = extraDivergeToIxs[dl]
            CapacityOfDivergeFrom = linkCapacitys[divergeFromLinkIx]
            MaximalFlowofDivergeFrom = linkMaxFlows[divergeFromLinkIx]
            turningRatios = turningRatiosList[dl]
            #print 'check point ______________'
            #print 'divergeFromLinkIx', divergeFromLinkIx
            #print 'turningRatios', turningRatios

            toBeDistributedLinks = extraDivergeToIxsList[dl]
            #print 'toBeDistributedLinks', toBeDistributedLinks
            restrictedSendingByOutgoings = MaximalFlowofDivergeFrom
    #define the sending ability,
            for ogl in range(len(toBeDistributedLinks)):

                extraDivergeToLinkIx = toBeDistributedLinks[ogl]
                CapacityOfDivergeTo = linkCapacitys[extraDivergeToLinkIx]
                MaximalFlowofDivergeTo = linkMaxFlows[extraDivergeToLinkIx]
##                print 'check point ______________'
##                print 'length of tobe diverged links', len(toBeDistributedLinks)
##                print extraDivergeToLinkIx
##                print 'previousStatuses[extraDivergeToLinkIx]'
##                print previousStatuses[extraDivergeToLinkIx]
##                print 'turningRatios'
##                print turningRatios
##                print 'ogl'
##                print ogl

                restrictedSendingByOutgoings = restrictedSendingByOutgoings - \
                max(MaximalFlowofDivergeTo - \
                (CapacityOfDivergeTo - previousStatuses[extraDivergeToLinkIx][1])/turningRatios[ogl], 0)
    #build the virtual cell for incoming / diverge from links

            overallsendingAbility = min(previousStatuses[divergeFromLinkIx][-2], max(restrictedSendingByOutgoings,0))
            currentStatuses[divergeFromLinkIx][-1] = CapacityOfDivergeFrom - overallsendingAbility

    #build the virtual cell for outgoing / diverge to links
            for ogl in range(len(toBeDistributedLinks)):

                extraDivergeToLinkIx = toBeDistributedLinks[ogl]
                CapacityOfDivergeTo = linkCapacitys[extraDivergeToLinkIx]
                MaximalFlowofDivergeTo = linkMaxFlows[extraDivergeToLinkIx]

                currentStatuses[extraDivergeToLinkIx][0] = \
                min(turningRatios[ogl]*overallsendingAbility,\
                 MaximalFlowofDivergeTo, \
                 CapacityOfDivergeTo - previousStatuses[extraDivergeToLinkIx][1])


        self.currentStatuses = currentStatuses
        print ' Status after all models are:'
        print self.currentStatuses

def main():
    ctm = CellTransmissionModel()
    ctm.readNetwork(filename)
    ctm.buildCTM()
    for timeStep in range(simulationTime):
        ctm.initFlow()
        ctm.flowModel()
        ctm.mergeModel()
        ctm.divergeModel()
        ctm.ExtraDivergeModel()

if __name__ == '__main__':
         main()