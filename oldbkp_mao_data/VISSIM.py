#import wx
import win32com
import win32com.client
import os
import string
import random
import csv
import numpy# as np
import scipy
from scipy import stats

import matplotlib.pyplot as plt

global debug
debug = 0

global filename, EvaluationResult, HistoResult
filename = 'PlatoonDispersion'
EvaluationResult = 'platoondispersion.mer'
HistoResult = 'result.csv'

global simulationtimes, simulationLength
simulationLength = 360
simulationtimes = 20

global detectionPoints, detectionResolution
detectionPoints = 4
detectionResolution = 1000 #used to tell different detection point


global histogramBin, histogramRawData, histogramStep
histogramStep = 4
histogramBin = [histogramStep*i for i in range(simulationLength/histogramStep+1)]
histogramBin_plot = [histogramStep*i for i in range(simulationLength/histogramStep)]
histogramRawData = []


global firstArrivalsTemp, firstArrivals
firstArrivalsTemp = [0 for i in range(detectionPoints)]
firstArrivals = []

global F
F = 0.9

def loadVISSIM():
    cwd = os.getcwd()
    VISSIM = win32com.client.Dispatch("Vissim.Vissim.540");
    VISSIM.LoadNet(cwd + '\\' + filename + '.inp');

    VISSIM_Graphics = VISSIM.Graphics
    VISSIM_Graphics.SetAttValue('VISUALIZATION',1)
    VISSIM_Graphics.SetAttValue('3D',0)


    VISSIM_Eval = VISSIM.Evaluation;
    VISSIM_Eval.SetAttValue("DATACOLLECTION",True);

    return VISSIM

def runVISSIM(VISSIM):
    VISSIM_Sim = VISSIM.Simulation;
    VISSIM_Sim.RandomSeed = random.randint(1,1000000)

    for i in range(simulationLength):
        #print i
        VISSIM_Sim.RunSingleStep()

    try: os.remove(str(simulationtime)+'.txt')
    except: pass
    os.rename(EvaluationResult,str(simulationtime)+'.txt')

def loadEvaOutput(simulationtime):
    toReadFile = open(str(simulationtime)+'.txt','r')
    reader = toReadFile.readlines()
    toReadFile.close()

    flag_isData = 0
    data = [[] for i in range(detectionPoints)]
    for row in reader:
        if flag_isData == 1:
            data_temp = row.split('\n')[0] #remove '\n' at the end of each line
            #data_temp = data_temp[0]
            data_temp = data_temp.split(' ')
            while '' in data_temp:
                data_temp.remove('')
            data_temp = map(float,data_temp)
            data_time = data_temp[2]
            if data_time > -1:
                data[int(data_temp[0]/detectionResolution)].append(data_time)
        else:
            if row.startswith(' Data C.P.'): flag_isData = 1

    for i in range(len(data)):
        row = data[i]
        firstArrivalsTemp[i] = firstArrivalsTemp[i] + min(row)
    #print firstArrivalsTemp

    histogramResult_Temp = []
    for row in data:
        histogramResult_Temp.append(numpy.histogram(row,bins=histogramBin)[0])
    histogramRawData.append(histogramResult_Temp)
    #print histogramRawData

def postProcess():
    histogramFinal = []
    for i in range(len(histogramRawData)):
        data = numpy.matrix(histogramRawData[i]).astype(float)
        #print data
        #print
        if histogramFinal == []:
            histogramFinal = data
        else:
            histogramFinal = data + histogramFinal
            #histogramFinal = F * (data + (1-F) * histogramFinal)
    histogramFinal = histogramFinal/len(histogramRawData)

    #print histogramFinal
    toWriteFile = open(HistoResult,'wb')
    CSVWriter = csv.writer(toWriteFile)
    for row in histogramFinal:
        toWriteLine = list(numpy.array(row).reshape(-1,))
        CSVWriter.writerow(toWriteLine)
    toWriteFile.close()

    return list(numpy.array(histogramFinal[0]).reshape(-1,))

def calFirstArrival():
    for firstArrival in firstArrivalsTemp:
        firstArrivals.append(firstArrival/simulationtimes)
    #print firstArrivals
    return firstArrivals


def platoonRobertson(detectionData):
    platoonRobertsonPrediction = [detectionData]

    for i in range(1,detectionPoints): #jump the first row
        paraAlfa = 0.2
        paraBeta = 0.8
        #average speed 50km/h ~ 13.89m/s
        #distance between detectors: 300m
        #average travel time = 300/18.89 = 21.6s
        paraTa = int(i*21.6/histogramStep)
        paraT = int(i*21.6*paraBeta/histogramStep)
        paraF = 1/(1 + paraAlfa*paraBeta*paraTa)
        platoonRobertsonPrediction.append([ 0 for j in range(len(detectionData))]) #new row for new prediction data
        #print (platoonRobertsonPrediction[i])
        for j in range(len(platoonRobertsonPrediction[i])):
            #print platoonRobertsonPrediction[i][j]
            if j-paraTa <= 0:
                pass
            else:
                platoonRobertsonPrediction[i][j] = paraF * platoonRobertsonPrediction[0][j-paraT] + (1-paraF) * platoonRobertsonPrediction[i][j-1]
    return platoonRobertsonPrediction

def platoonSeddon(detectionData):
    platoonSeddonPrediction = [detectionData]

    for i in range(1,detectionPoints): #jump the first row
        paraAlfa = 0.4
        paraBeta = 0.8
        #average speed 50km/h ~ 13.89m/s
        #distance between detectors: 300m
        #average travel time = 300/18.89 = 21.6s
        paraTa = int(i*21.6/histogramStep)
        paraT = int(i*21.6*paraBeta/histogramStep)
        paraF = 1/(1 + paraAlfa*paraBeta*paraTa)
        platoonSeddonPrediction.append([ 0 for j in range(len(detectionData))]) #new row for new prediction data
        #print (platoonSeddonPrediction[i])
        for j in range(len(platoonSeddonPrediction[i])):
            #print platoonSeddonPrediction[i][j]
            if j-paraTa <= 0:
                pass
            else:
                for h in range(paraT, j):
                    platoonSeddonPrediction[i][j] = platoonSeddonPrediction[i][j] + paraF * pow((1-paraF),h-paraT) * platoonSeddonPrediction[0][j-h]
    return platoonSeddonPrediction

def plotHist(platoonRobertsonPrediction, platoonSeddonPrediction):
    toReadFile = open(HistoResult,'r')
    csvReader = csv.reader(toReadFile)

    plotColumns = 3
    #plotColumn = 2
    subplotIndex = 1
    for line in csvReader:
        data = map(float,line)
        plt.subplot(detectionPoints, plotColumns, subplotIndex)
        plt.bar(histogramBin_plot,data,width=4,color='blue')
        print sum(data)
        plt.axis([0, 360, 0, 10])
        plt.grid(color='gray', linestyle='-', linewidth=0.1)
        subplotIndex = subplotIndex + plotColumns
        plt.gca().invert_xaxis() #!!!reverse x axis

    toReadFile.close()
    #plt.show()


    subplotIndex = 2 + plotColumns
    for i in range(1,len(platoonRobertsonPrediction)):
        data = platoonRobertsonPrediction[i]
        plt.subplot(detectionPoints, plotColumns, subplotIndex)
        plt.bar(histogramBin_plot,data,width=4,color='green')
        print sum(data)
        plt.axis([0, 360, 0, 10])
        plt.grid(color='gray', linestyle='-', linewidth=0.1)
        subplotIndex = subplotIndex + plotColumns
        plt.gca().invert_xaxis() #!!!reverse x axis


    subplotIndex = 3 + plotColumns
    for i in range(1,len(platoonSeddonPrediction)):
        data = platoonSeddonPrediction[i]
        plt.subplot(detectionPoints, plotColumns, subplotIndex)
        plt.bar(histogramBin_plot,data,width=4,color='red')
        print sum(data)
        plt.axis([0, 360, 0, 10])
        plt.grid(color='gray', linestyle='-', linewidth=0.1)
        subplotIndex = subplotIndex + plotColumns
        plt.gca().invert_xaxis() #!!!reverse x axis

    plt.show()


if __name__ == '__main__':
    debug = 0
    simulationtimes = 1
    if debug == 0:
        VISSIM = loadVISSIM()

    for simulationtime in range(simulationtimes):
        if debug == 0:
            runVISSIM(VISSIM)
        loadEvaOutput(simulationtime)

    if debug == 0:
        VISSIM = None

    detectionData = postProcess() #to get the raw detection data at the stop line
    #print len(histogramRawData)
    firstArrivals = calFirstArrival() #to get the average first arrival time to each detetion points
    #print firstArrivals
    platoonRobertsonPrediction = platoonRobertson(detectionData)
    platoonSeddonPrediction = platoonSeddon(detectionData)
    plotHist(platoonRobertsonPrediction, platoonSeddonPrediction)
