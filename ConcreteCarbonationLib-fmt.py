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
    TVals = np.linspace(0, tMax, int(tMax/Dt))
    pass




# Hydration Degree
def  HydrationDegree(CementType, Time, Temp):
    if CementType == "Type1":
        # Constants
        A = 0.5
        B = 0.5
        C = 0.5
        D = 0.5
        E = 0.5
        F = 0.5
        G = 0.5
        H = 0.5
        I = 0.5
        J = 0.5
        K = 0.5
        L = 0.5
        M = 0.5
        N = 0.5
        O = 0.5
        P = 0.5
        Q = 0.5
        R = 0.5
        S = 0.5
        T = 0.5
        U = 0.5
        V = 0.5
        W = 0.5
        X = 0.5
        Y = 0.5
        Z = 0.5
        AA = 0.5
        AB = 0.5
        AC = 0.5
        AD = 0.5
        AE = 0.5
        AF = 0.5
        AG = 0.5
        AH = 0.5
        AI = 0.5
        AJ = 0.5
        AK = 0.5
        AL = 0.5
        AM = 0.5
        AN = 0.5
        AO = 0.5
        AP = 0.5
        AQ = 0.5
        AR = 0.5
        AS = 0.5
        AT = 0.5
        AU = 0.5
        AV = 0.5
        AW = 0.5
        AX = 0.5
        AY = 0.5
        AZ = 0.5
        BA = 0.5
        BB = 0.5
        BC = 0.5
        BD = 0.5
        BE = 0.5
        BF = 0.5
        BG = 0.5