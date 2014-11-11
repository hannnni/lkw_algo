#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     14.01.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import win32com
import win32com.client
import os
import string
import random
import csv
import sys
if "C:\\My_Python_Lib" not in sys.path:
    sys.path.append("C:\\My_Python_Lib")

import numpy# as np
import scipy
import GA_New
import allPos

import cPickle as pickle

import csv
import sys
#from scipy import stats
#import matplotlib.pyplot as plt

global filename,vissimResultFileName
#define the file name, when it under the same folder with py file.
#filename = 'p1'
#vissimResultFileName = filename+'.fzp'

global simulationtimes, simulationLength, cycle, cycleTimes
#define the number of cycles, cycle time and simulation times
cycle = 30
cycleTimes = 70
simulationLength = cycle * cycleTimes
simulationtimes = 8

global inputLinks,inputLinksHGV

inputLinksHGV = [23,25,512,22,30,32,38,40,517,523,33,45,46,51,53,54,55,56,529,\
                530,533,534,535,30,47,48,49,50,52,59,60,531,532,536,539,61,64,65,70,72,543,548,\
                73,83,90,552,555,91,92,94,103,105,559,564,565,117,118,120,121,575]
inputLinks= [14,25,36,29,55,68,75,80,86,98,109,120,126]


global RandomSeed
# Please use a fix  seed Number, in oder to get the same traffic situation fot comparation!
#RandomSeed = 15

global HGVType
HGVType = 201

def loadVISSIM():
    cwd = os.getcwd()
    VISSIM = win32com.client.Dispatch("Vissim.Vissim.540");
    VISSIM.LoadNet(cwd + '\\' + filename + '.inp');

    VISSIM_Eval = VISSIM.Evaluation;
    #VISSIM_Eval.SetAttValue("DATACOLLECTION",True);
    VISSIM_Eval.SetAttValue("VEHICLERECORD",True);

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
    #Vissim_SignalController = Vissim_SignalControllers.GetSignalControllerByNumber(1)
    #Vissim_SignalGroup = Vissim_SignalController.SignalGroups(1)
    #vehcleInputs = [0]*len(inputLinks)
    spRun = []

    for i in range(simulationLength):

        VISSIM_Sim.RunSingleStep()


        if (i+1)%cycleTimes == 0:
            print 'simulation timestep:', i
            print 'start to Optimization:'
            print 'get overall vehicles:'
            vehcleInputs = [0]*len(inputLinks)

            pickleObjs = []
            pickleObj = []
            #load pickle file
            try: pickleObjs = pickle.load(open("picklerFile.txt", "r"))
            except:pass

            for j in range(len(inputLinks)):
                inputLink = Vissim_Net_Links.GetLinkByNumber(inputLinks[j])
                #print 'inputLink',inputLink
                vehicles = inputLink.GetVehicles()
                vehcleInputs[j] = vehicles.Count
                #vehiclesCount = vehicles.Count
                #vehcleInputs[j] = vehcleInputs[j] + vehiclesCount

            #get HGVs:----------------------------------------
            print vehcleInputs
            print 'get HGV vehicles:'

            HGVInputs = [0]*len(inputLinksHGV)
            for x in range(len(HGVInputs)):
                HGVInputs[x] =[]
            for k in range(len(inputLinksHGV)):
                inputLinkHGV = Vissim_Net_Links.GetLinkByNumber(inputLinksHGV[k])
                #get length of link here
                linkLength = inputLinkHGV.AttValue('LENGTH')
                HGVs = inputLinkHGV.GetVehicles()
                platoonList = []
                Headways = []
                for v in HGVs:
                    veh_Type = v.AttValue('TYPE')
                    #print 'veh_Type', veh_Type
                    if veh_Type == HGVType:
                        veh_Position = v.AttValue('LINKCOORD')
                        #print 'veh_Position',veh_Position
                        platoonList.append(veh_Position/linkLength)
                    #HGVCounts = HGVs.Count
                HGVInputs[k] = platoonList#divide by length?

            #only the number of lkw is recorded in HGVInputsONo
            HGVInputsONo = [0]*len(HGVInputs)
            for i in range(len(HGVInputsONo)):
                HGVInputsONo[i]= len(HGVInputs[i])

            #to test all posibilities:
            #allPos.mainTest(vehcleInputs,HGVInputs)
            #return signal prgramm, or signal plans:
            (firstCycleSpIxs,bestGenomeBits,bestFitnessValue) = GA_New.maintest(vehcleInputs,HGVInputs)

            firstCycleSpIxs = firstCycleSpIxs[1:6]
            for i in range(len(firstCycleSpIxs)):
                firstCycleSpIxs[i] = firstCycleSpIxs[i]+1
            print 'firstCycleSpIxs:', firstCycleSpIxs
            spRun.append(firstCycleSpIxs)

            pickleObj = [HGVInputsONo,bestGenomeBits,bestFitnessValue]
            pickleObjs.append(pickleObj)
            #create a new picklefile to save the new result
            try: os.remove("picklerFile.txt")
            except: pass
            pickle.dump(pickleObjs, open("picklerFile.txt", "w"))

            sp = 0
            for controller in Vissim_SignalControllers:
                if sp>4:
                    break
                else:
                    originalSPN = controller.AttValue('PROGRAM')
                    controller.SetAttValue('PROGRAM', firstCycleSpIxs[sp]) #firstCycleSpIxs[sp]+1
                    print 'the signal programm of Intersection ', sp, 'has changed to No.',firstCycleSpIxs[sp]
                    sp = sp+1
    return spRun

def runVISSIM_1(VISSIM):
    VISSIM_Sim = VISSIM.Simulation;

    VISSIM_Sim.RandomSeed = RandomSeed
    #VISSIM_Sim.RandomSeed = random.randint(1,100)


    for i in range(simulationLength):

        VISSIM_Sim.RunSingleStep()


if __name__ == '__main__':

    Files = ['p1','p2']#all the senarios name
    for i in range(len(Files)):
        filename = Files[i]
        vissimResultFileName = filename+'.fzp'
        #print 'vissimResultFileName:',vissimResultFileName
        SpAll = []
        for i in range(simulationtimes):
            print 'run:',i
            RandomSeed = random.randint(1,100)
        #without optimisation:
            VISSIM = loadVISSIM()
            spRun = runVISSIM_1(VISSIM)
            VISSIM = None
            simulationtime = i+1
            try: os.remove(filename+'_'+str(simulationtime)+'_withOutLPM'+'.txt')
            except: pass
            os.rename(vissimResultFileName,filename+'_'+str(simulationtime)+'_withOutLPM'+'.txt')
        #with optimisation:
            VISSIM = loadVISSIM()
            spRun = runVISSIM(VISSIM)
            SpAll.append(spRun)
            VISSIM = None
            simulationtime = i+1
            try: os.remove(filename+'_'+str(simulationtime)+'_withLPM'+'.txt')
            except: pass
            os.rename(vissimResultFileName,filename+'_'+str(simulationtime)+'_withLPM'+'.txt')
        print 'SpAll:',SpAll
