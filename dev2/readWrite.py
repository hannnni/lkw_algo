#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     19.09.2014
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
#from scipy import stats
import csv
import sys

global VissimFileName,csvName,simulationtimes

VissimFileName = 'p2'#p1
csvName = 'new.csv'
simulationtimes = 1#8

def main():
    for i in range(simulationtimes):
        simulationtime = i+8 #+1
        fileName = VissimFileName+'_'+str(simulationtime)+'_withLPM'#'_withOutLPM'#
        #fileName = 'p1_basic'
        #fileName = 'p2_basic'
        toReadFile = open(fileName+'.txt','r')
        reader = toReadFile.readlines()
        toReadFile.close()

        #data = [[] for i in range(detectionPoints)]#
        data = []
        vehiclNrs = []
        delay = []
        stop =[]
        stopforLKW = []
        delayforLKW = []
        for row in reader:

            data_temp = row.split('\n')[0] #remove '\n' at the end of each line
            #data_temp = data_temp[0]


            data_temp = data_temp.split(' ')
            while '' in data_temp:
                data_temp.remove('')
            while ';' in data_temp:
                data_temp.remove(';')
            #print 'data_temp:',data_temp
            data_temp[0]= int(data_temp[0])#vehicle No
            data_temp[1]= int(data_temp[1])#vehicle type
            data_temp[2]= float(data_temp[2])#stops
            data_temp[3]= float(data_temp[3])#delay
    ##        for i in range(len(data_temp)):
    ##            data_temp[i]= float(data_temp[i])
            #print 'data_temp:',data_temp
            vehNo = data_temp[0]
            vehIx = 0
            newVeh = False
            try: vehIx = vehiclNrs.index(vehNo)
            except: newVeh = True
            if newVeh:
                vehiclNrs.append(vehNo)
                delay.append(data_temp[3])
                stop.append(data_temp[2])
                if data_temp[1] == 201:
                    stopforLKW.append(data_temp[2])
                    delayforLKW.append(data_temp[3])
                else:
                    stopforLKW.append(0)
                    delayforLKW.append(0)
            else:
                delay[vehIx] = max(delay[vehIx],data_temp[3])
                stop[vehIx] = max(stop[vehIx],data_temp[2])
                if data_temp[1] == 201:
                    stopforLKW[vehIx] = max(stopforLKW[vehIx],data_temp[2])
                    delayforLKW[vehIx] = max(delayforLKW[vehIx],data_temp[3])







            data.append(data_temp)
    ##        delay.append(data_temp[3])
    ##        stop.append(data_temp[2])
        print 'simulationtime:',simulationtime
        #print 'delay',delay
        #print 'stops',stop
        #print 'Lkw Stops',stopforLKW
        #print 'vehicleNo',vehiclNrs
        print 'sum delay:',sum(delay)
        print 'sum stops:',sum(stop)
        print 'sum Lkw Stops:', sum(stopforLKW)
        print 'sum lkw Delays:', sum(delayforLKW)
        #print 'lengh of data ',len(data[0])
        with open(csvName, "wb") as outcsv:
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            #writer.writerow(['number', 'text', 'number'])
            for item in data:
    #Write item to outcsv
                 writer.writerow(item)
    ##        writer = csv.writer(f)
    ##        #writer.writerows(data)
    ##
    ####    writer = csv.writer(sys.stdout)
    ####
    ##        for item in data:
    ##            writer.writerow([item[0], item[1]])


            #print 'length of datatemp', len(data_temp)
    ##        data_temp = map(float,data_temp)
    ##        print 'data_temp:',data_temp
    ##        data_time = data_temp[2]
    ##        if data_time > -1:
    ##            data[int(data_temp[0]/detectionResolution)].append(data_time)
    ##
    ##        if row.startswith(' Data C.P.'): flag_isData = 1
    ##
    ##    for i in range(len(data)):
    ##        row = data[i]
    ##        firstArrivalsTemp[i] = firstArrivalsTemp[i] + min(row)
    ##    #print firstArrivalsTemp
    ##
    ##    histogramResult_Temp = []
    ##    for row in data:
    ##        histogramResult_Temp.append(numpy.histogram(row,bins=histogramBin)[0])
    ##    histogramRawData.append(histogramResult_Temp)

if __name__ == '__main__':
    main()
