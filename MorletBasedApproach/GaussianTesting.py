import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SamUtils import *

'''
Experimenting with using Gaussians instead of Morlets. This will be helpful for working with Sam as we progress. 
'''
def PlotCenteredGaussian(amp, x, sig):
    wave = np.array(range(0, x))
    gaussian = generateGaussian(amp, len(wave) / 2, sig, wave)
    fig, ax = plt.subplots()
    ax.plot(gaussian)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()

def main():
    PlotCenteredGaussian(10, 800, 100)



if __name__ == '__main__':
    main()