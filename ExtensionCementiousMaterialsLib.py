# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:17:57 2025

@author: Thommes Eliott
"""

# Experiment extension to cementious materials library

# Other Lib
import pandas as pd
import numpy as np
from ExperimentLib import Composition

# Custom Lib
from PlotLib import ParamPLT, StartPlots, CloseALLPlots, PLTShow, DefaultParamPLT, PLTPie, PLTPlot

"""
CemMaterials : Cementious materials objects
"""
class CemMaterials(Composition):
    def __init__(self, Val, Name, ProductionDate, Experiments):
        super().__init__(Name=Name, ProductionDate=ProductionDate,
                         Experiments=Experiments)
        
        # Ingredients
        self.Cement = []
        self.Water = []
        self.Aggregates = []
        self.Adjuvants = []




"""
Ingredients : Genrals ingredients for cementious materials
"""
class Ingredients:
    def __init__(self, Name, MatType, Color=None):
        self.Name = Name
        self.MatType = MatType
        self.Color = Color

        # properties
        self.Volume = 0
        self.BulkDensity = 0
        self.ParticleDensity = 0

    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getMatType(self):
        return self.MatType

    @getMatType.setter
    def getMatType(self, MatType):
        self.MatType = MatType

    @property
    def getColor(self):
        return self.Color

    @getColor.setter
    def getColor(self, Color):
        self.Color = Color

    @property
    def getVolume(self):
        return self.Volume

    @getVolume.setter
    def getVolume(self, Volume):
        self.Volume = Volume

    @property
    def getBulkDensity(self):
        return self.BulkDensity

    @getBulkDensity.setter
    def getBulkDensity(self, BulkDensity):
        self.BulkDensity = BulkDensity

    @property
    def getParticleDensity(self):
        return self.ParticleDensity

    @getParticleDensity.setter
    def getParticleDensity(self, ParticleDensity):
        self.ParticleDensity = ParticleDensity

    @property
    def getMass(self):
        return self.getVolume * self.getBulkDensity

    @getMass.setter
    def getMass(self, Mass, BParticleDensity=False):
        if BParticleDensity:
            self.getVolume = Mass / self.ParticleDensity
        else:
            self.getVolume = Mass / self.BulkDensity


"""
Cement
Colors : Grey
"""
class Cement(Ingredients):
    def __init__(self, Name, CementClass, CementType):
        super().__init__(self, Name=Name, MatType="Cement")
        Self.CementClass = False  # [int] Class of cement (CEM X, ...)
        Self.CementType = False  # [str] Type of cement (Portland, Blast Furnace, ...)

        self.getCementClass = CementClass
        self.getCementType = CementType

    @property
    def getCementClass(self):
        return self.CementClass

    @getCementClass.setter
    def getCementClass(self, CementClass):
        if isinstance(CementClass, int):
            if CementClass>=1 and CementClass<=6:
                self.CementClass = CementClass
            else:
                print("Error : Cement Class not defined")
        else:
            print("Error : Invalid input for Cement Class")

    @property
    def getCementType(self):
        return self.CementType

    @getCementType.setter
    def getCementType(self, CementType):
        if isinstance(CementType, str):
            if CementType=="Portland":
                self.CementType = "Portland"
            elif CementType=="Blast Furnace":
                self.CementType = "Blast Furnace"
            elif CementType=="Fly Ash":
                self.CementType = "Fly Ash"
            elif CementType=="Silica Fume":
                self.CementType = "Silica Fume"
            elif CementType=="Natural Pozzolan":
                self.CementType = "Natural Pozzolan"
            elif CementType=="Limestone":
                self.CementType = "Limestone"
            else:
                print("Warning : Cement Type not defined")
                self.CementType = CementType
        elif isinstance(CementType, int):
            if CementType==1:
                self.CementType = "Portland"
            elif CementType==2:
                self.CementType = "Blast Furnace"
            elif CementType==3:
                self.CementType = "Fly Ash"
            elif CementType==4:
                self.CementType = "Silica Fume"
            elif CementType==5:
                self.CementType = "Natural Pozzolan"
            elif CementType==6:
                self.CementType = "Limestone"
            elif CementType==7:
                print("Error : Cement Type not defined")
        else:
            print("Error : Invalid input for Cement Type")



"""
Water
Colors : Blue
"""
class Water(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Water")

"""
Aggregat
Colors : Brown
"""
class Aggregat(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Aggregat")
        
        # Granulometry
        self.GranuloDiam = [] # [float] Diameter of granulometry [mm]
        self.GranuloRatio = [] # [float] Ratio of granulometry [0; 1]

    @property
    def getGranuloDiam(self):
       return self.GranuloDiam

    @getGranuloDiam.setter
    def getGranuloDiam(self, GranuloDiam):
        if isinstance(GranuloDiam, float):
            self.GranuloDiam = GranuloDiam
        elif isinstance(GranuloDiam, list):
            self.GranuloDiam = GranuloDiam
        else:
            print("Error : Invalid input for Granulometry Diameter")

    @property
    def getGranuloRatio(self):
        return self.GranuloRatio

    @getGranuloRatio.setter
    def getGranuloRatio(self, GranuloRatio):
        if isinstance(GranuloRatio, float):
            self.GranuloRatio = GranuloRatio
        elif isinstance(GranuloRatio, list):
            self.GranuloRatio = GranuloRatio
        else:
            print("Error : Invalid input for Granulometry Ratio")

    def PLTGranulometry(self, paramPLT=False, BStart=True):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        PLTPlot(self.getGranuloDiam, self.getGranuloRatio, paramPLT)

        PLTShow(paramPLT)

"""
Adjuvant
Colors : Green
"""
class Adjuvant(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Adjuvant")