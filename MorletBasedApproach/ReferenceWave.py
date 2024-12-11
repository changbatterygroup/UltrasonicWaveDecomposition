import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickleJar as pj
import os.path



#data_dir = "/Users/michael/OneDrive - Drexel University/Documents - Chang Lab/General/Group/Data/Ultrasound/Layered Electrode Study/"
data_dir = "/Users/michael/OneDrive - Drexel University/Documents - Chang Lab/General/Individual/Andre Tayamen/Data/Acoustics/AT_EUM_002/"
data_file = "AT_EUM_002_01_dX-55_dZ-28_step_0p5.sqlite3"

'''
 dx - x   dz - y  dx/step + 1, same for dz.  !! PlotScanWaveforms() !!
'''

temp_data = "/Users/michael/Documents/Programming/tempLab/AT_EUM_002_02_dX-55_dZ-28_step_0p5.sqlite3"

class ReferenceWave:
    def __init__(self, file=data_file, dir=data_dir):
        self.data_dir = dir
        self.file = file
        self.data = self.data_dir + self.file
        self.waveArr = self.PickleReferenceWave()

    def PlotWave(self):

        fig, ax = plt.subplots()
        ax.plot(self.waveArr)
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

    def GetFullLength(self):
        return 800

    def GetStartXCoord(self):
        for x, y in enumerate(self.waveArr):
            if y > 0.01:
                return x
        print("Get X Coord failed.")

    def GetEndXCoord(self):
        for x, y in enumerate(self.waveArr):
            if y > 0.01:
                return x
        print("Get X Coord failed.")

    #TODO: Get the length, start point, and end point of the wave
