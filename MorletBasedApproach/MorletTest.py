import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import Reference

from MaterialBasedApproach.Material import *
from MorletBasedApproach.Morlet import Morlet
from GeneratedWave import *
from ReferenceWave import *
import numpy as np
from scipy.signal import correlate
from AssortedGAStuff import *


def Test():
    TestMor = Morlet(5, 2, np.linspace(-10, 10, 1000), 2)
    TestMor.GraphMorlet(1)

    TestWave = GeneratedWave(5, 800, 200, 600)
    TestWave.PlotMorletMatrix()
    SquishedArr = TestWave.CombineMorlets()
    fig, ax = plt.subplots()
    ax.plot(SquishedArr)
    plt.show()
    TestWave.Mutate(0, 'ShiftOmega')
    SquishedArr = TestWave.CombineMorlets()
    fig, ax = plt.subplots()
    ax.plot(SquishedArr)
    plt.show()

    TestRef = ReferenceWave()
    TestRef.PlotWave()


def main():
    Test()


if __name__ == '__main__':
    main()