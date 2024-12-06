import numpy as np


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
