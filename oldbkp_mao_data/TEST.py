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
import numpy# as np
import scipy
import GA_New
import allPos
#from scipy import stats

#import matplotlib.pyplot as plt

global debug
debug = 0

global filename #, EvaluationResult, HistoResult
#define the file name, when it under the same folder with py file.
filename = 'test intersection'

global simulationtimes, simulationLength, cycle, cycleTimes
#define the number of cycles, cycle time and simulation time
cycle = 3
cycleTimes = 60
simulationLength = cycle * cycleTimes
simulationtimes = 1

global inputLinks,inputLinksHGV
#define manuelly or, should be read from the excel table? maybe make it as global variable
#get input link
inputLinksHGV = [1,6]
inputLinks= [1,8,7,6,10,9]

global RandomSeed
# Please use a fix  seed Number, in oder to get the same traffic situation fot comparation!
RandomSeed = 15

global HGVType

HGVType = 201



def loadVISSIM():
    cwd = os.getcwd()
    VISSIM = win32com.client.Dispatch("Vissim.Vissim.540");
    VISSIM.LoadNet(cwd + '\\' + filename + '.inp');

    #VISSIM_Graphics = VISSIM.Graphics
    #VISSIM_Graphics.SetAttValue('VISUALIZATION',1)
    #VISSIM_Graphics.SetAttValue('3D',0)
    #VISSIM_Eval = VISSIM.Evaluation;
    #VISSIM_Eval.SetAttValue("DATACOLLECTION",True);

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

    for i in range(simulationLength):

        VISSIM_Sim.RunSingleStep()

        if (i+1)%60 == 0:
            print 'simulation timestep:', i
            #print '(i+1)%60', (i+1)%60
            print 'start to Optimization:'
            print 'get overall vehicles:'
            vehcleInputs = [0]*len(inputLinks)
            for j in range(len(inputLinks)):
                inputLink = Vissim_Net_Links.GetLinkByNumber(inputLinks[j])
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
                        print 'veh_Position',veh_Position
                        platoonList.append(veh_Position/linkLength)
                    #HGVCounts = HGVs.Count
                HGVInputs[k] = platoonList#divide by length?
            print HGVInputs
            #to test all posibilities:

            #allPos.mainTest(vehcleInputs,HGVInputs)

            #return signal prgramm, or signal plans:
            firstCycleSpIxs = GA_New.maintest(vehcleInputs,HGVInputs)
            sp = 0
            for controller in Vissim_SignalControllers:
                originalSPN = controller.AttValue('PROGRAMM')
                controller.SetAttValue('PROGRAMM', firstCycleSpIxs[sp]+1) #firstCycleSpIxs[sp]+1
                print 'the signal programm of Intersection ', sp, 'has changed to No.',firstCycleSpIxs[sp]+1
                sp = sp+1
            #vehcleInputs = [0]*len(inputLinks)
#        else:#get verhicle number also ever cycle, dont need to get it every second,
#        #if use the link to get vehicles, but when use detectors then, need to get the detector data every second
##            for j in range(len(inputLinks)):
##                inputLink = Vissim_Net_Links.GetLinkByNumber(inputLinks[j])
##                vehicles = inputLink.GetVehicles()
##                vehiclesCount = vehicles.Count
##                vehcleInputs[j] = vehcleInputs[j] + vehiclesCount
        #platoon recognization:
##        VISSIM_Vehicles_On_DETE = PlatoonLink.GetVehicles()
##
##        if not VISSIM_Vehicles_On_DETE is None:
##            NumOfVehs = VISSIM_Vehicles_On_DETE.Count
##            print 'the number of vehicles is:',NumOfVehs
##            platoonList = []
##            Headways = []
##            for v in VISSIM_Vehicles_On_DETE:
##                VISSIM_ROUTE = v.AttValue('ROUTE')
##                print VISSIM_ROUTE
##                v.SetAttValue('SPEED',10)
##
##                veh_Type = v.AttValue('TYPE')
##                veh_Position = v.AttValue('LINKCOORD')
##                print 'veh_Type', veh_Type
##                if veh_Type == 201:
##                    platoonList.append(veh_Position)
##            print 'platoon list:', platoonList
##            for i in range(len(platoonList)-1):
##                headway = abs(platoonList[i+1] - platoonList[i])
##                Headways.append(headway)
##            if len(Headways) !=0:
##                if min(Headways)<=30:
##                    HGVPlatoon = 1
##                    print 'Signal group 1 state :', Vissim_SignalGroup.STATE
##                    Vissim_SignalGroup.SetAttValue('STATE',3)
##                    #try to change programm

      #v.SetAttValue('ROUTE') route is not writeable
                #dir(VISSIM_Vehicles_On_DETE)
            #VISSIM_Vehicles_On_DETE.GetMultiAttValues(Empty, "LINKCOORD", VehiclePositons)
            #print VehiclePositons
            #VISSIM_Vehicles_On_DETE.GetMultiAttValues(Empty, "TYPE", VehicleType)
            #print VehicleType
        #for v in range(len(VISSIM_Vehicles_On_DETE)):
            #VehiclePositons = VehiclePositons.append(VISSIM_Vehicles_On_DETE[v])
        #print 'Signal group 1 state :', Vissim_SignalGroup.STATE
        #Vissim_SignalGroup.SetAttValue('STATE',3)
    #try: os.remove(str(simulationtime)+'.txt')
    #except: pass
    #os.rename(EvaluationResult,str(simulationtime)+'.txt')

if __name__ == '__main__':

    #if debug == 0:
    VISSIM = loadVISSIM()
    #for simulationtime in range(simulationtimes):
        #if debug == 0:
    runVISSIM(VISSIM)
    #loadEvaOutput(simulationtime)
    #if debug == 0:
    VISSIM = None
