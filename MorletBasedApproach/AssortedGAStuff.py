import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import Reference

from MaterialBasedApproach.Material import *
from MorletBasedApproach.Morlet import Morlet
from GeneratedWave import *
from ReferenceWave import *
import numpy as np
from scipy.signal import correlate


def FitnessTest(individual, reference):

    individual_norm = individual / np.max(np.abs(individual))
    reference_norm = reference / np.max(np.abs(reference))

    corr_coef = np.max(np.abs(correlate(individual_norm, reference_norm)))

    mse = np.mean((individual_norm - reference_norm)**2)

    fitness = corr_coef - mse

    return fitness