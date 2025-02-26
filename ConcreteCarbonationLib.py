# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:24:54 2025

@author: Thommes Eliott
"""

# Carbonation of concrete Library
import numpy as np

# Custom Lib


"""

"""
def CarbonationFiniteDiff(Cco2Ini, Ccaoh2Ini, tMax, dt):
    # Constants
    MCaOH2 = 74.093 # g/mol
    MCO2 = 44.01 # g/mol
    MCaCO3 = 100.086 # g/mol

    CCo2Arrays = np.zeros(int(tMax/dt))
    CCaOH2Arrays = np.zeros(int(tMax/dt))
    CCaCO3Arrays = np.zeros(int(tMax/dt))
    TimeArrays = np.zeros(int(tMax/dt))
    CCo2Arrays[0] = Cco2Ini
    CCaOH2Arrays[0] = Ccaoh2Ini
    CCaCO3Arrays[0] = 0
    TimeArrays[0] = 0

    for i in range(1, int(tMax/dt)):
        CCo2Arrays[i] = CCo2Arrays[i-1] - dt*CarbonationRate(CCaOH2Arrays[i-1], CCo2Arrays[i-1], Cco2Ini, Ccaoh2Ini)*Ccaoh2Ini/MCaOH2*MCO2
        CCaOH2Arrays[i] = CCaOH2Arrays[i-1] - dt*CarbonationRate(CCaOH2Arrays[i-1], CCo2Arrays[i-1], Cco2Ini, Ccaoh2Ini)*Ccaoh2Ini
        CCaCO3Arrays[i] = CCaCO3Arrays[i-1] + dt*CarbonationRate(CCaOH2Arrays[i-1], CCo2Arrays[i-1], Cco2Ini, Ccaoh2Ini)*Ccaoh2Ini/MCaOH2*MCaCO3
        TimeArrays[i] = i*dt
    return TimeArrays, CCo2Arrays, CCaOH2Arrays, CCaCO3Arrays

def CarbonationRate(CCaOH2, CCo2, Cco2Ini, Ccaoh2Ini):
    # Constants
    Alpha1 = 2.8*10**(-7)
    m = 1
    E0 = 48096
    R = 8.314
    T0 = 296
    
    T = 294
    RH = 0.95

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




