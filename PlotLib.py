# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:15:29 2024

@author: Thommes Eliott
"""

# General Plotting library

import matplotlib.pyplot as plt
import numpy as np


# Custom Lib


"""
Base de donnée
"""


# Paramètre d'affichage
class ParamPLT:
    def __init__(self, colour, linetype, marker, linesize, fontsize, scale, scale3D):
        """
        Ajouter le système de liste si différents éléments, pas que pour les légendes,...
        """
        # Plot
        if isinstance(colour, list):
            self.Colour = colour
        else:
            self.Colour = [colour]
        self.LineType = linetype
        self.LineSize = 2
        self.MarkerType = marker
        self.MarkerSize = 50
        self.Alpha = 1  # Blending value, from 0 (transparent) to 1 (opaque)
        self.HatchType = 0

        # Text
        self.FontSize = fontsize
        self.TitleSize = fontsize
        self.TicksSize = fontsize
        self.XLabel = None
        self.YLabel = None
        self.ZLabel = None
        self.Title = None
        self.Legends = []

        # Scale
        self.Scale = scale
        self.Scale3D = scale3D

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
            return self.Colour.pop(0)

    @getColour.setter
    def getColour(self, colour):
        if isinstance(colour, list):
            self.Colour += colour
        else:
            self.Colour.append(colour)

    @property
    def getLineType(self):
        # Determine line type based on linetype input
        LineTypeDict = {0: '-', 1: '-', 2: '--', 3: '-.', 4: ':'}
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
        HatchTypeDict = {0: '', 1: '/', 2: '\\', 3: '|', 4: '-', 5: '+',
                            6: 'x', 7: 'o', 8: 'O', 9: '.', 10: '*'}
        Hatch = ''
        if isinstance(self.HatchType, list):
            for Val in self.HatchType:
                Hatch += HatchTypeDict.get(Val, '')
        else:
            Hatch = HatchTypeDict.get(self.HatchType, '')
        return Hatch

    @getHatch.setter
    def getHatch(self, HatchType):
        self.HatchType = HatchType

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

    @property
    def getScale(self):
        return self.Scale

    @getScale.setter
    def getScale(self, scale):
        self.Scale = scale

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

"""
Type de Plots
"""
# 2D
def PLTTitleAxis(paramPLT):
    plt.xlabel(paramPLT.getXLabel, fontsize=paramPLT.getFontSize)
    plt.ylabel(paramPLT.getYLabel, fontsize=paramPLT.getFontSize)
    plt.title(paramPLT.getTitle, fontsize=paramPLT.getTitleSize)

def PLTSizeAxis(paramPLT):
    plt.xticks(fontsize=paramPLT.getTicksSize)
    plt.yticks(fontsize=paramPLT.getTicksSize)

def PLTLegend(paramPLT):
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

def PLTShow(paramPLT):
    PLTTitleAxis(paramPLT)

    PLTSizeAxis(paramPLT)

    if paramPLT.getAspect:
        plt.gca().set_aspect('equal', adjustable='box')

    PLTLegend(paramPLT)

    PLTGrid(paramPLT)

    PLTLimit(paramPLT)

    plt.show(block=False)  # Show plot without blocking


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
        plt.fill(XPoint, YPoint, paramPLT.getColour, zorder=0,
                 label=paramPLT.getLegends)


'Fonction de plot de graphe en 2d'
# 3D

