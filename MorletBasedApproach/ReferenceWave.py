import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickleJar as pj
import os.path



#data_dir = "/Users/michael/OneDrive - Drexel University/Documents - Chang Lab/General/Group/Data/Ultrasound/Layered Electrode Study/"
data_dir = "/Users/michael/Library/CloudStorage/OneDrive-DrexelUniversity/Documents - Chang Lab/General/Individual/Andre Tayamen/Data/Acoustics/AT_EUM_002/"
data_file = "AT_EUM_002_01_dX-55_dZ-28_step_0p5.sqlite3"

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


    def PickleReferenceWave(self):
        file = data_dir + data_file
        pj.sqliteToPickle(file)
        pickleFile = os.path.splitext(file)[0] + '.pickle'
        data = pj.loadPickle(pickleFile)
        plt.plot(data, 'max')
        return data

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
