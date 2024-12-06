import numpy as np
import matplotlib.pyplot as plt
from random import random


class Morlet:
    def __init__(self, omega, amp, total_travel, width):
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
        match alg:
            case 1:
                return amp * np.cos(5 * (total_travel - omega) / width) * np.exp(-((total_travel - omega) / width) ** 2 / 2) # Change to sin
            case 2:
                return np.real(np.exp(1j*(omega*total_travel)/width) * np.exp(-0.5*(total_travel/width)**2) * np.pi**(-0.25) * np.sqrt(1/width))

    def GraphMorlet(self, index):
        fig, ax = plt.subplots()
        ax.plot(self.total_travel, self.wavelet, label=f"Constituent #{index}")
        plt.title(f"Constituent #{index}")
        plt.show()

    #TODO: Symmetric modulations
    def IncreaseAmplitude(self, amount):
        self.amp += amount
        pass

    def ShiftOmega(self, direction, amount):
        self.omega += amount
        #Shift center

    def ChangeFrequency(self):
        #Frequency
        pass


    #TODO: Asymmetric modulations

    def ShrinkLeft(self):
        n = len(self.wavelet)
        modulation_function = np.linspace(0, 1, n // 2)
        self.wavelet[: (n // 2)] *= modulation_function
        return self.wavelet

    def ShrinkRight(self):
        pass

