# -*- coding: utf-8 -*-
"""
Created on Tuesday Sept  30 11:20:09 2025

@author: Thommes Eliott
"""

# Library for mathematical operations on data 

# Other Lib
import numpy as np
import pandas as pd
from scipy.signal import medfilt, savgol_filter, butter, filtfilt, bessel, wiener
from scipy import integrate
from pykalman import KalmanFilter

# Custom Lib
from DataManagementLib import LenData

"""
DataTreatment

# Improvement to be done:
- Add differents data treatment methods
- Add differents links with DataLag class
"""
class DataTreatment:
    def __init__(self):
        pass
        # Data

    def DTMovingAverage(self, Data, FWindow=5):
        """
        Applys a moving average filter to the data.
        From scipy library.
        
        Args:
            Data (array): Input data array.
            FWindow (int): Size of the moving average filter window.

        Returns:
            Data (array): Filtered data array.
        """
        return np.convolve(Data, np.ones(FWindow)/FWindow, mode='same')

    def DTMedianFilter(self, Data, FWindow=5):
        """
        Applys a median filter to the data.
        From scipy library.
        
        Args:
            Data (array): Input data array.
            FWindow (int): Size of the median filter window. Must be an odd integer.
        Returns:
            Data (array): Filtered data array.
        """
        return medfilt(Data, kernel_size=FWindow)

    def DTSavitzkyGolay(self, Data, FWindow=5, PolyOrder=2):
        """
        Applys a Savitzky-Golay filter to the data.
        From scipy library.

        Args:
            Data (array): Input data array.
            FWindow (int): Size of the filter window. Must be an odd integer.
            PolyOrder (int): Order of the polynomial used to fit the samples. Must be less than FWindow.

        Returns:
            Data (array): Filtered data array.
        """
        return savgol_filter(Data, window_length=FWindow, polyorder=PolyOrder)

    def DTButterworth(self, Data, FSample=1.0, FCut=0.1, Order=4, BType='low'):
        """
        Applys a Butterworth filter to the data.
        From scipy library.
        Args:
            Data (array): Input data array.
            FSample (float): Sampling frequency of the data.
            FCut (float): Cutoff frequency of the filter.
            Order (int): Order of the filter.
            BType (str): Type of the filter. Can be 'low', 'high', 'bandpass' or 'bandstop'.
        Returns:
            Data (array): Filtered data array.
        """
        Nyquist = 0.5 * FSample
        NormalCutoff = FCut / Nyquist
        BButter, AButter = butter(N=Order, Wn=NormalCutoff, btype=BType, analog=False)
        return filtfilt(BButter, AButter, Data)

    def DTBessel(self, Data, FSample=1.0, FCut=0.1, Order=4, BType='low'):
        """
        Applys a Bessel filter to the data.
        From scipy library.
        Args:
            Data (array): Input data array.
            FSample (float): Sampling frequency of the data.
            FCut (float): Cutoff frequency of the filter.
            Order (int): Order of the filter.
            BType (str): Type of the filter. Can be 'low', 'high', 'bandpass' or 'bandstop'.

        Returns:
            Data (array): Filtered data array.
        """
        Nyquist = 0.5 * FSample
        NormalCutoff = FCut / Nyquist
        BBessel, ABessel = bessel(N=Order, Wn=NormalCutoff, btype=BType, analog=False)
        return filtfilt(BBessel, ABessel, Data)

    def DTWiener(self, Data, MySize=5, Noise=None):
        """
        Applys a Wiener filter to the data.
        From scipy library.

        Args:
            Data (array): Input data array.
            MySize (int): Size of the Wiener filter window.
            Noise (float): Estimated noise power. If None, it is estimated from the data.

        Returns:
            Data (array): Filtered data array.
        """
        return wiener(Data, mysize=MySize, noise=Noise)

    def DTKalman(self, Data, TransitionMatrix=1, ObservationMatrix=1, InitialStateMean=0, 
                 InitialStateCovariance=1, ObservationCovariance=1, TransitionCovariance=0.01):
        """
        Applys a Kalman filter to the data.
        From pykalman library.

        Args:
            Data (array): Input data array.
            TransitionMatrix (float or array): State transition matrix.
            ObservationMatrix (float or array): Observation matrix.
            InitialStateMean (float or array): Initial state mean.
            InitialStateCovariance (float or array): Initial state covariance.
            ObservationCovariance (float or array): Observation covariance.
            TransitionCovariance (float or array): Transition covariance.

        Returns:
            Data (array): Filtered data array.
        """
        kf = KalmanFilter(transition_matrices=TransitionMatrix,
                          observation_matrices=ObservationMatrix,
                          initial_state_mean=InitialStateMean,
                          initial_state_covariance=InitialStateCovariance,
                          observation_covariance=ObservationCovariance,
                          transition_covariance=TransitionCovariance)
        StateMeans, _ = kf.filter(Data)
        return StateMeans.flatten()

# Math functions
def CMPTDerivativeFirst(DataVal, DataAbs=None):
    """
    Computes the numerical derivative of the data.
    
    Args:
        DataVal (array): Input data array.
        DataAbs (array): Optional array of time or x-values corresponding to DataVal.
        Derivative (array): Numerical derivative of the data.
    """
    DataVal = np.asarray(DataVal)
    if DataAbs is None:
        # Assume uniform spacing
        Derivative = np.gradient(DataVal)
    else:
        DataAbs = np.asarray(DataAbs)
        Derivative = np.gradient(DataVal, DataAbs)
    return Derivative

def CMPTIntegralTrap(VectDerivative, DataAbs=None, FInitialVal=0, FDx=1.0):
    """
    Computes the numerical integral of the data using the trapezoidal rule.
    
    Args:
        VectDerivative (array): Numerical derivative of the data.
        DataAbs (array): Optional array of time or x-values corresponding to DataVal.
        FInitialVal (float): Optional initial value for the integral.
        FDx (float): Optional spacing between data points if DataAbs is not provided.
        
    Returns:
        Integral (array): Numerical integral of the data.
    """
    Derivative = np.asarray(VectDerivative, dtype=float)

    if DataAbs is None:
        # Assume uniform spacing
        Integral = integrate.cumulative_trapezoid(y=Derivative, dx=FDx, initial=FInitialVal)
    else:
        DataAbs = np.asarray(DataAbs, dtype=float)
        # Check if DataAbs is the same length as Derivative
        if LenData(DataAbs) != LenData(Derivative):
            print("Error: DataAbs and Derivative must have the same length.")
            return None

        # Trapezoidal integration
        Integral = integrate.cumulative_trapezoid(y=Derivative, x=DataAbs, initial=FInitialVal)
    return Integral