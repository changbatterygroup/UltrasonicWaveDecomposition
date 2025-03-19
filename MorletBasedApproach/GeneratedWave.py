from random import choice

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
 - layers: Number of layers
 - MorletArr: Array of all morlets in the wave
 - MorSum: Linear combination of all morlets
 - score: fitness score
 - tag: Associated string for debugging purposes
 
 Constructor values - 
 - center: Center position of the wave
            Pass to GenerateMorletMatrix
 - TimeArr: reference wave's time array
            Pass to GenerateMorletMatrix
 - layers: Number of layers
           Set class member
 - tag(optional): associated string for debugging
                  Set class member
'''

class GeneratedWave:
    def __init__(self, layers, center, timeArr, tag=""):
        self.layers = layers
        self.MorletArr = self.GenerateMorletMatrix(center, timeArr)
        self.MorSum = self.CombineMorlets()
        self.score = 0
        self.tag = "Made from constructor"
        self.FitnessDetails = {'extrema': False, 'extrema_diff': 0, 'invert': False, 'time': False, 'time_diff': 0, 'voltage': False, 'voltage_diff': 0, 'mutations': [1, 2, 3, 4, 5, 6, 7, 8, 9]}

    def GenerateMorletMatrix(self, center, timeArr):
        morArr = []
        for n in range(0, self.layers):
            newMor = Morlet(center, 20, timeArr, 50)
            morArr.append(newMor)
        return morArr

    def PlotMorletMatrix(self):
        fig, ax = plt.subplots()
        ax.set_xlim([12100, 14300])
        ax.set_ylim([-20, 20])
        for c, wave in enumerate(self.MorletArr):
            ax.plot(wave.total_travel, wave.wavelet)
        plt.show()

    def CombineMorlets(self):
        waveletArr = []
        for wave in self.MorletArr:
            waveletArr.append(wave.wavelet)
        mor_sum = np.sum(waveletArr, axis=0)
        return mor_sum

    def SetScore(self, score):
        self.score = score

    def Mutate(self, index, mutantID, reference):
        mutation = choice(self.FitnessDetails['mutations'])
        print(f"Mutation ({mutantID}): {mutation}")
        match mutation:
            case 1:
                mutatedWave = self
                mutatedWave.MorletArr[index] = self.MorletArr[index].ShrinkLeft()
                mutatedWave.tag = mutantID
                return mutatedWave
            case 2:
                mutatedWave = self
                randAmount = Random().randint(1, 5)
                mutatedWave.MorletArr[index] = self.MorletArr[index].IncreaseAmplitude(self.FitnessDetails['voltage_diff'])
                mutatedWave.tag = mutantID
                return mutatedWave
            case 3:
                mutatedWave = self
                randAmount = Random().randint(1, 5)
                mutatedWave.MorletArr[index] = self.MorletArr[index].DecreaseAmplitude(self.FitnessDetails['voltage_diff'])
                mutatedWave.tag = mutantID
                return mutatedWave

            case 4:
                mutatedWave = self
                randAmount = Random().randint(5, 50)
                randDir = Random().randint(1, 2)
                mutatedWave.MorletArr[index] = self.MorletArr[index].ShiftOmega(randDir, randAmount)
                mutatedWave.tag = mutantID
                return mutatedWave

            case 5:
                mutatedWave = self
                mutatedWave.MorletArr[index] = self.MorletArr[index].ShrinkRight()
                mutatedWave.tag = mutantID
                return mutatedWave

            case 6:
                mutatedWave = self
                mutatedWave.MorletArr[index] = self.MorletArr[index].ApplyParabola(reference)
                mutatedWave.tag = mutantID
                return mutatedWave

            case 7:
                mutatedWave = self
                mutatedWave.MorletArr[index] = self.MorletArr[index].ApplyNegativeParabola(reference)
                mutatedWave.tag = mutantID
                return mutatedWave

            case 8:
                mutatedWave = self
                mutatedWave.MorletArr[index] = self.MorletArr[index].ShaveEnd(reference)
                mutatedWave.tag = mutantID
                return mutatedWave

            case 9:
                mutatedWave = self
                mutatedWave.MorletArr[index] = self.MorletArr[index].ShaveFront(reference)
                mutatedWave.tag = mutantID
                return mutatedWave

    def NotSuperEfficentFitTest(self, reference: ReferenceWave, xStart, xEnd):
        # Tests for: Equality and proximity to number of local extrema, max y, min y, first x, and last x
        equality_score = 0
        extrema_score = 0
        voltage_score = 0
        time_score = 0
        score = 0

        # Equality test
        for i, j in enumerate((range(xStart, xEnd, 2))):
            if j < xEnd:
                indVal = math.floor(self.MorletArr[0].wavelet[i])
                refVal = math.floor(reference.waveArr['voltage'][i])
                if indVal == refVal and indVal != 0 and refVal != 0:
                    equality_score += (1 - abs(self.MorletArr[0].wavelet[i] - reference.waveArr['voltage'][i]))
                elif indVal != refVal and indVal != 0 and refVal != 0:
                    equality_score -= 2

        # Extrema Test
        ref_minima = reference.num_local_minima
        ref_maxima = reference.num_local_maxima
        ind_minima = Wave.FindLocalMinima(self.MorletArr[0].wavelet)
        ind_maxima = Wave.FindLocalMaxima(self.MorletArr[0].wavelet)
        if ref_maxima == ind_maxima and ref_minima == ind_minima:
            self.FitnessDetails['extrema'] = True
        elif ref_maxima != ind_maxima or ref_minima != ind_minima:
            self.FitnessDetails['extrema'] = False
        elif ref_maxima == ind_minima and ref_minima == ind_maxima:
            self.FitnessDetails['invert'] = True

        self.FitnessDetails['extrema_diff'] = (ref_minima - ind_minima) + (ref_maxima - ind_maxima)
        extrema_score = 5*(5 - ((abs(ref_minima - ind_minima)) + (abs(ref_maxima - ind_maxima))))

        volt_max_temp_score = 0
        for volt in reference.maxima:
            volt_max_temp_score += (abs(reference.waveArr['voltage'][volt] - self.MorletArr[0].wavelet[volt]))
        extrema_score += (100 - (5 * volt_max_temp_score))

        volt_min_temp_score = 0
        for volt in reference.minima:
            volt_min_temp_score += (abs(reference.waveArr['voltage'][volt] - self.MorletArr[0].wavelet[volt]))
        extrema_score += (100 - (5 * volt_min_temp_score))

        # Voltage Test
        ref_max = reference.max_voltage
        ref_min = reference.min_voltage
        ind_max = Wave.FindMaxY(self.MorletArr[0].wavelet)
        ind_min = Wave.FindMinY(self.MorletArr[0].wavelet)

        self.FitnessDetails['voltage_diff'] = ref_max / ind_max
        self.FitnessDetails['voltage'] = self.FitnessDetails['voltage_diff'] == 1
        voltage_score = 50 - ((abs(ref_max - ind_max)) + (abs(ref_min - ind_min)))

        # Time Test
        ref_start = reference.first_time_index
        ref_stop = reference.last_time_index
        ind_start = Wave.FindFirstX(self.MorletArr[0].wavelet)
        ind_stop = Wave.FindLastX(self.MorletArr[0].wavelet)

        self.FitnessDetails['time_diff'] = (ref_start - ind_start)
        self.FitnessDetails['time'] = math.floor(self.FitnessDetails['time_diff']) == 0
        time_score = 50 - ((abs(ref_start - ind_start)) + (abs(ref_stop - ind_stop)))

        score = equality_score + extrema_score + voltage_score + time_score
        self.SetScore(score)
        self.SetMutations()
        print(score)

    def SetMutations(self):
        if self.FitnessDetails['extrema'] and 8 in self.FitnessDetails['mutations'] : self.FitnessDetails['mutations'].remove(8)
        elif not self.FitnessDetails['extrema'] and 8 not in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].append(8)
        if self.FitnessDetails['voltage'] and 2 in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].remove(2)
        elif not self.FitnessDetails['voltage'] and 2 not in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].append(2)
        if self.FitnessDetails['voltage'] and 3 in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].remove(3)
        elif not self.FitnessDetails['voltage'] and 3 not in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].append(3)
        if self.FitnessDetails['time'] and 4 in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].remove(4)
        elif not self.FitnessDetails['time'] and 4 not in self.FitnessDetails['mutations']: self.FitnessDetails['mutations'].append(4)

        if self.FitnessDetails['invert']:
            self.FitnessDetails['mutations'].clear()
            self.FitnessDetails['mutations'].append(4)

