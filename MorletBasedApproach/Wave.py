import numpy as np
from scipy.signal import find_peaks

def FindFirstX(arr):
    first_voltage_threshold = 0.5
    return np.argmax(np.abs(arr) > first_voltage_threshold)

def FindLastX(arr):
    last_voltage_threshold = 1
    last_time_index = np.argmax(np.abs(arr[::-1]) > last_voltage_threshold)
    last_time_index = len(arr) - last_time_index - 1
    return last_time_index

def FindMaxY(arr):
    return arr.max()

def FindMinY(arr):
    return arr.min()

def FindLocalMinima(arr):
    local_minima = find_peaks(-(arr), prominence=0.6)
    num_local_minima = len(local_minima)
    return num_local_minima

def GetLocalMinima(arr):
    local_minima = find_peaks(-(arr), prominence=0.6)
    return local_minima

def FindLocalMaxima(arr):
    local_maxima = find_peaks(arr, prominence=0.6)
    num_local_maxima = len(local_maxima)
    return num_local_maxima

def GetLocalMaxima(arr):
    local_maxima = find_peaks(arr, prominence=0.6)
    return local_maxima