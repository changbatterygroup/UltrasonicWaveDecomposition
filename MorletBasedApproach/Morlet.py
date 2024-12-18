import numpy as np
import matplotlib.pyplot as plt
from random import random

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
'''


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
        newMorlet = self
        self.amp += amount
        newMorlet.amp += amount
        return newMorlet

    def ShiftOmega(self, direction, amount):
        newMorlet = self
        self.omega += amount
        newMorlet.omega += amount
        return newMorlet        #Shift center

    def ChangeFrequency(self):
        #Frequency
        pass


    #TODO: Asymmetric modulations

    def ShrinkLeft(self):
        n = len(self.wavelet)
        modulation_function = np.linspace(0, 1, n // 2)
        self.wavelet[: (n // 2)] *= modulation_function
        return self

    def ShrinkRight(self):
        pass

