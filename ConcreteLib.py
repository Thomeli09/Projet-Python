# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:43:03 2025

@author: Thommes Eliott
"""

# Concrete library


# Other Lib
from turtle import color
import pandas as pd
import numpy as np


# Custom Lib
from PlotLib import ParamPLT, StartPlots, CloseALLPlots, PLTShow, DefaultParamPLT, PLTPie, PLTPlot
from DataManagementLib import ListSort, ListFindFirstMaxPair
from MaterialLib import Material


"""
CemMat : Cementious materials objects
"""
class CemMat(Material):
    def __init__(self, Name, ID, Type):
        # Type of cementious material
        if isinstance(Type, int):
            if Type==1:
                MatType="Concrete"
            elif Type==2:
                MatType="Mortar"
            elif Type==3:
                MatType="Cement Paste"
            else:
                print("Error : Type of cementious material not defined")
        else:
            if Type not in ["Concrete", "Mortar", "Cement Paste"]:
                print("Error : Type of cementious material not defined")
            else:
                MatType = Type

        super().__init__(Name=Name, ID=ID, Type=MatType)

        # Ingredients
        # Absolute volume of => p:Gravel, s:Sand, c:Cement, e:Water, v:Void
        self.Cement = False  # [Cement] Cement object (Limited to one object)
        self.Water = False  # [Water] Water object (Limited to one object)
        self.LAggregates = []  # [Aggregat] Aggregates objects (Unlimited)
        self.LAdjuvants = []  # [Adjuvant] Adjuvants objects (Unlimited)

        # Properties of the composition
        self.VRock = 0  # [float] Volume of rock (p) [m^3/m^3 of concrete]
        self.VSand = 0 # [float] Volume of sand (s) [m^3/m^3 of concrete]

        self.VVoids = 0  # [float] Volume of voids in the concrete (v) [m^3/m^3 of concrete]

        self.VConcrete = 0  # [float] Volume of concrete (p+s+c+e+v) [m^3/m^3 of concrete]
        self.VSolids = 0  # [float] Volume of solids (p+s+c) [m^3/m^3 of concrete]
        self.VAggregats = 0  # [float] Volume of aggregates (p+s) [m^3/m^3 of concrete]
        self.VMortar = 0  # [float] Volume of mortar (s+c+e+v) [m^3/m^3 of concrete]
        self.VCementPaste = 0  # [float] Volume of cement paste (c+e+v) [m^3/m^3 of concrete]

        self.DMax = 0  # [float] Maximum diameter of the composition [mm]
        self.Obectif = 0  # [float] Objective of composition 

        # Parameters
        self.DmaxSand = 2  # [float] Maximum diameter of sand [mm]

        # Experiments
        self.LExperiments = []  # [L of Experiment] Experiments done on the cementious material

    # Ingredients
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
        return self.LAggregates

    @getAggregates.setter
    def getAggregates(self, ItemAggregat):
        if isinstance(ItemAggregat, list):
            self.LAggregates = ItemAggregat
        elif isinstance(ItemAggregat, Aggregat):
            self.LAggregates.append(ItemAggregat)
        else:
            print("Error : Invalid input for Aggregates")

    @property
    def getAdjuvants(self):
        return self.LAdjuvants

    @getAdjuvants.setter
    def getAdjuvants(self, Adjuvants):
        if isinstance(Adjuvants, list):
            self.LAdjuvants = Adjuvants
        elif isinstance(Adjuvants, Adjuvant):
            self.LAdjuvants.append(Adjuvants)
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
Ingredients : General class for all the ingredients in cementious materials
"""
class Ingredient(Material):
    def __init__(self, Name, ID, MatType, Color=None):
        super().__init__(Name=Name, ID=ID, Type=MatType)

        # Graphics
        self.getColor = Color

        # Properties
        self.BulkDensity = 0  # [float] Bulk density of the ingredient [kg/m^3]
        self.ParticleDensity = 0  # [float] Particle density of the ingredient [kg/m^3]

        # Quantities
        self.Volume = 0  # [float] Volume of the ingredient [m^3/m^3 of concrete]
        self.Mass = 0  # [float] Mass of the ingredient [kg/m^3 of concrete]

    @property
    def getBulkDensity(self):
        return self.BulkDensity

    @getBulkDensity.setter
    def getBulkDensity(self, BulkDensity):
        self.BulkDensity = BulkDensity
        self.Mass = self.getVolume * BulkDensity

    @property
    def getParticleDensity(self):
        return self.ParticleDensity

    @getParticleDensity.setter
    def getParticleDensity(self, ParticleDensity):
        self.ParticleDensity = ParticleDensity

    @property
    def getVolume(self):
        return self.Volume

    @getVolume.setter
    def getVolume(self, Volume):
        self.Volume = Volume
        self.Mass = Volume * self.getBulkDensity

    @property
    def getMass(self):
        return self.Mass

    @getMass.setter
    def getMass(self, Mass):
        self.Mass = Mass
        if self.getParticleDensity != 0:
            self.Volume = Mass / self.getBulkDensity
        else:
            print("Error : Bulk Density not defined")
            self.Volume = 0

"""
Cement
Default colors : Gray
"""
class Cement(Ingredient):
    def __init__(self, Name, ID, CementClass, CementType, CementStrength):
        super().__init__(Name=Name, ID=ID, MatType="Cement", Color="slategray")


        self.CementClass = None  # [int] Class of cement (CEM X)
        self.CementType = None  # [str] Type of cement (Portland, Blast Furnace, ...)
        self.CementStrength = CementStrength  # [float] Strength of the cement [MPa]

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

    @property
    def getCementStrength(self):
        return self.CementStrength

    @getCementStrength.setter
    def getCementStrength(self, CementStrength):
        if isinstance(CementStrength, float):
            self.CementStrength = CementStrength
        else:
            print("Error : Invalid input for Cement Strength")
            self.CementStrength = 0


"""
Water
Default colors : Blue
"""
class Water(Ingredient):
    def __init__(self, Name, ID):
        super().__init__(Name=Name, ID=ID, MatType="Water", Color="b")

        self.VolumeEeff = 0

    @property
    def getVolumeEeff(self):
        return self.VolumeEeff

    @getVolumeEeff.setter
    def getVolumeEeff(self, VolumeEeff):
        self.VolumeEeff = VolumeEeff


"""
Aggregat
Default colors : Brown
"""
"""
Improovements :
- Add caracteristics of the aggregates (Rock type, Size (min/max), Type of aggregates (rolled, crushed, ...))
"""
class Aggregat(Ingredient):
    def __init__(self, Name, ID, MatType, StrRockType, StrAggregatType, StrDiamExtend=None):
        # MatType : Type of aggregate (Gravel, Sand, ...)
        if isinstance(MatType, int):
            if MatType==1:
                MatType="Aggregat"
                Color = "sienna"
            elif MatType==2:
                MatType="Sand"
                Color = "orange"
            else:
                print("Error : Type of aggregate not defined")
        elif isinstance(MatType, str):
            if MatType=="Aggregat":
                Color = "sienna"
            elif MatType=="Sand":
                Color = "orange"
            else:
                print("Error : Type of aggregate not defined")

        super().__init__(Name=Name, ID=ID, MatType=MatType, Color=Color)

        # Caracteristics of the aggregate
        self.RockType = StrRockType  # [str] Type of rock (Granite, Basalt, Limestone, ...)
        self.AggregatType = StrAggregatType  # [str] Type of aggregates (Rolled, Crushed, ...)
        self.DiamExtend = StrDiamExtend  # [str] Maximum and minimum diameter of the aggregates [mm]

        # Granulometry
        self.GranuloDiam = [] # [float] Diameter of granulometry [mm]
        self.GranuloRatio = [] # [float] Ratio of granulometry [0; 1]

    # Caracteristics of the aggregate
    @property
    def getRockType(self):
        return self.RockType

    @getRockType.setter
    def getRockType(self, RockType):
        self.RockType = RockType

    @property
    def getAggregatType(self):
        return self.AggregatType

    @getAggregatType.setter
    def getAggregatType(self, AggregatType):
        self.AggregatType = AggregatType

    @property
    def getDiamExtend(self):
        return self.DiamExtend

    @getDiamExtend.setter
    def getDiamExtend(self, DiamExtend):
        self.DiamExtend = DiamExtend

    # Granulometry
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

    # Granulometry plot
    def PLTGranulometry(self, paramPLT=False, BStart=True, BEnd=True, BPourcent=True):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Parameters of the plot
        paramPLT.getTitle = "Particle size distribution of the " + self.getName
        paramPLT.getXLabel = "Particle size (mm)"
        paramPLT.getYLabel = "Ratio of passers-by (-)"

        GranuloRatio = self.getGranuloRatio
        if BPourcent:
            paramPLT.getYLabel = "Percentage of passers-by (%)"
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
Default colors : Green
"""
class Adjuvant(Ingredient):
    def __init__(self, Name, ID):
        super().__init__(Name=Name, ID=ID, MatType="Adjuvant", Color="lime")


"""
Experiments : Experiments specific to cementious materials
"""
# Adsorption par immersion, ...



# Type of differents typical samples in concrete sector