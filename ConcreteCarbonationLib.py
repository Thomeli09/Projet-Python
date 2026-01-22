# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:24:54 2025

@author: Thommes Eliott
"""

# Carbonation of concrete Library
from tkinter import W
import numpy as np
import math
import scipy.special

# Custom Lib
from DataStorageLib import DataLog
from MathOperationLib import CMPTInterpolationLinear, CMPTInterpolationSpline
from DataManagementLib import DataSort



# Methods

# Transport model
def TransportDiff(Xini, Xmax, Dx, tMax, Dt, Cco20, DiffCoef):
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
    NStepst = int(tMax/Dt) + 1
    TimeArray = np.linspace(0, tMax, NStepst)
    NStepsX = int((Xmax-Xini)/Dx) + 1
    XArray = np.linspace(Xini, Xmax, NStepsX) - Xini

    # Create time and space matrices using broadcasting
    TimeMatrix = TimeArray[:, np.newaxis]  # Shape: (NSteps, 1)
    XMatrix = XArray[np.newaxis, :]     # Shape: (1, NStepX)

    # Compute diffusion profile efficiently using NumPy broadcasting
    CMatrix = Cco20 * (1 - scipy.special.erf(XMatrix / (2 * np.sqrt(DiffCoef * TimeMatrix)) ))
    
    # Impose that the concentration at the boundaries is the initial concentration
    CMatrix[:, 0] = Cco20

    XArray = XArray + Xini
    return TimeArray, XArray, CMatrix

def TransportAdvec(Xini, Xmax, tMax, Dt, Cco20, u):
    """
    Advection model

    Parameters:
        Xini (float): Initial position.
        Xmax (float): Maximum position.
        tMax (float): Maximum time.
        Dt (float): Time step.
        Cco20 (float): Initial CO2 concentration.
        u (float): Advection velocity.
        CoefSmallDx (float): Coefficient for the smaller spatial step.

    Returns:
        TimeArray (numpy.ndarray): Array of time steps.
        XArray (numpy.ndarray): Array of spatial positions
        CArray (numpy.ndarray): Computed concentration values over time and space.
    """
    # Verify that the advection velocity is positive
    if u <= 0:
        print("Error: The advection velocity must be positive.")
        return None

    # Generate spatial and temporal grid
    NStepst = int(tMax/Dt) + 1
    TimeArray = np.linspace(0, tMax, NStepst)
    Dt = TimeArray[1] - TimeArray[0]
    Dx = u * Dt
    CoefSmallDx = 0  # The smaller the value the closer to the exact solution with step function
    SmallDx = CoefSmallDx * Dx
    ComplementDX = Dx - SmallDx
    XList = [Xini]
    XCurrent = Xini
    Toggle = False  # Start with ComplementDX

    while True:
        Step = ComplementDX if Toggle else SmallDx
        NextVal = XCurrent + Step

        # If the next value goes beyond Xmax, stop or append Xmax if needed
        if NextVal >= Xmax:
            if not np.isclose(XCurrent, Xmax):
                XList.append(Xmax)  # Append final step to reach Xmax exactly
            break

        XList.append(NextVal)
        XCurrent = NextVal
        Toggle = not Toggle  # Alternate between Dx and SmallDx

    XArray = np.array(XList)
    
    CMatrix = np.zeros((len(TimeArray), len(XArray)))
    
    # Initial condition
    CMatrix[0, :] = 0
    CMatrix[0, 0] = Cco20

    # Time-stepping loop
    for i in range(1, len(TimeArray)):
        # Translation of the concentration profile to the smaller spatial step
        CMatrix[i, 1:] = CMatrix[i-1, :-1]
        CMatrix[i, 0] = Cco20
        # Translation of the concentration profile to the larger spatial step so that total step is Dx
        CMatrix[i, 1:] = CMatrix[i, :-1]
        CMatrix[i, 0] = Cco20

    return TimeArray, XArray, CMatrix

def TransportAdvecDiff(Xini, Xmax, Dx, tMax, Dt, Cco20, DiffCoef, u=0):
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
    NStepst = int(tMax/Dt) + 1
    TimeArray = np.linspace(0, tMax, NStepst)
    TimeArray[0] = Dt # For numerical purposes, to avoid division by zero
    NStepsX = int((Xmax-Xini)/Dx) + 1
    XArray = np.linspace(Xini, Xmax, NStepsX) - Xini

    # Create time and space matrices using broadcasting
    TimeMatrix = TimeArray[:, np.newaxis]  # Shape: (NSteps, 1)
    XMatrix = XArray[np.newaxis, :]     # Shape: (1, NStepX)

    # Compute diffusion profile efficiently using NumPy broadcasting
    term1 = np.exp(u * XMatrix / (2 * DiffCoef))
    
    term2 = np.exp(-XMatrix * u / (2 * DiffCoef)) * \
            scipy.special.erfc((XMatrix / (2 * np.sqrt(DiffCoef * TimeMatrix))) - np.sqrt((u**2 * TimeMatrix) / (4 * DiffCoef)))
    
    term3 = np.exp(XMatrix * u / (2 * DiffCoef)) * \
            scipy.special.erfc((XMatrix / (2 * np.sqrt(DiffCoef * TimeMatrix))) + np.sqrt((u**2 * TimeMatrix) / (4 * DiffCoef)))

    CMatrix = (Cco20 / 2) * term1 * (term2 + term3)

    # Impose that initial the initial concentration is null initially (because it's not possible to compute at t=0)
    CMatrix[0, :] = 0
    # Impose that the concentration at the boundaries is the initial concentration
    CMatrix[:, 0] = Cco20

    # Get back to the original XArray and TimeArray
    XArray = XArray + Xini
    TimeArray[0] = 0

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
    
    NSteps = int(tMax/Dt) + 1
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

def CarboSaettaAnalOld(Cco2Ini, Ccaoh2Ini, tMax, Dt, RH, T):
    """
    Saetta's model for the carbonation of concrete without considering diffusion.
    The partial differential equation is solved analytically with the help of Wolfram Alpha.

    Warning: This function is not the most efficient way to solve the problem.
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
    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)

    # From Wolfram Alpha
    # Compute x(t)
    NumeratorX = (Gamma3*X0-Gamma4*Y0)*(X0/(Gamma4*Y0))**(Gamma3*X0/(Gamma3*X0-Gamma4*Y0))
    DenominatorX = Gamma3*(X0/(Gamma4*Y0))**(Gamma3*X0/(Gamma3*X0-Gamma4*Y0)) - np.exp(tVect*(-(Gamma3*X0)+Gamma4*Y0))*(X0/(Gamma4*Y0))**(Gamma4*Y0/(Gamma3*X0-Gamma4*Y0))

    Ccaoh2Vals = NumeratorX/DenominatorX

    # Compute y(t)
    NumeratorY = np.exp(tVect*(-(Gamma3*X0)+Gamma4*Y0)) * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)) * (-Gamma3*X0+Gamma4*Y0)
    DenominatorY = Gamma4 * (-Gamma3*(X0/(Gamma4*Y0))**((Gamma3*X0)/(Gamma3*X0-Gamma4*Y0)) + np.exp(tVect*(-(Gamma3*X0)+Gamma4*Y0)) * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)))
    Cco2Vals = NumeratorY/DenominatorY

    # Compute z(t)
    NumeratorZ = -Gamma5 * (-np.exp(tVect*(-(Gamma3*X0)+Gamma4*Y0)) * X0 * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)) + Gamma4 * (X0/(Gamma4*Y0))**((Gamma3*X0)/(Gamma3*X0-Gamma4*Y0)) * Y0)
    DenominatorZ = Gamma4 * (-Gamma3 * (X0/(Gamma4*Y0))**((Gamma3*X0)/(Gamma3*X0-Gamma4*Y0)) + np.exp(tVect*(-(Gamma3*X0)+Gamma4*Y0)) * (X0/(Gamma4*Y0))**((Gamma4*Y0)/(Gamma3*X0-Gamma4*Y0)))
    Ccaco3Vals = NumeratorZ/DenominatorZ

    return tVect, Ccaoh2Vals, Cco2Vals, Ccaco3Vals

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
    X0 = Cco2Ini  # Initial concentration of CO2
    Y0 = Ccaoh2Ini  # Initial concentration of Ca(OH)2
    Z0 = 0  # Initial concentration of CaCO3

    # Defining Gamma values for the equations
    Gamma3 = Gamma2*MCO2/MCaOH2  # Parameter for the partial differential equation of CO2
    Gamma4 = Gamma2  # Parameter for the partial differential equation of Ca(OH)2
    Gamma5 = Gamma2*MCaCO3/MCaOH2  # Parameter for the partial differential equation of CaCO3

    # Generate time values
    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)

    # From Wolfram Alpha
    ## Compute x(t) CO2
    NumeratorY = np.exp(Gamma3*tVect*Y0) * Y0 * (-Gamma4*X0+Gamma3*Y0)
    DenominatorY = -np.exp(Gamma4*tVect*X0) * Gamma4 * X0 + np.exp(Gamma3*tVect*Y0) * Gamma3 * Y0
    Y = NumeratorY/DenominatorY
    Cco2Vals = X0 + Gamma3/Gamma4 * (Y-Y0)

    # Compute y(t) Ca(OH)2
    NumeratorY = np.exp(Gamma3*tVect*Y0) * Y0 * (-Gamma4*X0+Gamma3*Y0)
    DenominatorY = -np.exp(Gamma4*tVect*X0) * Gamma4 * X0 + np.exp(Gamma3*tVect*Y0) * Gamma3 * Y0
    Ccaoh2Vals = NumeratorY/DenominatorY

    # Compute z(t) CaCO3
    Ccaco3Vals = Z0 - Gamma5/Gamma4 * (Y-Y0)

    return tVect, Ccaoh2Vals, Cco2Vals, Ccaco3Vals

# Simplified Carbonation Model
def CarboSilva(SigmaCO2, RH, RhoClincker, fc, ExpositionClass=1, tMax=5, Dt=0.1):
    """
    Silva's model for the carbonation of concrete.
    Model class : 1
    
    Args:
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
    Returns:
        tVect: numpy.ndarray
            Array of time steps (years).
        xc: numpy.ndarray
            Array of carbonation depths (mm).
    """
    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)

    if 0 <= RH <= 70:  # Dry environment
        kd = 0.556*SigmaCO2 - 3.602*ExpositionClass - 0.148*fc + 18.734
        xc = kd*tVect**0.5  # [mm]
    elif 70 <= RH <= 100:  # Wet environment
        kw = 3.355*SigmaCO2 - 0.019*RhoClincker - 0.042*fc + 10.830  # Wet environment
        xc = kw*tVect**0.5  # [mm]

    return tVect, xc

def CarboPetreLazar(Gamma, RH, fc, tMax=5, Dt=0.1):
    """
    Petre Lazar's model for the carbonation of concrete.
    Model class : 1

    Args:
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
    Returns:
        tVect: numpy.ndarray
            Array of time steps (years).
        xc: numpy.ndarray
            Array of carbonation depths (mm).

    """
    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)
    
    fRH = -3.5833*(RH/100)**2 + 3.4833*(RH/100) + 0.2
    k = 365**0.5 * (1/(2.1*fc**0.5)-0.06)
    xc = 10 * Gamma * fRH * k * tVect**0.5  # [mm]

    return tVect, xc

def CarboCEB(SigmaCO2, DCO2Ref, SigmaCement, OmegaCementCaO, ECRatio, CondCure, CondSurface, CondProtecTRH, tMax=5, Dt=0.1):
    """
    CEB model for the carbonation of concrete.
    Model class : 2

    Args:

    Returns:
        tVect: numpy.ndarray
            Array of time steps (years).
        xc: numpy.ndarray
            Array of carbonation depths (mm).

    """
    # Constants
    MCO2 = 44.01  # g/mol
    MCaO = 56.08  # g/mol

    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)
    t0 = 1  # year

    # Model Coefficients
    if CondCure == "Mauvaise" or CondCure == 0:
        k1 = 0.3
        k2 = 2.0
        k3 = 1.5
        W = 0.3

    elif CondCure == "Bonne" or CondCure == 1:
        if CondProtecTRH == "Mauvaise" or CondProtecTRH == 0:
            if CondSurface == "Mauvaise" or CondSurface == 0:
                k1 = 0.3
                k2 = 1.0
                k3 = 1.2
                W = 0.3
            elif CondSurface == "Bonne" or CondSurface == 1:
                k1 = 0.4
                k2 = 1.0
                k3 = 1.2
                W = 0.2
        elif CondProtecTRH == "Bonne" or CondProtecTRH == 1:
            if CondSurface == "Mauvaise" or CondSurface == 0:
                k1 = 0.5
                k2 = 1.0
                k3 = 1.0
                W = 0.1
            elif CondSurface == "Bonne" or CondSurface == 1:
                k1 = 0.6
                k2 = 1.0
                k3 = 1.0
                W = 0.05
        elif CondProtecTRH == "Intérieur" or CondProtecTRH == 2:
            k1 = 1.0
            k2 = 1.0
            k3 = 1.0
            W = 0


    AlphaH = HydrationDegree(ECRatio=ECRatio, BPrint=False)  # Hydration degree
    CrCO2 = 0.75*SigmaCement*OmegaCementCaO*AlphaH*(MCO2/MCaO)  # [kg/m^3]
    DeltaCO2 = SigmaCO2
    xc = (2*k1*k2*k3*DCO2Ref*DeltaCO2/CrCO2)*(tVect**(0.5))*((t0/tVect)**W) # [mm]

    return tVect, xc

def CarboPapadakis(SigmaCO2, DCO2Ref=False, tMax=5, Dt=0.1):
    """
    Papadakis model for the carbonation of concrete.
    Model class : 2
    Args:

    Returns:
        tVect: numpy.ndarray
            Array of time steps (years).
        xc: numpy.ndarray
            Array of carbonation depths (mm).
        
    """
    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)
    """
    # CO2 concentration in air from volumic to massic [mol/m^3]
    CCO2 = SigmaCO2

    # Chemical concentrations in concrete [mol/m^3]
    CCH =
    CCSH = 
    CC3S = 
    CC2S = 

    # Diffusion coefficient of CO2 in concrete [m^2/s]
    PhiP = Phi*(1+(ACRatio*RhoC/RhoA)/(1+ECRatio*RhoC/RhoE))
    DCO2Ref = 1.64*10**(-6)*PhiP**1.8*(1-HR/100)**2.2
    
    # Carbonation depth calculation
    xc =  ((2*DCO2Ref*CCO2/(CCH+3*CCSH+3*CC3S+2*CC2S))**0.5)*(tVect**0.5)  # [mm]

    return tVect, xc
    """
def CarboHyvert(SigmaCO2, DCO2, CCH, CCSH=0, CAFm=0, CAFt=0, PhiCP=1, RHRealPurcent=65, tCure=7, CCO2=0, tMax=5, Dt=0.1):
    """
    Hyvert model for the carbonation of concrete.
    Model class : 3
    Args:
        SigmaCO2: float Volumic concentration of CO2 in the air (m^3/m^3).
        DCO2: float Diffusion coefficient of CO2 in concrete (m^2/s) in any condition.
        But in reference conditions : RH=65%, T=20°C, tCure=7 days, if provide RHRealPurcent, tCure must be provided.
        CCH: float Chemical concentration of Ca(OH)2 in the concrete (mol/m^3) or in the cement paste (mol/m^3) if PhiCP is provided.
        CCSH: float Chemical concentration of C-S-H in the concrete (mol/m^3) or in the cement paste (mol/m^3) if PhiCP is provided.
        CAFm: float Chemical concentration of C4AF in the concrete (mol/m^3) or in the cement paste (mol/m^3) if PhiCP is provided.
        CAFt: float Chemical concentration of C3A in the concrete (mol/m^3) or in the cement paste (mol/m^3) if PhiCP is provided.
        PhiCP: float Volumic fraction of cement paste in concrete Vol cement paste / Vol concrete.
        RHRealPurcent: float Real relative humidity of the air (%).
        tCure: float Curing time of the concrete (days).
        CCO2: float Initial chemical concentration of CO2 in the concrete (mol/m^3).
        tMax: float Maximum time for the simulation (years).
        Dt: float Time step for the simulation (years).
    Returns:
        tVect: numpy.ndarray
            Array of time steps (years).
        xc: numpy.ndarray
            Array of carbonation depths (mm).

    """
    tVect = np.linspace(0, tMax, int(tMax/Dt) + 1)
    tVectSec = tVect * 365.25 * 24 * 3600  # Convert years to seconds
    # CO2 concentration in air from volumic to massic [mol/m^3]
    PAtm = 101325  # Pa
    PCO2 = PAtm*SigmaCO2
    R = 8.314  # J/(mol*K)
    T = 293  # K

    # Chemical concentrations in concrete [mol/m^3]
    Q1 = PhiCP*(CCH+4*CAFm+6*CAFt)
    C2 = CCSH*1.65 # mol/L Concentration of Calcium inside the cement paste in C-S-H phase
    C2Prim = PhiCP*CCSH*1.65

    # Model Coefficients
    RHRealScal = RHRealPurcent/100
    RHRefScal = 65/100
    g_e = 2.5
    f_e = 5.0
    ke = ((1-RHRealScal**f_e)/(1-RHRefScal**f_e))**g_e  # Environmental coefficient
    kc = (tCure/7)**(-0.57)  # Curing coefficient 
    kt = 1  # Temperature coefficient

    Alpha = 23.5  # 23.5 L/mol
    n = 0.67  # By default

    # Diffusion coefficient of CO2 in concrete [m^2/s]
    DCO2Ref = DCO2
    
    # Carbonation depth calculation
    if PCO2 >= 0:
        xc = ((2*ke*kc*kt*DCO2Ref*PCO2/R/T*tVectSec)/((1+Alpha*C2*(PCO2/PAtm)**n)*(C2Prim/(n+1)*(PCO2/PAtm)**n+Q1)))**0.5  # [mm]
    else:
        PCO2 = CCO2*R*T  # Convert initial concentration to partial pressure
        xc = ((2*ke*kc*kt*DCO2Ref*CCO2*tVectSec)/((1+Alpha*C2*(PCO2/PAtm)**n)*(C2Prim/(n+1)*(PCO2/PAtm)**n+Q1)))**0.5  # [mm]
    return tVect, xc
    

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

def CarboSimul2CarboDepth(DataSimul):
    """
    Returns the carbonation depth from a carbonation simulation.

    Args:
        DataSimul (DataLog): DataLog object containing the simulation data.
    """

    # Extract Data inputs and outputs
    DataInput = DataSimul.getFuncInput
    DataOutput = DataSimul.getFuncOutput

    # Verify the status of the FuncOutput register
    if DataOutput == None:
        # Initialize the FuncOutput register
        print("Info: FuncOutput register is empty. Initializing")
        UniqueTimeSteps, NTimeSteps = DataSimul.getUniqueTimeSteps
        Index = 0
        CarboDepthArray = np.zeros(NTimeSteps) # to be modified
        Temp = [UniqueTimeSteps, CarboDepthArray, Index]
    else:
        # Extract the current Index
        Temp = DataOutput
        UniqueTimeSteps = Temp[0]
        CarboDepthArray = Temp[1]
        Index = Temp[2]

    # Extract necessary parameters
    ReactionRatioThreshold = DataInput[0]
    MaxContent = DataInput[1]
    Method = DataInput[2]

    if Method not in ["Linear", "Spline", 0, 1]:
        print("Warning: Invalid Method for CarboDepth calculation. Choose 'Linear' or 'Spline'.")
        print("Info : Assuming 'Linear' method.")
        Method = "Linear"

    # Extract Position and Concentration arrays
    XArrays = DataSimul.getAbsVal
    CArrays = DataSimul.getOrdVal
    DataSort(L1=CArrays, L2=XArrays)


    # Reaction Ratio Arrays
    ReactionRatioArrays = CArrays / MaxContent

    # Check if the Reaction Ratio Threshold is within the simulated range
    MinReactionRatio = min(ReactionRatioArrays)
    MaxReactionRatio = max(ReactionRatioArrays)
    if ReactionRatioThreshold < MinReactionRatio or ReactionRatioThreshold > MaxReactionRatio:
        if ReactionRatioThreshold < MinReactionRatio:
            CarboDepthValue = 0
        else:
            CarboDepthValue = -1  # Indicating that the carbonation front is beyond the maximum simulated depth
    # Resulting Carbonation Depth Value
    elif Method == "Linear" or Method == 0:
        CarboDepthValue = CMPTInterpolationLinear(
            XPointData=ReactionRatioArrays,
            YPointData=XArrays,
            XNew=ReactionRatioThreshold,
            ValLeft=0,
            ValRight=0)
    elif Method == "Spline" or Method == 1:
        # Find the closest index to the estimated position
        IndexEstimate = np.argmin((ReactionRatioArrays - ReactionRatioThreshold)**2)

        # Define a small window around the estimated index for spline interpolation
        WindowSize = 3
        StartIndex = max(0, IndexEstimate - WindowSize)
        EndIndex = min(len(XArrays), IndexEstimate + WindowSize+1)
        ReactionRatioArraysUnique = ReactionRatioArrays[StartIndex:EndIndex]
        XArraysSec = XArrays[StartIndex:EndIndex]

        # Perform spline interpolation within the defined window
        CarboDepthValue = CMPTInterpolationSpline(
            XPointData=ReactionRatioArraysUnique,
            YPointData=XArraysSec,
            XNew=ReactionRatioThreshold,
            ValLeft=0,
            ValRight=0,
            Method=5)


    # Updating the FuncOutput register
    CarboDepthArray[Index] = CarboDepthValue
    Index += 1
    DataSimul.getFuncOutput = [UniqueTimeSteps, CarboDepthArray, Index]
