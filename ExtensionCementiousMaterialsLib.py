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
from DataManagementLib import ListSort, ListFindFirstMaxPair

"""
CemMaterials : Cementious materials objects
"""
class CemMaterials(Composition):
    def __init__(self, Name, ProductionDate, Experiments):
        super().__init__(Name=Name, ProductionDate=ProductionDate,
                         Experiments=Experiments)
        
        # Ingredients
        # Absolute volume of=> p:Gravel,s:Sand ,c:Cement, e:Water, v:Void
        self.Cement = False  # [Cement] Cement object (Limited to one object)
        self.Water = False  # [Water] Water object (Limited to one object)
        self.Aggregates = []  # [Aggregat] Aggregates objects (Unlimited)
        self.Adjuvants = []  # [Adjuvant] Adjuvants objects (Unlimited)

        # Properties of the composition
        self.VRock = 0  # [float] Volume of rock (p) [m^3/m^3 of concrete]
        self.VSand = 0 # [float] Volume of sand (s) [m^3/m^3 of concrete]

        self.VVoids = 0  # [float] Volume of voids in the concrete (v) [m^3/m^3 of concrete]

        self.VConcrete = 0  # [float] Volume of concrete (p+s+c+e+v) [m^3/m^3 of concrete]
        self.VSOlids = 0  # [float] Volume of solids (p+s+c) [m^3/m^3 of concrete]
        self.VAggregats = 0  # [float] Volume of aggregates (p+s) [m^3/m^3 of concrete]
        self.VMortar = 0  # [float] Volume of mortar (s+c+e+v) [m^3/m^3 of concrete]
        self.VCementPaste = 0  # [float] Volume of cement paste (c+e+v) [m^3/m^3 of concrete]


        self.DMax = 0  # [float] Maximum diameter of the composition [mm]
        self.Obectif = 0  # [float] Objective of composition 

        
        # Parameters
        self.DmaxSand = 2  # [float] Maximum diameter of sand [mm]

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
        # Rajouter des paramètres en plus
        # Résoudres le problème des arguments de PLTPie
        # Résoudres le problème des couleurs

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


    # Water to cement ratio
    def FeretFormula(self, BSimpli=False):
        """
        Compute the Feret formula for the composition
        
        Values of the formula:
        - K : Granular coefficient
        - Rc : Compression strength of the normalised mortar [MPa]
        - K0 : ???
        - Lambda : Cement matrix quality factor
        - FcCube : Compression strength of the concrete [MPa]

        c, e, v : Cement, Water, Void are in volume
        """
        K = 4.9 # [float] Experimental value
        Rc = 1
        e=1
        c=1
        v=1
        K0 = K * Rc
        if BSimpli:  # Simplified formula
            Lambda = 1/(1+e/c) 
        else:  # Normal formula
            Lambda = c/(c+e+v)
        FcCube = K0 * Lambda**2

        return FcCube

    def BolomeyFormula(self, K, h1):
        """
        Compute the Bolomey formula for the composition

        Values of the formula:
        - K : Coefficient [26-36]
        - h1 : Coefficient [0.45-0.87]

        C, E : Cement, Water are by mass
        """
        if K<26 or K>36:
            print("Error : Coefficient K not in the range [26-36]")
            return 0
        if h1<0.45 or h1>0.87:
            print("Error : Coefficient h1 not in the range [0.45-0.87]")
            return 0
        E = 1
        h1 = 1
        C = 1
        FcCube = K*(C/E-h1)
        return FcCube

    # Granular squeletton
    def FullerCurve(self, dList):
        """
        Compute the Fuller curve for the composition

        Args:
        dList: List of diameters of the granulometry [mm]

        return:
        x: List of the percentage of passers-by [-]
        """
        DMax = self.DMax # [float] Maximum diameter of the composition [mm]
        x = [100*(d/DMax)**0.5 for d in dList]

        return x

    def BolomeyCurve(self, dList, A):
        """
        Compute the Bolomey curve for the composition

        Args:
        dList: List of diameters of the granulometry [mm]
        A: Coefficient depending on the type of aggregates [8-16]

        return:
        x: List of the percentage of passers-by [-]
        """
        DMax = self.DMax

        if A<8 or A>16:
            print("Error : Coefficient A not in the range [8-16]")
            return 0

        x = [A*(100-A)*(d/DMax)**0.5 for d in dList]
        return x

    def FauryCurve(self, dList, A):
        """
        Compute the Faury curve for the composition
        Args:
        dList: List of diameters of the granulometry [mm]
        A: Coefficient depending on the type of aggregates [8-16]
        return:
        x: List of the percentage of passers-by [-]
        """
        B = 1
        R = 1
        D = 1
        DMax = self.DMax
        if A<8 or A>16:
            print("Error : Coefficient A not in the range [8-16]")
            return 0
        x = [A+17*(DMax**1/5)+(B/(R/D-0.75)) for d in dList]
        return x
    # Eeff volume of water

        
    




"""
Ingredients : Genrals ingredients for cementious materials
"""
class Ingredients:
    def __init__(self, Name, MatType, Color=None):
        self.Name = Name
        self.MatType = MatType
        self.Color = Color
        self.Hatch = None

        # properties
        self.BulkDensity = 0  # [float] Bulk density of the ingredient [kg/m^3]
        self.ParticleDensity = 0  # [float] Particle density of the ingredient [kg/m^3]

        # quantities
        self.Volume = 0  # [float] Volume of the ingredient [m^3/m^3 of concrete]
        self.Mass = 0  # [float] Mass of the ingredient [kg/m^3 of concrete]

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
    def getHatch(self):
        return self.Hatch

    @getHatch.setter
    def getHatch(self, Hatch):
        self.Hatch = Hatch

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
        super().__init__(Name=Name, MatType="Cement")
        self.CementClass = None  # [int] Class of cement (CEM X, ...)
        self.CementType = None  # [str] Type of cement (Portland, Blast Furnace, ...)

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

        self.VolumeEeff = 0

"""
Aggregat
Colors : Brown
"""
class Aggregat(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Aggregat")
        """
        Improovements :
        - Add caracteristics of the aggregates 
        (Rock type, Size (min/max), Type of aggregates (rolled, crushed, ...))
        """

        # Granulometry
        self.GranuloDiam = [] # [float] Diameter of granulometry [mm]
        self.GranuloRatio = [] # [float] Ratio of granulometry [0; 1]

    @property
    def getGranuloDiam(self):
       return self.GranuloDiam

    @getGranuloDiam.setter
    def getGranuloDiam(self, GranuloDiam):
        if isinstance(GranuloDiam, float):
            self.GranuloDiam.append(GranuloDiam)
        elif isinstance(GranuloDiam, list):
            self.GranuloDiam = GranuloDiam
        else:
            print("Error : Invalid input for Granulometry Diameter")
        self.GranuloDiam = ListSort(self.GranuloDiam)

    @property
    def getGranuloRatio(self):
        return self.GranuloRatio

    @getGranuloRatio.setter
    def getGranuloRatio(self, GranuloRatio):
        if isinstance(GranuloRatio, float):
            self.GranuloRatio.append(GranuloRatio)
        elif isinstance(GranuloRatio, list):
            self.GranuloRatio = GranuloRatio
        else:
            print("Error : Invalid input for Granulometry Ratio")
        self.GranuloRatio = ListSort(self.GranuloRatio)

    @property
    def getDmax(self):
        # [float] Maximum diameter of the granulometry [mm]
        if self.getGranuloDiam and self.getGranuloRatio:
            MaxRatio, MaxDiam = ListFindFirstMaxPair(self.getGranuloRatio, self.getGranuloDiam)
            return MaxDiam
        else:
            print("Error: Granulometry not defined")
            return 0



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