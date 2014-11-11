#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gu62mal
#
# Created:     10.03.2014
# Copyright:   (c) gu62mal 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import string
import random
import csv
import numpy# as np
import scipy
import math
import TrafficModels
import cPickle as pickle

#import matplotlib.pyplot as plt

global NoOfIntersections, NoOfSignalProgramms,NoOfCycle,NoOfIntersectionsOverall
NoOfIntersections = 5
#but only 5 of the intersections are in testfeld, others assumed to use fixtime control....
NoOfIntersectionsOverall = 10

NoOfSignalProgramms = 4
NoOfCycles = 3
#have to be the same as in test.py

global path
#path for the signal plans! but take care of the folder names!!!
path = 'C:\Users\ga78bip\Desktop\Johannes\SP1'

global NameofIntersections, OptIntersections, NonOptIntersections,OverallIntersections

NameOfIntersections = {0:'56-14',1:'56-05',2:'56-90',3:'56-01',4:'56-03',5:'56-06',6:'57-01-1',7:'57-69',8:'57-01-02',9:'57-70'}#only one example
OptIntersections = ['56-05','56-90','56-01','56-03','56-06']
OverallIntersections = ['56-14','56-05','56-90','56-01','56-03','56-06','57-01-1','57-69','57-01-2','57-70']

# signal plan for one intersection, normally 4-6 different signals
class signalProgramm:
    #genome part
        def __init__(self):
             self.Ix = 0
             self.intersection = []
             self.cycleTime = 0
             self.sgList = []
             self.signalPlans = []
             self.biCode = []

        # load name and number of trafic
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

        # load signalplan for every element in the signalgroup
        def getSignalplans(self,getSignalplansName):
            #print 'getSignalplansName',getSignalplansName
            with open(getSignalplansName, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                #l = 0
                #for row in spamreader:
                    #l=l+1

                self.signalPlans = [0]*len(self.sgList)
                #print 'len(self.sgList)',len(self.sgList)
                for l in range(len(self.signalPlans)):
                    self.signalPlans[l] = []

                i = 0
                for row in spamreader:
                    rowlist = row[0].split(';')
                    for j in range(len(rowlist)):
                        #print 'j',j
                        self.signalPlans[j].append(int(rowlist[j]))
                    i=i+1
                #print 'signal plans:', self.signalPlans

# signal programs combined for every intersection
class signalProgramms:
            def __init__(self):

                 self.overallSignalProgramms = [0]*NoOfIntersectionsOverall

            def readSignalProgramms(self,path):

                 for i in range(NoOfIntersectionsOverall):
                    signalProgrammForIntersection = [0]*NoOfSignalProgramms
                    for j in range(NoOfSignalProgramms):
                        #the path should be also include at the beginning
                        #oderPosition = path + '\intersection' + str(i) + '\SignalProgramm' + str(j)
                        oderPosition = path + '\\' + OverallIntersections[i] + '\SignalProgramm' + str(j)
                        fileName_sgList = oderPosition + '\sgList.csv'
                        fileName_signalPlans =oderPosition + '\signalPlans.csv'
                        #print 'fileName_sgList:'
                        #print fileName_sgList
                        sp = signalProgramm()
                        sp.getSgList(fileName_sgList)
                        sp.getSignalplans(fileName_signalPlans)
                        sp.Ix = j
                        sp.intersection = OverallIntersections[i]#check
##                        print 'signal plans', sp.signalPlans
##                        print 'length of sp', len(sp.signalPlans)

                        signalProgrammForIntersection[j]= sp
                        #print 'signal programm j:', signalProgrammForIntersection[j].signalPlans
                    #print 'signal programms No.:', len(signalProgrammForIntersection)
                    self.overallSignalProgramms[i] = signalProgrammForIntersection
                 #print 'self.overallSignalProgramms[-1]', self.overallSignalProgramms[3][0].signalPlans

# algorithm class, generic algo, one indiviual
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
            gen = self.bits
            sectionLength = int(math.sqrt(NoOfSignalProgramms))
            noOfOverallSps = int(len(gen)/sectionLength)
            spIxs = []
            #print 'gen', gen
            for i in range(noOfOverallSps):
                biSection = gen[i*2:i*2+sectionLength]
                spIxs.append(self.bin2int(biSection))
            #print 'Signal Plan No. :', spIxs
            self.spIxs = [0,0,0]+spIxs+[0,0,0,0,0,0,0,0,0,0,0,0]
            #print 'Signal Length. :', len(self.spIxs)
            #here put the other signalplans from the intersections out of the optimization range
            #print'  '
            #print'  '
            # Translation
            #self.tobeEvaluatedSps = [0]*NoOfIntersections
            self.tobeEvaluatedSps = []
            #print 'NoOfIntersections:',NoOfIntersections
            #print 'overallSignalProgramms', len(overallSignalProgramms)
            #print 'overallSignalProgramms[-1]', overallSignalProgramms[3][0].signalPlans
            for i in range(NoOfIntersectionsOverall):
                spIxsforThisIntersection = \
                self.spIxs[i*NoOfCycles:i*NoOfCycles+NoOfCycles]
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
##            print 'length:', len(self.tobeEvaluatedSps)
##            print 'self.tobeEvaluatedSps[3]', self.tobeEvaluatedSps[3]
            return self.tobeEvaluatedSps#pass to traffic model

        # creates fitness for
        def getFitness(self, overallSignalProgramms,vehcleInputs,HGVInputs):
            #x = self.bin2int(self.bits)
            #print 'x', x
            #exec(expr)
            #self.fitness = y
            #print 'y', y
            #optimaztation weight
            weightFactorForWaitingTime = 0
            weightFactorForStops = 1
            self.decode(overallSignalProgramms)
            #print 'call Traffic Models>>'
            (overallWaitingTime, overallStops) = TrafficModels.maintest(self.tobeEvaluatedSps,vehcleInputs,HGVInputs)
            self.fitness = -overallWaitingTime*weightFactorForWaitingTime - weightFactorForStops*overallStops
            #think about the fitness function, maybe directly use the sum is not ideal

# genetischer algo
class ga:

        def __init__(self,
                         pop_size,
                         crossover_rate = 0.9, # threshold to next generation
                         mutation_rate = 0.5, # mutation probability of single bit
                         max_generation = 15
                         ):

                 self.crossover_rate = crossover_rate
                 self.mutation_rate = mutation_rate
                 self.pop_size = pop_size
                 self.genome_len = int(math.sqrt(NoOfSignalProgramms))*NoOfIntersections*NoOfCycles
                 self.generation = 0
                 self.genomes = []
                 self.pre_genomes = []
                 self.busy = False
                 self.fittest_genome = genome()
                 self.best_fitness_score = 0
                 self.total_fitness_score = 0
                 self.max_generation = max_generation
                 #special variable:
                 #self.tobeEvaluatedSps = []
                 #self.overallSignalProgramms = []
                 #self.NameOfIntersections = {0:'56-1',1:'56-02'}#

        def create_start_populations(self):# think about how to deal with the individual which in reality doesnt exist! random and check , or do a preselection here?
                # default start random population
                #del self.genomes[0:]

                for i in range(self.pop_size):
                         self.genomes.append(genome())#self.genome_len
                #self.generation = 0
                self.best_fitness_score = -99999
                self.total_fitness_score = 0


                #should have one method to generate a candidate for basic senario
        def search_old_solutions(self,HGVInputs):
            # search for best solutions in historic data
            maxOldSolutions = 4

            HGVInputsONo = [0]*len(HGVInputs)
            # saves number of lkws in every link
            for i in range(len(HGVInputsONo)):
                HGVInputsONo[i]= len(HGVInputs[i])

            pickleObjs = []
            pickleObj = []
            #load pickle file, historic data
            try: pickleObjs = pickle.load(open("picklerFile.txt", "r"))
            except:pass
            #sililIndex is the index for comparison traffic situations in oder
            #to find out the best matched situations
            similIndex = [0]*len(pickleObjs)
            #calculate the simularity:
            # TODO threshold of historic data, check computation length
            # test computation time, test correctness
            if len(pickleObjs)>0:
                for i in range(len(pickleObjs)):
                    simil = 0 # comparison index
                    for j in range(len(pickleObjs[i][1])): # just take number of lkw in links
                        maxNV = max(HGVInputsONo[j],pickleObjs[i][1][j])
                        minNV = min(HGVInputsONo[j],pickleObjs[i][1][j])
                        if maxNV!= 0:
                            simil = simil + minNV/maxNV
                    similIndex[i] = simil
            similIndexBackUp = similIndex[:]
            #find the best matched solutions
            if len(pickleObjs)>0:
                for i in range(len(pickleObjs)):
                    if i >= maxOldSolutions:
                        break
                    bestMatchPos = similIndex.index(max(similIndex))
                    bestMatch = pickleObjs[bestMatchPos][1]
                    #print 'bestMatch',bestMatch
                    self.genomes[i].bits = bestMatch
                    similIndex[bestMatchPos] = 0
            #for i in range(len(self.genomes)):
                #print 'self.genomes[i].bits',self.genomes[i].bits
                # TODO write in method
            self.genomes[5].bits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # probably best gnome selected
        def selection(self):
                    # TODO uniform never 1?
                 f_slice = random.uniform(0, 1) * self.total_fitness_score
                 #print 'f_slice', f_slice
                 c_f_slice = 0.0
                 selected_genome = 0
                 for i in range(self.pop_size):
                         c_f_slice = c_f_slice + self.genomes[i].fitness
                         if c_f_slice > f_slice:
                                 selected_genome = i
                                 break
                 return self.genomes[i]

        # return two children for selected mum and dad
        def crossover(self, mum, dad):
                 baby1 = []
                 baby2 = []

                 # probability children equal parents is 1- crosover.rate
                 if (random.uniform(0, 1) > self.crossover_rate):
                         baby1 = mum.bits;
                         baby2 = dad.bits;
                         return baby1, baby2

                 # position from which all bits are changed
                 cp = random.randint(0, self.genome_len - 1)
                 #crossover point selection, for our case need to be restricted
                 #select crossover only between juctions and signal plans
                 #and then transfer to postion of the whole genome
                 #thinking about one or two crossover point?

                 # TODO just change bit units
                 for i in range(cp):
                         baby1.append(mum.bits[i])
                         baby2.append(dad.bits[i])
                 for i in range(cp, self.genome_len):
                         baby1.append(dad.bits[i])
                         baby2.append(mum.bits[i])
                 return baby1, baby2

        def mutate(self, bits):
            #mutate babies
        #considering the same prosilility to be mutated(for all the programms), one position or morem positions mutation?

                if (random.uniform(0, 1) < self.mutation_rate):
                    # chose how many bits mutated ( one or two in common case)
                    digits = random.randint(1,int(math.sqrt(NoOfSignalProgramms)))
                    # get mutation position
                    mPosition = random.randint(0, self.genome_len - 1)
                    # go thorugh bits
                    #
                    for i in range(digits):
                        # TODO always correct, never else?
                        if mPosition<self.genome_len:
                            # check if 0 or 1 mutate
                            bits[mPosition] = int(not bits[mPosition])
                            mPosition = mPosition + 1
                        else:
                            mPosition = 0
                            bits[mPosition] = int(not bits[mPosition])
                            mPosition = mPosition + 1

        def update_fitness_scores(self, overallSignalProgramms,vehcleInputs,HGVInputs):
             self.total_fitness_score = 0
             for i in range(self.pop_size):
                 self.genomes[i].getFitness(overallSignalProgramms,vehcleInputs,HGVInputs)
                 self.total_fitness_score += self.genomes[i].fitness
                 if self.genomes[i].fitness > self.best_fitness_score:
                         self.best_fitness_score = self.genomes[i].fitness
                         self.fittest_genome = self.genomes[i]

        def update_fitness_scores2(self, overallSignalProgramms,vehcleInputs,HGVInputs):
             #self.total_fitness_score = 0
             for i in range(self.pop_size):
                 self.genomes[i].getFitness(overallSignalProgramms,vehcleInputs,HGVInputs)
##                         self.total_fitness_score += self.genomes[i].fitness
##                         if self.genomes[i].fitness > self.best_fitness_score:
##                                 self.best_fitness_score = self.genomes[i].fitness
##                                 self.fittest_genome = self.genomes[i]
        def generation_mix(self,overallSignalProgramms,vehcleInputs,HGVInputs):
            # search for eight best gnome of  the old and new generation

            # get new fitness
            self.update_fitness_scores2(overallSignalProgramms,vehcleInputs,HGVInputs)

            two_generations = []
            two_generations = self.genomes + self.pre_genomes
            fitness_two_gens = []
            #print '1'
            # save all fitness values
            for i in range(len(two_generations)):
                fitness_two_gens.append(two_generations[i].fitness)
            mix_gens = []
            pop = len(two_generations)

            # not more then pop_size ( eight)
            while (pop > self.pop_size):
                # delete lowest fitness valued gnome
                min_pos = fitness_two_gens.index(min(fitness_two_gens))
                del fitness_two_gens[min_pos]
                del two_generations[min_pos]
                pop = pop - 1

            # check
            if len(two_generations)==self.pop_size:
                self.genomes = two_generations

            # save total fitness score
            pre_total_fitness_score = self.total_fitness_score
            self.total_fitness_score = 0

            # get new total fitness score
            for i in range(self.pop_size):
                 self.total_fitness_score += self.genomes[i].fitness
                 if self.genomes[i].fitness > self.best_fitness_score:
                         self.best_fitness_score = self.genomes[i].fitness
                         self.fittest_genome = self.genomes[i]

        def inbreedingRate(self,mum,dad):
            # compare mum and dad if similiar
            # TODO number of bits = really the int(square)?
            NoOfDigits = int(math.sqrt(NoOfSignalProgramms))
            # TODO int works fore uneven, test
            NoOfSP = int(self.genome_len/NoOfDigits)
            iRate = 0
            # compares bit units
            for i in range(NoOfSP):
                diff = 0
                for j in range(NoOfDigits):
                    if mum.bits[i*NoOfDigits+j] != dad.bits[i*NoOfDigits+j]:
                        diff = 1
                        break
                if diff == 0:
                    iRate = iRate +1
            return iRate

        def epoch(self, overallSignalProgramms,vehcleInputs,HGVInputs):

             if len(self.pre_genomes)==0:
                 self.update_fitness_scores(overallSignalProgramms,vehcleInputs,HGVInputs)

             new_babies = 0
             baby_genomes = []

             while (new_babies < self.pop_size):
                     baby1 = genome()
                     baby2 = genome()
                     mum = self.selection()
                     #print 'mama is: ', mum.spIxs
                     #inzucht koefficient berechenen
                     dad = self.selection()

                     # checks if mum and dad ar similiar
                     MaxiRate = int(self.genome_len/int(math.sqrt(NoOfSignalProgramms))) # numbers of bit units
                     iRate = self.inbreedingRate(mum,dad)

                     iteTime = 0
                     # 10 right threshold?
                     while (iteTime<10):
                        if iRate>=MaxiRate-1: # mum and dad the same
                            # (memory index) not select same dad?
                            dad = self.selection()
                            iRate = self.inbreedingRate(mum,dad)
                            iteTime = iteTime + 1
                        else:
                            break

                     baby1.bits, baby2.bits = self.crossover(mum, dad)
                     self.mutate(baby1.bits)
                     self.mutate(baby2.bits)
                     baby_genomes.append(baby1)
                     baby_genomes.append(baby2)
                     new_babies = new_babies + 2
             self.pre_genomes = self.genomes
             self.genomes = baby_genomes
             self.generation_mix(overallSignalProgramms,vehcleInputs,HGVInputs)

             self.generation += 1
             if self.generation >= self.max_generation:
                     self.busy = False

        def start(self,HGVInputs):
            #if we should check the old solutions or just start from random pop
                 checkOldSolution = True
                 self.busy = True
                 # creates randomly eight popolations
                 self.create_start_populations()

                 if checkOldSolution:
                     self.search_old_solutions(HGVInputs)

        def get_best_genome(self):
                return self.fittest_genome.bits
        #def get_best_variable(self):
                #return self.bin2int(self.fittest_genome.bits)
        def get_best_fitness_Value(self):
            return self.fittest_genome.fitness

        def get_max_value(self,overallSignalProgramms):

            maxValue = self.fittest_genome.decode(overallSignalProgramms)
            return maxValue
        def get_first_cycle(self):
            allSpIxs = self.fittest_genome.spIxs
            firstCycleSpIxs = []
            for i in range(NoOfIntersectionsOverall):
                firstCycleSpIxs.append(allSpIxs[i*NoOfCycles])
            return firstCycleSpIxs

def maintest(vehcleInputs,HGVInputs):
        print "-----------------"
        print 'start GA'
        # load
        overallSps = signalProgramms()
        # read from input data
        overallSps.readSignalProgramms(path)
        #ctm = TrafficModels.pretest()
        #print 'overallSignalProgramms', overallSps.overallSignalProgramms[3][0].signalPlans
        overallFitness = []
        bestFitness = []
        # start generic algo with 8 individuals, populations size
        #first generation, generate ga object, search for similiar historic generation
        testga = ga(pop_size = 8)
        testga.start(HGVInputs)

        # creates next generations
        while testga.busy:
                 testga.epoch(overallSps.overallSignalProgramms,vehcleInputs,HGVInputs)
                 #print 'check 3'
                 bestFitness.append(testga.fittest_genome.fitness)
                 overallFitness.append(testga.total_fitness_score)

        # print and return

        print "overallFitness: " ,overallFitness
        print 'the best Fitness:',bestFitness
        print "The best genome is: "
        bestGenomeBits = testga.get_best_genome()
        print testga.get_best_genome()
        testga.fittest_genome.decode(overallSps.overallSignalProgramms)
        print 'fittest signal programms:',testga.fittest_genome.spIxs
        firstCycleSpIxs = testga.get_first_cycle()
        print 'the best fitness value:'
        bestFitnessValue = testga.get_best_fitness_Value()
        print testga.get_best_fitness_Value()
        return firstCycleSpIxs,bestGenomeBits,bestFitnessValue
        #print'  '
        #print'  '
        #print "The variable is: %d" % testga.get_best_variable()
        #maxValue = testga.get_max_value(overallSps.overallSignalProgramms)
        #print "The max value is ", maxValue
        del testga
        print "-----------------"

if __name__ == '__main__':
         maintest()
