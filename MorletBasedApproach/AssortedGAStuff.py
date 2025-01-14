import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import Reference

from MaterialBasedApproach.Material import *
from MorletBasedApproach.Morlet import Morlet
from GeneratedWave import *
from ReferenceWave import *
import numpy as np
from scipy.signal import correlate
import random

'''
Genetic algorithm specific code, including fitness tests, mutation generation, etc.
'''

def CreateFirstGen(ref, size=5):
    xTot = int(ref.GetFullLength())
    xStart = int(ref.GetStart())
    xEnd = int(ref.GetEnd())

    gen1 = []
    for i in range(0, size):
        firstX = ref.GetStartXCoord() * ((i / 100) + 1)
                #xStart + ((xTot / (size + 1)) * (i + 1)))
        lastX = ref.GetEndXCoord()
        gen1.append(GeneratedWave(1, int(((xEnd + 2) - xStart) / 2), firstX, lastX, xStart, xEnd))
                  #  Morlet(omega, 2, np.linspace(xStart, xEnd, xTot), 100))

    highScoreInd = 0
    for i, ind in enumerate(gen1):
        ind.PlotMorletMatrix()
        ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
        if gen1[i].score > gen1[highScoreInd].score:
            highScoreInd = i

    return gen1

def GALoop(ref, genSize=5):
    xTot = int(ref.GetFullLength())
    xStart = int(ref.GetStart())
    xEnd = int(ref.GetEnd())
    singleGen = CreateFirstGen(ref, genSize)

    highScoreInd = 0
    for i, ind in enumerate(singleGen):
        ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
        if singleGen[i].score > singleGen[highScoreInd].score:
            highScoreInd = i
    singleGen[highScoreInd].PlotMorletMatrix()

    for i in range(0, 80):
        HighScorer = singleGen[highScoreInd]
        if HighScorer.score > 999:
            print("Close match found!")
            break
        singleGen.clear()
        for j in range(0, genSize):
            firstX = HighScorer.firstX
            lastX = firstX + 100
            mutatedInd = HighScorer.Mutate(0, random.Random().randint(2, 4))
            print(mutatedInd.tag)
            singleGen.append(mutatedInd)
        for k, ind in enumerate(singleGen):
            ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
            print(ind.tag)
            if singleGen[k].score > singleGen[highScoreInd].score:
                highScoreInd = k
        if i % 10 == 0:
            singleGen[highScoreInd].PlotMorletMatrix()


def FitnessTest(individual : GeneratedWave, reference : ReferenceWave):

    individual_norm = individual.MorletMatrix / np.max(np.abs(individual))
    reference_norm = reference / np.max(np.abs(reference))

    corr_coef = np.max(np.abs(correlate(individual_norm, reference_norm)))

    mse = np.mean((individual_norm - reference_norm)**2)

    fitness = corr_coef - mse

    return fitness