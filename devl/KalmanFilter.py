# Kalman filter
import os
import string
import random
import csv
import numpy# as np
import scipy
import math

global HistFileName
HistFileName = 'kftest.csv'#C:\Users\gu62mal\Desktop\

class trafficDemandPrediction:
    def __init__(self):
            self.histData = []
            self.detecData = []
            self.detecDataf = []
            self.predictData = []
            self.detecError = 0
            self.histError = 0
            self.KG = 0


    def readHistData(self):
            with open(HistFileName, 'U') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                #i = 0
                for row in spamreader:
                    rowlist = row[0].split(';')

                    self.histData.append(int(rowlist[0]))
                    self.detecDataf.append(int(rowlist[3]))
            self.detecData = [99999]*len(self.histData)
            self.predictData = [99999]*len(self.histData)
            self.detecError = [0]*len(self.histData)
            self.histError = [0]*len(self.histData)


    def getDetecData(self,detecDataInput,timeStep):
            #self.detecData = [99999]*len(self.histData)
            if timeStep<len(self.histData):
                #initial value get -1, means no input
                #only used by simulation,
                if detecDataInput > 0:
                    self.detecData[timeStep] = detecDataInput
                else:
                    self.detecData[timeStep] = self.detecDataf[timeStep]
                #print 'self.detecDataf[timeStep]',self.detecDataf[timeStep]
                #print 'self.detecData[timeStep] ',self.detecData[timeStep]

            else:
                print 'Please check the Timestep!'

    def prediction(self,timeStep):
        if timeStep == 0 or self.predictData[timeStep-1]>10000:
            if self.detecData >10000:
                self.predictData[timeStep] = self.histData[timeStep]
            else:
                self.predictData[timeStep] = self.detecData[timeStep]
        else:
            self.histError = (self.histData[timeStep-1]-self.detecData[timeStep-1])*(self.histData[timeStep-1]-self.detecData[timeStep-1])

            self.detecError = (self.predictData[timeStep-1]-self.detecData[timeStep-1])*(self.predictData[timeStep-1]-self.detecData[timeStep-1])
            try:self.KG = math.sqrt(self.detecError/(self.detecError+self.histError))
            except:self.KG = 0
            #print 'KG', self.KG
            #print 'self.detecData[timeStep-1]',self.detecData[timeStep-1]

            self.predictData[timeStep] = self.detecData[timeStep-1] + self.KG*(self.histData[timeStep]-self.detecData[timeStep-1])

            #print'Prediction of Time Step', timeStep, ' is ',self.predictData[timeStep]

if __name__ == '__main__':
    demand = trafficDemandPrediction()
    demand.readHistData()
    print 'histdata', demand.histData
    print 'detedata', demand.detecData
    print 'detedataf', demand.detecDataf

    timeInterval = 0
    detecDataInput = -1
    for i in range(len(demand.histData)):
        demand.getDetecData(detecDataInput,timeInterval)
        #print 'detecData:',demand.detecData
        demand.prediction(timeInterval)
        timeInterval = timeInterval + 1
    print 'predicData:',demand.predictData

