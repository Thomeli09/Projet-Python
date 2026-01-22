# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:43:03 2025

@author: Thommes Eliott
"""

# Concrete library

"""
Improovements :
- Ajouter des méthodes de calcul de la composition (ex: Feret, Bolomey, ...)
"""

# Other Lib
import numpy as np


# Custom Lib
from PlotLib import ParamPLT, StartPlots, CloseAllPlots, PLTShow, DefaultParamPLT, PLTPie, PLTPlot
from DataManagementLib import ListSort, ListFindFirstMaxPair
from MaterialLib import Material
from GeometryLib import Volume


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

        # Initialize the material
        super().__init__(Name=Name, ID=ID, MatType=MatType)

        # Graphics
        self.getColour = "dimgray"  # Default color for cementious materials

        # Ingredients
        # Absolute volume of => p:Gravel, s:Sand, c:Cement, e:Water, v:Void
        self.LCement = []  # [L of Cement] Cement object (Unlimited)
        self.Water = []  # [Water] Water object (Limited to one object)
        self.LAggregates = []  # [L of Aggregate] Aggregates objects (Unlimited)
        self.LAdjuvants = []  # [L of Adjuvant] Adjuvants objects (Unlimited)

        # Properties of the mixture
        self.MCement = 0  # [float] Mass of cement (c) [kg/m^3 of concrete]
        self.VCement = 0  # [float] Volume of cement (c) [m^3/m^3 of concrete]
        self.MWater = 0  # [float] Mass of water (e) [kg/m^3 of concrete]
        self.VWater = 0  # [float] Volume of water (e) [m^3/m^3 of concrete]
        self.MRock = 0  # [float] Mass of rock (p) [kg/m^3 of concrete]
        self.VRock = 0  # [float] Volume of rock (p) [m^3/m^3 of concrete]
        self.MSand = 0 # [float] Mass of sand (s) [kg/m^3 of concrete]
        self.VSand = 0 # [float] Volume of sand (s) [m^3/m^3 of concrete]

        self.VVoids = 0  # [float] Volume of voids in the concrete (v) [m^3/m^3 of concrete]

        self.MAggregates = 0  # [float] Mass of aggregates (p+s) [kg/m^3 of concrete]
        self.VAggregates = 0  # [float] Volume of aggregates (p+s) [m^3/m^3 of concrete]
        self.MSolids = 0  # [float] Mass of solids (p+s+c) [kg/m^3 of concrete]
        self.VSolids = 0  # [float] Volume of solids (p+s+c) [m^3/m^3 of concrete]
        self.MCementPaste = 0  # [float] Mass of cement paste (c+e+v) [kg/m^3 of concrete]
        self.VCementPaste = 0  # [float] Volume of cement paste (c+e+v) [m^3/m^3 of concrete]
        self.MMortar = 0  # [float] Mass of mortar (s+c+e+v) [kg/m^3 of concrete]
        self.VMortar = 0  # [float] Volume of mortar (s+c+e+v) [m^3/m^3 of concrete]
        self.MConcrete = 0  # [float] Mass of concrete (p+s+c+e+v) [kg/m^3 of concrete]
        self.VConcrete = 0  # [float] Volume of concrete (p+s+c+e+v) [m^3/m^3 of concrete]
 

        self.DMax = 0  # [float] Maximum diameter of the composition [mm]
        self.GranuloDiamMix = None  # Vector of diameter for the granulometry of the composition [mm]
        self.GranuloRatioMix = None  # Vector of ratio for the granulometry of the composition [-] or [%]

        # Objectives
        self.Obectif = 0  # [L of objectives] Objective of composition 

        # Parameters
        self.DmaxSand = 2  # [float] Maximum diameter of sand [mm]
        self.BDmaxSand = False  # [bool] Boolean to indicate if the DmaxSand is used in the computation of sand and rock or default material denomination

    # Ingredients
    @property
    def getCement(self):
        return self.LCement

    @getCement.setter
    def getCement(self, ItemCement):
        if isinstance(ItemCement, list):
            self.LCement = ItemCement
        elif isinstance(ItemCement, Cement):
            self.LCement.append(ItemCement)
        else:
            print("Error : Invalid input for Cement")

    @property
    def getWater(self):
        return self.Water

    @getWater.setter
    def getWater(self, ItemWater):
        if isinstance(ItemWater, list):
            self.Water = ItemWater
        elif isinstance(ItemWater, Water):
            self.Water.append(ItemWater)
        else:
            print("Error : Invalid input for Water")

    @property
    def getAggregates(self):
        return self.LAggregates

    @getAggregates.setter
    def getAggregates(self, ItemAggregate):
        if isinstance(ItemAggregate, list):
            self.LAggregates = ItemAggregate
        elif isinstance(ItemAggregate, Aggregate):
            self.LAggregates.append(ItemAggregate)
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

    # Properties of the composition
    @property
    def getMCement(self):
        return self.MCement

    @getMCement.setter
    def getMCement(self, MCement):
        self.MCement = MCement

    @property
    def CMPTCement(self):
        """
        Compute the mass and volume of cement (c)
        """
        MCement = 0
        VCement = 0
        for Cement in self.getCement:
            VCement += Cement.getVolume
            MCement += Cement.getMass
        self.getMCement = MCement
        self.getVCement = VCement
        return MCement, VCement

    @property
    def getVCement(self):
        return self.VCement

    @getVCement.setter
    def getVCement(self, VCement):
        self.VCement = VCement

    @property
    def CMPTWater(self):
        """
        Compute the mass and volume of water (e)
        """
        MWater = 0
        VWater = 0
        for Water in self.getWater:
            MWater += Water.getMass
            VWater += Water.getVolume
        self.getMWater = MWater
        self.getVWater = VWater
        return MWater, VWater

    @property
    def getMRock(self):
        return self.MRock

    @getMRock.setter
    def getMRock(self, MRock):
        self.MRock = MRock

    @property
    def getVRock(self):
        return self.VRock

    @getVRock.setter
    def getVRock(self, VRock):
        self.VRock = VRock

    @property
    def CMPTRock(self):
        """
        Compute the mass and volume of rock based on the aggregates (p)

        Improovements :
        Refine when BDmaxSand is True to only take the part of the aggregates above the DmaxSand 
        not all the volume of the aggregates
        """
        MRock = 0
        VRock = 0
        if self.getBDmaxSand:
            for Aggregate in self.getAggregates:
                if Aggregate.getDmax > self.getDmaxSand:
                    MRock += Aggregate.getMass
                    VRock += Aggregate.getVolume
        else:
            for Aggregate in self.getAggregates:
                if Aggregate.getMatType == "Aggregate":
                    MRock += Aggregate.getMass
                    VRock += Aggregate.getVolume
        self.getMRock = MRock
        self.getVRock = VRock
        return self.getMRock, self.getVRock

    @property
    def getMSand(self):
        return self.MSand

    @getMSand.setter
    def getMSand(self, MSand):
        self.MSand = MSand

    @property
    def getVSand(self):
        return self.VSand

    @getVSand.setter
    def getVSand(self, VSand):
        self.VSand = VSand

    @property
    def CMPTSand(self):
        """
        Compute the mass and volume of sand based on the aggregates (s)
        """
        MSand = 0
        VSand = 0
        if self.getBDmaxSand:
            for Aggregate in self.getAggregates:
                if Aggregate.getDmax < self.getDmaxSand:
                    MSand += Aggregate.getMass
                    VSand += Aggregate.getVolume
        else:
            for Aggregate in self.getAggregates:
                if Aggregate.getMatType == "Sand":
                    MSand += Aggregate.getMass
                    VSand += Aggregate.getVolume
        self.getMSand = MSand
        self.getVSand = VSand
        return self.getMSand, self.getVSand

    @property
    def getVVoids(self):
        return self.VVoids

    @getVVoids.setter
    def getVVoids(self, VVoids):
        self.VVoids = VVoids
    
    @property
    def getMAggregates(self):
        return self.MAggregates

    @getMAggregates.setter
    def getMAggregates(self, MAggregates):
        self.MAggregates = MAggregates

    @property
    def getVAggregates(self):
        return self.VAggregates

    @getVAggregates.setter
    def getVAggregates(self, VAggregates):
        self.VAggregates = VAggregates

    @property
    def CMPTAggregates(self):
        """
        Compute the mass and volume of aggregates (p+s)
        """
        self.CMPTSand
        self.CMPTRock
        self.getMAggregates = self.getMSand
        self.getVAggregates = self.getVSand
        self.getMAggregates += self.getMRock
        self.getVAggregates += self.getVRock
        return self.getMAggregates, self.getVAggregates

    @property
    def getMSolids(self):
        return self.MSolids

    @getMSolids.setter
    def getMSolids(self, MSolids):
        self.MSolids = MSolids

    @property
    def getVSolids(self):
        return self.VSolids

    @getVSolids.setter
    def getVSolids(self, VSolids):
        self.VSolids = VSolids

    @property
    def CMPTSolids(self):
        """
        Compute the mass and volume of solids (p+s+c)
        """
        self.CMPTAggregates
        self.CMPTCement
        self.getMSolids = self.getMAggregates
        self.getVSolids = self.getVAggregates
        self.getMSolids += self.getMCement
        self.getVSolids += self.getVCement
        return self.getMSolids, self.getVSolids

    @property
    def getMCementPaste(self):
        return self.MCementPaste

    @getMCementPaste.setter
    def getMCementPaste(self, MCementPaste):
        self.MCementPaste = MCementPaste

    @property
    def getVCementPaste(self):
        return self.VCementPaste

    @getVCementPaste.setter
    def getVCementPaste(self, VCementPaste):
        self.VCementPaste = VCementPaste

    @property
    def CMPTCementPaste(self):
        """
        Compute the mass and volume of cement paste (c+e+v)
        """
        self.CMPTCement
        self.CMPTWater
        self.getMCementPaste = self.getMCement
        self.getVCementPaste = self.getVCement
        self.getMCementPaste += self.getMWater
        self.getVCementPaste += self.getVWater
        self.getVCementPaste += self.getVVoids
        return self.getMCementPaste, self.getVCementPaste

    @property
    def getMMortar(self):
        return self.MMortar

    @getMMortar.setter
    def getMMortar(self, MMortar):
        self.MMortar = MMortar

    @property
    def getVMortar(self):
        return self.VMortar

    @getVMortar.setter
    def getVMortar(self, VMortar):
        self.VMortar = VMortar

    @property
    def CMPTMortar(self):
        """
        Compute the mass and volume of mortar (s+c+e+v)
        """
        self.CMPTSand
        self.CMPTCementPaste
        self.getMMortar = self.getMSand
        self.getVMortar = self.getVSand
        self.getMMortar += self.getMCementPaste
        self.getVMortar += self.getVCementPaste
        return self.getMMortar, self.getVMortar

    @property
    def getMConcrete(self):
        return self.MConcrete

    @getMConcrete.setter
    def getMConcrete(self, MConcrete):
        self.MConcrete = MConcrete

    @property
    def getVConcrete(self):
        return self.VConcrete

    @getVConcrete.setter
    def getVConcrete(self, VConcrete):
        self.VConcrete = VConcrete

    @property
    def CMPTConcrete(self):
        """
        Compute the mass and volume of concrete (p+s+c+e+v)
        """
        self.CMPTAggregates
        self.CMPTMortar
        self.getMConcrete = self.getMRock
        self.getVConcrete = self.getVRock
        self.getMConcrete += self.getMMortar
        self.getVConcrete += self.getVMortar
        return self.getMConcrete, self.getVConcrete

    @property
    def getDMax(self):
        return self.DMax

    @getDMax.setter
    def getDMax(self, DMax):
        """
        Compute the maximum diameter of the composition
        """
        DMax = 0
        for Aggregate in self.getAggregates:
            if Aggregate.getDmax > DMax:
                DMax = Aggregate.getDmax
        self.DMax = DMax
        return self.getDMax

    @property
    def getGranuloDiamMix(self):
        return self.GranuloDiamMix

    @getGranuloDiamMix.setter
    def getGranuloDiamMix(self, GranuloDiamMix):
        self.GranuloDiamMix = GranuloDiamMix

    @property
    def getGranuloRatioMix(self):
        return self.GranuloRatioMix

    @getGranuloRatioMix.setter
    def getGranuloRatioMix(self, GranuloRatioMix):
        self.GranuloRatioMix = GranuloRatioMix

    @property
    def CMPGranuloRatioMix(self):
        """
        Compute the granulometry of the mix of aggregates
        """
        # Mass and volume of aggregates in the mix
        MAggregates, VAggregates = self.CMPTAggregates # vérifier si celà marche correctement

        # Merging all the diameters of the aggregates in the mix
        LAggregates = self.getAggregates
        GranuloDiamMix = np.concatenate([np.asarray(Aggregate.getGranuloDiam, dtype=float) for Aggregate in LAggregates])
        GranuloDiamMix = np.unique(GranuloDiamMix)
        LogGranuloDiamMix = np.log10(GranuloDiamMix)
        GranuloRatioMix = np.zeros_like(GranuloDiamMix, dtype=float)

        # For each aggregate, add its granulometry ratio weighted by its mass proportion in the mix to the mix granulometry while interpolating the missing values
        for Aggregate in LAggregates:
            ProportMass = Aggregate.getMass/MAggregates
            GranuloDiamAgg = np.asarray(Aggregate.getGranuloDiam, dtype=float)
            GranuloRatioAgg = np.asarray(Aggregate.getGranuloRatio, dtype=float)

            # Sorting the granulometry of the aggregate
            Order = np.argsort(GranuloDiamAgg)
            GranuloDiamAgg = GranuloDiamAgg[Order]
            GranuloRatioAgg = GranuloRatioAgg[Order]

            # Adding the weighted granulometry ratio to the mix granulometry ratio with interpolation
            LogGranuloDiamAgg = np.log10(GranuloDiamAgg) # Warning : Need to do the interpolation in log scale because of the logarithmic scale of the granulometric plot
            GranuloRatioMix += np.interp(LogGranuloDiamMix, LogGranuloDiamAgg, GranuloRatioAgg) * ProportMass

        self.getGranuloDiamMix = GranuloDiamMix
        self.getGranuloRatioMix = GranuloRatioMix
        return self.getGranuloDiamMix, self.getGranuloRatioMix
    # Objectives

    # Parameters
    @property
    def getDmaxSand(self):
        return self.DmaxSand

    @getDmaxSand.setter
    def getDmaxSand(self, DmaxSand):
        self.DmaxSand = DmaxSand

    @property
    def getBDmaxSand(self):
        return self.BDmaxSand

    @getBDmaxSand.setter
    def getBDmaxSand(self, BDmaxSand):
        self.BDmaxSand = BDmaxSand

    # Plot of the granulometries of the ingredients
    def PLTGranuloAggregates(self, paramPLT=False, BStart=True, BEnd=True, BPourcent=True):
        """
        Plot the granulometry of each aggregate in the composition

        Args:
            paramPLT: Parameters of the plot
            BStart: Boolean to indicate if the plot starts in a new figure
            BEnd: Boolean to indicate if the plot ends and shows the figure
            BPourcent: Boolean to indicate if the y-axis is in percentage (True) or ratio (False)

        Returns:
            Plot of the granulometry of each aggregate

        Improvement : Add the the differents markers for each granulometry
        """
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Plot of granulometries
        for Aggregate in self.getAggregates:
            paramPLT.getLegends = [Aggregate.getName]
            Aggregate.PLTGranulometry(paramPLT, BStart=False, BEnd=False, BPourcent=BPourcent)

        paramPLT.getTitle = "Particle size distribution of the aggregates in " + self.getName

        if BEnd:
            PLTShow(paramPLT)

    # Plot of the granulometry curves of the composition
    def PLTGranuloAggregatesMix(self, paramPLT=False, BStart=True, BEnd=True, BPourcent=True):
        """
        Plot the granulometry of the mix of aggregates
        
        Args:
            paramPLT: Parameters of the plot
            BStart: Boolean to indicate if the plot starts in a new figure
            BEnd: Boolean to indicate if the plot ends and shows the figure
            BPourcent: Boolean to indicate if the y-axis is in percentage (True) or ratio (False)

        Returns:
            Plot of the granulometry of the mix
        """
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        GranuloDiamMix, GranuloRatioMix = self.CMPGranuloRatioMix

        # Convert to percentage if needed
        if BPourcent:
            paramPLT.getYLabel = "Percentage of passers-by (%)"
            GranuloRatioMix = GranuloRatioMix * 100.0

        # Plot the granulometry of the mix
        paramPLT.getXScaleType = 1
        PLTPlot(GranuloDiamMix, GranuloRatioMix, paramPLT)

        paramPLT.getTitle = "Particle size distribution of the " + self.getName
        paramPLT.getXLabel = "Particle size (mm)"
        paramPLT.getYLabel = "Ratio of passers-by (%)"

        if BEnd:
            PLTShow(paramPLT)

    # Plots of the composition
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

    # Computation of the composition
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
        # # Water to cement ratio

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
        super().__init__(Name=Name, ID=ID, MatType=MatType)

        # Graphics
        self.getColour = Color

        # Properties

        # Quantities
        self.Volume = 0  # [float] Volume of the ingredient [m^3/m^3 of concrete]
        self.Mass = 0  # [float] Mass of the ingredient [kg/m^3 of concrete]

    @property
    def getVolume(self):
        return self.Volume

    @getVolume.setter
    def getVolume(self, Volume):
        self.Volume = Volume

    @property
    def getMass(self):
        return self.Mass

    @getMass.setter
    def getMass(self, Mass):
        self.Mass = Mass

    def getVolume2Mass(self, BDensity=True):
        """
        Convert volume to mass based on the density of the material
        """
        if BDensity:
            self.getMass = self.getVolume * self.getDensity
        else:
            self.getMass = self.getVolume * self.getBulkDensity
        return self.getMass

    def getMass2Volume(self, BDensity=True):
        """
        Convert mass to volume based on the density of the material
        """
        if BDensity:
            if self.getDensity == 0:
                print("Error : Density is zero, cannot compute volume")
                return 0
            self.getVolume = self.getMass / self.getDensity
        else:
            if self.getBulkDensity == 0:
                print("Error : Bulk Density is zero, cannot compute volume")
                return 0
            self.getVolume = self.getMass / self.getBulkDensity
        return self.getVolume

    def getDensity(self, BDensity=True):
        """
        Compute the density of the material based on the mass and volume
        """
        if self.getVolume == 0:
            print("Error : Volume is zero, cannot compute density")
            return 0
        if BDensity:
            self.getDensity = self.getMass / self.getVolume
            return self.getDensity
        else:
            self.getBulkDensity = self.getMass / self.getVolume
            return self.getBulkDensity

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
        """
        Property setter for Cement Type based on CementType input and CementClass.

        Args:
    
        Improovements :
           Adding CementClass verification for CementType definition
        """
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

        self.getDensity = 1000  # [float] Density of water [kg/m^3]
        self.getBulkDensity = 1000  # [float] Bulk density of water [kg/m^3]


"""
Aggregate
Default colors : Sienna or Orange
"""
"""
Improovements :
- Add caracteristics of the aggregates (Rock type, Size (min/max), Type of aggregates (rolled, crushed, ...))
"""
class Aggregate(Ingredient):
    def __init__(self, Name, ID, MatType, StrRockType, StrAggregateType, StrDiamExtend=None):
        # MatType : Type of aggregate (Gravel, Sand, ...)
        if isinstance(MatType, int):
            if MatType==1:
                MatType="Aggregate"
                Color = "sienna"
            elif MatType==2:
                MatType="Sand"
                Color = "orange"
            else:
                print("Error : Type of aggregate not defined")
        elif isinstance(MatType, str):
            if MatType=="Aggregate":
                Color = "sienna"
            elif MatType=="Sand":
                Color = "orange"
            else:
                print("Error : Type of aggregate not defined")

        super().__init__(Name=Name, ID=ID, MatType=MatType, Color=Color)

        # Caracteristics of the aggregate
        self.RockType = StrRockType  # [str] Type of rock (Granite, Basalt, Limestone, ...)
        self.AggregateType = StrAggregateType  # [str] Type of aggregates (Rolled, Crushed, ...)
        self.DiamExtend = StrDiamExtend  # [str] Maximum and minimum diameter of the aggregates [mm]

        # Granulometry
        self.GranuloDiam = [] # [float] Diameter of granulometry [mm]
        self.GranuloRatio = [] # [float] Ratio of granulometry [0; 1]

        # Water-related properties
        self.WaterAbsorption = 0  # [float] Water absorption of the aggregate mass [%]

    # Caracteristics of the aggregate
    @property
    def getRockType(self):
        return self.RockType

    @getRockType.setter
    def getRockType(self, RockType):
        self.RockType = RockType

    @property
    def getAggregateType(self):
        return self.AggregateType

    @getAggregateType.setter
    def getAggregateType(self, AggregateType):
        self.AggregateType = AggregateType

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

    # Water-related properties
    @property
    def getWaterAbsorption(self):
        return self.WaterAbsorption

    @getWaterAbsorption.setter
    def getWaterAbsorption(self, WaterAbsorption):
        self.WaterAbsorption = WaterAbsorption

    # Granulometry plot
    def PLTGranulometry(self, paramPLT=False, BStart=True, BEnd=True, BPourcent=True):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Recovering parameters of the plot
        GranuloRatio = self.getGranuloRatio
        if BPourcent:
            paramPLT.getYLabel = "Percentage of passers-by (%)"
            GranuloRatio = [x*100 for x in GranuloRatio]

        TempColor = paramPLT.getColour
        paramPLT.getColour = self.getColour

        PLTPlot(self.getGranuloDiam, GranuloRatio, paramPLT)

        paramPLT.getColour = TempColor

        # Parameters of the plot
        paramPLT.getTitle = "Particle size distribution of the " + self.getName
        paramPLT.getXLabel = "Particle size (mm)"
        paramPLT.getYLabel = "Ratio of passers-by (%)"

        paramPLT.getXScaleType = 1

        if BEnd:
            PLTShow(paramPLT)

"""
Adjuvant
Default colors : Green
"""
class Adjuvant(Ingredient):
    def __init__(self, Name, ID):
        super().__init__(Name=Name, ID=ID, MatType="Adjuvant", Color="lime")


# Type of differents typical samples in concrete sector
class SampleConcrete(Volume):
    def __init__(self, Name, ID, LSurface):
        # Metadata
        super().__init__(LSurface=LSurface, Name=Name)
        self.ID = ID

        # Results of computations
        self.CMPTResults = None

    # Metadata
    @property
    def getID(self):
        return self.ID

    @getID.setter
    def getID(self, ID):
        self.ID = ID

    # Results of computations
    @property
    def getCMPTResults(self):
        return self.CMPTResults

    @getCMPTResults.setter
    def getCMPTResults(self, CMPTResults):
        self.CMPTResults = CMPTResults

# Cube : 150x150x150 mm
class SampleCube(SampleConcrete):
    def __init__(self, Name, ID, LSurface):
        super().__init__(Name="Cube", ID=ID, LSurface=LSurface)

# Cylinder : 150 mm diameter, 300 mm height
class SampleCylinder(SampleConcrete):
    def __init__(self, Name, ID, LSurface):
        super().__init__(Name="Cylinder", ID=ID, LSurface=LSurface)
