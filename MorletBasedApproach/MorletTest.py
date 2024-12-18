import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import Reference

from MaterialBasedApproach.Material import *
from MorletBasedApproach.Morlet import Morlet
from GeneratedWave import *
from ReferenceWave import *
import numpy as np
from scipy.signal import correlate
from AssortedGAStuff import *

'''
'Main' for testing purposes. 
'''

def Test():
    '''
    ###
    TestMor = Morlet(5, 2, np.linspace(-10, 10, 1000), 2)
    TestMor.GraphMorlet(1)
    ###
    '''

    '''
    ###
    TestWave = GeneratedWave(5, 800, 200, 600)
    TestWave.PlotMorletMatrix()
    ###
    '''
    '''
    ###
    SquishedArr = TestWave.CombineMorlets()
    fig, ax = plt.subplots()
    ax.plot(SquishedArr)
    ###
    '''
    #plt.show()
    '''
    ###
    TestWave.Mutate(0, 'ShiftOmega')
    SquishedArr = TestWave.CombineMorlets()
    fig, ax = plt.subplots()
    ax.plot(SquishedArr)
    ###
    '''
    #plt.show()

    ### We picklin
    TestRef = ReferenceWave()

    xTot = int(TestRef.GetFullLength())
    xStart = TestRef.GetStart()
    xEnd =  TestRef.GetEnd()

    # @TODO: Automatically determine omega, width, amp
  #  FirstGen = CreateFirstGen(TestRef)
  #  for iteration in FirstGen:
  #      iteration.PlotMorletMatrix()

    GALoop(TestRef)
       # print(FitnessTest(iteration, TestRef))
    #FirstGen.GraphMorlet(1)
    plt.show()


def main():
    Test()


if __name__ == '__main__':
    main()