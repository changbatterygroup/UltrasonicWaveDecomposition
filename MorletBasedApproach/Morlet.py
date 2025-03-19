import math

import numpy as np
import matplotlib.pyplot as plt
import random
import Wave

'''
General class for morlet definition
'''


'''
@TODO: Implement GA (Basic addition)
 - Extract time scale from reference
 - First order of business is aligning the generated morlets with the reference. 
 - visualize (plot each generation)
 - So step one: Generate 5 morlets with various start times (this example takes the form of a morlet so just operate on one)
 - In theory, the one closest aligned with reference should be the most fit. We'll see. 
 NOTE: May need to alter morlet generation to fit the pickle formatting. Again, we'll see. 
 
 
 Make sure the wavelet addition function works
'''


class Morlet:
    """
    Summary:

    Description:
    """
    def __init__(self, omega, amp, total_travel, width):
        """
        Summary:

        Description:

        :param omega: Center of the morlet
        :param int amp: Amplitude at center of morlet
        :param total_travel: Evenly spaced array over the travel time of the reference
        :type total_travel: np.linspace
        :param int width: Width. Duh.
        """
        self.omega = omega
        self.total_travel = total_travel
        self.width = width
        self.amp = amp
        self.wavelet = self.GenerateMorlet(omega, amp, total_travel, width, 1)

    '''
    omega - initial center of the morlet (corresponds to total # of morlets)
    total_travel - np.linspace representing the total travel time of the reference
    '''
    def GenerateMorlet(self, omega, amp, total_travel, width, alg):
        """

        :param omega:
        :param amp:
        :param total_travel:
        :param width:
        :param alg:
        :return:
        """
        match alg:
            case 1:
                return amp * np.cos(5 * (total_travel - omega) / width) * np.exp(-((total_travel - omega) / width) ** 2 / 2) # Change to sin
            case 2:
                return np.real(np.exp(1j*(omega*total_travel)/width) * np.exp(-0.5*(total_travel/width)**2) * np.pi**(-0.25) * np.sqrt(1/width))

    def GraphMorlet(self, index):
        """

        :param index:
        :return:
        """
        fig, ax = plt.subplots()
        ax.plot(self.total_travel, self.wavelet, label=f"Constituent #{index}")
        plt.title(f"Constituent #{index}")
        plt.show()

    def GetStartIndex(self):
        index = np.argmax((self.wavelet > 0.5) | (self.wavelet < -0.5))
        return index - 10

    def GetEndIndex(self):
        indices = np.where((self.wavelet > 0.5) | (self.wavelet < -0.5))[0]
        index = indices[-1] if indices.size > 0 else -1
        return index + 10

    #TODO: Symmetric modulations
    def IncreaseAmplitude(self, amount):
        """

        :param amount:
        :return:
        """
        newMorlet = self
        newMorlet.amp *= amount
        newMorlet.wavelet *= amount
        return newMorlet

    def DecreaseAmplitude(self, amount):
        """

        :param amount:
        :return:
        """
        newMorlet = self
        self.amp /= amount
        newMorlet.amp /= amount
        self.wavelet /= amount
        newMorlet.wavelet /= amount
        return newMorlet

    def ShiftOmega(self, direction, amount):
        """

        :param direction:
        :param amount:
        :return:
        """
        newMorlet = self
        center = math.floor((self.omega - min(self.total_travel)) / 2)
        if direction == 1:
            newMorlet.omega += (amount * 2)
            newMorlet.wavelet = np.roll(newMorlet.wavelet, amount)
        elif direction == 2:
            newMorlet.omega -= (amount * 2)
            newMorlet.wavelet = np.roll(newMorlet.wavelet, -1 * amount)
        return newMorlet
        #Shift center

    def ChangeFrequency(self):
        """

        :return:
        """
        #Frequency
        pass


    #TODO: Asymmetric modulations

    def ShrinkLeft(self):
        """

        :return:
        """
        modFunction = random.randint(1, 20) / 10
        newMorlet = self
        center = math.floor(self.GetStartIndex() + ((self.GetEndIndex() - self.GetStartIndex()) / 2))
        newMorlet.wavelet[:center] = newMorlet.wavelet[:center] / modFunction
        return newMorlet


    def ShrinkRight(self):
        """

        :return:
        """
        modFunction = random.randint(1, 20) / 10
        newMorlet = self
        center = math.floor(self.GetStartIndex() + ((self.GetEndIndex() - self.GetStartIndex()) / 2))
        newMorlet.wavelet[center:] = newMorlet.wavelet[center:] / modFunction
        return newMorlet

    def ApplyParabola(self, ref):
        index = random.choice(Wave.GetLocalMaxima(self.wavelet)[0])
        waveWidth = self.GetEndIndex() - self.GetStartIndex()
        width = random.randint(2, 4)
       # startTime = random.randint(self.GetStartIndex(), self.GetEndIndex() - width)
        x = np.linspace((-1 * width) / 2, width / 2)
        y = np.abs(-x ** 2)
        newMorlet = self
        startTime = math.floor(index - (len(y) / 2))
        endTime = math.floor(index + (len(y) / 2))
        newMorlet.wavelet[startTime:endTime] += y
        return newMorlet

    def ApplyNegativeParabola(self, ref):
        index = random.choice(Wave.GetLocalMinima(self.wavelet)[0])
        waveWidth = self.GetEndIndex() - self.GetStartIndex()
        width = random.randint(2, 4)
        #startTime = random.randint(self.GetStartIndex(), self.GetEndIndex() - width)
        x = np.linspace((-1 * width) / 2, width / 2)
        y = -x ** 2
        newMorlet = self
        startTime = math.floor(index - (len(y) / 2))
        endTime = math.floor(index + (len(y) / 2))
        newMorlet.wavelet[startTime:endTime] += y
        return newMorlet

    def ShaveEnd(self, ref):
        lastMax = Wave.GetLocalMaxima(self.wavelet)[0][-1]
        lastMin = Wave.GetLocalMinima(self.wavelet)[0][-1]
        pos = lastMax > lastMin
        if pos: self.wavelet[lastMin:] *= 0
        elif not pos: self.wavelet[lastMax:] *= 0
        return self

    def ShaveFront(self, ref):
        firstMax = Wave.GetLocalMaxima(self.wavelet)[0][0]
        firstMin = Wave.GetLocalMinima(self.wavelet)[0][0]
        pos = firstMax > firstMin
        if pos: self.wavelet[:firstMin] *= 0
        elif not pos: self.wavelet[:firstMax] *= 0
        return self
