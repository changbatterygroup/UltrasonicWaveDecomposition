import random

from fontTools.merge.util import first

from Morlet import *
import numpy as np
import matplotlib.pyplot as plt
from ReferenceWave import *
from random import Random
import math

'''
Class for an automatically generated wave. 
'''

# @TODO: time array


# @TODO: clean up and document these class members. A lot of them are extremely similar and their specifics need to be more clear.
'''
members - 
Actually maybe a 
 - One for first value of actual wave
 - One for first x (time)
 - One for last x (time)
 - Morlet matrix - linear combo of all morlets x time
    - Function to derive time(?)
 - Morlet array - array of individual morlets 
 - 
 
 
lastX
firstX
xLen
layers
refStart
xEnd
MorletMatrix
MorletArr
TimeArr
MorSum
score
tag
'''

class GeneratedWave:
    def __init__(self, layers, xLen, firstX, lastX, refStart=0, xEnd=1000):
        self.lastX = lastX
        self.firstX = firstX
        self.xLen = xLen
        self.layers = layers
        self.refStart = refStart
        self.xEnd = xEnd
        self.MorletMatrix, self.MorletArr, self.TimeArr = self.GenerateMorletMatrix(layers, xLen, firstX, lastX, refStart, xEnd)
        self.MorSum = self.CombineMorlets()
        self.score = 0
        self.tag = "Made from constructor"


    def GenerateMorletMatrix(self, layers, xLen, firstX, lastX, refStart, xEnd):
        morMatrix = np.zeros((layers, xLen))
        #np.array((range(refStart, refStart + xLen), (range(1, layers)))))
        morArr = []
        for n in range(0, layers):
           # width = (lastX - firstX)/(layers + 2)
            timeArr = np.linspace(refStart, xEnd, 1000)
            morArr.append(Morlet(firstX, 20, timeArr, 50))
                # refStart, refStart + xLen, 1000), 50))

            morMatrix[n, :] = morArr[n].wavelet
        return morMatrix, morArr, timeArr

    def RegenerateMatrix(self):
        for n in range(0, self.layers):
            self.MorletMatrix[n, :] = self.MorletArr[n].wavelet


    def PlotMorletMatrix(self):
        fig, ax = plt.subplots()
        ax.set_xlim([12100, 14300])
        ax.set_ylim([-20, 20])
        for c, wave in enumerate(self.MorletMatrix):
            ax.plot( self.TimeArr, wave)
        plt.show()

    def CombineMorlets(self):
        mor_sum = np.sum(self.MorletMatrix, axis=0)
        return mor_sum

    def SetScore(self, score):
        self.score = score

    def Mutate(self, index, mutation):
        match mutation:
            case 1:
                mutatedWave = self
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].ShrinkLeft(self.refStart, self.refStart + self.xLen)
                mutatedWave.RegenerateMatrix()
                mutatedWave.tag = "Generated from mutation function"
            #    self.MorletMatrix, self.MorletArr = mutatedWave.GenerateMorletMatrix(mutatedWave.layers, mutatedWave.xLen, mutatedWave.firstX, mutatedWave.lastX, mutatedWave.refStart)
                return mutatedWave
            case 2:
                mutatedWave = self
                randAmount = Random().randint(1, 5)
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].IncreaseAmplitude(randAmount / 100)
                mutatedWave.tag = "Generated from mutation function"

              #  self.MorletMatrix, self.MorletArr = mutatedWave.GenerateMorletMatrix(mutatedWave.layers, mutatedWave.xLen,
                                                           #         mutatedWave.firstX, mutatedWave.lastX,
                                                            #        mutatedWave.refStart)
                return mutatedWave
            case 3:
                mutatedWave = self
                randAmount = Random().randint(1, 5)
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].DecreaseAmplitude(randAmount / 100)
                mutatedWave.tag = "Generated from mutation function"
                return mutatedWave

            case 4:
                mutatedWave = self
                randAmount = Random().randint(10, 50)
                randDir = Random().randint(1, 2)
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].ShiftOmega(randDir, randAmount)
                mutatedWave.tag = "Generated from mutation function"
           #     self.MorletMatrix, self.MorletArr = mutatedWave.GenerateMorletMatrix(mutatedWave.layers, mutatedWave.xLen,
                                                             #       mutatedWave.firstX, mutatedWave.lastX,
                                                            #        mutatedWave.refStart)
                return mutatedWave

    def NotSuperEfficentFitTest(self, reference: ReferenceWave, xStart, xEnd):
        score = 0
        for i, j in enumerate((range(xStart, xEnd, 2))):
            if j < xEnd:
                indVal = math.floor(self.MorletMatrix[0][i])
                refVal = math.floor(reference.waveArr['voltage'][i])
                if indVal == refVal and indVal != 0 and refVal != 0:
                    score += 1
        self.SetScore(score)
        print(score)


