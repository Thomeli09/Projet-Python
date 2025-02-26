# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:24:54 2025

@author: Thommes Eliott
"""

# Carbonation of concrete Library
import numpy as np

# Custom Lib



# Methods

# Saetta's Model
def CarboSaettaFD(Cco2Ini, Ccaoh2Ini, tMax, Dt, RH, T):
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

def Carbo(Cco2, tMax, Dt):
    pass
