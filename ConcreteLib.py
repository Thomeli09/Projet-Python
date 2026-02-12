# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:43:03 2025

@author: Thommes Eliott
"""

# Concrete library

"""
Improovements :
should add the getmass adjusted in the pie chart to have the real mass 
add the adjuvant and take into account it's water in the water content but not in the pie chart
"""

# Other Lib
from tkinter import SE
from matplotlib import hatch
import numpy as np


# Custom Lib
from PlotLib import ParamPLT, StartPlots, CloseAllPlots, PLTShow, DefaultParamPLT, PLTPie, PLTPlot
from DataManagementLib import DataSort, ListFindFirstMaxPair
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
 

        self.Dmax = 0  # [float] Maximum diameter of the composition [mm]
        self.Dmin = 0  # [float] Minimum diameter of the composition [mm]
        self.GranuloDiamMix = None  # Vector of diameter for the granulometry of the composition [mm]
        self.GranuloRatioMix = None  # Vector of ratio for the granulometry of the composition [-] or [%]

        # Water properties
        self.AggWaterContent = Water(Name="Water", ID="Water")  # [Water] Water object to define the water content of the aggregates
        self.ECRatio = 0  # [float] Water to cement ratio (E/C)
        self.ECEffRatio = 0  # [float] Effective water to cement ratio (E-Absorbed water)/C

        # Composition targets
        self.CompTarget = None # [CompositionTarget] Composition target object

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
    def getVCement(self):
        return self.VCement

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
    def getMWater(self):
        return self.MWater

    @getMWater.setter
    def getMWater(self, MWater):
        self.MWater = MWater

    @property
    def getVWater(self):
        return self.VWater

    @getVWater.setter
    def getVWater(self, VWater):
        self.VWater = VWater

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
        self.CMPTAggWaterContent
        self.getMCementPaste = self.getMCement
        self.getVCementPaste = self.getVCement
        self.getMCementPaste += self.getMWater
        self.getVCementPaste += self.getVWater
        self.getMCementPaste += self.getAggWaterContent.getMass
        self.getVCementPaste += self.getAggWaterContent.getVolume
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
    def getDmax(self):
        return self.Dmax

    @getDmax.setter
    def getDmax(self, Dmax):
        """
        Compute the maximum diameter of the composition
        """
        Dmax = 0
        for Aggregate in self.getAggregates:
            if Aggregate.getDmax > Dmax:
                Dmax = Aggregate.getDmax
        self.Dmax = Dmax
        return self.getDmax

    @property
    def getDmin(self):
        return self.Dmin

    @getDmin.setter
    def getDmin(self, Dmin):
        """
        Compute the minimum diameter of the composition
        """
        Dmin = 0
        for Aggregate in self.getAggregates:
            if Aggregate.getDmin < Dmin:
                Dmin = Aggregate.getDmin
        self.Dmin = Dmin
        return self.getDmin

    @property
    def getGranuloDiamMix(self):
        return self.GranuloDiamMix

    @getGranuloDiamMix.setter
    def getGranuloDiamMix(self, GranuloDiamMix):
        if isinstance(GranuloDiamMix, float):
            # Append the ratio to the numpy array
            return
        elif isinstance(GranuloDiamMix, list):
            self.GranuloDiamMix = np.asarray(GranuloDiamMix, dtype=float)
        elif isinstance(GranuloDiamMix, np.ndarray):
            self.GranuloDiamMix = GranuloDiamMix
        else:
            print("Error : Invalid input for Granulometry Diameter")
        self.GranuloDiamMix = DataSort(self.GranuloDiamMix)

    @property
    def getGranuloRatioMix(self):
        return self.GranuloRatioMix

    @getGranuloRatioMix.setter
    def getGranuloRatioMix(self, GranuloRatioMix):
        if isinstance(GranuloRatioMix, float):
            # Append the ratio to the numpy array
            return
        elif isinstance(GranuloRatioMix, list):
            self.GranuloRatioMix = np.asarray(GranuloRatioMix, dtype=float)
        elif isinstance(GranuloRatioMix, np.ndarray):
            self.GranuloRatioMix = GranuloRatioMix
        else:
            print("Error : Invalid input for Granulometry Ratio")
        self.GranuloRatioMix = DataSort(self.GranuloRatioMix)

    @property
    def CMPGranuloRatioMix(self):
        """
        Compute the granulometry of the mix of aggregates
        """
        # Mass and volume of aggregates in the mix
        MAggregates, VAggregates = self.CMPTAggregates # vérifier si celà marche correctement

        # Merging all the diameters of the aggregates in the mix
        LAggregates = self.getAggregates
        GranuloDiamMix = np.concatenate([Aggregate.getGranuloDiam for Aggregate in LAggregates])
        GranuloDiamMix = np.unique(GranuloDiamMix)
        LogGranuloDiamMix = np.log10(GranuloDiamMix)
        GranuloRatioMix = np.zeros_like(GranuloDiamMix, dtype=float)

        # For each aggregate, add its granulometry ratio weighted by its mass proportion in the mix to the mix granulometry while interpolating the missing values
        for Aggregate in LAggregates:
            ProportMass = Aggregate.getMass/MAggregates
            GranuloDiamAgg = Aggregate.getGranuloDiam
            GranuloRatioAgg = Aggregate.getGranuloRatio

            # Sorting the granulometry of the aggregate
            Order = np.argsort(GranuloDiamAgg)
            GranuloDiamAgg = GranuloDiamAgg[Order]
            GranuloRatioAgg = GranuloRatioAgg[Order]

            # Adding the weighted granulometry ratio to the mix granulometry ratio with interpolation
            LogGranuloDiamAgg = np.log10(GranuloDiamAgg) # Warning : Need to do the interpolation in log scale because of the logarithmic scale of the granulometric plot
            GranuloRatioMix += np.interp(LogGranuloDiamMix, LogGranuloDiamAgg, GranuloRatioAgg, left=0) * ProportMass

        self.getGranuloDiamMix = GranuloDiamMix
        self.getGranuloRatioMix = GranuloRatioMix
        return self.getGranuloDiamMix, self.getGranuloRatioMix

    # Water properties
    @property
    def getAggWaterContent(self):
        return self.AggWaterContent

    @property
    def CMPTAggWaterContent(self):
        """
        Compute the water content of the aggregates
        """
        MAggWaterContent = 0
        for Aggregate in self.getAggregates:
            MAggWaterContent += Aggregate.CMPTWaterContained

        self.getAggWaterContent.getMass = MAggWaterContent
        self.getAggWaterContent.getVolume = MAggWaterContent / self.getAggWaterContent.getDensity
        return MAggWaterContent

    @property
    def CMPTAggWaterAbsorbed(self):
        """
        Compute the total absorbed water by the aggregates, assuming aggregates are fully dried
        """
        MAggWaterAbsorbed = 0
        for Aggregate in self.getAggregates:
            MAggWaterAbsorbed += Aggregate.CMPTWaterAbsorbed
        return MAggWaterAbsorbed

    @property
    def getECRatio(self):
        return self.ECRatio

    @getECRatio.setter
    def getECRatio(self, ECRatio):
        self.ECRatio = ECRatio

    @property
    def CMPTECRatio(self):
        """
        Compute the water to cement ratio (e/c)
        """
        self.CMPTCement
        self.CMPTWater
        self.CMPTAggWaterContent
        if self.getMCement > 0:
            ECRatio = (self.getMWater + self.getAggWaterContent.getMass) / self.getMCement
        else:
            ECRatio = 0
            print("Error : Cement mass is zero, cannot compute E/C ratio")
        self.getECRatio = ECRatio
        return self.getECRatio

    @property
    def getECEffRatio(self):
        return self.ECEffRatio

    @getECEffRatio.setter
    def getECEffRatio(self, ECEffRatio):
        self.ECEffRatio = ECEffRatio

    @property
    def CMPTECEffRatio(self):
        """
        Compute the effective water to cement ratio (E-Absorbed water)/C
        """
        self.CMPTCement
        self.CMPTWater
        self.CMPTAggWaterContent
        AggWaterAbsorption = self.CMPTAggWaterAbsorbed
        EffectiveWater = self.getMWater + self.getAggWaterContent.getMass - AggWaterAbsorption
        if self.getMCement > 0:
            ECEffRatio = EffectiveWater / self.getMCement
        else:
            ECEffRatio = 0
            print("Error : Cement mass is zero, cannot compute effective e/c ratio")
        self.getECEffRatio = ECEffRatio
        return self.getECEffRatio

    # Composition targets
    @property
    def getCompTarget(self):
        return self.CompTarget

    @getCompTarget.setter
    def getCompTarget(self, CompTarget):
        self.CompTarget = CompTarget
        CompTarget.CemMat = self

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
        if not BPourcent:
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
    def PLTPieCompo(self, paramPLT=False, BRealQuantity=False, TypeAutopct=1, PrecisionPct=1, AbsUnit="kg", PrecisionAbs=0, 
           Radius=1, StartAngle=0, LabelDist=1.25, PctDist=0.6, BShadow=False, explode=None, EnableAnnotations=False):
        """
        Plot the composition of the cementious material as a pie chart

        Args:
        - paramPLT (object): Object containing plot parameters (e.g., getColour, getHatch).
        - BRealQuantity (bool): Whether to display effective quantities (True, considering absorbed water) or total quantities (False, not considering absorbed water) in the pie chart.
        - TypeAutopct (int): Type of percentage display:
            0: Display only percentages (%).
            1: Display absolute values.
            2: Display both percentages and absolute values.
        - PrecisionPct (int): Decimal precision for percentages (e.g., 1 for 1 decimal place).
        - AbsUnit (str): Unit for absolute values (e.g., 'g', 'kg').
        - PrecisionAbs (int): Decimal precision for absolute values (e.g., 2 for 2 decimal places).
        - Radius (float): Radius of the pie chart.
        - StartAngle (float): Starting angle for the pie chart, in degrees.
        - LabelDist (float): Distance of labels from the center of the pie chart, as a fraction of the radius.
        - PctDist (float): Distance of percentage values from the center of the pie chart, as a fraction of the radius.
        - BShadow (bool): Whether to add a shadow effect to the pie chart.
        - explode (list): Fraction by which to offset a slice from the pie (e.g., [0, 0.1, 0, 0]).
        - EnableAnnotations (bool): Whether to add annotations (e.g., arrows and labels) to the pie chart.

        Returns:
            Pie chart of the composition
        """
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        StartPlots()

        # Pie chart
        Labels = []
        Weights = []
        Colors = []
        Hatches = []

        # Cement
        for Cement in self.getCement:
            Labels.append(Cement.getName)
            Colors.append(Cement.getColour)
            Weights.append(Cement.getMass)
            Hatches.append(None)
        # Water
        for Water in self.getWater:
            Labels.append(Water.getName)
            Colors.append(Water.getColour)
            Weights.append(Water.getMass)
            Hatches.append(None)

        if BRealQuantity:
            # Absorbed water by the aggregates
            AbsorbedWater = self.CMPTAggWaterAbsorbed
            Labels.append(AbsorbedWater.getName)
            Colors.append(AbsorbedWater.getColour)
            Weights.append(AbsorbedWater.getMass)
            Hatches.append(None)
            # Aggregates
            for Aggregate in self.getAggregates:
                Labels.append(Aggregate.getName)
                Colors.append(Aggregate.getColour)
                Weights.append(Aggregate.getMass)
                Hatches.append(None)
            # Adjuvants
            for Adjuvant in self.getAdjuvants:
                Labels.append(Adjuvant.getName)
                Colors.append(Adjuvant.getColour)
                Weights.append(Adjuvant.getMass)
                Hatches.append(None)
        else: 
            """
            To be changed to have quantity with out considering the absorbed water by the aggregates, but for now, we will just use the total quantities of each ingredient without considering the absorbed water
            to use the different getmass for the aggregatees
            """
            # Aggregates
            for Aggregate in self.getAggregates:
                Labels.append(Aggregate.getName)
                Colors.append(Aggregate.getColour)
                Weights.append(Aggregate.getUnSatMass)
                Hatches.append(None)
            # Adjuvants
            for Adjuvant in self.getAdjuvants:
                Labels.append(Adjuvant.getName)
                Colors.append(Adjuvant.getColour)
                Weights.append(Adjuvant.getMass)
                Hatches.append(None)

        paramPLT.getHatch = Hatches
        paramPLT.getColour = Colors
        PLTPie(Val=Weights, Labels=Labels, paramPLT=paramPLT, TypeAutopct=1, PrecisionPct=1, AbsUnit="kg", PrecisionAbs=0, 
           Radius=1, StartAngle=0, LabelDist=1.25, PctDist=0.6, BShadow=False, explode=None, 
           EnableAnnotations=False)

        # Parameters of the plot
        paramPLT.getTitle = "Composition of the " + self.getName

        PLTShow(paramPLT)

    def CMPTFcCubeFeret(self, K=4.9, Rc=False, BSimpli=False):
        """
        Compute the estimated compressive strength of the concrete cube based on the Feret formula
        
        Args:
        - K : [float] Granular coefficient and equal to 4.9 for concrete (Technologie des bétons et matériaux nouveaux)
        - Rc : [float] Compression strength of the normalised mortar [MPa] (EN 196-1) if False, compute based on the mean cement strength
        - BSimpli : [bool] Boolean to indicate if the simplified formula is used

        Returns:
        - FcCube : Compressive strength of the concrete cube [MPa]
        """
        if Rc==False: # If Rc not given, compute it based on the mean cement strength
            LCement = self.getCement
            LCementStrengthCK = [Cement.getCementStrength for Cement in LCement]
            Rc = sum(LCementStrengthCK) / len(LCementStrengthCK)
  
        # Computation of lambda and K0
        self.CMPTConcrete
        if BSimpli:  # Simplified formula
            Lambda = 1/(1+self.getVWater/self.getVCement) # [float] Quality factor of the cement matrix
        else:  # Normal formula
            Lambda = self.getVCement/self.getVCementPaste # [float] Quality factor of the cement matrix
        K0 = K * Rc
        FcCube = K0 * Lambda**2

        return FcCube

    def CMPTFcCubeBolomey(self, BGCoef=False, K=[26, 36], h1=[0.45, 0.87], AggregQuality=0):
        """
        Compute the estimated compressive strength of the concrete cube based on the Bolomey formula
        
        Args:
        - BGCoef : [Bool] Boolean to indicate if the coefficient G is used. If False, G=1.0 else G is given by user or if negative, computed based on Dmax, aggregates quality and K should be mean cement strength
        - K : [float] or [L of float] Coefficient depending on multiples params, defaults values are [26, 36] (Technologie des bétons et matériaux nouveaux)
        - h1 : [float] or [L of float] Coefficient depending on multiples params, 
        defaults values are [0.45, 0.87] (Technologie des bétons et matériaux nouveaux) and 0.5 (Technologie du béton)
        - AggregQuality : [int] Quality of the aggregates, 0: High, 1: Medium, 2: Low (only used if BGCoef is negative)

        Returns:
        - FcCube : Compressive strength of the concrete cube [MPa]
        """
        if BGCoef:
            if BGCoef > 0:
                G = BGCoef  # [float] Granular coefficient given by user
            else:
                # Diameter-based formula for G
                D = self.getDmax  # [float] Maximum diameter of the composition [mm]
                # Diameter to aggregate size bin
                if D <= 16:
                    SizeBin = 0
                elif 25 <= D < 40:
                    SizeBin = 1
                elif 63 <= D:
                    SizeBin = 2
                GMatrix = np.matrix([[0.55, 0.6, 0.65], [0.45, 0.5, 0.55], [0.35, 0.4, 0.45]])
                G = GMatrix[AggregQuality, SizeBin]  # [float] Granular coefficient based on Dmax and aggregates quality
        else:
            G = 1.0  # [float] Granular coefficient
        if isinstance(K, list) and isinstance(h1, list):
            KMin = min(K)
            KMax = max(K)
            h1Min = min(h1)
            h1Max = max(h1)
            if KMin<26 or KMax>36:
                print("Warning : Coefficient K not in the usual range [26-36]")
            if h1Min<0.45 or h1Max>0.87:
                print("Warning : Coefficient h1 not in the usual range [0.45-0.87]")

            FcCubeMin = G * KMin * ((self.getMCement/self.getMWater) - h1Max)
            FcCubeMax = G * KMax * ((self.getMCement/self.getMWater) - h1Min)
            FcCube = [FcCubeMin, FcCubeMax]

        elif isinstance(K, float) and isinstance(h1, float):
            if K<26 or K>36:
                print("Warning : Coefficient K not in the usual range [26-36]")
            if h1<0.45 or h1>0.87:
                print("Warning : Coefficient h1 not in the usual range [0.45-0.87]")

            FcCube = G * K * ((self.getMCement/self.getMWater) - h1)

        else:
            print("Error : K and h1 must be float or list")
            return 0

        return FcCube

    def CMPTFcCubeAbrams(self, K=4.9):
        """
        Compute the estimated compressive strength of the concrete cube based on the Abrams formula
        
        Args:
        - K : [float] Granular coefficient

        Returns:
        - FcCube : Compressive strength of the concrete cube [MPa]
        """
        ECRatio = self.getMWater / self.getMCement  # [float] Water to cement ratio (e/c)
        FcCube = K / 7**(1.5 * ECRatio)
        return FcCube

    def CMPTFcCubeBuist(self):
        """
        Compute the estimated compressive strength of the concrete cube based on the Buist formula
        
        Args:
        - 

        Returns:
        - FcCube : Compressive strength of the concrete cube [MPa]
        """
        # Parameters from (Technologie du béton))
        aDict = {"CEM I": 0.85, "CEM II/B-V": 0.85, "CEM III/A": 0.80, "CEM III/B": 0.75}
        bDict = {"CEM I": 33.0, "CEM II/B-V": 33.0, "CEM III/A": 25.0, "CEM III/B": 18.0}
        cDict = {"CEM I": 62.0, "CEM II/B-V": 62.0, "CEM III/A": 45.0, "CEM III/B": 30.0}
        NDict = {"CEM I 42.5 R": [55,60], "CEM I 52.5": [60,64], "CEM II/A-M 42.5": [56,59], 
                 "CEM II/B-M 42.5": [46,49], "CEM III/A 32.5": [46,51], "CEM III/A 42.5": [56,60],
                 "CEM III/B 32.5": [45,49], "CEM III/B 32.5": [50,60]}

        # Coefficients
        ECRatio = self.getMWater / self.getMCement  # [float] Water to cement ratio (e/c)
        a = aDict.get(self.getCement[0].getCementType, 0.85)
        b = bDict.get(self.getCement[0].getCementType, 33.0)
        c = cDict.get(self.getCement[0].getCementType, 62.0)
        NList = NDict.get(self.getCement[0].getCementStrength, [55,60])

        # Computation
        FcCube = [a * N + b / ECRatio + c for N in NList]
        return FcCube
        
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
    def __init__(self, Name, ID, CementClass, CementType, CementStrengthClass):
        super().__init__(Name=Name, ID=ID, MatType="Cement", Color="slategray")

        # Caracteristics identification of the cement
        self.CementClass = None  # [int] Class of cement (CEM X)
        self.CementType = None  # [str] Type of cement (Portland, Blast Furnace, ...)
        self.CementStrengthClass = CementStrengthClass  # [float] Strength of the cement class [MPa]
        self.Cement28MeanStrength = None  # 

        # Cement Composition
        self.CaO = 0  # [float] Calcium oxide content [%]
        self.SiO2 = 0  # [float] Silicon dioxide content [%]
        self.Al2O3 = 0  # [float] Aluminium oxide content [%]
        self.SO3 = 0  # [float] Sulfur trioxide content [%]
        self.Fe2O3 = 0  # [float] Iron oxide content [%]
        self.MgO = 0  # [float] Magnesium oxide content [%]
        self.Na2O = 0  # [float] Sodium oxide content [%]
        self.K2O = 0  # [float] Potassium oxide content [%]

        # Property setters
        self.getCementClass = CementClass
        self.getCementType = CementType
      
    # Caracteristics identification of the cement
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
        - Adding CementClass verification for CementType definition
        - Add caracteristics of the cement absorption of water based on book page 337 for aggregate water consumption and compute free water
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

    # Cement Composition
    @property
    def getCaO(self):
        return self.CaO

    @getCaO.setter
    def getCaO(self, CaO):
        self.CaO = CaO

    @property
    def getSiO2(self):
        return self.SiO2

    @getSiO2.setter
    def getSiO2(self, SiO2):
        self.SiO2 = SiO2

    @property
    def getAl2O3(self):
        return self.Al2O3

    @getAl2O3.setter
    def getAl2O3(self, Al2O3):
        self.Al2O3 = Al2O3

    @property
    def getSO3(self):
        return self.SO3

    @getSO3.setter
    def getSO3(self, SO3):
        self.SO3 = SO3

    @property
    def getFe2O3(self):
        return self.Fe2O3

    @getFe2O3.setter
    def getFe2O3(self, Fe2O3):
        self.Fe2O3 = Fe2O3

    @property
    def getMgO(self):
        return self.MgO

    @getMgO.setter
    def getMgO(self, MgO):
        self.MgO = MgO

    @property
    def getNa2O(self):
        return self.Na2O

    @getNa2O.setter
    def getNa2O(self, Na2O):
        self.Na2O = Na2O

    @property
    def getK2O(self):
        return self.K2O

    @getK2O.setter
    def getK2O(self, K2O):
        self.K2O = K2O

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
- Add caracteristics of the aggregate absorption of water based on book page 337 for aggregate water consumption
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
        self.GranuloDiam = None # [Vect of float] Diameter of granulometry [mm]
        self.GranuloRatio = None # [Vect of float] Ratio of granulometry [-] or [%]

        # Water-related properties
        self.WaterAbsorption = 0  # [float] Water absorption of the aggregate mass [-]
        self.WaterContent = 0  # [float] Water content of the aggregate mass [-]
   
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
            # Append the diameter to the numpy array
            # self.GranuloDiam = np.append(self.GranuloDiam, GranuloDiam) si pas initialisé problème
            return
        elif isinstance(GranuloDiam, list):
            self.GranuloDiam = np.asarray(GranuloDiam, dtype=float)
        elif isinstance(GranuloDiam, np.ndarray):
            self.GranuloDiam = GranuloDiam
        else:
            print("Error : Invalid input for Granulometry Diameter")
        self.GranuloDiam = DataSort(self.GranuloDiam)

    @property
    def getGranuloRatio(self):
        return self.GranuloRatio

    @getGranuloRatio.setter
    def getGranuloRatio(self, GranuloRatio):
        if isinstance(GranuloRatio, float):
            # Append the ratio to the numpy array
            return
        elif isinstance(GranuloRatio, list):
            self.GranuloRatio = np.asarray(GranuloRatio, dtype=float)
        elif isinstance(GranuloRatio, np.ndarray):
            self.GranuloRatio = GranuloRatio
        else:
            print("Error : Invalid input for Granulometry Ratio")
        self.GranuloRatio = DataSort(self.GranuloRatio)

    @property
    def getDmax(self):
        # [float] Maximum diameter of the granulometry [mm]
        if self.getGranuloDiam is not None and self.getGranuloRatio is not None:
            # Find the maximum diameter corresponding to 100% ratio
            MaxRatio = max(self.getGranuloRatio)
            # Found the index of the first maximum ratio in granulo ratio
            IndexMax = np.where(self.getGranuloRatio == MaxRatio)[0][0]
            MaxDiam = self.getGranuloDiam[IndexMax]
            return MaxDiam
        else:
            print("Error: Granulometry not defined")
            return 0

    @property
    def getDmin(self):
        # [float] Minimum diameter of the granulometry [mm]
        if self.getGranuloDiam is not None and self.getGranuloRatio is not None:
            # Find the minimum diameter corresponding to 0% ratio
            MinRatio = min(self.getGranuloRatio)
            # Found the index of the last maximum ratio in granulo ratio
            IndexMin = np.where(self.getGranuloRatio == MinRatio)[0][-1]
            MinDiam = self.getGranuloDiam[IndexMin]
            return MinDiam
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

    @property
    def CMPTWaterAbsorbed(self):
        """
        Compute the mass of water absorbed by the aggregate based on its water absorption and mass
        Returns:
            Mass of water absorbed by the aggregate [kg]
        """
        WaterAbsorbed = self.getWaterAbsorption * self.getMass
        return WaterAbsorbed

    @property
    def getWaterContent(self):
        return self.WaterContent

    @getWaterContent.setter
    def getWaterContent(self, WaterContent):
        self.WaterContent = WaterContent

    @property
    def CMPTWaterContained(self):
        """
        Compute the mass of water absorbed by the aggregate based on its water absorption and mass
        Returns:
            Mass of water absorbed by the aggregate [kg]
        """
        WaterContained = self.getWaterContent * self.getMass
        return WaterContained
    
    # Unsaturated mass aggregate
    @property
    def getWaterAdjustedMass(self):
        """
        Compute the adjusted mass of the aggregate considering its water content, which reduces the effective solid mass of the aggregate in the mix.
        Returns:
        - Adjusted mass of the aggregate considering water content [kg]
        """
        RealMass = self.getMass * (1 + self.getWaterContent)
        return RealMass


    # Granulometry plot
    def PLTGranulometry(self, paramPLT=False, BStart=True, BEnd=True, BPourcent=True):
        if not paramPLT:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Recovering parameters of the plot
        GranuloRatio = self.getGranuloRatio
        if not BPourcent:
            paramPLT.getYLabel = "Percentage of passers-by (%)"
            GranuloRatio = GranuloRatio*100.0

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

Improovements :
- Add caracteristics of the adjuvant absorption of water based on book page 337 for aggregate water consumption
- Take the additionnal water from the adjuvant into account in the computation of the effective water to cement ratio (E-Absorbed water)/C and in the composition of the cementious material
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
