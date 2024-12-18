from fontTools.merge.util import first

from Morlet import *
import numpy as np
import matplotlib.pyplot as plt

'''
Class for an automatically generated wave. 
'''


class GeneratedWave:
    def __init__(self, layers, xLen, firstX, lastX, refStart=0):
        self.lastX = lastX
        self.firstX = firstX
        self.xLen = xLen
        self.layers = layers
        self.refStart = refStart
        self.MorletMatrix, self.MorletArr = self.GenerateMorletMatrix(layers, xLen, firstX, lastX, refStart)
        self.MorSum = self.CombineMorlets()
        self.score = 0
        self.tag = "Made from constructor"


    def GenerateMorletMatrix(self, layers, xLen, firstX, lastX, refStart):
        morMatrix = np.zeros((layers, xLen))
        #np.array((range(refStart, refStart + xLen), (range(1, layers)))))
        morArr = []
        for n in range(0, layers):
           # width = (lastX - firstX)/(layers + 2)
            morArr.append(Morlet(firstX, 5, np.linspace(refStart, refStart + xLen, 1000), 100))

            morMatrix[n, :] = morArr[n].wavelet
        return morMatrix, morArr

    def PlotMorletMatrix(self):
        fig, ax = plt.subplots()
        for c, wave in enumerate(self.MorletMatrix):
            ax.plot(wave)
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
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].ShrinkLeft()
                mutatedWave.tag = "Generated from mutation function"
            #    self.MorletMatrix, self.MorletArr = mutatedWave.GenerateMorletMatrix(mutatedWave.layers, mutatedWave.xLen, mutatedWave.firstX, mutatedWave.lastX, mutatedWave.refStart)
                return mutatedWave
            case 2:
                mutatedWave = self
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].IncreaseAmplitude(2)
                mutatedWave.tag = "Generated from mutation function"

              #  self.MorletMatrix, self.MorletArr = mutatedWave.GenerateMorletMatrix(mutatedWave.layers, mutatedWave.xLen,
                                                           #         mutatedWave.firstX, mutatedWave.lastX,
                                                            #        mutatedWave.refStart)
                return mutatedWave
            case 3:
                mutatedWave = self
                mutatedWave.MorletArr[index] = mutatedWave.MorletArr[index].ShiftOmega(10, 10)
                mutatedWave.tag = "Generated from mutation function"

           #     self.MorletMatrix, self.MorletArr = mutatedWave.GenerateMorletMatrix(mutatedWave.layers, mutatedWave.xLen,
                                                             #       mutatedWave.firstX, mutatedWave.lastX,
                                                            #        mutatedWave.refStart)

                return mutatedWave


