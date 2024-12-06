import numpy as np
import matplotlib.pyplot as plt
import pywt

MaterialLibrary = {"Aluminum": "Al.json", "Copper": "Cu.json", "Celgard": "Cel.json"}

class Material(object):
    def __init__(self, time, frequency, time_delay, phase):
         # self.material_type = material_type # Name of the material e.g. copper
        # self.density = density # Individual layer density
         # self.thickness = thickness # Individual layer thickness
        # self.waveform = MaterialLibrary[material_type] # Material waveform from the lab database
        self.GraphMorlet(self.GenerateMorlet(time, frequency, time_delay, phase))

    def GenerateMorlet(self, time, frequency, time_delay, phase):
        sigma = time_delay / (2 * np.pi * frequency)
        return np.exp((-1 * time) ** 2 / (2 * sigma ** 2)) * np.cos(2 * np.pi * frequency * time + phase)

    def GraphMorlet(self, morlet):
        fig, ax = plt.subplots()
        ax.plot(morlet)
        plt.show()

    def GraphMorletTwo(self):
        t = np.linspace(-4, 4, 1000)
        omega0 = 5
        real_part = np.pi ** (-0.25) * np.cos(omega0 * t) * np.exp(-t ** 2 / 2)
        plt.plot(t, real_part, label='Real Part', color='blue')
        plt.show()

    def GraphPywtMor(self):
        morlet = pywt.ContinuousWavelet('morl')
        plt.plot(morlet)
        plt.show()



