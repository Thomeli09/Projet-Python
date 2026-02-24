# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 15:43:03 2026

@author: Thommes Eliott
"""

# Concrete composition library
"""
Improovements :
- Ajouter des méthodes de calcul de la composition (ex: Feret, Bolomey, ...)
"""

# Other Lib
from ast import Return
import numpy as np
from scipy.optimize import minimize


# Custom Lib
from ConcreteLib import CemMat
from GranulometryLib import Granulometry, PLTGranulometry
from PlotLib import ParamPLT, StartPlots, CloseAllPlots, PLTShow, DefaultParamPLT, PLTPie, PLTPlot


"""
CompositionTarget : Composition target class of cementious materials
"""
class CompositionTarget:
    def __init__(self, CemMat):
        # Parents CemMat
        self.CemMat = CemMat # Cementious materials object

        # Models parameters
        self.ErrorMeasureMethod = "SquareError" # Method to measure the error between the target composition and the computed composition

        # Models computation results
        self.GranuloMix = Granulometry() # Granulometry object for the granulometry of the mix
        self.VectAggMass = None # Vector of the mass of each aggregate in the mix [kg]

        # Composition targets
        self.TargGranuloMix = Granulometry() # Granulometry object for the target granulometry of the mix

        self.TargECEffRatio = 0.0 # [float] Target water to cement ratio effective

        self.TargVolume = None # [float] Target volume of the composition [m3]
        self.TargOutSideSurf = None # [float] Target outside surface of the composition [m2]

        self.TargOpeningSurf = None # [float] Target opening surface of the composition [m2]
        self.TargOpeningPerim = None # [float] Target opening perimeter of the composition [m]

        # Initialization of objects
        self.getGranuloMix.getName = "Granulometry of the computed mix"
        self.getGranuloMix.getColour = "red"
        self.getTargGranuloMix.getName = "Granulometry of the target mix"
        self.getTargGranuloMix.getColour = "blue"

    # Parents CemMat
    @property
    def getCemMat(self):
        return self.CemMat

    @getCemMat.setter
    def getCemMat(self, CemMat):
        self.CemMat = CemMat
        CemMat.CompTarget = self

    # Models parameters
    @property
    def getErrorMeasureMethod(self):
        return self.ErrorMeasureMethod

    @getErrorMeasureMethod.setter
    def getErrorMeasureMethod(self, ErrorMeasureMethod):
        if isinstance(ErrorMeasureMethod, str):
            if ErrorMeasureMethod in ["SquareError", "AbsoluteError", "RelativeError"]:
                self.ErrorMeasureMethod = ErrorMeasureMethod
        elif isinstance(ErrorMeasureMethod, int):
            self.ErrorMeasureMethod = {0: "SquareError", 1: "AbsoluteError", 2: "RelativeError"}.get(ErrorMeasureMethod, "SquareError")

    # Models results
    @property
    def getGranuloMix(self):
        return self.GranuloMix

    @property
    def getVectAggMass(self):
        return self.VectAggMass

    @getVectAggMass.setter
    def getVectAggMass(self, VectAggMass):
        self.VectAggMass = VectAggMass

    @property
    def getGranuloDiamVect(self):
        """
        Provide the vector of diameters of the granulometry of the mix based on the diameters of the aggregates in the mix

        Args:

        Return:
        - GranuloDiamMix: Vector of diameters of the granulometry of the mix [mm]
        """
        # Merging all the diameters of the aggregates in the mix
        LAggregates = self.getCemMat.getAggregates
        GranuloDiamMix = np.concatenate([Aggregate.getGranulo.getGranuloDiam for Aggregate in LAggregates])
        GranuloDiamMix = np.unique(GranuloDiamMix)
        return GranuloDiamMix

    # Composition targets
    @property
    def getTargGranuloMix(self):
        return self.TargGranuloMix

    @property
    def getTargECEffRatio(self):
        return self.TargECEffRatio

    @getTargECEffRatio.setter
    def getTargECEffRatio(self, TargECEffRatio):
        self.TargECEffRatio = TargECEffRatio

    @property
    def getTargVolume(self):
        return self.TargVolume

    @getTargVolume.setter
    def getTargVolume(self, TargVolume):
        self.TargVolume = TargVolume

    @property
    def getTargOutSideSurf(self):
        return self.TargOutSideSurf

    @getTargOutSideSurf.setter
    def getTargOutSideSurf(self, TargOutSideSurf):
        self.TargOutSideSurf = TargOutSideSurf

    @property
    def getTargOpeningSurf(self):
        return self.TargOpeningSurf

    @getTargOpeningSurf.setter
    def getTargOpeningSurf(self, TargOpeningSurf):
        self.TargOpeningSurf = TargOpeningSurf

    @property
    def getTargOpeningPerim(self):
        return self.TargOpeningPerim

    @getTargOpeningPerim.setter
    def getTargOpeningPerim(self, TargOpeningPerim):
        self.TargOpeningPerim = TargOpeningPerim

    # Methods
    # EC Ratio estimation

    # Dmax verification due to wall effect
    def CMPTVerifWallEffectDmax(self, LWallEffectFactor=[0.8, 1]):
        """
        Verify if the Dmax of the composition is suitable for the target volume and outside surface to avoid wall effect
        Args:
        - LWallEffectFactor: List of wall effect factors depending on the type of composition and desired workability. Default is [0.8, 1]

        Return:
        - Print warning if Dmax is not suitable for the target volume and outside surface, otherwise print info
        """
        RWallEffect = self.getCemMat.getDmax
        if self.getTargOutSideSurf is not None and self.getTargVolume is not None:
            RWallEffect = self.getTargVolume / self.getTargOutSideSurf # [m] Radius of the composition based on the target volume and outside surface

        MinRWallEffect = min(RWallEffect)
        MaxRWallEffect = max(RWallEffect)
        MinWallEffectRatio = min(LWallEffectFactor) # Minimum wall effect ratio
        MaxWallEffectRatio = max(LWallEffectFactor) # Maximum wall effect ratio

        if MinRWallEffect * MaxWallEffectRatio * 1e3 < self.getCemMat.getDmax:
            print("Warning: Dmax is larger than the target range for the target volume and outside surface, wall effect may occur")
            print("- Maximum Dmax for no wall effect: {:.2f} mm".format(MinRWallEffect * MaxWallEffectRatio*1000))
        elif MaxRWallEffect * MinWallEffectRatio * 1e3 > self.getCemMat.getDmax:
            print("Info: Dmax is smaller than the target range for the target volume and outside surface")
            print("- Minimum Dmax for no wall effect: {:.2f} mm".format(MaxRWallEffect * MinWallEffectRatio*1000))
        else:
            print("Info: Dmax is in the target range for the target volume and outside surface")
    
    # Dmax verification due to opening effect
    def CMPTVerifOpeningEffectDmax(self, BCrushedAggregates=True):
        """
        Verify if the Dmax of the composition is suitable for the target opening surface and perimeter to avoid opening effect
        
        Args:
        - BCrushedAggregates: Boolean to indicate if the aggregates are crushed or rolled, which affects the shape factor for the opening effect.

        Return:
        - Print warning if Dmax is not suitable for the target opening surface and perimeter, otherwise print info
        """
        if BCrushedAggregates:
            AggFactor = 1.25 # Factor to take into account the shape of crushed aggregates
        else:
            AggFactor = 1.45 # Factor to take into account the shape of rolled aggregates 

        if self.getTargOpeningSurf is not None or self.getTargOpeningPerim is not None:
            ROpeningEffect = self.getTargOpeningSurf / self.getTargOpeningPerim # [m] Radius of the composition based on the target opening surface and perimeter
        else:
            print("Error: No target opening surface or perimeter defined, cannot verify opening effect")
            return 0

        MinROpeningEffect = min(ROpeningEffect)  # [m] Minimum radius of the composition based on the target opening surface and perimeter

        if MinROpeningEffect * AggFactor * 1e3 < self.getCemMat.getDmax:
            print("Warning: Dmax is larger than the target range for the target opening surface and perimeter, opening effect may occur")
            print("- Maximum Dmax for no opening effect: {:.2f} mm".format(MinROpeningEffect * AggFactor*1000))
        else:
            print("Info: Dmax is smaller than the target range for the target opening surface and perimeter")
            

    # Granular squeletton computation - Ideal curves
    def CMPTIdealGranuloFuller(self, PLTDmin=0.01, PLTDmax=20, Num=100, VectDiam=None, BPourcent=False,
                               DmaxLoc=None):
        """
        Compute the Fuller curve for the composition [P+S]

        Args:
        - PLTDmin: Minimum diameter
        - PLTDmax: Maximum diameter
        - Num: Number of points to wich the curve is computed between PLTDmin and PLTDmax
        - VectDiam: Vector of diameters to which the curve is computed, if not None, PLTDmin, PLTDmax and Num are not used
        - BPourcent: Boolean to indicate if the percentage of passers-by is in percentage (True) or ratio (False)
        - DmaxLoc: Maximum diameter of the composition, if not None, it is used instead of the Dmax of the CemMat object

        return:
        - VectDiam: Vector of diameters of the granulometry [mm]
        - VectPassBy: Vector of the percentage of passers-by [-] or [%]
        """
        # Parameters
        if DmaxLoc is not None:
            Dmax = DmaxLoc # [mm] Maximum diameter of the composition
        else:
            Dmax = self.getCemMat.getDmax # [mm] Maximum diameter of the composition

        # Vector of diameters
        if VectDiam is None:
            VectDiam = np.logspace(np.log10(PLTDmin), np.log10(PLTDmax), num=Num) # [mm] Vector of diameters from PLTDmin to PLTDmax

        # Compute the percentage of passers-by
        VectPassBy = (VectDiam / Dmax) ** 0.5 # [-] Vector of the percentage of passers-by

        VectPassBy = np.minimum(VectPassBy, 1.0) # Limit the percentage of passers-by to 1 if the value is higher than 1
        VectPassBy = np.maximum(VectPassBy, 0.0) # Limit the percentage of passers-by to 0 if the value is lower than 0

        self.getTargGranuloMix.getGranuloDiam = VectDiam
        self.getTargGranuloMix.getGranuloRatio = VectPassBy

        if BPourcent:
            VectPassBy = 100 * VectPassBy # [%] Vector of the percentage of passers-by
        
        self.getTargGranuloMix.getName = "Fuller curve"
        self.getTargGranuloMix.getColour = "powderblue"

        return VectDiam, VectPassBy

    def CMPTIdealGranuloPowerLaw(self, PLTDmin=0.01, PLTDmax=20, Num=100, VectDiam=None, BPourcent=False,
                                DminLoc=None, DmaxLoc=None, FloatPower=0.5):
        """
        Compute the power law curve for the composition [P+S]

        Args:
        - PLTDmin: Minimum diameter
        - PLTDmax: Maximum diameter
        - Num: Number of points to wich the curve is computed between PLTDmin and PLTDmax
        - VectDiam: Vector of diameters to which the curve is computed, if not None, PLTDmin, PLTDmax and Num are not used
        - BPourcent: Boolean to indicate if the percentage of passers-by is in percentage (True) or ratio (False)
        - DminLoc: Minimum diameter of the composition, if not None, it is used instead of the Dmin of the CemMat object
        - DmaxLoc: Maximum diameter of the composition, if not None, it is used instead of the Dmax of the CemMat object
        - FloatPower: Float to indicate the power of the Fuller curve, which affects the shape of the curve. Default is 0.5 for the original Fuller curve, but can be modified to obtain generalized power curve (Eric P. Koehler, What Aggregate Packing is Optimal?, 2014). Suggested values are between 0.2 (Faury) and 0.45 (Kennedy).
        
        return:
        - VectDiam: Vector of diameters of the granulometry [mm]
        - VectPassBy: Vector of the percentage of passers-by [-] or [%]
        
        Improovements :
        - Add Dmin to the cemmat object
        """
        # Parameters
        if DminLoc is not None:
            Dmin = DminLoc # [mm] Maximum diameter of the composition
        else:
            Dmin = self.getCemMat.getDmin # [mm] Maximum diameter of the composition

        if DmaxLoc is not None:
            Dmax = DmaxLoc # [mm] Maximum diameter of the composition
        else:
            Dmax = self.getCemMat.getDmax # [mm] Maximum diameter of the composition

        # Vector of diameters
        if VectDiam is None:
            VectDiam = np.logspace(np.log10(PLTDmin), np.log10(PLTDmax), num=Num) # [mm] Vector of diameters from PLTDmin to PLTDmax

        # Compute the percentage of passers-by
        VectPassBy = (VectDiam / Dmax) ** FloatPower - (Dmin / Dmax) ** FloatPower # [-] Vector of the percentage of passers-by

        VectPassBy = np.minimum(VectPassBy, 1.0) # Limit the percentage of passers-by to 1 if the value is higher than 1
        VectPassBy = np.maximum(VectPassBy, 0.0) # Limit the percentage of passers-by to 0 if the value is lower than 0

        self.getTargGranuloMix.getGranuloDiam = VectDiam
        self.getTargGranuloMix.getGranuloRatio = VectPassBy

        if BPourcent:
            VectPassBy = 100 * VectPassBy # [%] Vector of the percentage of passers-by
        
        self.getTargGranuloMix.getName = "Power law curve (power={:.2f})".format(FloatPower)
        self.getTargGranuloMix.getColour = "cyan"

        return VectDiam, VectPassBy

    def CMPTIdealGranuloBolomey(self, PLTDmin=0.01, PLTDmax=20, Num=100, VectDiam=None, BPourcent=False,
                                DmaxLoc=None, BCrushedAggregates=True, IntFluidity=1, ACoef=10,
                                BVerifA=True):
        """
        Compute the Bolomey curve for the composition [P+S]

        Args:
        - PLTDmin: Minimum diameter
        - PLTDmax: Maximum diameter
        - Num: Number of points to wich the curve is computed between PLTDmin and PLTDmax
        - VectDiam: Vector of diameters to which the curve is computed, if not None, PLTDmin, PLTDmax and Num are not used
        - BPourcent: Boolean to indicate if the percentage of passers-by is in percentage (True) or ratio (False)
        - DmaxLoc: Maximum diameter of the composition, if not None, it is used instead of the Dmax of the CemMat object
        - BCrushedAggregates: Boolean to indicate if the aggregates are crushed or rolled, which affects the shape factor for the Bolomey curve.
        - IntFluidity: Float to indicate the desired fluidity of the composition, which affects the shape factor for the Bolomey curve. Comprised between 0 (dry) and 2 (very fluid)
        - ACoef: Coefficient A for the Bolomey curve, which affects the shape of the curve.
        - BVerifA: Boolean to indicate if the ACoef value is verified to be in the recommended range for the desired fluidity and aggregate type, if True, a warning is printed if the value is not in the recommended range.
        
        return:
        - VectDiam: Vector of diameters of the granulometry [mm]
        - VectPassBy: Vector of the percentage of passers-by [-] or [%]
        """
        # Dmax computation
        if DmaxLoc is not None:
            Dmax = DmaxLoc # [mm] Maximum diameter of the composition
        else:
            Dmax = self.getCemMat.getDmax # [mm] Maximum diameter of the composition
        
        # Verification of the A coefficient value of the Bolomey curve
        if IntFluidity < 0 or 2 < IntFluidity:
            print("Error: IntFluidity value not in the range [0-2]")
            return None, None

        if BCrushedAggregates:
            ADictVal = {0: [6,10], 1: [10,12], 2: [12,14]} # Dictionary of A coefficient values for crushed aggregates
        else:
            ADictVal = {0: [4,8], 1: [8,10], 2: [10,12]} # Dictionary of A coefficient values for rolled aggregates
        ARefVal = ADictVal.get(IntFluidity)

        if BVerifA and (ACoef < ARefVal[0] or ARefVal[1] < ACoef):
            print("Warning: ACoef value not in the recommended range for the desired fluidity and aggregate type, the curve may not be representative of the desired composition")
            print("- Recommended ACoef range for the desired fluidity and aggregate type: [{:.1f}-{:.1f}]".format(ARefVal[0], ARefVal[1]))
        
        # Vector of diameters
        if VectDiam is None:
            VectDiam = np.logspace(np.log10(PLTDmin), np.log10(PLTDmax), num=Num) # [mm] Vector of diameters from PLTDmin to PLTDmax

        # Compute the percentage of passers-by
        ACoefAdim = ACoef/100
        VectPassBy = ACoefAdim + (1-ACoefAdim) * (VectDiam / Dmax) ** 0.5 # [-] Vector of the percentage of passers-by

        VectPassBy = np.minimum(VectPassBy, 1.0) # Limit the percentage of passers-by to 1 if the value is higher than 1
        VectPassBy = np.maximum(VectPassBy, 0.0) # Limit the percentage of passers-by to 0 if the value is lower than 0

        self.getTargGranuloMix.getGranuloDiam = VectDiam
        self.getTargGranuloMix.getGranuloRatio = VectPassBy

        if BPourcent:
            VectPassBy = 100 * VectPassBy # [%] Vector of the percentage of passers-by
        
        self.getTargGranuloMix.getName = "Bolomey curve (A={:.1f})".format(ACoef)
        self.getTargGranuloMix.getColour = "deepskyblue"

        return VectDiam, VectPassBy

    def CMPTIdealGranuloFaury(self, PLTDmin=0.01, PLTDmax=20, Num=100, VectDiam=None, BPourcent=False,
                              DmaxLoc=None, IntCrushedAggregates=1, IntFluidity=2, BNormalVibration=True, 
                              ACoef=29, BCoef=1.125, BVerifA=True, BVerifB=True):
        """
        Compute the Faury curve for the composition [P+S]

        Args:
        - PLTDmin: Minimum diameter
        - PLTDmax: Maximum diameter
        - Num: Number of points to wich the curve is computed between PLTDmin and PLTDmax
        - VectDiam: Vector of diameters to which the curve is computed, if not None, PLTDmin, PLTDmax and Num are not used
        - BPourcent: Boolean to indicate if the percentage of passers-by is in percentage (True) or ratio (False)
        - DmaxLoc: Maximum diameter of the composition, if not None, it is used instead of the Dmax of the CemMat object
        - IntCrushedAggregates: Int to indicate if the aggregates are crushed or rolled or in between, which affects the shape factor for the Faury curve. 0 for rolled aggregates, 1 for rolled-crushed aggregates and 2 for crushed aggregates.
        - IntFluidity: Int to indicate the desired fluidity of the composition, which affects the shape factor for the Bolomey curve. Comprised between 0 (dry) and 2 (very fluid)
        - BNormalVibration: Boolean to indicate if the vibration is normal or heavy, which affects the shape factor for the Faury curve.
        - ACoef: Coefficient A for the Bolomey curve, which affects the shape of the curve.
        - BVerifA: Boolean to indicate if the ACoef value is verified to be in the recommended range for the desired fluidity and aggregate type, if True, a warning is printed if the value is not in the recommended range.
        - BVerifB: Boolean to indicate if the BCoef value is verified to be in the recommended range for the desired vibration, if True, a warning is printed if the value is not in the recommended range.
        return:
        - VectDiam: Vector of diameters of the granulometry [mm]
        - VectPassBy: Vector of the percentage of passers-by [-] or [%]
        """
        # Dmax computation
        if DmaxLoc is not None:
            Dmax = DmaxLoc # [mm] Maximum diameter of the composition
        else:
            Dmax = self.getCemMat.getDmax # [mm] Maximum diameter of the composition
        
        # Verification of the A coefficient value of the Bolomey curve
        if IntFluidity < 0 or 5 < IntFluidity:
            print("Error: IntFluidity value not in the range [0-5]")
            return None, None

        MinARef = 10
        MaxARef = 45
        if IntCrushedAggregates==0:
            ADictVal = {0: [MinARef,24], 1: [24,26], 2: [26,28], 3: [28,30], 4: [30,32], 5: [32,MaxARef]} # Dictionary of A coefficient values for rolled aggregates
        elif IntCrushedAggregates==1:
            ADictVal = {0: [MinARef,26], 1: [26,28], 2: [28,30], 3: [30,32], 4: [32,34], 5: [34,MaxARef]} # Dictionary of A coefficient values for rolled-crushed aggregates
        else:
            ADictVal = {0: [MinARef,30], 1: [30,32], 2: [32,34], 3: [34,36], 4: [36,38], 5: [36,MaxARef]} # Dictionary of A coefficient values for crushed aggregates
        ARefVal = ADictVal.get(IntFluidity)

        if BNormalVibration:
            BRefVal = [1, 1.25] # Recommended B coefficient values for normal vibration
        else:
            BRefVal = [1.25, 1.5] # Recommended B coefficient values for heavy vibration

        if BVerifA and (ACoef < ARefVal[0] or ARefVal[1] < ACoef):
            print("Warning: ACoef value not in the recommended range for the desired fluidity and aggregate type, the curve may not be representative of the desired composition")
            print("- Recommended ACoef range for the desired fluidity and aggregate type: [{:.1f}-{:.1f}]".format(ARefVal[0], ARefVal[1]))
        
        if BVerifB and (BCoef < BRefVal[0] or BRefVal[1] < BCoef):
            print("Warning: BCoef value not in the recommended range for the desired vibration, the curve may not be representative of the desired composition")
            print("- Recommended BCoef range for the desired vibration: [{:.2f}-{:.2f}]".format(BRefVal[0], BRefVal[1]))

        # Vector of diameters
        if VectDiam is None:
            VectDiam = np.logspace(np.log10(PLTDmin), np.log10(PLTDmax), num=Num) # [mm] Vector of diameters from PLTDmin to PLTDmax

        # Compute the point of the curve where the slope changes
        RHydraulic = Dmax # [mm] Hydraulic radius of the composition, which is approximated by the Dmax for the Faury curve
        if self.getTargOutSideSurf is not None and self.getTargVolume is not None:
            RHydraulic = min(self.getTargVolume / self.getTargOutSideSurf) * 1e3
        YVal = ACoef + 17*(Dmax)**(1/5) + BCoef/(RHydraulic/Dmax-0.75)

        # Fill the curve with the corresponding values
        VectPassByRef = np.array([0.0, YVal/100, 1.0]) # [-] Vector of the passers-by for the reference points of the curve
        VectDiamRef = np.array([0.0065, Dmax/2, Dmax]) # [mm] Vector of diameters for the reference points of the curve

        # Interpolate the curve to the desired diameters based on the reference curve on a fifth root scale to fit the curve linearly
        VectDiamRefFauryAxis = VectDiamRef ** (1/5) # [mm^(1/5)]
        VectDiamFauryAxis = VectDiam ** (1/5) # [mm^(1/5)]
        VectPassBy = np.interp(VectDiamFauryAxis, VectDiamRefFauryAxis, VectPassByRef) # [-] Vector of the percentage of passers-by based on the reference curve
        

        VectPassBy = np.minimum(VectPassBy, 1.0) # Limit the percentage of passers-by to 1 if the value is higher than 1
        VectPassBy = np.maximum(VectPassBy, 0.0) # Limit the percentage of passers-by to 0 if the value is lower than 0

        self.getTargGranuloMix.getGranuloDiam = VectDiam
        self.getTargGranuloMix.getGranuloRatio = VectPassBy

        if BPourcent:
            VectPassBy = 100 * VectPassBy # [%] Vector of the percentage of passers-by
        
        self.getTargGranuloMix.getName = "Faury curve (A={:.1f}, B={:.2f})".format(ACoef, BCoef)
        self.getTargGranuloMix.getColour = "dodgerblue"

        return VectDiam, VectPassBy

    def CMPTIdealGranuloDreux(self, PLTDmin=0.01, PLTDmax=20, Num=100, VectDiam=None, BPourcent=False,
                              DmaxLoc=None, BCrushedAggregates=True, IntVibration=1, CementMassLoc=None, BPumpable=False,
                              KCoef=3.2, Mf=2.5, KPumpCoef=0, BVerifK=True, BVerifKPump=True):
        """
        Compute the Dreux curve for the composition [P+S]

        Args:
        - PLTDmin: Minimum diameter
        - PLTDmax: Maximum diameter
        - Num: Number of points to wich the curve is computed between PLTDmin and PLTDmax
        - VectDiam: Vector of diameters to which the curve is computed, if not None, PLTDmin, PLTDmax and Num are not used
        - BPourcent: Boolean to indicate if the percentage of passers-by is in percentage (True) or ratio (False)
        - DmaxLoc: Maximum diameter of the composition, if not None, it is used instead of the Dmax of the CemMat object
        - BCrushedAggregates: Bool to indicate if the aggregates are crushed or rolled or in between, which affects the shape factor for the Dreux curve. 0 for rolled aggregates and 1 for crushed aggregates.
        - IntVibration: Int to indicate if the vibration is normal or heavy, which affects the shape factor for the Faury curve.
        - CementMass: Mass of cement in the composition, which affects the shape factor for the Dreux curve. Default is None to use the mass of cement in the CemMat object, but can be modified to use a specific mass of cement for the composition.
        - BPumpable: Boolean to indicate if the composition is pumpable or not, which affects the shape factor for the Dreux curve. If True, the curve is computed for a pumpable composition, if False, the curve is computed for a non-pumpable composition.
        - KCoef: Float coefficient A for the Dreux curve, which affects the shape of the curve.
        - Mf: Float to indicate the finesse modulus of the sand, which affects the shape factor for the Dreux curve. Default is 2.5 to not have an effect on the curve, but can be modified to use a specific finesse modulus for the sand in the composition.
        - KPumpCoef: Float coefficient for the Dreux curve, which affects the shape of the curve for pumpable compositions.
        - BVerifK: Boolean to indicate if the KCoef value is verified to be in the recommended range for the desired fluidity and aggregate type, if True, a warning is printed if the value is not in the recommended range.
        - BVerifKPump: Boolean to indicate if the BCoef value is verified to be in the recommended range for the desired pumpability, if True, a warning is printed if the value is not in the recommended range.
        return:
        - VectDiam: Vector of diameters of the granulometry [mm]
        - VectPassBy: Vector of the percentage of passers-by [-] or [%]
        """
        # Dmax computation
        if DmaxLoc is not None:
            Dmax = DmaxLoc # [mm] Maximum diameter of the composition
        else:
            Dmax = self.getCemMat.getDmax # [mm] Maximum diameter of the composition

        # Cement mass computation
        if CementMassLoc is not None:
            CementMass = CementMassLoc # [kg] Mass of cement in the composition
        else:
            CementMass, VCement = self.getCemMat.CMPTCement # [kg, m3] Mass and volume of cement in the composition
        
        # Verification of the coefficient values of the Dreux curve
        if IntVibration==0:
            if BCrushedAggregates:
                VectCementMass = np.array([200, 250, 300, 350, 400, 450]) # [kg/m3]
                VectKRefVal = np.array([10.0, 8.0, 6.0, 4.0, 2.0, 0.0])
            else:
                VectCementMass = np.array([200, 250, 300, 350, 400, 450]) # [kg/m3]
                VectKRefVal = np.array([8.0, 6.0, 4.0, 2.0, 0.0, -2.0])
        elif IntVibration==1:
            if BCrushedAggregates:
                VectCementMass = np.array([200, 250, 300, 350, 400, 450]) # [kg/m3]
                VectKRefVal = np.array([8.0, 6.0, 4.0, 2.0, 0.0, -2.0])
            else:
                VectCementMass = np.array([200, 250, 300, 350, 400, 450]) # [kg/m3]
                VectKRefVal = np.array([6.0, 4.0, 2.0, 0.0, -2.0, -4.0])
        else:
            if BCrushedAggregates:
                VectCementMass = np.array([200, 250, 300, 350, 400, 450]) # [kg/m3]
                VectKRefVal = np.array([6.0, 4.0, 2.0, 0.0, -2.0, -4.0])
            else:
                VectCementMass = np.array([200, 250, 300, 350, 400, 450]) # [kg/m3]
                VectKRefVal = np.array([4.0, 2.0, 0.0, -2.0, -4.0, -6.0])

        KRefVal = np.interp(CementMass, VectCementMass, VectKRefVal) 
        KRefVal = [KRefVal*0.9, KRefVal*1.1]
        KRefVal = [min(KRefVal), max(KRefVal)]

        KsCoef = 6*Mf - 15 # [-] Shape factor for the sand based on its finesse modulus
        KPumpRefVal = [0, 0] if not BPumpable else [5.0, 10.0] # Recommended KPump coefficient values for non-pumpable and pumpable compositions

        if BVerifK and (KCoef < KRefVal[0] or KRefVal[1] < KCoef):
            print("Warning: KCoef value not in the recommended range for the desired fluidity and aggregate type, the curve may not be representative of the desired composition")
            print("- Recommended KCoef range for the desired fluidity and aggregate type: [{:.1f}-{:.1f}]".format(KRefVal[0], KRefVal[1]))
        
        if BVerifKPump and (KPumpCoef < KPumpRefVal[0] or KPumpRefVal[1] < KPumpCoef):
            print("Warning: KPumpCoef value not in the recommended range for the desired pumpability, the curve may not be representative of the desired composition")
            print("- Recommended KPumpCoef range for the desired pumpability: [{:.1f}-{:.1f}]".format(KPumpRefVal[0], KPumpRefVal[1]))
            

        # Vector of diameters
        if VectDiam is None:
            VectDiam = np.logspace(np.log10(PLTDmin), np.log10(PLTDmax), num=Num) # [mm] Vector of diameters from PLTDmin to PLTDmax

        # Compute the point of the curve where the slope changes
        YVal = 50 - Dmax**0.5 + KCoef + KsCoef + KPumpCoef
        XVal = Dmax/2 if Dmax <= 25 else 5 + (Dmax-5)/2 # [mm]

        # Fill the curve with the corresponding values
        VectPassByRef = np.array([0.0, YVal/100, 1.0]) # [-] Vector of the passers-by for the reference points of the curve
        VectDiamRef = np.array([0.08, XVal, Dmax]) # [mm] Vector of diameters for the reference points of the curve

        # Interpolate the curve to the desired diameters based on the reference curve on a fifth root scale to fit the curve linearly
        VectDiamRefDreuxAxis = np.log10(VectDiamRef) # [mm] Vector of diameters for the reference points of the curve on a logarithmic scale
        VectDiamDreuxAxis = np.log10(VectDiam) # [mm] Vector of diameters for the desired points of the curve on a logarithmic scale
        VectPassBy = np.interp(VectDiamDreuxAxis, VectDiamRefDreuxAxis, VectPassByRef) # [-] Vector of the percentage of passers-by based on the reference curve
        
        self.getTargGranuloMix.getGranuloDiam = VectDiam
        self.getTargGranuloMix.getGranuloRatio = VectPassBy

        VectPassBy = np.minimum(VectPassBy, 1.0) # Limit the percentage of passers-by to 1 if the value is higher than 1
        VectPassBy = np.maximum(VectPassBy, 0.0) # Limit the percentage of passers-by to 0 if the value is lower than 0

        if BPourcent:
            VectPassBy = 100 * VectPassBy # [%] Vector of the percentage of passers-by
        
        self.getTargGranuloMix.getName = "Dreux curve (K={:.1f}, Ks={:.1f}, KPump={:.1f})".format(KCoef, KsCoef, KPumpCoef)
        self.getTargGranuloMix.getColour = "teal"
        return VectDiam, VectPassBy

    # Granular squeletton computation - Fitting to a target curve (ideal or experimental)
    def CMPGranuloRatioMix(self, VectAggregatesMass, VectGranuloDiamMix=None):
        """
        Compute the granulometry of the mix of aggregates based on the aggregate inside the CemMat object and their provided mass.
        Args:
        - VectAggregatesMass: Vector of the mass of each aggregate in the mix [kg]
        - VectGranuloDiamMix: Vector of diameters to which the curve is computed
       
        Return:
        - GranuloDiamMix: Vector of diameters of the granulometry of the mix [mm]
        - GranuloRatioMix: Vector of the percentage of passers-by of the granulometry of the mix [-] or [%]
        """

        # Mass of aggregates in the mix
        MAggregates = sum(VectAggregatesMass) # [kg] Total mass of aggregates in the mix

        # Merging all the diameters of the aggregates in the mix
        LAggregates = self.getCemMat.getAggregates
        GranuloDiamMix = self.getGranuloDiamVect
        LogGranuloDiamMix = np.log10(GranuloDiamMix)
        GranuloRatioMix = np.zeros_like(GranuloDiamMix, dtype=float)

        # Verify the provided mass of aggregates in the mix is consistent with the number of aggregates in the CemMat object
        if len(VectAggregatesMass) != len(LAggregates):
            print("Error: The provided mass of aggregates in the mix is not consistent with the number of aggregates in the CemMat object")
            return None, None

        # For each aggregate, add its granulometry ratio weighted by its mass proportion in the mix to the mix granulometry while interpolating the missing values
        for Aggregate in LAggregates:
            ProportMass = VectAggregatesMass[int(LAggregates.index(Aggregate))] / MAggregates # [-] Proportion of the aggregate mass in the mix
            GranuloDiamAgg = Aggregate.getGranulo.getGranuloDiam
            GranuloRatioAgg = Aggregate.getGranulo.getGranuloRatio

            # Sorting the granulometry of the aggregate
            Order = np.argsort(GranuloDiamAgg)
            GranuloDiamAgg = GranuloDiamAgg[Order]
            GranuloRatioAgg = GranuloRatioAgg[Order]

            # Adding the weighted granulometry ratio to the mix granulometry ratio with interpolation
            LogGranuloDiamAgg = np.log10(GranuloDiamAgg) # Warning : Need to do the interpolation in log scale because of the logarithmic scale of the granulometric plot
            GranuloRatioMix += np.interp(LogGranuloDiamMix, LogGranuloDiamAgg, GranuloRatioAgg, left=0) * ProportMass

        if VectGranuloDiamMix is not None:
            VectLogGranuloDiamMix = np.log10(VectGranuloDiamMix)
            VectGranuloRatioMix = np.interp(VectLogGranuloDiamMix, LogGranuloDiamMix, GranuloRatioMix, left=0)
            self.getGranuloMix.getGranuloDiam = VectGranuloDiamMix
            self.getGranuloMix.getGranuloRatio = VectGranuloRatioMix
            return VectLogGranuloDiamMix, VectGranuloRatioMix
        else:
            self.getGranuloMix.getGranuloDiam = GranuloDiamMix
            self.getGranuloMix.getGranuloRatio = GranuloRatioMix
            return GranuloDiamMix, GranuloRatioMix

    def CMPGranuloRatioMixConstraint(self, VectAggregatesMass):
        """
        Apply constraints to the computation of the granulometry of the mix of aggregates, based on the constraints defined
        in the constraints parts of the composition object, such as maximum and minimum proportion of aggregates in the mix,
        substitution of aggregates, etc.
        Args:
        Return:
        """
        # Add a reference value for the mass of the first aggregate in the mix to avoid issues with the optimization algorithm 
        # when the mass of the aggregates in the mix is too low. Solved by adding 1.0 at the first value of the mass of aggregates in the mix.
        VectAggregatesMass = np.concatenate(([1.0], VectAggregatesMass))

        # Verify and enforce non-negativity of the mass of aggregates in the mix
        VectAggregatesMass = np.maximum(VectAggregatesMass, 0.0)


        return VectAggregatesMass

    def CMPTGranuloRatioMixInitialGuess(self):
        """
        Compute an initial guess of the granulometry of the mix of aggregates based on the constraints
        defined in the constraints parts of the composition object, such as maximum and minimum 
        proportion of aggregates in the mix, substitution of aggregates, etc.
        Args:

        Return:
         - VectAggregatesMass: Vector of the mass of each aggregate in the mix [kg] Initial guess of the mass of each aggregate in the mix
        """
        VectAggregatesMass = np.zeros(len(self.getCemMat.getAggregates)-1) # [kg] Initial guess of the mass of each aggregate in the mix
        return VectAggregatesMass

    def CMPTGranuloDiffIdeal2Real(self):
        """
        Compute the difference between the granulometry of the composition and a target curve (ideal or experimental) 
        based on the ratio of passers-by at the diameters of the composition granulometry, at each diameter.
       
        Args:

        Return:

        """
        if self.getGranuloMix is None or self.getGranuloMix is None:
            print("Error: No target curve defined for the granulometry, please define a target curve to compute the difference between the granulometry of the composition and the target curve")
            return None
        if self.getGranuloMix.getGranuloDiam is None or self.getGranuloMix.getGranuloRatio is None:
            print("Error: Granulometry of the mix not computed, please compute the granulometry of the mix to compute the difference between the granulometry of the composition and the target curve")
            return None
        if self.getTargGranuloMix.getGranuloDiam is None or self.getTargGranuloMix.getGranuloRatio is None:
            print("Error: Target granulometry of the mix not computed, please compute the target granulometry of the mix to compute the difference between the granulometry of the composition and the target curve")
            return None

        if len(self.getGranuloMix.getGranuloRatio) != len(self.getTargGranuloMix.getGranuloRatio) or len(self.getGranuloMix.getGranuloDiam) != len(self.getTargGranuloMix.getGranuloDiam):
            print("Error: The number of points of the granulometry of the mix and the target granulometry of the mix are not the same, please compute the granulometry of the mix and the target granulometry of the mix with the same number of points to compute the difference between the granulometry of the composition and the target curve")
            return None
        if len(self.getGranuloMix.getGranuloRatio) != len(self.getGranuloMix.getGranuloDiam):
            print("Error: The number of points of the granulometry of the mix and the number of diameters of the granulometry of the mix are not the same, please compute the granulometry of the mix with the same number of points and diameters to compute the difference between the granulometry of the composition and the target curve")

        if not np.array_equal(self.getGranuloMix.getGranuloDiam, self.getTargGranuloMix.getGranuloDiam):
            print("Error: The diameters of the granulometry of the mix and the target granulometry of the mix are not the same, please compute the granulometry of the mix and the target granulometry of the mix with the same diameters to compute the difference between the granulometry of the composition and the target curve")
            return None

        return self.getGranuloMix.getGranuloRatio - self.getTargGranuloMix.getGranuloRatio

    def CMPTGranuloIdealRealError(self):
        """
        Compute a measure of the error between the granulometry of the composition and a target curve (ideal or experimental)
       
        Args:
        Return:
        - SumDiffMeasure: Float to indicate the measure of the error between the granulometry of the composition and the target curve, 
        which can be used as an objective function to minimize to optimize the granulometry of the composition
        """
        GranuloDiff = self.CMPTGranuloDiffIdeal2Real()
        if GranuloDiff is None:
            return None
        else:
            if self.getErrorMeasureMethod == "SquareError":
                DiffMeasure = GranuloDiff**2 # [-]
            elif self.getErrorMeasureMethod == "AbsoluteError":
                DiffMeasure = np.abs(GranuloDiff) # [-]
            elif self.getErrorMeasureMethod == "RelativeError":
                DiffMeasure = np.abs(GranuloDiff) / np.maximum(np.abs(self.getTargGranuloMix.getGranuloRatio), 1e-4) # [-] Relative error, with a small value in the denominator to avoid division by zero
            else:
                print("Error: ErrorMeasureMethod value not recognized, please choose between 'Abs' and 'Square' for the method to compute the error between the granulometry of the composition and the target curve")
                return None
            SumDiffMeasure = np.sum(DiffMeasure)
            return SumDiffMeasure

    def CMPTGranuloIdealRealFun2Min(self, VectAggregatesMass):
        """
        Function to be minimized to optimize the granulometry of the composition by fitting the percentage of
        passers-by to a target curve (ideal or experimental).
        Args:
        Return:
        """
        # Apply constraints to the computation of the granulometry of the mix of aggregates
        VectAggregatesMass = self.CMPGranuloRatioMixConstraint(VectAggregatesMass)

        # Compute the granulometry of the mix of aggregates based on the aggregate inside the CemMat object and their provided mass
        self.CMPGranuloRatioMix(VectAggregatesMass, VectGranuloDiamMix=None)

        # Compute the measure of the error between the granulometry of the composition and a target curve (ideal or experimental)
        Error = self.CMPTGranuloIdealRealError()
        return Error
        

    def CMPTGranuloLeastSquareMethod(self):
        """
        Compute the granulometry of the composition by fitting the percentage of passers-by to a target curve 
        (ideal or experimental) using the least square method
        Args:
        -

        Return:
        - 
        """
        # Verify the existence of the target curve
        if self.getTargGranuloMix is None or self.getTargGranuloMix.getGranuloDiam is None or self.getTargGranuloMix.getGranuloRatio is None:
            print("Error: No target curve defined for the granulometry, please define a target curve to use the least square method")
            return None

        # Initial guess
        VectAggregatesMass = self.CMPTGranuloRatioMixInitialGuess()

        # Optimization of the granulometry of the composition by fitting the percentage of passers-by to a target curve (ideal or experimental) using the least square method
        print("Info: Optimisation of the composition started")

        Result = minimize(self.CMPTGranuloIdealRealFun2Min, VectAggregatesMass,
                          method='Nelder-Mead', tol=1e-6)

        print("Info: Optimisation of the composition completed")
        
        # Verify the success of the optimization
        if not Result.success:
            print("Error: Optimization of the granulometry of the composition did not converge, the results may not be reliable")
            print("Info: {}".format(Result.message))

        # Extract the optimized mass of aggregates in the mix
        VectAggregatesMass = Result.x

        # Apply constraints to the computation of the granulometry of the mix of aggregates
        VectAggregatesMass = self.CMPGranuloRatioMixConstraint(VectAggregatesMass)
        self.getVectAggMass = VectAggregatesMass

        # Print the error of the optimization with regard to the target curve
        print("Info: Optimization of the granulometry of the composition completed with an error of {:.6f}".format(Result.fun))

        # Verify the volume of concrete produced with the optimized mass of aggregates in the mix 
        # to produce at the end 1 m3 of concrete
        pass

        # Provide the optimized mass of aggregates in the mix to CemMat object
        pass
        
        # Compute the granulometry of the mix of aggregates based on the aggregate inside the CemMat object and their provided mass
        
        # Compute the amount of water needed for the composition
        pass


        return VectAggregatesMass
    
    def CMPTGranuloDreuxGorrisseMethod(self):
        """
        Compute the granulometry of the composition by fitting the percentage of passers-by to a target curve 
        (ideal or experimental) using the Dreux-Gorrisse method. The method consists in founding the intersection 
        between the target curve and the line linking the 95% passing-by point of the smaller fraction and the 5%
        passing-by point of the next larger fraction of the composition. This method is repeated from smaller to larger diameters
        until the Dmax of the composition is reached. The proportion of each fraction is then computed based on proportion 
        at the intersection when using the larger fraction diminished by the proportion at the intersection 
        when using the smaller fraction.
        Args:
        -   

        Return:
        -
        """
        # Sort the aggregates in the mix by their maximum diameter

        # For each aggregate, compute the line linking the 95% passing-by point of the aggregate mix with the 5% passing-by point of the next 
        # larger aggregate mix, and compute the intersection of this line with the target curve to determine the proportion of the aggregate 
        # in the mix

    # Compute the volume of concrete produced with the computed mass of aggregates in the mix
    def CMPTVolumeAgg(self):
        """
        Compute the volume of aggregates produced with the computed mass of aggregates in the mix

        Args:

        Return:
        - 

        """
        VolAgg = 0.0 # [m3] Volume of aggregates in the mix
        LAggregates = self.getCemMat.getAggregates

        # Verify that the mass of aggregates in the mix is provided
        if VectAggMass is None:
            VectAggMass = self.getVectAggMass
            if VectAggMass is None:
                print("Error: No mass of aggregates in the mix provided, please provide the mass of aggregates in the mix")
                return

        # Verify the provided mass of aggregates in the mix is consistent with the number of aggregates in the CemMat object
        if len(VectAggMass) != len(LAggregates):
            print("Error: The provided mass of aggregates in the mix is not consistent with the number of aggregates in the CemMat object")
            return

        # Set the mass of each aggregate in the mix in the CemMat object
        for Aggregate in LAggregates:
            MassAgg = VectAggMass[int(LAggregates.index(Aggregate))] # [kg] Mass of the aggregate in the mix
            VolAgg += MassAgg / Aggregate.getDensity # [m3] Volume of the aggregate in the mix
        
        return VolAgg

    # Compute the amount of water needed for the composition based on the target effective water to cement ratio and the water balance of the composition
    def CMPTWater(self):
        """
        Compute the added water needed for the composition based on the target effective water to cement ratio
        
        Args:
        -

        return:
        - Change water amount in the CemMat object
        """
        # Parameters
        MCement, VCement = self.getCemMat.CMPTCement  # [kg] Cement quantity
        MAggWaterAbsorbed = self.getCemMat.CMPTAggWaterAbsorbed  # [kg] Water absorbed by aggregates
        MAggWaterContent = self.getCemMat.CMPTAggWaterContent  # [kg] Water content in aggregates

        # Compute the needed water amount
        if MCement is None:
            print("Error: No cement quantity defined in the CemMat object")
            return

        MWaterECEffRatio = self.getTargECRatioEff * MCement  # [kg] Water amount needed based on the target effective water to cement ratio
        MWaterAggBalance = MAggWaterAbsorbed - MAggWaterContent  # [kg] Balance of water absorbed by aggregates, positive if the aggregates absorb water and negative if the aggregates release water
        MWaterTot = MWaterECEffRatio + MAggWaterAbsorbed  # [kg] Total water amount needed for the composition, including the water absorbed by aggregates
        MAddedWater = MWaterECEffRatio + MWaterAggBalance  # [kg] Added water amount based on the target effective water to cement ratio and the balance of water absorbed by aggregates


        if MAddedWater < 0:
            print("Error: The additionnal water amount is negative, an error may have occurred in the computation of the water amount, please check the input parameters and the water balance")

        # Set the added water amount in the CemMat object
        LWater = self.getCemMat.getWater
        LWater[0].getMass = MAddedWater

        print("Info: Additional water amount set to {:.2f} kg".format(MAddedWater))

        # Verify the water added
        MWater, VWater = self.getCemMat.CMPTWater

        if abs(MWater - MAddedWater)/MAddedWater > 1e-1:
            print("Warning: Output water amount does not match the added water amount")


    # Provide the computed mass of aggregates in the mix to CemMat object
    def TRNSFAggMassMix2CemMat(self, VectAggMass=None):
        """
        Enforce the computed mass of aggregates in the mix in the CemMat object 
        to be used for the computation of the granulometry of the mix and the water balance.
        
        Args:
        - VectAggMass: Vector of the mass of each aggregate in the mix [kg]
        
        Return:
         - Change the mass of each aggregate in the mix in the CemMat object
        """
        LAggregates = self.getCemMat.getAggregates

        # Verify that the mass of aggregates in the mix is provided
        if VectAggMass is None:
            VectAggMass = self.getVectAggMass
            if VectAggMass is None:
                print("Error: No mass of aggregates in the mix provided, please provide the mass of aggregates in the mix")
                return

        # Verify the provided mass of aggregates in the mix is consistent with the number of aggregates in the CemMat object
        if len(VectAggMass) != len(LAggregates):
            print("Error: The provided mass of aggregates in the mix is not consistent with the number of aggregates in the CemMat object")
            return

        # Set the mass of each aggregate in the mix in the CemMat object
        for Aggregate in LAggregates:
            MassAgg = VectAggMass[int(LAggregates.index(Aggregate))] # [kg] Mass of the aggregate in the mix
            Aggregate.getMass = MassAgg # Set the mass of the aggregate in the mix in the CemMat object


    # Plotting functions
    # Plot of the granulometry curves of the composition
    def PlotGranuloCompo(self, paramPLT=None, BStart=True, BEnd=True, BPourcent=True,
                      BDefaultColour=True):
        """
        Plot the granulometry of the mix of aggregates
        
        Args:
            paramPLT: Parameters of the plot
            BStart: Boolean to indicate if the plot starts in a new figure
            BEnd: Boolean to indicate if the plot ends and shows the figure
            BPourcent: Boolean to indicate if the y-axis is in percentage (True) or ratio (False)
            BDefaultColour: Boolean to indicate if the default colour of the curve is used (True) or if the colour defined in the getTargGranuloMix attribute is used (False)
        Returns:
            Plot of the granulometry of the mix
        """
        if paramPLT is None:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Plot the granulometry of the mix
        if BDefaultColour:
            TempColour = paramPLT.getColour
            paramPLT.getColour = self.getGranuloMix.getColour

        paramPLT.getLegends = [self.getGranuloMix.getName]
        self.getGranuloMix.PLTGranulometry(paramPLT=paramPLT, StrTitleName="ideal curve", 
                                           BStart=False, BEnd=False, BPourcent=BPourcent)

        paramPLT.getColour = TempColour

        if BEnd:
            PLTShow(paramPLT)

    # PLT Ideal Curves
    def PLTIdealCurve(self, paramPLT=None, BStart=True, BEnd=True, BPourcent=True,
                      BDefaultColour=True):
        """
        Plot the granulometry of the ideal curve defined in the getTargGranuloMix attribute
        
        Args:
            paramPLT: Parameters of the plot
            BStart: Boolean to indicate if the plot starts in a new figure
            BEnd: Boolean to indicate if the plot ends and shows the figure
            BPourcent: Boolean to indicate if the y-axis is in percentage (True) or ratio (False)
            BDefaultColour: Boolean to indicate if the default colour of the curve is used (True) or if the colour defined in the getTargGranuloMix attribute is used (False)
        Returns:
            Plot of the granulometry of the mix
        """
        if paramPLT is None:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        # Plot the granulometry of the mix
        if BDefaultColour:
            TempColour = paramPLT.getColour
            paramPLT.getColour = self.getTargGranuloMix.getColour

        paramPLT.getLegends = [self.getTargGranuloMix.getName]
        self.getTargGranuloMix.PLTGranulometry(paramPLT=paramPLT, StrTitleName="ideal curve", 
                                           BStart=False, BEnd=False, BPourcent=BPourcent)

        paramPLT.getColour = TempColour

        if BEnd:
            PLTShow(paramPLT)