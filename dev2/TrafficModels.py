
import os
import string
import random
import csv
import numpy# as np
import scipy
import pygame
import math

global NetworkFileName
#, signalPlanFileName
#filename = 'networkTest.csv'
NetworkFileName = 'NetworkTestFeld.csv'
#signalPlanFileName = 'temporarySp.csv'
"""
Should predefine link Number or should be read from the excle sheet?
"""
global NumberOfLinks
NumberOfLinks = 158#or can be readed from excel tables????, wenn constant , then need to be checked!!!

global simulationCycle, cycleTime, simulationTime
simulationCycle = 3
cycleTime = 70
simulationTime = simulationCycle*cycleTime
#have to be the same as in test.py, or should all passed from there....


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
    #just in case that all the variables dont get the initial empty value!!!!
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

            self.signalPlans = []

            self.networkLinks =[]
# variable for evaluation:
            self.waitingTime = 0
            self.overallWaitingTime = 0

    def readNetwork(self):
            with open(NetworkFileName, 'rb') as csvfile:
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
                    #print 'No.of Link ' ,i
                    #print self.networkLinks[i].linkCapacity
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
                    #print 'self.networkLinks[i].divergeTo',self.networkLinks[i].divergeTo

                    extraDivergeToList = rowlist[9].split('|')
                    self.networkLinks[i].extraDivergeTo = []
                    if extraDivergeToList[0]!= '':
                        for exstraDivergeLink in extraDivergeToList:
                            self.networkLinks[i].extraDivergeTo.append(int(exstraDivergeLink))
                    #print self.networkLinks[i].extraDivergeTo
                    #
                    i = i+1
                #print 'the No. of the link ',i
            #return self.networkLinks # x, y = return(a, b), return more than 1 values

#   temparary fix time plan, should be get this from GA
    def readSignalPlans(self):
        with open(signalPlanFileName, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                self.signalPlans = [0]*len(self.extraDivergeToIds)
                for l in range(len(self.signalPlans)):
                    self.signalPlans[l] = []

                i = 0
                for row in spamreader:
                    rowlist = row[0].split(';')
                    for j in range(len(rowlist)):
                        self.signalPlans[j].append(int(rowlist[j]))
                    i=i+1
                #print 'self.signalPlans', self.signalPlans

    def buildCTM(self):
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

        self.previousStatuses = self.currentStatuses
        self.previousFlows = self.currentFlows
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
        #print 'self.divergeToIxsList:', self.divergeToIxsList

        for el in range(len(self.extraDivergeToIds)):
            linkIx = self.linkIDs.index(self.extraDivergeToIds[el])
            self.extraDivergeToIxs.append(linkIx)

            EIdsTemp = self.extraDivergeToIdsList[el]
            EIxTemp = [0]*len(self.extraDivergeToIdsList[el])
            for eln in range(len(EIxTemp)):
                EIxTemp[eln] = self.linkIDs.index(EIdsTemp[eln])
            self.extraDivergeToIxsList.append(EIxTemp)

    def initFlow(self,vehcleInputs):
        j = 0
        #print 'vehcleInputs',vehcleInputs

        for i in range(len(self.isInLink)):
            if self.isInLink[i] == 1:
                self.previousStatuses[i][1] = round(float(vehcleInputs[j])/float(cycleTime),3)
                #print 'self.previousStatuses[1][1] during',self.previousStatuses[1][1]
                j = j+1
        #print 'vehcleInputs[1]',vehcleInputs[1]
        #print 'initFlow self.previousStatuses[5]',self.previousStatuses[5]
                 # assume evrery inlink get 0.1 flow every second
                #need to be assigned according to the detector data for all the inlinks
    def initFlow_0(self,vehcleInputs):
        j = 0
        for i in range(len(self.isInLink)):
            if self.isInLink[i] == 1:
                #print 'vehcleInputs[j]',vehcleInputs[j]
                for k in range(1,len(self.previousStatuses[i])-1):
                    self.previousStatuses[i][k] = round(float(vehcleInputs[j])/float(cycleTime),3)
                #print 'self.currentStatuses[i][1]',self.currentStatuses[i][1]
                j = j+1
                 # assume evrery inlink get 0.1 flow every second
                #need to be assigned according to the detector data for all the inlinks

    def flowModel(self):
        #new empty list for currenflow and status, think about it, which model will be calculated at the very beginning , initialize should be there
        currentStatuses = [0]*len(self.currentStatuses)
        currentFlows = [0]*len(self.currentFlows)
        for nl in range(len(self.currentStatuses)):
            currentStatuses[nl] = [0.0]*len(self.currentStatuses[nl])
            currentFlows[nl] = [0.0]*len(self.currentFlows[nl])

        previousStatuses = self.previousStatuses[:]
        previousFlows = self.previousFlows[:]
        self.previousFlows = self.currentFlows[:]
        self.previousStatuses = self.currentStatuses[:]
        linkCapacitys = self.linkCapacitys
        linkMaxFlows = self.linkMaxFlows
    #check the linkIndexForStatus ?= linkIndexForFlow

        for l in range(len(self.currentStatuses)):
            capacity = linkCapacitys[l]
            maxFlow = linkMaxFlows[l]
            previousStatus = previousStatuses[l]
            previousFlow = previousFlows[l]
            cellNumber = len(currentStatuses[l])
    #calculate flows
            for c in range(cellNumber-1):
                if previousStatus[c]>maxFlow:
                    sigma = 0.45 # proprotion between backwavespeed and freeflow speed
                else:
                    sigma = 1.0
                currentFlows[l][c] = \
                round(min(previousStatus[c], maxFlow, \
                sigma*(capacity-previousStatus[c+1])),3)
    #update
            for c2 in range(1,cellNumber-1):
                currentStatuses[l][c2] = \
                round(previousStatus[c2] + \
                currentFlows[l][c2-1] - currentFlows[l][c2],3)

        self.currentStatuses = currentStatuses
        self.currentFlows = currentFlows


    def waitingTimeEvaluation(self):
        currentFlows = self.currentFlows
        priviousStatuses = self.previousStatuses
        self.waitingTime = 0
        for i in range(len(currentFlows)):
            currentFlow = currentFlows[i]
            priviousStatus = priviousStatuses[i]
            for j in range(len(currentFlow)):
                self.waitingTime = self.waitingTime + abs(priviousStatus[j]-currentFlow[j])
        self.overallWaitingTime = self.overallWaitingTime + self.waitingTime
        #print 'Waiting time:',self.waitingTime

    def mergeModel(self):
        #currentStatuses = self.currentStatuses
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
                        previousStatuses[toBeDistributedLinkIx][-1] = \
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
                        previousStatuses[toBeDistributedLinkIx][-1] = \
                        linkCapacitys[toBeDistributedLinkIx] -toBeDistributedVolume

                    previousStatuses[mergeToLinkIx][0] = CapacityForMergeTo - previousStatuses[mergeToLinkIx][1]
                    break

    #step 3
    #current, previous........take care
    #decide the receiving value,
                if toBeDistributedLinks ==[]:
                    for tbl in range(len(mergeFromIxsList[ml])):# this is already changed.....!!!!!
                        toBeDistributedLinkIx = mergeFromIxsList[ml][tbl]
                        previousStatuses[mergeToLinkIx][0]  = previousStatuses[mergeToLinkIx][0]  + \
                        previousStatuses[toBeDistributedLinkIx][-2]
                        #print 'Merge linkIx:', mergeFromIxs[ml]
                        #print 'currentStatuses[ml][0] a ', currentStatuses[mergeToLinkIx][0]
                    break
                else:
                    previousStatuses[mergeToLinkIx][0]  = min(CapacityForMergeTo - previousStatuses[mergeToLinkIx][1], receivingMaxflow)
                    #print 'currentStatuses[ml][0] b ', currentStatuses[mergeToLinkIx][0]

        self.previousStatuses = previousStatuses
        #print 'Mergemodel ctm pre sta 4',self.previousStatuses[4]

    def divergeModel(self):
        previousStatuses = self.previousStatuses
        linkMaxFlows = self.linkMaxFlows
        linkCapacitys = self.linkCapacitys# still Number of Lanes
        linkIDs = self.linkIDs
        divergeToIxs = self.divergeToIxs
        divergeToIxsList = self.divergeToIxsList
        turningRatiosList = self.turningRatiosDiverge

        for dl in range(len(divergeToIxs)):

            divergeFromLinkIx = divergeToIxs[dl]
            CapacityOfDivergeFrom = linkCapacitys[divergeFromLinkIx]
            MaximalFlowofDivergeFrom = linkMaxFlows[divergeFromLinkIx]
            turningRatios = turningRatiosList[dl]

            toBeDistributedLinks = divergeToIxsList[dl]
            restrictedSendingByOutgoings = MaximalFlowofDivergeFrom
    #define the sending ability,
            for ogl in range(len(toBeDistributedLinks)):

                divergeToLinkIx = toBeDistributedLinks[ogl]
                CapacityOfDivergeTo = linkCapacitys[divergeToLinkIx]
                MaximalFlowofDivergeTo = linkMaxFlows[divergeToLinkIx]
                restrictedSendingByOutgoings = restrictedSendingByOutgoings - \
                max(MaximalFlowofDivergeTo - \
                (CapacityOfDivergeTo - previousStatuses[divergeToLinkIx][1])/turningRatios[ogl], 0)
    #build the virtual cell for incoming / diverge from links

            overallsendingAbility = min(previousStatuses[divergeFromLinkIx][-2], max(restrictedSendingByOutgoings,0))
            previousStatuses[divergeFromLinkIx][-1] = CapacityOfDivergeFrom - overallsendingAbility

    #build the virtual cell for outgoing / diverge to links
            for ogl in range(len(toBeDistributedLinks)):

                divergeToLinkIx = toBeDistributedLinks[ogl]
                CapacityOfDivergeTo = linkCapacitys[divergeToLinkIx]
                MaximalFlowofDivergeTo = linkMaxFlows[divergeToLinkIx]

                previousStatuses[divergeToLinkIx][0] = \
                min(turningRatios[ogl]*overallsendingAbility,\
                 MaximalFlowofDivergeTo, \
                 CapacityOfDivergeTo - previousStatuses[divergeToLinkIx][1])
        self.previousStatuses = previousStatuses

    def ExtraDivergeModel(self, timeStep):

        previousStatuses = self.previousStatuses
        linkMaxFlows = self.linkMaxFlows
        linkCapacitys = self.linkCapacitys# still Number of Lanes

        extraDivergeToIxs = self.extraDivergeToIxs
        extraDivergeToIxsList = self.extraDivergeToIxsList
        turningRatiosList = self.turningRatiosExtraDiverge
        signalPlans = self.signalPlans
        timeStepInCycle = timeStep

        for dl in range(len(extraDivergeToIxs)):

            divergeFromLinkIx = extraDivergeToIxs[dl]
            CapacityOfDivergeFrom = linkCapacitys[divergeFromLinkIx]
            MaximalFlowofDivergeFrom = linkMaxFlows[divergeFromLinkIx]
            turningRatios = turningRatiosList[dl]

            toBeDistributedLinks = extraDivergeToIxsList[dl]
            restrictedSendingByOutgoings = MaximalFlowofDivergeFrom


            if signalPlans[dl][timeStepInCycle] == 0:
                previousStatuses[divergeFromLinkIx][-1] = CapacityOfDivergeFrom
                for ogl in range(len(toBeDistributedLinks)):
                    extraDivergeToLinkIx = toBeDistributedLinks[ogl]
                    previousStatuses[extraDivergeToLinkIx][0] = 0
            else:
                #define the sending ability,
                for ogl in range(len(toBeDistributedLinks)):

                    extraDivergeToLinkIx = toBeDistributedLinks[ogl]
                    CapacityOfDivergeTo = linkCapacitys[extraDivergeToLinkIx]
                    MaximalFlowofDivergeTo = linkMaxFlows[extraDivergeToLinkIx]

                    restrictedSendingByOutgoings = restrictedSendingByOutgoings - \
                    max(MaximalFlowofDivergeTo - \
                    (CapacityOfDivergeTo - previousStatuses[extraDivergeToLinkIx][1])/turningRatios[ogl], 0)
                #build the virtual cell for incoming / diverge from links
                overallsendingAbility = min(previousStatuses[divergeFromLinkIx][-2], max(restrictedSendingByOutgoings,0))
                previousStatuses[divergeFromLinkIx][-1] = CapacityOfDivergeFrom - overallsendingAbility

                #build the virtual cell for outgoing / diverge to links
                for ogl in range(len(toBeDistributedLinks)):

                    extraDivergeToLinkIx = toBeDistributedLinks[ogl]
                    CapacityOfDivergeTo = linkCapacitys[extraDivergeToLinkIx]
                    MaximalFlowofDivergeTo = linkMaxFlows[extraDivergeToLinkIx]

                    previousStatuses[extraDivergeToLinkIx][0] = \
                    min(turningRatios[ogl]*overallsendingAbility,\
                     MaximalFlowofDivergeTo, \
                     CapacityOfDivergeTo - previousStatuses[extraDivergeToLinkIx][1])
        self.previousStatuses = previousStatuses


class CNSMixModel:
    def __init__(self, ctm):
            self.linkIDs = ctm.linkIDs
            self.linkCapacitys = ctm.linkCapacitys
            self.linkMaxFlows = ctm.linkMaxFlows

            self.SpeedsList = []
            #self.CTM_currentStatuses = ctm.currentStatuses
            self.CTM_previousStatuses = ctm.previousStatuses
            self.CTM_currentFlows = ctm.currentFlows
            #self.currentStatuses = []
            self.previousStatuses = []
            #self.currentFlows = []
            self.previousFlows = []
            self.SpeedsList = [0]*len(self.CTM_previousStatuses)
            self.currentStatuses = [0]*len(self.CTM_previousStatuses)
            #print 'currentStatuses length', len(self.currentStatuses)
            self.currentFlows = [0]*len(self.CTM_currentFlows)
            for nl in range(len(self.currentStatuses)):
                self.SpeedsList[nl] = [0]*len(self.CTM_previousStatuses[nl])
                self.currentStatuses[nl] = [0]*len(self.CTM_previousStatuses[nl])
                self.currentFlows[nl] = [0]*len(self.CTM_currentFlows[nl])
#ID Index:
            self.mergeFromIds = ctm.mergeFromIds
            self.divergeToIds = ctm.divergeToIds
            self.extraDivergeToIds = ctm.extraDivergeToIds
            self.mergeFromIdsList = ctm.mergeFromIdsList
            self.divergeToIdsList = ctm.divergeToIdsList
            self.extraDivergeToIdsList = ctm.extraDivergeToIdsList
#IX Index:
            self.mergeFromIxs = ctm.mergeFromIxs
            self.divergeToIxs = ctm.divergeToIxs
            self.extraDivergeToIxs = ctm.extraDivergeToIxs
            self.mergeFromIxsList = ctm.mergeFromIxsList
            self.divergeToIxsList = ctm.divergeToIxsList
            self.extraDivergeToIxsList = ctm.extraDivergeToIxsList

            self.isTurning = ctm.isTurning
            self.isInLink = ctm.isInLink
            self.isOutLink = ctm.isOutLink
            self.isSignalized = ctm.isSignalized

            self.turningRatiosDiverge = ctm.turningRatiosDiverge
            self.turningRatiosExtraDiverge = ctm.turningRatiosExtraDiverge
#variable for evaluation:
            self.stops = 0
            self.overallStops = 0

    def SpeedDiriving(self,ctm,timeStep):
        # to decide if HGV can move forward:
        # and initialize the statues and flows
        self.CTM_previousStatuses = ctm.previousStatuses
        self.CTM_currentFlows = ctm.currentFlows
        self.previousStatuses = self.currentStatuses[:]
        self.previousFlows = self.currentFlows[:]
        self.SpeedsList = [0]*len(self.CTM_previousStatuses)
        self.currentStatuses = [0]*len(self.CTM_previousStatuses)
        self.currentFlows = [0]*len(self.CTM_currentFlows)


        for nl in range(len(self.currentStatuses)):
            self.SpeedsList[nl] = [0]*len(self.CTM_previousStatuses[nl])
            self.currentStatuses[nl] = [0]*len(self.CTM_previousStatuses[nl])
            self.currentFlows[nl] = [0]*len(self.CTM_currentFlows[nl])
        for nl in range(len(self.SpeedsList)):

            CTM_currentFlow = self.CTM_currentFlows[nl]
            CTM_previousStatus = self.CTM_previousStatuses[nl]

            maxFlow = self.linkMaxFlows[nl]

            for nc in range(1,len(self.SpeedsList[nl])):
                if CTM_currentFlow[nc-1] >= CTM_previousStatus[nc-1]*0.95 or math.fabs(CTM_currentFlow[nc-1]- maxFlow)<0.05:
                    self.SpeedsList[nl][nc] = 1

                else:
                    self.SpeedsList[nl][nc] = 0
        extraDivergeToIxs = ctm.extraDivergeToIxs
        #extraDivergeToIxsList = ctm.extraDivergeToIxsList
        #print 'extraDivergeToIxs',extraDivergeToIxs
        #print 'extraDivergeToIxsList',extraDivergeToIxsList
        #turningRatiosList = self.turningRatiosExtraDiverge
        signalPlans = ctm.signalPlans
        timeStepInCycle = timeStep

        for dl in range(len(extraDivergeToIxs)):

            divergeFromLinkIx = extraDivergeToIxs[dl]
            if signalPlans[dl][timeStepInCycle] == 0:
                self.SpeedsList[divergeFromLinkIx][-1] = 0
            else:
                self.SpeedsList[divergeFromLinkIx][-1] = 1

    def HGVPositioning(self,HGVInputs):
        #print 'HGVPositioning'
        # here just some random input for test
        #randomNumber = random.randint(0,100)
        #if randomNumber>49:
        #--------------------------------------------------------------------------------------------------------------manually data supply!!!!
        HGVInputLinkIxs = [3,5,9,14,15,17,22,25,29,35,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,\
        58,59,60,61,62,63,64,65,66,67,72,74,81,86,88,92,96,99,101,103,104,106,111,113,119,124,125,137,143,145,146,151]#need to check...................................................
        for i in range(len(HGVInputLinkIxs)):
            if len(HGVInputs[i])!=0:
                linkIx = HGVInputLinkIxs[i]
                HGVPositions = [0]*len(HGVInputs[i])
                #print 'linkIx',linkIx
                #print 'len(self.previousStatuses)',len(self.previousStatuses)
                cellNumber = len(self.previousStatuses[linkIx])
                for j in range(len(HGVPositions)):

                    HGVPositions[j] = int(HGVInputs[i][j]*cellNumber)
                    self.previousStatuses[linkIx][HGVPositions[j]] = self.previousStatuses[linkIx][HGVPositions[j]] + 1

    def flowModel(self):
        #calculate flow
        for nl in range(len(self.currentFlows)):
            maxFlow = int(self.linkMaxFlows[nl]*2)
            for nc in range(1,len(self.SpeedsList[nl])):
                if self.SpeedsList[nl][nc] == 1:
                    self.currentFlows[nl][nc-1] = max(0,int(min(self.previousStatuses[nl][nc-1], maxFlow, maxFlow-self.previousStatuses[nl][nc])))
                else:
                    self.currentFlows[nl][nc-1] = 0

            for ncc in range(1,len(self.SpeedsList[nl])-1):
                self.currentStatuses[nl][ncc] = max(0,self.previousStatuses[nl][ncc] + self.currentFlows[nl][ncc-1] - self.currentFlows[nl][ncc])

    def stopsEvaluation(self):

        self.stops = 0

        for i in range(len(self.previousFlows)):
            for j in range(1,len(self.previousFlows[i])):
                self.stops = self.stops - min((self.currentFlows[i][j]-self.previousFlows[i][j-1]),0)



        self.overallStops = self.stops + self.overallStops

    def initVcell(self):
        for nl in range(len(self.previousStatuses)):
            self.previousStatuses[nl][0] = 0
            self.previousStatuses[nl][-1] = 0





    def mergeModel(self):

        for nl in range(len(self.mergeFromIxs)):

            mergeToLinkIx = self.mergeFromIxs[nl]
            mergeFromLinksIxList = self.mergeFromIxsList[nl]
            mergeVolume = 0
            maxMergeVolume = 0
            restVolume = 0
            capacity_mtl = int(self.linkMaxFlows[mergeToLinkIx]*2)

            for nn in range(len(mergeFromLinksIxList)):
                mergeFromLinkIx = mergeFromLinksIxList[nn]
                mergeVolume = mergeVolume + self.previousStatuses[mergeFromLinkIx][-2]


            if self.SpeedsList[mergeToLinkIx][1] ==1:

                if mergeVolume <= capacity_mtl - self.previousStatuses[mergeToLinkIx][1]:
                    self.previousStatuses[mergeToLinkIx][0] = mergeVolume
                    for nn in range(len(mergeFromLinksIxList)):
                        mergeFromLinkIx = mergeFromLinksIxList[nn]
                        capacity_mfl = int(self.linkMaxFlows[mergeFromLinkIx]*2)
                        self.previousStatuses[mergeFromLinkIx][-1] = max(0,capacity_mfl - self.previousStatuses[mergeFromLinkIx][-2])

                else:
                    maxMergeVolume = capacity_mtl - self.previousStatuses[mergeToLinkIx][1]
                    restVolume = maxMergeVolume
                    receivedVolume = 0
                    itN = 0
                    while restVolume>=1:

                        for nn in range(len(mergeFromLinksIxList)):
                            mergeFromLinkIx = random.randint(0,len(mergeFromLinksIxList)-1)

                            capacity_mfl = int(self.linkMaxFlows[mergeFromLinkIx]*2)
                            if self.previousStatuses[mergeFromLinkIx][-1] < capacity_mfl:
                                self.previousStatuses[mergeFromLinkIx][-1] = self.previousStatuses[mergeFromLinkIx][-1] + 1
                                restVolume = restVolume -1
                                receivedVolume = restVolume +1
                        itN = itN+1
                        if itN>len(mergeFromLinksIxList):
                            break

                    self.previousStatuses[mergeToLinkIx][0] = receivedVolume
            else:
                self.previousStatuses[mergeToLinkIx][0] = 0
                for nn in range(len(mergeFromLinksIxList)):
                        mergeFromLinkIx = mergeFromLinksIxList[nn]
                        capacity_mfl = int(self.linkMaxFlows[mergeFromLinkIx]*2)
                        self.previousStatuses[mergeFromLinkIx][-1] = capacity_mfl






    def divergeModel(self):

        for nl in range(len(self.divergeToIxs)):
            divergeFromLinkIx = self.divergeToIxs[nl]
            divergeTolinksIxList = self.divergeToIxsList[nl]
            turningRatios = self.turningRatiosDiverge[nl]
            allValue = 0.0
            distributedVehicles = 0

            for nn in range(len(turningRatios)):
                allValue = allValue + turningRatios[nn]

            spiltPoints = [0]*len(turningRatios)
            splitPoint = 0.0

            for nn in range(len(turningRatios)):
                spiltPoints[nn] = splitPoint + turningRatios[nn]/allValue
                splitPoint = splitPoint + turningRatios[nn]/allValue
            #print 'split point', spiltPoints
            NoOfVehicles = 0
            NoOfVehicles = self.previousStatuses[divergeFromLinkIx][-2]
            irN = 0

            while NoOfVehicles>=1:
                if irN >=len(turningRatios):
                    break
                irN = irN+1
                randomDecision = random.random()
                for nn in range(len(turningRatios)):
                    if randomDecision < spiltPoints[nn]:
                        distributedLinkIx = divergeTolinksIxList[nn]
                        capacity = int(self.linkMaxFlows[distributedLinkIx]*2)
                        if self.previousStatuses[distributedLinkIx][0] < capacity:
                            self.previousStatuses[distributedLinkIx][0] =\
                            self.previousStatuses[distributedLinkIx][0] + 1
                            NoOfVehicles = NoOfVehicles -1
                            break


            distributedVehicles = self.previousStatuses[divergeFromLinkIx][-2] - NoOfVehicles
            self.previousStatuses[divergeFromLinkIx][-1] = int(self.linkMaxFlows[divergeFromLinkIx]*2) - distributedVehicles



    def extraDivergemodel(self):
        #the same as diverge
        for nl in range(len(self.extraDivergeToIxs)):
            divergeFromLinkIx = self.extraDivergeToIxs[nl]
            divergeTolinksIxList = self.extraDivergeToIxsList[nl]
            turningRatios = self.turningRatiosExtraDiverge[nl]
            allValue = 0.0
            distributedVehicles = 0
            if self.SpeedsList[divergeFromLinkIx][-1] == 1:
                for nn in range(len(turningRatios)):
                    allValue = allValue + turningRatios[nn]

                spiltPoints = [0]*len(turningRatios)
                splitPoint = 0.0

                for nn in range(len(turningRatios)):
                    spiltPoints[nn] = splitPoint + turningRatios[nn]/allValue
                    splitPoint = splitPoint + turningRatios[nn]/allValue
                NoOfVehicles = 0
                NoOfVehicles = self.previousStatuses[divergeFromLinkIx][-2]
                testno = 0

                while NoOfVehicles>=1:
                    if testno >= len(turningRatios):
                        break
                    testno = testno +1
                    randomDecision = random.random()
                    for nn in range(len(turningRatios)):
                        if randomDecision < spiltPoints[nn]:
                            distributedLinkIx = divergeTolinksIxList[nn]
                            capacity = int(self.linkMaxFlows[distributedLinkIx]*2)
                            if self.previousStatuses[distributedLinkIx][0] < capacity:
                                self.previousStatuses[distributedLinkIx][0] =\
                                self.previousStatuses[distributedLinkIx][0] + 1
                                NoOfVehicles = NoOfVehicles -1
                                break

                distributedVehicles = self.previousStatuses[divergeFromLinkIx][-2] - NoOfVehicles
                self.previousStatuses[divergeFromLinkIx][-1] = int(self.linkMaxFlows[divergeFromLinkIx]*2) - distributedVehicles
            else:
                self.previousStatuses[divergeFromLinkIx][-1] = int(self.linkMaxFlows[divergeFromLinkIx]*2)
                for nn in range(len(turningRatios)):
                    distributedLinkIx = divergeTolinksIxList[nn]
                    self.previousStatuses[distributedLinkIx][0] = 0

def pretest():
    ctm = CellTransmissionModel()
    ctm.readNetwork()
    ctm.buildCTM()
    return ctm



def maintest(sps,vehcleInputs,HGVInputs):
    #os.system('cls')
    ctm = CellTransmissionModel()
    ctm.readNetwork()
    ctm.buildCTM()
    #ctm.readSignalPlans()#get signal plan from GA
    ctm.signalPlans = sps
    #print 'ctm.signalPlans', ctm.signalPlans
    mcns = CNSMixModel(ctm)
    #get HGV from Vissim
    ctm.initFlow_0(vehcleInputs)

    for timeStep in range(simulationTime):

        ctm.initFlow(vehcleInputs) #get traffic demand from vissim

        ctm.mergeModel()
        ctm.divergeModel()
        ctm.ExtraDivergeModel(timeStep)

        ctm.flowModel()
        ctm.waitingTimeEvaluation()

        mcns.SpeedDiriving(ctm,timeStep)
        if timeStep == 0:
            mcns.HGVPositioning(HGVInputs)
        mcns.initVcell()
        mcns.mergeModel()
        mcns.divergeModel()
        mcns.extraDivergemodel()
        mcns.flowModel()
        mcns.stopsEvaluation()

        #mcns.stopsEvaluation()
    return ctm.overallWaitingTime, mcns.overallStops
#(overallWaitingTime, mcns.overallStops) = maintest(sps)


if __name__ == '__main__':
         maintest()