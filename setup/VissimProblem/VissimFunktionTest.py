#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     04.09.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import win32com
import win32com.client
import os
import string
import random
import csv
import numpy# as np
import scipy
#import GA_New
#import allPos
#from scipy import stats

#import matplotlib.pyplot as plt

##global debug
##debug = 0

global filename
#define the file name, when it under the same folder with py file.
filename = 'test'

global simulationtimes, simulationLength, cycle, cycleTimes
#define the number of cycles, cycle time and simulation time
cycle = 3
cycleTimes = 60
simulationLength = cycle * cycleTimes
simulationtimes = 1



global RandomSeed
# Please use a fix  seed Number, in oder to get the same traffic situation fot comparation!
RandomSeed = 15

global HGVType
HGVType = 201

def loadVISSIM():
    cwd = os.getcwd()
    VISSIM = win32com.client.Dispatch("Vissim.Vissim.540");
    VISSIM.LoadNet(cwd + '\\' + filename + '.inp');

    VISSIM_Eval = VISSIM.Evaluation;
    VISSIM_Eval.SetAttValue("DATACOLLECTION",True);

    return VISSIM

def runVISSIM(VISSIM):
    VISSIM_Sim = VISSIM.Simulation;

    #for real implementation don't need this variable
    VISSIM_Sim.RandomSeed = RandomSeed
    #VISSIM_Sim.RandomSeed = random.randint(1,100)

    Vissim_Net = VISSIM.Net
    Vissim_Net_Links = Vissim_Net.Links

    #inputLinks = [1,8,7,6,10,9]#oder according to ix index in traffic models
    #ix [0,3,6,21,25,28]
    #inputLinksHGV = [1,6]
    #PlatoonLink = Vissim_Net_Links.GetLinkByNumber(1)
    Vissim_SignalControllers = Vissim_Net.SignalControllers
    Vissim_DataCollections = Vissim_Net.DataCollections
    print 'length of Vissim_DataCollections', len(Vissim_DataCollections)
    #Vissim_SignalController = Vissim_SignalControllers.GetSignalControllerByNumber(1)
    #Vissim_SignalGroup = Vissim_SignalController.SignalGroups(1)
    #vehcleInputs = [0]*len(inputLinks)
    dataCollection = 0

    for i in range(simulationLength):

        VISSIM_Sim.RunSingleStep()
        #print '1'
        dataCollection1 = Vissim_DataCollections.GetDataCollectionByNumber(1)
        #dir()
        print '2'

        dataCollection = dataCollection + \
        dataCollection1.GetResult('NVEHICLES','SUM', 0)
        print 'dataCollection:',dataCollection




##        for dataCollection in Vissim_DataCollections:
##            pass

        if (i+1)%cycleTimes == 0:

            for controller in Vissim_SignalControllers:
                originalSPN = controller.AttValue('PROGRAM')
                print 'originalSPN',originalSPN
                controller.SetAttValue('PROGRAM', 2) #firstCycleSpIxs[sp]+1
                print 'the signal programm of Intersection has changed to No.',2


if __name__ == '__main__':


    VISSIM = loadVISSIM()
    runVISSIM(VISSIM)
    VISSIM = None
