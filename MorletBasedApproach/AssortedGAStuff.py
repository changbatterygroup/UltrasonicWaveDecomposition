import copy
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

def CreateFirstGen(ref, size=20):
    xStart = int(ref.GetStart())
    xEnd = int(ref.GetEnd())
    timeArr = ref.GetTimeArr()
    gen1 = []

    for i in range(0, size):
        center = ref.GetStartXCoord() * ((i / 300) + 1)
        gen1.append(GeneratedWave(1, center, timeArr))

    return gen1

def GALoop(ref, genSize=20):
    xTot = int(ref.GetFullLength())
    xStart = int(ref.GetStart())
    xEnd = int(ref.GetEnd())
    singleGen = CreateFirstGen(ref, genSize)
    prevGen = []
    # Determine most fit individual from previous gen
    for i, ind in enumerate(singleGen):
      #  ind.PlotMorletMatrix()
        ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
    singleGen.sort(key=lambda x: x.score, reverse=True)
    prevGen = singleGen[:5]
    print("Most fit gen1:", singleGen[0].tag)
    singleGen[0].PlotMorletMatrix()

    for i in range(0, 100):
        HighScorers = singleGen[:5]
        if HighScorers[0].score > 999:
            print("Close match found!")
            break
        singleGen = []
        mutantID = i * 1000
        firstMutant = GeneratedWave(1, ref.GetStartXCoord(), ref.GetTimeArr())
        firstMutant.NotSuperEfficentFitTest(ref, xStart, xEnd)
        mutatedInd = copy.deepcopy(firstMutant).Mutate(0, mutantID, ref)
        singleGen.append(mutatedInd)
        for j in range(0, 5):
            for k in range(0, 5):
                mutantID = (i * 1000) + (j * 10) + k
                mutatedInd = copy.deepcopy(HighScorers[k]).Mutate(0, mutantID, ref)
                singleGen.append(mutatedInd)
        for l, ind in enumerate(singleGen):
            ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
            print(f"Tag:", ind.tag)
        singleGen.sort(key=lambda x: x.score, reverse=True)
        for index in range(0, 5):
            if prevGen[index].score > singleGen[index].score:
                singleGen[index] = prevGen[index]
        prevGen = singleGen[:5]
        if i == 99:
            for ind in singleGen[:3]:
                ind.PlotMorletMatrix()


def FitnessTest(individual : GeneratedWave, reference : ReferenceWave):

    individual_norm = individual.MorletMatrix / np.max(np.abs(individual))
    reference_norm = reference / np.max(np.abs(reference))

    corr_coef = np.max(np.abs(correlate(individual_norm, reference_norm)))

    mse = np.mean((individual_norm - reference_norm)**2)

    fitness = corr_coef - mse

    return fitness