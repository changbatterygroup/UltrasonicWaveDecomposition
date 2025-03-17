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

def CreateFirstGen(ref, size=5):
    xStart = int(ref.GetStart())
    xEnd = int(ref.GetEnd())
    timeArr = ref.GetTimeArr()
    gen1 = []

    for i in range(0, size):
        center = ref.GetStartXCoord() * ((i / 100) + 1)
        gen1.append(GeneratedWave(1, center, timeArr))

    return gen1

def GALoop(ref, genSize=5):
    xTot = int(ref.GetFullLength())
    xStart = int(ref.GetStart())
    xEnd = int(ref.GetEnd())
    singleGen = CreateFirstGen(ref, genSize)

    # Determine most fit individual from previous gen
    highScoreInd = 0
    for i, ind in enumerate(singleGen):
      #  ind.PlotMorletMatrix()
        ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
        if singleGen[i].score > singleGen[highScoreInd].score:
            highScoreInd = i
    print("Most fit gen1:", highScoreInd)
    singleGen[highScoreInd].PlotMorletMatrix()

    for i in range(0, 80):
        HighScorer = singleGen[highScoreInd]
        if HighScorer.score > 999:
            print("Close match found!")
            break
        singleGen = []
        for j in range(0, genSize):
            mutation = random.Random().randint(1, 4)
            mutantID = (i*100) + (j * 10) + mutation
            mutatedInd = copy.deepcopy(HighScorer).Mutate(0, mutation, mutantID)
            singleGen.append(mutatedInd)
            print(f"Mutation ({j}): {mutation}")
        for k, ind in enumerate(singleGen):
            ind.NotSuperEfficentFitTest(ref, xStart, xEnd)
            print(f"Tag:", ind.tag)
            if singleGen[k].score > singleGen[highScoreInd].score:
                highScoreInd = k
        if i % 10 == 0:
            for ind in singleGen:
                ind.PlotMorletMatrix()
        print(f"Most fit gen{i}: {highScoreInd}")


def FitnessTest(individual : GeneratedWave, reference : ReferenceWave):

    individual_norm = individual.MorletMatrix / np.max(np.abs(individual))
    reference_norm = reference / np.max(np.abs(reference))

    corr_coef = np.max(np.abs(correlate(individual_norm, reference_norm)))

    mse = np.mean((individual_norm - reference_norm)**2)

    fitness = corr_coef - mse

    return fitness