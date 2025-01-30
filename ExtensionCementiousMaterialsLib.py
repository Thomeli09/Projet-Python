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
        self.Cement = False  # [Cement] Cement object (Limited to one object)
        self.Water = False  # [Water] Water object (Limited to one object)
        self.Aggregates = []  # [Aggregat] Aggregates objects (Unlimited)
        self.Adjuvants = []  # [Adjuvant] Adjuvants objects (Unlimited)

    @property
    def getCement(self):
        return self.Cement

    @getCement.setter
    def getCement(self, ItemCement):
        if isinstance(ItemCement, Cement):
            self.Cement = ItemCement
        else:
            print("Error : Invalid input for Cement")

    @property
    def getWater(self):
        return self.Water

    @getWater.setter
    def getWater(self, ItemWater):
        if isinstance(ItemWater, Water):
            self.Water = ItemWater
        else:
            print("Error : Invalid input for Water")


    @property
    def getAggregates(self):
        return self.Aggregates

    @getAggregates.setter
    def getAggregates(self, ItemAggregat):
        if isinstance(ItemAggregat, list):
            self.Aggregates = ItemAggregat
        elif isinstance(ItemAggregat, Aggregat):
            self.Aggregates.append(ItemAggregat)
        else:
            print("Error : Invalid input for Aggregates")

    @property
    def getAdjuvants(self):
        return self.Adjuvants

    @getAdjuvants.setter
    def getAdjuvants(self, Adjuvants):
        if isinstance(Adjuvants, list):
            self.Adjuvants = Adjuvants
        elif isinstance(Adjuvants, Adjuvant):
            self.Adjuvants.append(Adjuvants)
        else:
            print("Error : Invalid input for Adjuvants")


    def PLTGranulos(self, paramPLT, BPourcent=True):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        StartPlots()
        # Improvement : Add the the differents markers for each granulometry

        # Plot of granulometries
        for Aggregat in self.getAggregates:
            Aggregat.PLTGranulometry(paramPLT, BStart=False, BEnd=False, BPourcent=BPourcent)

        PLTShow(paramPLT)

    def PLTIngredients(self, paramPLT):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        StartPlots()

        # Parameters of the plot
        paramPLT.getTitle = "Composition of the " + self.getName
        # Rajouter des param�tres en plus
        # R�soudres le probl�me des arguments de PLTPie
        # R�soudres le probl�me des couleurs

        # Pie chart
        Labels = ['Cement', 'Water']
        Sizes = [self.getCement.getMass, self.getWater.getMass]
        PLTPie(Labels, Sizes, paramPLT)

        PLTShow(paramPLT)

    def CmptComposition(self):
        # Compute the composition of the cementious material

        # Check if necessary ingredients are defined
        if not self.getCement:
            print("Error : Cement not defined")
            return
        if not self.getWater:
            print("Error : Water not defined")
            return
        if not self.getAggregates:
            print("Error : Aggregates not defined")
            return

        # Compute the composition by means of differents methods

        pass
    




"""
Ingredients : Genrals ingredients for cementious materials
"""
class Ingredients:
    def __init__(self, Name, MatType, Color=None):
        self.Name = Name
        self.MatType = MatType
        self.Color = Color

        # properties
        self.BulkDensity = 0
        self.ParticleDensity = 0

        # quantities
        self.Volume = 0
        self.Mass = 0

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
    def getVolume(self, Volume, BParticleDensity=False):
        self.Volume = Volume
        if BParticleDensity:
            self.Mass = self.Volume * self.getParticleDensity
        else:
            self.Mass = self.Volume * self.getBulkDensity

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
        return self.Mass

    @getMass.setter
    def getMass(self, Mass, BParticleDensity=False):
        self.Mass = Mass
        if BParticleDensity:
            if self.getParticleDensity != 0:
                self.Volume = self.Mass / self.getParticleDensity
            else:
                print("Error : Particle Density not defined")
                self.Volume = 0
        else:
            if self.getBulkDensity != 0:
                self.Volume = self.Mass / self.getBulkDensity
            else:
                print("Error : Bulk Density not defined")
                self.Volume = 0


"""
Cement
Colors : Grey
"""
class Cement(Ingredients):
    def __init__(self, Name, CementClass, CementType):
        super().__init__(self, Name=Name, MatType="Cement")
        self.CementClass = False  # [int] Class of cement (CEM X, ...)
        self.CementType = False  # [str] Type of cement (Portland, Blast Furnace, ...)

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

    def PLTGranulometry(self, paramPLT=False, BStart=True, BEnd=True, BPourcent=True):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Parameters of the plot
        paramPLT.getTitle = "Particle size distribution of the " + self.getName
        paramPLT.getXLabel = "Particle size [mm]"
        paramPLT.getYLabel = "Ratio of passers-by [-]"

        GranuloRatio = self.getGranuloRatio
        if BPourcent:
            paramPLT.getYLabel = "Percentage of passers-by [%]"
            GranuloRatio = [x*100 for x in GranuloRatio]

        TempColor = paramPLT.getColor
        paramPLT.getColor = self.getColor

        paramPLT.getXScaleType = 1

        PLTPlot(self.getGranuloDiam, GranuloRatio, paramPLT)

        paramPLT.getColor = TempColor

        if BEnd:
            PLTShow(paramPLT)

"""
Adjuvant
Colors : Green
"""
class Adjuvant(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Adjuvant")