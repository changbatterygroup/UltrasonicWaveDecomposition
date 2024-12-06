from fontTools.merge.util import first

from Morlet import *
import numpy as np
import matplotlib.pyplot as plt

class GeneratedWave:
    def __init__(self, layers, xLen, firstX, lastX):
        self.lastX = lastX
        self.firstX = firstX
        self.xLen = xLen
        self.layers = layers
        self.MorletMatrix, self.MorletArr = self.GenerateMorletMatrix(layers, xLen, firstX, lastX)
        self.MorSum = self.CombineMorlets()

    def GenerateMorletMatrix(self, layers, xLen, firstX, lastX):
        morMatrix = np.zeros((layers, xLen))
        morArr = []
        for n in range(0, layers):
            width = (lastX - firstX)/(layers + 2)
            morArr.append(Morlet((firstX + (width * n)), 5, np.linspace(0, xLen, xLen), width / 5))
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

    def Mutate(self, index, mutation):
        match mutation:
            case 'ShrinkLeft':
                self.MorletArr[index].ShrinkLeft()
                self.GenerateMorletMatrix(self.layers, self.xLen, self.firstX, self.lastX)
            case 'IncreaseAmplitude':
                self.MorletArr[index].IncreaseAmplitude(2)
                self.GenerateMorletMatrix(self.layers, self.xLen, self.firstX, self.lastX)
            case 'ShiftOmega':
                self.MorletArr[index].ShiftOmega(10, 10)
                self.GenerateMorletMatrix(self.layers, self.xLen, self.firstX, self.lastX)
