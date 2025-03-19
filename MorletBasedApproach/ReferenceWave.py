import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pywt import threshold
from scipy.ndimage import median_filter
from scipy.signal import find_peaks
import Wave
import pickleJar as pj
import os.path
import math
import scipy

'''
Class defining and analyzing the reference wave
'''

#data_dir = "/Users/michael/OneDrive - Drexel University/Documents - Chang Lab/General/Group/Data/Ultrasound/Layered Electrode Study/"
data_dir = "/Users/michael/OneDrive - Drexel University/Documents - Chang Lab/General/Individual/Andre Tayamen/Data/Acoustics/AT_EUM_002/"
data_file = "AT_EUM_002_01_dX-55_dZ-28_step_0p5.sqlite3"

'''
 dx - x   dz - y  dx/step + 1, same for dz.  !! PlotScanWaveforms() !!
'''

temp_data = "/Users/michael/Documents/Programming/tempLab/AT_EUM_002_02_dX-55_dZ-28_step_0p5.sqlite3"

'''
Reference wave analysis
    Values to scan for: 
        - Number of local extrema
        - min/max y values
        - Start and stop times
'''
class ReferenceWave:
    def __init__(self, file=data_file, dir=data_dir):
        self.data_dir = dir
        self.file = file
        self.data = self.data_dir + self.file
        self.waveArr = self.PickleReferenceWave()
        self.max_voltage, self.min_voltage = None, None
        self.num_local_maxima, self.num_local_minima = None, None
        self.first_time_index, self.last_time_index = None, None
        self.maxima, self.minima, self.maxima_voltages, self.minima_voltages = None, None, [], []
        self.AnalyzeReferenceWave()

    def PlotWave(self):
        fig, ax = plt.subplots()
        ax.plot(self.waveArr['time'], self.waveArr['voltage'])
        plt.show()

# This is it, I got it. Go me. Yippee.
    # *sqlitetopickle -> plotscanwaveform()
    def PickleReferenceWave(self):
        file = data_dir + data_file
        print(temp_data)
        pickleFile = os.path.splitext(temp_data)[0] + '.pickle'
        pickleData = pj.loadPickle(pickleFile) if pj.sqliteToPickle(temp_data) == -1 else pj.sqliteToPickle(temp_data)
        # data = pj.loadPickle(pickleFile)
        pickleLength = len(pickleData) - 3
        coor1 = (1, 0)
        coor2 = (pickleData[pickleLength]['X'], pickleData[pickleLength]['Z'])
        coors = [coor1, coor2]
        pj.plotScanWaveforms(pickleData, coors)
        maxTime = 0
        for i, data in enumerate(pickleData):
            if isinstance(data, int) :
                timeLength = len(pickleData[data]['time']) - 1
                if maxTime < pickleData[data]['time'][timeLength]:
                    maxTime = pickleData[data]['time'][timeLength]
        print(pickleData[1]['time'][0])
        print(maxTime - pickleData[1]['time'][0])
        self.startTime = pickleData[1]['time'][0]
        self.endTime = maxTime
        return pickleData[0]


    def GetRefereneceWave(self):
        connection = sqlite3.connect(self.data)
        cursor = connection.cursor()
        query = """SELECT name FROM sqlite_master WHERE type='table'"""
        cursor.execute(query)
        table = cursor.fetchall()
        query = f'SELECT * FROM "{table[0][0]}"'
        df = pd.read_sql(sql=query, con=connection)

        waves = df['amps'].str.strip('[]').str.split(',')
        waveMatrix = np.zeros((len(waves), len(waves[0])))
        for i, wave in enumerate(waves):
            waveMatrix[i, :] = wave

        return waveMatrix[0]

    def AnalyzeReferenceWave(self):
        # Local extrema
        self.num_local_maxima = Wave.FindLocalMaxima(self.waveArr['voltage'])
        self.num_local_minima = Wave.FindLocalMinima(self.waveArr['voltage'])
        self.maxima = Wave.GetLocalMaxima(self.waveArr['voltage'])[0]
        self.minima = Wave.GetLocalMinima(self.waveArr['voltage'])[0]
        for volt in self.maxima: self.maxima_voltages.append(self.waveArr['voltage'][volt])
        for volt in self.minima: self.minima_voltages.append(self.waveArr['voltage'][volt])

        # Max y value
        self.max_voltage = Wave.FindMaxY(self.waveArr['voltage'])

        # Min y value
        self.min_voltage = Wave.FindMinY(self.waveArr['voltage'])

        # First x coord
        self.first_time_index = Wave.FindFirstX(self.waveArr['voltage'])

        # last x coord
        self.last_time_index = Wave.FindLastX(self.waveArr['voltage'])

    def GetTimeArr(self):
        return self.waveArr['time']

    def GetFullLength(self):
        return ((self.endTime - self.startTime) / 2) + 1

    def GetStart(self):
        return self.waveArr['time'][0]

    def GetEnd(self):
        return self.endTime

    def GetStartXCoord(self):
        for x, y in enumerate(self.waveArr['voltage']):
            try:
                y = float(y)
            except Exception:
                pass
            if isinstance(y, float) :
                if math.floor(y) >= 1:
                    return self.waveArr['time'][x]
        print("Get X Coord failed.")

    def GetEndXCoord(self):
        for x, y in enumerate(reversed(self.waveArr['voltage'])):
            try:
                y = float(y)
            except Exception:
                pass
            if isinstance(y, float):
                if math.floor(y) >= 1:
                    return self.waveArr['time'][x]
        print("Get X Coord failed.")

    #TODO: Get the length, start point, and end point of the wave
