# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:24:54 2025

@author: Thommes Eliott
"""

# Carbonation of concrete Library
import numpy as np
import scipy.special

# Custom Lib



# Methods

# Transport model
def CarboDiff(Xini, Xmax, Dx, tMax, Dt, Cco20, DiffCoef):
    """
    Diffusion model

    Parameters:
        Xini (float): Initial position.
        Xmax (float): Maximum position.
        Dx (float): Spatial step.
        tMax (float): Maximum time.
        Dt (float): Time step.
        Cco20 (float): Initial CO2 concentration.
        DiffCoef (float): Diffusion coefficient.

    Returns:
        TimeArray (numpy.ndarray): Array of time steps.
        XArray (numpy.ndarray): Array of spatial positions.
        CArray (numpy.ndarray): Computed concentration values over time and space.
    """
    
    # Generate spatial and temporal grid
    NStepst = int(tMax/Dt)
    TimeArray = np.linspace(0, tMax, NStepst)
    NStepsX = int((Xmax-Xini)/Dx)
    XArray = np.linspace(Xini, Xmax, NStepsX)

    # Create time and space matrices using broadcasting
    TMatrix = TimeArray[:, np.newaxis]  # Shape: (NSteps, 1)
    XMatrix = XArray[np.newaxis, :]     # Shape: (1, NStepX)

    # Compute diffusion profile efficiently using NumPy broadcasting
    DenomTerm = np.sqrt(4 * DiffCoef * TMatrix)  # Precompute sqrt(4Dt) for all time steps
    CMatrix = Cco20 * (1 - scipy.special.erf(np.abs(XMatrix) / DenomTerm))
    return TimeArray, XArray, CMatrix

def CarboAdvecDiff(Xini, Xmax, Dx, tMax, Dt, Cco20, DiffCoef, u):
    """
    Advection-Diffusion model
 
    Parameters:
        Xini (float): Initial position.
        Xmax (float): Maximum position.
        Dx (float): Spatial step.
        tMax (float): Maximum time.
        Dt (float): Time step.
        Cco20 (float): Initial CO2 concentration.
        DiffCoef (float): Diffusion coefficient.
        u (float): Advection velocity.

    Returns:
        TimeArray (numpy.ndarray): Array of time steps.
        XArray (numpy.ndarray): Array of spatial positions.
        CMatrix (numpy.ndarray): Computed CO2 concentration over time and space.
    """
    # Generate spatial and temporal grid
    NStepst = int(tMax/Dt)
    TimeArray = np.linspace(0, tMax, NStepst)
    NStepsX = int((Xmax-Xini)/Dx)
    XArray = np.linspace(Xini, Xmax, NStepsX)

    # Create time and space matrices using broadcasting
    TMatrix = TimeArray[:, np.newaxis]  # Shape: (NSteps, 1)
    XMatrix = XArray[np.newaxis, :]     # Shape: (1, NStepX)

    # Compute diffusion profile efficiently using NumPy broadcasting
    term1 = np.exp(u * XMatrix / (2 * DiffCoef))
    
    term2 = np.exp(-XMatrix * u / (2 * DiffCoef)) * \
            scipy.special.erfc((XMatrix / (2 * np.sqrt(DiffCoef * TMatrix))) - np.sqrt((u**2 * TMatrix) / (4 * DiffCoef)))
    
    term3 = np.exp(XMatrix * u / (2 * DiffCoef)) * \
            scipy.special.erfc((XMatrix / (2 * np.sqrt(DiffCoef * TMatrix))) + np.sqrt((u**2 * TMatrix) / (4 * DiffCoef)))

    CMatrix = (Cco20 / 2) * term1 * (term2 + term3)
    return TimeArray, XArray, CMatrix


# Saetta's Model
def CarboSaettaFD(Cco2Ini, Ccaoh2Ini, tMax, Dt, RH, T):
    """
    Saetta's model for the carbonation of concrete without considering diffusion.
    The partial differential equation is solved using a finite difference method.
    """
    # Constants
    MCaOH2 = 74.093  # g/mol
    MCO2 = 44.01  # g/mol
    MCaCO3 = 100.086  # g/mol
    
    NSteps = int(tMax/Dt)
    TimeArray = np.linspace(0, tMax, NSteps)
    CCo2Array = np.zeros(NSteps)
    CCaOH2Array = np.zeros(NSteps)
    CCaCO3Array = np.zeros(NSteps)
    
    # Initial conditions
    CCo2Array[0] = Cco2Ini
    CCaOH2Array[0] = Ccaoh2Ini
    CCaCO3Array[0] = 0
    
    # Time-stepping loop
    for i in range(1, NSteps):
        Rate = CarboSaettaRate(CCaOH2Array[i-1], CCo2Array[i-1], Cco2Ini, Ccaoh2Ini, RH, T)
        
        CCo2Array[i] = CCo2Array[i-1] - Dt * Rate * Ccaoh2Ini / MCaOH2 * MCO2
        CCaOH2Array[i] = CCaOH2Array[i-1] - Dt * Rate * Ccaoh2Ini
        CCaCO3Array[i] = CCaCO3Array[i-1] + Dt * Rate * Ccaoh2Ini / MCaOH2 * MCaCO3

    return TimeArray, CCaOH2Array, CCo2Array, CCaCO3Array

def CarboSaettaRate(CCaOH2, CCo2, Cco2Ini, Ccaoh2Ini, RH, T):
    # Constants
    Alpha1 = 2.8*10**(-7)
    m = 1
    E0 = 48096
    R = 8.314
    T0 = 296

    if RH <= 0.5:
        fh = 0
    elif RH > 0.5 and RH <= 0.9:
        fh = 5/2*(RH - 0.5)
    else:
        fh = 1
    fCo2 = CCo2/Cco2Ini
    fCaOH2 = 1-(1-CCaOH2/Ccaoh2Ini)**m
    fT = np.exp(E0/R*(1/T0-1/T))
    
    ReactionRate = Alpha1*fh*fCo2*fCaOH2*fT
    return ReactionRate

def CarboSaettaAnal(Cco2Ini, Ccaoh2Ini, tMax, Dt, RH, T):
    """
    Saetta's model for the carbonation of concrete without considering diffusion.
    The partial differential equation is solved analytically with the help of Wolfram Alpha.
    """
    # Chemicals Constants
    MCaOH2 = 74.093 # g/mol 
    MCO2 = 44.01 # g/mol
    MCaCO3 = 100.086 # g/mol

    # Model Constants
    Alpha1 = 2.8*10**(-7)
    m = 1
    E0 = 48096
    R = 8.314
    T0 = 296

    # Model Variables Determination
    if RH <= 0.5:
        fh = 0
    elif RH > 0.5 and RH <= 0.9:
        fh = 5/2*(RH - 0.5)
    else:
        fh = 1
    fT = np.exp(E0/R*(1/T0-1/T))

    # Determined Model Variables
    Gamma2 = (Ccaoh2Ini*Alpha1*fh*fT)/(Cco2Ini*Ccaoh2Ini)

    # Defining Initial Conditions
    X0 = Ccaoh2Ini  # Initial x value
    Y0 = Cco2Ini  # Initial y value

    # Defining Gamma values for the equations
    Gamma3 = Gamma2*MCO2/MCaOH2  # Given parameter
    Gamma4 = Gamma2  # Given parameter
    Gamma5 = Gamma2*MCaCO3/MCaOH2  # Given parameter

    # Generate time values
    TVals = np.linspace(0, tMax, int(tMax/Dt))

    # From Wolfram Alpha
    # Compute x(t)
    NumeratorX = (Gamma3*X0-Gamma4*Y0)*(X0/(Gamma4*Y0))**(Gamma3*X0/(Gamma3*X0-Gamma4*Y0))
    DenominatorX = Gamma3*(X0/(Gamma4*Y0))**(Gamma3*X0/(Gamma3*X0-Gamma4*Y0)) - np.exp(TVals*(-(Gamma3*X0)+Gamma4*Y0))*(X0/(Gamma4*Y0))**(Gamma4*Y0/(Gamma3*X0-Gamma4*Y0))

    Ccaoh2Vals = NumeratorX/DenominatorX

    # Compute y(t)
    NumeratorY = np.exp(TVals*(-(Gamma3*X0)+Gamma4*Y0)) * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)) * (-Gamma3*X0+Gamma4*Y0)
    DenominatorY = Gamma4 * (-Gamma3*(X0/(Gamma4*Y0))**((Gamma3*X0)/(Gamma3*X0-Gamma4*Y0)) + np.exp(TVals*(-(Gamma3*X0)+Gamma4*Y0)) * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)))
    Cco2Vals = NumeratorY/DenominatorY

    # Compute z(t)
    NumeratorZ = -Gamma5 * (-np.exp(TVals*(-(Gamma3*X0)+Gamma4*Y0)) * X0 * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)) + Gamma4 * (X0/(Gamma4*Y0))**((Gamma3*X0)/(Gamma3*X0-Gamma4*Y0)) * Y0)
    DenominatorZ = Gamma4 * (-Gamma3 * (X0/(Gamma4*Y0))**((Gamma3*X0)/(Gamma3*X0-Gamma4*Y0)) + np.exp(TVals*(-(Gamma3*X0)+Gamma4*Y0)) * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)))
    Ccaco3Vals = NumeratorZ/DenominatorZ

    return TVals, Ccaoh2Vals, Cco2Vals, Ccaco3Vals

# Simplified Carbonation Model
def CarboSilva(SigmaCO2, RH, RhoClincker, fc, ExpositionClass=1, tMax=5, Dt=0.1):
    """
    Silva's model for the carbonation of concrete.
    Model class : 1
    
    Inputs:
        SigmaCO2: float
            Volumic concentration of CO2 in the air (m^3/m^3).
        RH: float
            Relative humidity of the air (%).
        RhoClincker: float
            Massic concentration of clinker in the concrete (kg/m^3).
        fc: float
            Compressive strength of the concrete (MPa).
        ExpositionClass: int [1; 3]
            Exposure class of the concrete. XC1=1, XC2=2, or XC4=3.
        tMax: float
            Maximum time for the simulation (years).
        Dt: float
            Time step for the simulation (years).
    """
    TVals = np.linspace(0, tMax, int(tMax/Dt))

    if 0 <= RH <= 70:  # Dry environment
        kd = 0.556*SigmaCO2 - 3.602*ExpositionClass - 0.148*fc + 18.734
        xc = kd*TVals**0.5  # [mm]
    elif 70 <= RH <= 10:  # Wet environment
        kw = 3.355*SigmaCO2 - 0.019*RhoClincker - 0.042*fc + 10.830  # Wet environment
        xc = kw*TVals**0.5  # [mm]

    return TVals, xc

def CarboPetreLazar(Gamma, RH, fc, tMax=5, Dt=0.1):
    """
    Petre Lazar's model for the carbonation of concrete.
    Model class : 1

    Inputs:
        Gamma: float
            Carbonation exposition coefficient.
            Gamma = 1.5 in structures exposed to high concentrations of CO2.
            Gamma = 0.9 in structures particularly exposed to rain.
            Gamma = 1.2 in structures sheltered from rain.
        RH: float
            Relative humidity of the air (%).
        fc: float
            Compressive strength of the concrete (MPa).
        tMax: float
            Maximum time for the simulation (years).
        Dt: float
            Time step for the simulation (years).

    """
    TVals = np.linspace(0, tMax, int(tMax/Dt))
    
    fRH = -3.5833*(RH/100)**2 + 3.4833*(RH/100) + 0.2
    k = 365**0.5 * (1/(2.1*fc**0.5)-0.06)
    xc = 10 * Gamma * fRH * k * TVals**0.5  # [mm]

    return TVals, xc

def CarboCEB():
    """
    CEB model for the carbonation of concrete.
    Model class : 2

    Inputs:

    """
    pass

def CarboPapadakis():
    """
    Papadakis model for the carbonation of concrete.
    Model class : 2
    Inputs:
        
    """
    pass

def CarboHyvert():
    """
    Hyvert model for the carbonation of concrete.
    Model class : 3
    Inputs:

    """
    pass
    

# Hydration Degree
def  HydrationDegree(ECRatio, BPrint=True):
    """
    Mills' model for the hydration degree of concrete.
    The ultimate hydration degree is a function of the water/cement ratio.
    """
    if isinstance(ECRatio, list):
        HydrationDegreeList = [HydrationDegree(ECRatio=EC, BPrint=False) for EC in ECRatio]
        if BPrint:
            for i, HD in enumerate(HydrationDegreeList):
                print(f"E/C: {ECRatio[i]} -> Hydration Degree: {HD}")
        return HydrationDegreeList 
    else:
        HydrationDegreeVal = (1.031*ECRatio)/(0.194+ECRatio)
        if BPrint:
            print(f"E/C: {ECRatio} -> Hydration Degree: {HydrationDegreeVal}")
        return HydrationDegreeVal
