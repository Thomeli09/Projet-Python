# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:15:29 2024

@author: Thommes Eliott
"""

# General Plotting library

from operator import index
from queue import Empty
import matplotlib.pyplot as plt
import numpy as np


# Custom Lib


"""
Base de donnée
"""


# Display parameters
class ParamPLT:
    def __init__(self, colour, linetype, marker, linesize, fontsize):
        """
        Ajouter le système de liste si différents éléments, pas que pour les légendes,...
        """
        # Plot
        self.Colour = colour
        self.ColourMap = None
        self.LineType = linetype
        self.LineSize = linesize
        self.MarkerType = marker
        self.MarkerSize = linesize
        self.Alpha = 1  # Blending value, from 0 (transparent) to 1 (opaque)
        self.HatchType = ''

        # Text
        self.FontSize = fontsize
        self.TitleSize = fontsize
        self.TicksSize = fontsize
        self.XLabel = None
        self.YLabel = None
        self.ZLabel = None
        self.Title = None
        self.Legends = []
        self.BLegends = True
        self.ColourBarTitle = None

        # Scale
        self.Scale = 1
        self.XScaleType = 'linear'
        self.YScaleType = 'linear'
        self.ZScaleType = 'linear'
        self.GenericScaleType = 'linear'
        self.Scale3D = 1

        # Plot Format
        self.PltAspect = None

        # Grid
        self.GridAxis = 'both'
        self.GridColour = None
        self.GridLineType = None
        self.GridLineSize = 0.4
        self.GridAlpha = 1

        # Limits
        self.XLimit = []
        self.YLimit = []
        self.Zlimit = []

    @property
    def getBoolColour(self):
        if not self.Colour:
            return False
        else:
            return True

    @property
    def getColour(self):
        if not self.Colour:
            return None
        else:
            if isinstance(self.Colour, list):
                return self.Colour.pop(0)
            else:
                return self.Colour

    @getColour.setter
    def getColour(self, colour):
        if isinstance(colour, list):
            if isinstance(self.Colour, list):
                self.Colour = self.Colour + colour
            else:
                self.Colour = None
                self.Colour = colour
        else:
            self.Colour = colour

    def getColourFillList(self, ColourTheme, LVals, FloatMin, FloatMax):
        # To be continued
        self.getColour = plt.get_cmap(ColourTheme)(np.linspace(FloatMin, FloatMax, len(LVals)))

    def getColourFullList(self, BEmptying=True):
        if isinstance(self.Colour, list):
            Temp = self.Colour
            if BEmptying:
                self.Colour = None
            return Temp
        else:
            print("Warning: No list of colours found.")
            return self.Colour

    @property
    def getColourMap(self):
        return self.ColourMap

    @getColourMap.setter
    def getColourMap(self, VColourMap):
        ColourMapDict = {"Perceptually Uniform Sequential": (0, 4),  # Indices: 0-4
                         0: "viridis", 1: "plasma", 2: "inferno", 3: "magma", 4: "cividis",

                         "Sequential": (5, 22),  # Indices: 5-22
                         5: "Greys", 6: "Purples", 7: "Blues", 8: "Greens", 9: "Oranges", 10: "Reds",
                         11: "YlOrBr", 12: "YlOrRd", 13: "OrRd", 14: "PuRd", 15: "RdPu", 16: "BuPu",
                         17: "GnBu", 18: "PuBu", 19: "YlGnBu", 20: "PuBuGn", 21: "BuGn", 22: "YlGn",

                         "Diverging": (23, 34),  # Indices: 23-34
                         23: "PiYG", 24: "PRGn", 25: "BrBG", 26: "PuOr", 27: "RdGy", 28: "RdBu",
                         29: "RdYlBu", 30: "RdYlGn", 31: "Spectral", 32: "coolwarm", 33: "bwr", 34: "seismic",

                         "Cyclic": (35, 37),  # Indices: 35-37
                         35: "twilight", 36: "twilight_shifted", 37: "hsv",

                         "Qualitative": (38, 49),  # Indices: 38-49
                         38: "Pastel1", 39: "Pastel2", 40: "Paired", 41: "Accent", 42: "Dark2",
                         43: "Set1", 44: "Set2", 45: "Set3", 46: "tab10", 47: "tab20", 48: "tab20b", 49: "tab20c",

                         "Miscellaneous": (50, 66),  # Indices: 50-66
                         50: "flag", 51: "prism", 52: "ocean", 53: "gist_earth", 54: "terrain", 55: "gist_stern",
                         56: "gnuplot", 57: "gnuplot2", 58: "CMRmap", 59: "cubehelix", 60: "brg",
                         61: "gist_rainbow", 62: "rainbow", 63: "jet", 64: "turbo", 65: "nipy_spectral", 66: "gist_ncar",

                         "Sequential (Miscellaneous)": (67, 82),  # Indices: 67-82
                         67: "binary", 68: "gist_yarg", 69: "gist_gray", 70: "gray", 71: "bone", 72: "pink",
                         73: "spring", 74: "summer", 75: "autumn", 76: "winter", 77: "cool", 78: "Wistia",
                         79: "hot", 80: "afmhot", 81: "gist_heat", 82: "copper",

                         "Perceptually Uniform Sequential (Reversed)": (83, 87),  # Indices: 83-87
                         83: "viridis_r", 84: "plasma_r", 85: "inferno_r", 86: "magma_r", 87: "cividis_r",

                         "Sequential (Reversed)": (88, 105),  # Indices: 88-105
                         88: "Greys_r", 89: "Purples_r", 90: "Blues_r", 91: "Greens_r", 92: "Oranges_r", 93: "Reds_r",
                         94: "YlOrBr_r", 95: "YlOrRd_r", 96: "OrRd_r", 97: "PuRd_r", 98: "RdPu_r", 99: "BuPu_r",
                         100: "GnBu_r", 101: "PuBu_r", 102: "YlGnBu_r", 103: "PuBuGn_r", 104: "BuGn_r", 105: "YlGn_r",
                         
                         "Diverging (Reversed)": (106, 117),  # Indices: 106-117
                         106: "PiYG_r", 107: "PRGn_r", 108: "BrBG_r", 109: "PuOr_r", 110: "RdGy_r", 111: "RdBu_r",
                         112: "RdYlBu_r", 113: "RdYlGn_r", 114: "Spectral_r", 115: "coolwarm_r", 116: "bwr_r", 117: "seismic_r",

                         "Cyclic (Reversed)": (118, 120),  # Indices: 118-120
                         118: "twilight_r", 119: "twilight_shifted_r", 120: "hsv_r",

                         "Miscellaneous (Reversed)": (121, 137),  # Indices: 121-137
                         121: "flag_r", 122: "prism_r", 123: "ocean_r", 124: "gist_earth_r", 125: "terrain_r", 126: "gist_stern_r",
                         127: "gnuplot_r", 128: "gnuplot2_r", 129: "CMRmap_r", 130: "cubehelix_r", 131: "brg_r",
                         132: "gist_rainbow_r", 133: "rainbow_r", 134: "jet_r", 135: "turbo_r", 136: "nipy_spectral_r", 137: "gist_ncar_r",

                         "Sequential (Miscellaneous) (Reversed)": (138, 153),  # Indices: 138-153
                         138: "binary_r", 139: "gist_yarg_r", 140: "gist_gray_r", 141: "gray_r", 142: "bone_r", 143: "pink_r",
                         144: "spring_r", 145: "summer_r", 146: "autumn_r", 147: "winter_r", 148: "cool_r", 149: "Wistia_r",
                         150: "hot_r", 151: "afmhot_r", 152: "gist_heat_r", 153: "copper_r"}

        self.ColourMap = ColourMapDict.get(VColourMap, 'viridis')

    @property
    def getLineType(self):
        # Determine line type based on linetype input
        LineTypeDict = {0: '-', 1: '--', 2: '-.', 3: ':'}
        LineType = LineTypeDict.get(self.LineType, '-')
        return LineType

    @getLineType.setter
    def getLineType(self, linetype):
        self.LineType = linetype

    @property
    def getLineSize(self):
        return self.LineSize

    @getLineSize.setter
    def getLineSize(self, linesize):
        self.LineSize = linesize

    @property
    def getMarker(self):
        MarkerTypeDict = {0: '', 1: '.', 2: ',', 3: 'o', 4: 'v', 5: '^',
                          6: '<', 7: '>', 8: '1', 9: '2', 10: '3', 11: '4',
                          12: '8', 13: 's', 14: 'p', 15: 'P', 16: '*', 17: 'h',
                          18: 'H', 19: '+', 20: 'x', 21: 'X', 22: 'D', 23: 'd',
                          24: '|', 25: '_'}
        MarkerType = MarkerTypeDict.get(self.MarkerType, '')
        return MarkerType

    @getMarker.setter
    def getMarker(self, marker):
        self.MarkerType = marker

    @property
    def getMarkerSize(self):
        return self.MarkerSize

    @getMarkerSize.setter
    def getMarkerSize(self, MarkerSize):
        self.MarkerSize = MarkerSize

    @property
    def getAlpha(self):
        return self.Alpha

    @getAlpha.setter
    def getAlpha(self, Alpha):
        self.Alpha = Alpha

    @property
    def getHatch(self):
        """
        Property that retrieves and modifies the `HatchType` attribute.
        - If `HatchType` is empty (`None` or equivalent), it returns `None`.
        - If `HatchType` is a list, it removes and returns the first element of the list (FIFO behavior).
        - If `HatchType` is not a list, it simply returns the value of `HatchType`.

        Returns:
            Any: 
                - If `HatchType` is empty, returns `None`.
                - If `HatchType` is a list, returns the first element while modifying the list.
                - If `HatchType` is a single value, returns that value.
        """

        # Check if `HatchType` is empty or `None`
        if not self.HatchType:
            return None  # Return None if no value is present
        else:
            # If `HatchType` is a list, pop and return the first element
            if isinstance(self.HatchType, list):
                return self.HatchType.pop(0)  # Remove the first element and return it
            else:
                # If `HatchType` is not a list, return the value directly
                return self.HatchType

    @getHatch.setter
    def getHatch(self, HatchType):
        """
        Sets the `HatchType` property of the object based on the specified hatch type (`HatchType`).
        The hatch type is mapped to predefined patterns using a dictionary.
        This method can handle simple integers or complex structures such as nested lists.

        Args:
            HatchType (int, list, or other): The hatch type to configure.
                - If `HatchType` is an integer, it is directly mapped to a pattern using the dictionary (Result = 1 Hatch).
                - If `HatchType` is a flat list, each element is individually mapped to create a combined pattern (Result = 1 Hatch).
                - If `HatchType` is a nested list, each sub-list is individually mapped to create multiple patterns (Result = # of sub-lists Hatch).

        Returns:
            None: Directly assigns the resulting value to `self.HatchType`.
        """

        # Dictionary mapping numeric values to hatch patterns
        HatchTypeDict = {
            0: '', 1: '/', 2: '\\', 3: '|', 4: '-', 5: '+',
            6: 'x', 7: 'o', 8: 'O', 9: '.', 10: '*'
        }

        # Variables to store the result
        Hatch = ''   # Combined pattern if HatchType is a flat list
        LHatch = []  # List of patterns if HatchType contains nested lists

        # Check if `HatchType` is a list
        if isinstance(HatchType, list):
            for Item in HatchType:
                if isinstance(Item, list):  # If an element is a nested list
                    LItem = Item
                    Hatch = ''  # Reset `Hatch` for each sub-list
                    for Val in LItem:
                        # Add the pattern corresponding to the value to `Hatch`
                        Hatch += HatchTypeDict.get(Val, '')  
                    LHatch.append(Hatch)  # Append the complete pattern of the sub-list to `LHatch`
                else:  # If the element is an integer or a simple value
                    Val = Item
                    Hatch += HatchTypeDict.get(Val, '')  # Add the pattern directly
        else:  # If `HatchType` is not a list
            Hatch = HatchTypeDict.get(HatchType, '')  # Retrieve the corresponding pattern

        # Assign the final value to `self.HatchType`
        if LHatch:  # If `LHatch` contains complex patterns
            self.HatchType = LHatch
        else:  # Otherwise, use the simple pattern
            self.HatchType = Hatch

    def getHatchFullList(self, BEmptying=True):
        """
        Property that retrieves the full list of hatch patterns if `HatchType` is a list.
        If `HatchType` is not a list, it displays a warning message and returns the current value of `HatchType`.

        Returns:
            list or other: If `HatchType` is a list, it returns the list of hatch patterns and resets `HatchType` to `None`.
                           If `HatchType` is not a list, it prints a warning message and returns the current value of `HatchType`.
        """
        # Check if `HatchType` is a list
        if isinstance(self.HatchType, list):
            Temp = self.HatchType  # Store the current list of hatch patterns in a temporary variable
            if BEmptying:
                self.HatchType = None  # Reset `HatchType` to `None`
            return Temp  # Return the stored list
        else:
            # Print a warning message if `HatchType` is not a list
            print("Warning: No list of hatch found.")
            return self.HatchType  # Return the current value of `HatchType`


    @property
    def getTitleSize(self):
        return self.TitleSize

    @getTitleSize.setter
    def getTitleSize(self, TitleSize):
        self.TitleSize = TitleSize

    @property
    def getFontSize(self):
        return self.FontSize

    @getFontSize.setter
    def getFontSize(self, fontsize):
        self.FontSize = fontsize

    @property
    def getTicksSize(self):
        return self.TicksSize

    @getTicksSize.setter
    def getTicksSize(self, TicksSize):
        self.TicksSize = TicksSize

    @property
    def getTitle(self):
        return self.Title

    @getTitle.setter
    def getTitle(self, Title):
        self.Title = Title

    @property
    def getXLabel(self):
        return self.XLabel

    @getXLabel.setter
    def getXLabel(self, XLabel):
        self.XLabel = XLabel

    @property
    def getYLabel(self):
        return self.YLabel

    @getYLabel.setter
    def getYLabel(self, YLabel):
        self.YLabel = YLabel

    @property
    def getZLabel(self):
        return self.ZLabel

    @getZLabel.setter
    def getZLabel(self, ZLabel):
        self.ZLabel = ZLabel

    def getLabelTitle(self, Title, XLabel, YLabel, ZLabel=None):
        self.Title = Title
        self.XLabel = XLabel
        self.YLabel = YLabel
        self.ZLabel = ZLabel

    @property
    def getLegends(self):
        if not self.Legends:
            return None
        else:
            return self.Legends.pop(0)

    @getLegends.setter
    def getLegends(self, Legends):
        self.Legends = Legends

    def getLegendsFullList(self, BEmptying=True):
        # Check if `Legends` is a list
        if isinstance(self.Legends, list):
            Temp = self.Legends  # Store the current list of legend in a temporary variable
            if BEmptying:
                self.Legends = None  # Reset `Legends` to `None`
            return Temp  # Return the stored list
        else:
            # Print a warning message if `Legends` is not a list
            print("Warning: No list of legend found.")
            return self.Legends  # Return the current value of `Legends`
  
    @property
    def getBLegends(self):
        return self.BLegends

    @getBLegends.setter
    def getBLegends(self, Bool):
        self.BLegends = Bool

    @property
    def getColourBarTitle(self):
        return self.ColourBarTitle

    @getColourBarTitle.setter
    def getColourBarTitle(self, Title):
        self.ColourBarTitle = Title

    @property
    def getScale(self):
        return self.Scale

    @getScale.setter
    def getScale(self, scale):
        self.Scale = scale

    def ScaleVal2Name(self, Val):
        ScaleTypeDict = {0: 'linear', 1: 'log', 2: 'logit',
                         3: 'symlog', 4: 'function',
                         5: 'functionlog', 6: 'asinh',
                         7: 'mercator'}
        ScaleType = ScaleTypeDict.get(Val, 'linear')
        return ScaleType

    @property
    def getXScaleType(self):
        return self.XScaleType

    @getXScaleType.setter
    def getXScaleType(self, Val):
        self.XScaleType = self.ScaleVal2Name(Val)

    @property
    def getYScaleType(self):
        return self.YScaleType

    @getYScaleType.setter
    def getYScaleType(self, Val):
        self.YScaleType = self.ScaleVal2Name(Val)

    @property
    def getZScaleType(self):
        return self.ZScaleType

    @getZScaleType.setter
    def getZScaleType(self, Val):
        self.ZScaleType = self.ScaleVal2Name(Val)

    @property
    def getGenericScaleType(self):
        return self.GenericScaleType

    @getGenericScaleType.setter
    def getGenericScaleType(self, Val):
        self.GenericScaleType = self.ScaleVal2Name(Val)

    @property
    def getScale3D(self):
        return self.Scale3D

    @getScale3D.setter
    def getScale3D(self, scale3D):
        self.Scale3D = scale3D

    @property
    def getFMT(self):
        # Construct plot format
        fmt = f"{self.getMarker}{self.getLineSize}{self.getColour}"
        return fmt

    @property
    def getAspect(self):
        return self.PltAspect

    @getAspect.setter
    def getAspect(self, Aspect):
        self.PltAspect = Aspect

    def getGrid(self, Axis, Colour=None):
        if Axis == 1:
            self.GridAxis = 'x'
        elif Axis == 2:
            self.GridAxis = 'y'
        elif Axis >= 0:
            self.GridAxis = 'both'
        else:
            self.GridAxis = None

        self.GridColour = Colour

        self.GridLineType = None
        self.GridLineSize = 0.4

    @property
    def getGridLineType(self):
        # Determine line type based on linetype input
        LineTypeDict = {0: '-', 1: '-', 2: '--', 3: '-.', 4: ':'}
        LineType = LineTypeDict.get(self.GridLineType, '-')
        return LineType

    @getGridLineType.setter
    def getGridLineType(self, LineType):
        self.GridLineType = LineType

    @property
    def getGridLineSize(self):
        return self.GridLineSize

    @getGridLineSize.setter
    def getGridLineSize(self, LineSize):
        self.GridLineSize = LineSize

    @property
    def getGridAxis(self):
        return self.GridAxis

    @getGridAxis.setter
    def getGridAxis(self, GridAxis):
        self.GridAxis = GridAxis

    @property
    def getGridAlpha(self):
        return self.GridAlpha

    @getGridAlpha.setter
    def getGridAlpha(self, Val):
        self.GridAlpha = Val

    @property
    def getXLimit(self):
        if not self.XLimit:
            return None
        else:
            return self.XLimit.pop(0)

    @getXLimit.setter
    def getXLimit(self, Limit):
        self.XLimit.append(Limit)
    
    @property
    def getYLimit(self):
        if not self.YLimit:
            return None
        else:
            return self.YLimit.pop(0)

    @getYLimit.setter
    def getYLimit(self, Limit):
        self.YLimit.append(Limit)
    
    @property
    def getZLimit(self):
        if not self.ZLimit:
            return None
        else:
            return self.ZLimit.pop(0)

    @getZLimit.setter
    def getZLimit(self, Limit):
        self.ZLimit.append(Limit)

    @property
    def getBoolXLimit(self):
        return bool(self.XLimit)
    
    @property
    def getBoolYLimit(self):
        return bool(self.YLimit)
    
    @property
    def getBoolZLimit(self):
        return bool(self.ZLimit)



"""
Fcts générales
"""
def ClosePlot(PlotOBJ):
    plt.close(PlotOBJ)

def CloseALLPlots():
    plt.close('all')

def ClosePlotsOnDemand():
    # To close all plots on demand
    input("Press Enter to close all plots...") 
    plt.close('all')

def StartPlots():
    plt.figure()

def PLTTitleAxis(paramPLT):
    plt.xlabel(paramPLT.getXLabel, fontsize=paramPLT.getFontSize)
    plt.ylabel(paramPLT.getYLabel, fontsize=paramPLT.getFontSize)
    plt.title(paramPLT.getTitle, fontsize=paramPLT.getTitleSize)

def PLTSizeAxis(paramPLT):
    plt.xticks(fontsize=paramPLT.getTicksSize)
    plt.yticks(fontsize=paramPLT.getTicksSize)

def PLTLegend(paramPLT):
    if paramPLT.getBLegends:
        plt.legend(fontsize=paramPLT.getFontSize)

def PLTGrid(paramPLT):
    if paramPLT.getGridAxis:
        plt.grid(axis=paramPLT.getGridAxis,
                 color=paramPLT.getColour,
                 linestyle=paramPLT.getGridLineType,
                 linewidth=paramPLT.getGridLineSize,
                 alpha=paramPLT.getGridAlpha)

def PLTLimit(paramPLT):
    if paramPLT.getBoolXLimit:
        plt.xlim(paramPLT.getXLimit)
    if paramPLT.getBoolYLimit:
        plt.ylim(paramPLT.getYLimit)

def PLTCmptLimit(Variable, Ratio=0.1):
    """
    Compute the limits of the plot based on the variable and a ratio.

    Improvements:
    - Based the computation on the current registered limits (self.XLimit, self.YLimit, self.ZLimit).
    """
    MaxVal = max(Variable)
    MinVal = min(Variable)
    Delta = MaxVal-MinVal
    LowerLimit = MinVal-Delta*Ratio
    UpperLimit = MaxVal+Delta*Ratio
    return [LowerLimit, UpperLimit]

def PLTScaleType(paramPLT):
    if paramPLT.getXScaleType:
        plt.xscale(paramPLT.getXScaleType)
    if paramPLT.getYScaleType:
        plt.yscale(paramPLT.getYScaleType)

def PLTShow(paramPLT, BMultiplot=False):
    PLTTitleAxis(paramPLT)

    PLTSizeAxis(paramPLT)

    if paramPLT.getAspect:
        plt.gca().set_aspect('equal', adjustable='box')

    PLTLegend(paramPLT)

    PLTGrid(paramPLT)

    PLTLimit(paramPLT)

    PLTScaleType(paramPLT)

    if not BMultiplot:
        plt.show(block=False)  # Show plot without blocking

def PLTMultiPlot(paramPLT, Rows, Cols=1, Index=1):
    if Index == 1:
        StartPlots()
        plt.subplot(Rows, Cols, Index)
        plt.suptitle(paramPLT.getTitle, fontsize=paramPLT.getTitleSize)
    elif Index == Rows*Cols+1:
        plt.tight_layout()
        PLTShow(paramPLT)
    elif 1 < Index <= Rows*Cols:
        PLTShow(paramPLT, BMultiplot=True)
        plt.subplot(Rows, Cols, Index)
    else:
        print("Warning: Invalid index for subplot.")
    return Index + 1

def PLTUpdateLayout():
    plt.tight_layout()

def PLTScreenMaximize(BTaskbar=True, BUpdateLayout=True):
    if BTaskbar:
        plt.get_current_fig_manager().window.state('zoomed')
    else:
        plt.get_current_fig_manager().full_screen_toggle()

    if BUpdateLayout:
        plt.pause(0.1) # Pause to allow the window to maximize and UpdateLayout to work
        # in case of unreliable behavior, increase the pause duration
        PLTUpdateLayout()

def PLTColorBar(paramPLT):
    """
    Add a color bar to the plot based on the specified parameters.
    """
    if paramPLT.getColourBarTitle:
        plt.colorbar(label=paramPLT.getColourBarTitle)

def DefaultParamPLT():
    return ParamPLT(colour='black', linetype=0, marker=0, linesize=2, fontsize=16)

# Version in 3D case with PLT3DShow

"""
Type de Plots
"""
# 2D

def PLTPlot(XValues, YValues, paramPLT):
    """
    Creates a 2D plot using customizable parameters.

    Args:
        XValues (list ou array-like): Les valeurs de l'axe X.
        YValues (list ou array-like): Les valeurs de l'axe Y.
        paramPLT (objet): Un objet contenant les attributs suivants pour personnaliser l'apparence du graphique

    Returns:
        None: Cette fonction ne retourne rien. Elle affiche simplement le graphique.
    """
    plt.plot(XValues, YValues,
            color=paramPLT.getColour,      # Couleur de la courbe
            alpha=paramPLT.getAlpha,       # Transparence de la courbe
            linestyle=paramPLT.getLineType,  # Style de la ligne (continu, pointillé, etc.)
            linewidth=paramPLT.getLineSize,  # Épaisseur de la ligne
            marker=paramPLT.getMarker,          # Style des marqueurs pour les points
            markersize=paramPLT.getMarkerSize, # Taille des marqueurs
            label=paramPLT.getLegends)       # Texte pour la légende

def PLTFill(XValues, YValues, paramPLT, ValZOrder=0, YValuesSec=False):
    """
    Creates a filled plot between two curves (primary and secondary) using customizable parameters.

    Inputs:
    - XValues (list or array-like): X-axis values.
    - YValues (list or array-like): Y-axis values for the primary curve.
    - paramPLT (object): Object containing plot parameters.
    - ValZOrder (int): Z-order value to determine which layer is on top.
    - YValuesSec (list or array-like): Y-axis values for the secondary curve (optional).
    """
    if YValuesSec:
        plt.fill_between(XValues, YValues, YValuesSec,
                         facecolor=paramPLT.getColour, edgecolor=paramPLT.getColour,
                         hatch=paramPLT.getHatch, alpha=paramPLT.getAlpha, zorder=ValZOrder,
                         label=paramPLT.getLegends)
    else:
        plt.fill(XValues, YValues,
                 facecolor=paramPLT.getColour, edgecolor=paramPLT.getColour,
                 hatch=paramPLT.getHatch, alpha=paramPLT.getAlpha, zorder=ValZOrder,
                 label=paramPLT.getLegends)


def PLTBar(Labels, Vals, paramPLT, StdErrors=None, BOrientation=True):
    """
    Creates a bar plot with optional error bars, customizable colors, labels, and orientation.

    Args:
    - Labels: List of labels for the bars.
    - Vals: List of values corresponding to the height (or width) of each bar.
    - paramPLT: An object containing plot parameters 
    - StdErrors (optional): List or array of standard errors for each bar.
        - Scalar: Symmetric +/- error for all bars.
        - Shape (N,): Symmetric +/- error for each bar.
        - Shape (2, N): Asymmetric error values where:
            - First row specifies lower errors.
            - Second row specifies upper errors.
    - BOrientation: Boolean flag to specify the orientation of the bars.
        - True: Vertical bar plot (default).
        - False: Horizontal bar plot.

    Returns:
        None: Cette fonction ne retourne rien. Elle affiche simplement le graphique.

    Improovements:
    - Allows stacking bars: Use `bottom=` parameter with previous bar values.
    - Allows grouping bars: Create offsets using arrays like:
        br1 = np.arange(len(Labels))
        br2 = [x + barWidth for x in br1]
        br3 = [x + barWidth for x in br2]
    """
    if BOrientation:
        plt.bar(Labels, Vals, yerr=StdErrors,
                facecolor=paramPLT.getColourFullList(BEmptying=False), edgecolor=paramPLT.getColourFullList(),
                width=paramPLT.getLineSize, label=paramPLT.getLegends)
    else:
        plt.barh(Labels, Vals, xerr=StdErrors,
                 facecolor=paramPLT.getColourFullList(BEmptying=False), edgecolor=paramPLT.getColourFullList(),
                 alpha=paramPLT.getAlpha,
                 height=paramPLT.getLineSize, label=paramPLT.getLegends)

def PLTPie(Val, paramPLT, TypeAutopct=0, PrecisionPct=1, AbsUnit="", PrecisionAbs=0, 
           Radius=1, StartAngle=0, LabelDist=1.25, PctDist=0.6, BShadow=False, explode=None, 
           EnableAnnotations=False):
    """
    Creates a pie plot with customizable options, including optional annotations.

    Parameters:
    - Val (list): Values for the pie chart.
    - paramPLT (object): Object containing plot parameters (e.g., colors, labels, hatches).
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
    - Displays a pie chart.

    Improvements:
    - Ajouter des vérifications entre les paramètres pour éviter les conflits.
    - Extraire un nombre limité de paramètres pour éviter des clash si plus de valeurs.
    """

    AnnotateTextSize=paramPLT.getFontSize
    paramPLT.GridAxis = None
    paramPLT.getBLegends = False

    def GeneAutopct(pct, allvals):
        absolute = np.round(pct / 100. * np.sum(allvals), PrecisionAbs)
        if TypeAutopct <= 0:
            return f"{pct:.{PrecisionPct}f}%"
        elif TypeAutopct == 1:
            return f"{absolute:.{PrecisionAbs}f} {AbsUnit}"
        elif TypeAutopct == 2:
            return f""
        elif TypeAutopct >= 3:
            return f"{pct:.{PrecisionPct}f}%\n({absolute:.{PrecisionAbs}f} {AbsUnit})"

    # Generate the pie chart
    LLegends = paramPLT.getLegendsFullList(BEmptying=EnableAnnotations)
    wedges, texts, autotexts = plt.pie(Val, labels=paramPLT.getLegendsFullList(), labeldistance=LabelDist,
                                       autopct=lambda pct: GeneAutopct(pct, Val), pctdistance=PctDist,
                                       colors=paramPLT.getColourFullList(), hatch=paramPLT.getHatchFullList(),
                                       radius=Radius, startangle=StartAngle,
                                       explode=explode, shadow=BShadow,
                                       textprops=dict(size=AnnotateTextSize, color="k"))  # Customize text properties

    # Optional Annotation logic
    if EnableAnnotations:
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="w", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            plt.annotate(LLegends[i],  # Use legend text
                         xy=(x, y), 
                         xytext=(1.35 * Radius * np.sign(x), 1.4 * Radius * y),
                         fontsize=AnnotateTextSize,
                         horizontalalignment=horizontalalignment, 
                         **kw)

def PLTImShow(ValMatrix, paramPLT, FInterpolType=0, BOrigin=True):
    """
    Displays an image plot of the provided matrix using custom parameters.
    """
    InterpolDict = {0: 'none', 1: 'auto', 2: 'nearest', 3: 'bilinear', 4: 'bicubic',
                    5: 'spline16', 6: 'spline36', 7: 'hanning', 8: 'hamming',
                    9: 'hermite', 10: 'kaiser', 11: 'quadric', 12: 'catrom',
                    13: 'gaussian', 14: 'bessel', 15: 'mitchell', 16: 'sinc', 17: 'lanczos',
                    18: 'blackman'}
    InterpolType = InterpolDict.get(FInterpolType, 'none')
    
    TypeOrigin =  'upper' if BOrigin else 'lower'

    plt.imshow(ValMatrix, cmap=paramPLT.getColourMap, alpha=paramPLT.getAlpha,
               norm=paramPLT.GenericScaleType, interpolation=InterpolType,
               origin=TypeOrigin)

    PLTColorBar(paramPLT)

    

# 2D Shapes
def PLT2DCircle(x, y, NPoints, Radius, paramPLT, BFill=False):
    # Calculate the angles for the tick marks
    Angles = np.linspace(0, 2*np.pi, NPoints+1, endpoint=True)
    PreVal = False
    xEnd = 0
    yEnd = 0
    XPoint = []
    YPoint = []
    for Angle in Angles:
        # Starting point of the tick (on the circle)
        xStart = x + Radius*np.cos(Angle)
        yStart = y + Radius*np.sin(Angle)

        if PreVal:
            plt.plot([xStart, xEnd],
                     [yStart, yEnd],
                     color=paramPLT.getColour,
                     linestyle=paramPLT.getLineType,
                     marker=paramPLT.getMarker,
                     linewidth=paramPLT.getLineSize,
                     markersize=paramPLT.getLineSize,
                     label=paramPLT.getLegends)
            XPoint.append(xEnd)
            YPoint.append(yEnd)
        else:
            PreVal = True
        xEnd = xStart
        yEnd = yStart
    if BFill:
        plt.fill(XPoint, YPoint, color=paramPLT.getColour, zorder=0,
                 label=paramPLT.getLegends)

# Plotting functions in 3D
# 3D

# 3D Shapes
