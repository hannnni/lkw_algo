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

import numpy
import scipy
import GA_New
import allPos
import cPickle as pickle

#from scipy import stats
#import matplotlib.pyplot as plt

global filename, vissimResultFileName
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

# possible lkw links
inputLinksHGV = [23,25,512,22,30,32,38,40,517,523,33,45,46,51,53,54,55,56,529,\
                530,533,534,535,30,47,48,49,50,52,59,60,531,532,536,539,61,64,65,70,72,543,548,\
                73,83,90,552,555,91,92,94,103,105,559,564,565,117,118,120,121,575]

# entrance links, check for new vehicles
inputLinks= [14,25,36,29,55,68,75,80,86,98,109,120,126]


global RandomSeed
# Please use a fix  seed Number, in oder to get the same traffic situation fot comparation!
#RandomSeed = 15

global HGVType
HGVType = 201

def loadVISSIM():
    # open vissim software
    cwd = os.getcwd()
    VISSIM = win32com.client.Dispatch("Vissim.Vissim.540");
    VISSIM.LoadNet(cwd + '\\' + filename + '.inp');
    VISSIM_Eval = VISSIM.Evaluation;
    #VISSIM_Eval.SetAttValue("DATACOLLECTION",True);
    VISSIM_Eval.SetAttValue("VEHICLERECORD",True);

    return VISSIM

def runVISSIM(VISSIM):
    # actual optimization
    VISSIM_Sim = VISSIM.Simulation;

    #for real implementation don't need this variable
    VISSIM_Sim.RandomSeed = RandomSeed
    #VISSIM_Sim.RandomSeed = random.randint(1,100)

    Vissim_Net = VISSIM.Net
    Vissim_Net_Links = Vissim_Net.Links

    Vissim_SignalControllers = Vissim_Net.SignalControllers
    spRun = []

    #run every second
    for i in range(simulationLength):

        VISSIM_Sim.RunSingleStep()
        # just every cycle time
        if (i+1)%cycleTimes == 0:
            print 'simulation timestep:', i+1
            print 'start to Optimization:'
            print 'get overall vehicles:'

            # new possbile vehicles object
            vehcleInputs = [0]*len(inputLinks)

            #memory objects
            pickleObjs = []
            pickleObj = []

            #load pickle file
            try: pickleObjs = pickle.load(open("picklerFile.txt", "r"))
            except:pass

            # get number of vehicles for every entrance
            for j in range(len(inputLinks)):
                inputLink = Vissim_Net_Links.GetLinkByNumber(inputLinks[j])
                #print 'inputLink',inputLink
                vehicles = inputLink.GetVehicles()
                vehcleInputs[j] = vehicles.Count
            print vehcleInputs

            #get HGVs:----------------------------------------
            print 'get HGV vehicles:'

            # Lkw object
            HGVInputs = [0]*len(inputLinksHGV)
            for x in range(len(HGVInputs)):
                HGVInputs[x] =[]

            # get numbers and position of lkw in all possible link
            for k in range(len(inputLinksHGV)):
                inputLinkHGV = Vissim_Net_Links.GetLinkByNumber(inputLinksHGV[k])
                #get length of link here
                linkLength = inputLinkHGV.AttValue('LENGTH')

                # change HGVs into veh
                HGVs = inputLinkHGV.GetVehicles()
                # relative position to total ( i.e 1/5 of whole link length)
                platoonList = []
                Headways = []
                for v in HGVs:
                    veh_Type = v.AttValue('TYPE')
                    #print 'veh_Type', veh_Type
                    if veh_Type == HGVType:
                        veh_Position = v.AttValue('LINKCOORD')
                        #print 'veh_Position',veh_Position
                        platoonList.append(veh_Position/linkLength)
                HGVInputs[k] = platoonList

            # number of lkws is recorded in HGVInputsONo
            HGVInputsONo = [0]*len(HGVInputs)
            for i in range(len(HGVInputsONo)):
                HGVInputsONo[i]= len(HGVInputs[i])

            #to test all posibilities:
            #allPos.mainTest(vehcleInputs,HGVInputs)
            #return signal prgramm, or signal plans:

            # algorithm is started
            # output:
            # firstCycleSpIxs : signal plan for first cycle
            # bestGenomeBits : signal plan binaric
            # bestFitnessValue : real Number
            (firstCycleSpIxs,bestGenomeBits,bestFitnessValue) = GA_New.maintest(vehcleInputs,HGVInputs)

            # chose the to be optimized intersections
            firstCycleSpIxs = firstCycleSpIxs[1:6]

            # number of next signal plan +1
            for i in range(len(firstCycleSpIxs)):
                firstCycleSpIxs[i] = firstCycleSpIxs[i]+1
            print 'firstCycleSpIxs:', firstCycleSpIxs

            # append new signal plan ( every cycle)
            spRun.append(firstCycleSpIxs)

            pickleObj = [HGVInputsONo, bestGenomeBits, bestFitnessValue]
            pickleObjs.append(pickleObj)

            #create a new picklefile to save the new result
            try: os.remove("picklerFile.txt")
            except: pass
            pickle.dump(pickleObjs, open("picklerFile.txt", "w"))

            sp = 0
            # every intersection renew signal plan
            for controller in Vissim_SignalControllers:
                # five intersections
                if sp>4:
                    break
                else:
                    # original number
                    originalSPN = controller.AttValue('PROGRAM')
                    controller.SetAttValue('PROGRAM', firstCycleSpIxs[sp])
                    print 'the signal programm of Intersection ', sp, 'has changed from ',originalSPN,'to No.',firstCycleSpIxs[sp]
                    sp = sp+1

    return spRun

def runVISSIM_1(VISSIM):
    # run vissim without optimization, random traffic

    VISSIM_Sim = VISSIM.Simulation;
    VISSIM_Sim.RandomSeed = RandomSeed
    #VISSIM_Sim.RandomSeed = random.randint(1,100)
    for i in range(simulationLength):

        VISSIM_Sim.RunSingleStep()

if __name__ == '__main__':

    Files = ['p1','p2']#all the senarios name
    #  p1 und p2 vissim file, netz, cars, etc. definition des Verkehr
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
