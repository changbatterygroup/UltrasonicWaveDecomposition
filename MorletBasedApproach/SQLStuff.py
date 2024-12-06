import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from tabulate import tabulate

data_dir = "/Users/michael/OneDrive - Drexel University/Documents - Chang Lab/General/Group/Data/Ultrasound/Layered Electrode Study/"
file = "20240216_WC_GJ_Al-n=1_dur15_del1p5_50MHz.sqlite3"


def PlotWave(index, file):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    query = """SELECT name FROM sqlite_master WHERE type='table'"""
    cursor.execute(query)
    table = cursor.fetchall()
    query = f'SELECT * FROM "{table[0][0]}"'
    df = pd.read_sql(sql=query, con=connection)
    #print(tabulate(df, headers='keys', tablefmt='psql'))
    amps = df.loc[index, 'amps'].strip('[]').split(',') #['amps'].loc(df.index[0]))
    times = range(0, len(amps))
    print(df.loc[0, 'time']) #.loc(df.index[0]))
    return amps, times



def generateGaussian(a, mu, sigma, times):
    return a * np.exp((-1 * (times - mu) ** 2) / (2 * sigma ** 2))

def generateGaussianMatrix(aArr, muArr, times, sigma, sigmaTolerance = 3):

    # add a check to make sure len(aArr)==len(muArr)
    if len(aArr) != len(muArr):
        print("generateGaussianSum: aArr and muArr have different lengths. Sum failed")
        # todo: this should be turned into an error
        return -1

    outputMatrix = np.zeros((len(muArr), len(times)))

    # iterate through gaussians
    for i in range(len(muArr)):

        # create a list of times within the sigma tolerance window
        currentMu = muArr[i]
        windowMin = currentMu - (sigma * sigmaTolerance)
        windowMax = currentMu + (sigma * sigmaTolerance)
        windowIndices = np.argwhere((windowMin < times) & (times < windowMax)).flatten()
        # find window index min and max so that assignment can be done by slices (faster)
        indMin = int(windowIndices[0])
        indMax = int(windowIndices[-1])
        timeWindow = times[indMin:indMax]

        # calculate that gaussian values within the time window
        gaussianVals = generateGaussian(aArr[i], currentMu, sigma, timeWindow)

        # assign slice of output matrix as coefficients
        outputMatrix[i, indMin:indMax] += gaussianVals

    return outputMatrix

'''
def printGausMatrix():
    wave, time = GeneratePlot()
    for waves in wave:
        for subwave in waves:
            print(subwave)
    print('\n')
    print("TIMES:")
    waveLen = len(wave[0])
    print(waveLen)
    timeLen = len(time)
    print(timeLen)
    gaussian = generateGaussianMatrix(wave[0], np.zeros(waveLen), time, 180)
    print(len(gaussian))
    for gaus in gaussian:
        plt.plot(gaus)
    print(gaussian[0])
    # plt.show()
#  for row in gaussian:
#    print(row)
'''

def main():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    wave = np.zeros((31, 800))
    time = range(0, 800)
    for i in range(0, 30):
        amps, times = (PlotWave(i, data_dir + file))
        wave[i, :] = amps
        ax1.plot(wave[i, :])
    ax2.plot(wave[0, :])
    plt.show()


if __name__ == '__main__':
    main()