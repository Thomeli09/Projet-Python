# -*- coding: utf-8 -*-
"""
Created on Thu Fen 12 2026

@author: Thommes Eliott
"""

# Granulometry library
"""
Improovements :
"""

# Other Lib
import numpy as np


# Custom Lib
from PlotLib import ParamPLT, StartPlots, CloseAllPlots, PLTShow, DefaultParamPLT, PLTPlot


"""
Granulometry : Generic granulometry class
"""
class Granulometry:
    def __init__(self):
        # Granulometry data
        self.GranuloDiam = None # Vector of diameters of the granulometry to plot [mm]
        self.GranuloRatio = None # Vector of the ratio of passers-by of the granulometry [-]
        self.GranuloPourcent = None # Vector of the percentage of passers-by of the granulometry [%]

    # Granulometry data
    @property
    def getGranuloDiam(self):
        """Getter for the vector of diameters of the granulometry to plot [mm]."""
        return self.GranuloDiam

    @getGranuloDiam.setter
    def getGranuloDiam(self, VectDiam):
        """Setter for the vector of diameters of the granulometry to plot [mm]."""
        if isinstance(VectDiam, float):
            VectGranuloDiam = np.array([VectDiam], dtype=float)
            self.GranuloDiam = np.concatenate((self.GranuloDiam, VectGranuloDiam))
            return
        elif isinstance(VectDiam, list):
            self.GranuloDiam = np.asarray(VectDiam, dtype=float)
        elif isinstance(VectDiam, np.ndarray):
            self.GranuloDiam = VectDiam.astype(float)
        else:
            raise ValueError("Error: GranuloDiam must be a float, a list or a numpy array.")

    @property
    def getGranuloRatio(self):
        """Getter for the vector of the ratio of passers-by of the granulometry [-]."""
        return self.GranuloRatio

    @getGranuloRatio.setter
    def getGranuloRatio(self, VectRatio):
        """Setter for the vector of the ratio of passers-by of the granulometry [-]."""
        if isinstance(VectRatio, float):
            VectGranuloRatio = np.array([VectRatio], dtype=float)
            self.GranuloRatio = np.concatenate((self.GranuloRatio, VectGranuloRatio))
            return
        elif isinstance(VectRatio, list):
            self.GranuloRatio = np.asarray(VectRatio, dtype=float)
        elif isinstance(VectRatio, np.ndarray):
            self.GranuloRatio = VectRatio.astype(float)
        else:
            raise ValueError("Error: GranuloRatio must be a float, a list or a numpy array.")
        self.GranuloPourcent = self.getGranuloRatio * 100.0

    @property
    def getGranuloPourcent(self):
        """Getter for the vector of the percentage of passers-by of the granulometry [%]."""
        return self.GranuloPourcent

    @getGranuloPourcent.setter
    def getGranuloPourcent(self, VectPourcent):
        """Setter for the vector of the percentage of passers-by of the granulometry [%]."""
        if isinstance(VectPourcent, float):
            VectGranuloPourcent = np.array([VectPourcent], dtype=float)
            self.GranuloPourcent = np.concatenate((self.GranuloPourcent, VectGranuloPourcent))
            return
        elif isinstance(VectPourcent, list):
            self.GranuloPourcent = np.asarray(VectPourcent, dtype=float)
        elif isinstance(VectPourcent, np.ndarray):
            self.GranuloPourcent = VectPourcent.astype(float)
        else:
            raise ValueError("Error: GranuloPourcent must be a float, a list or a numpy array.")
        self.GranuloRatio = self.getGranuloPourcent / 100.0

    # Plotting function
    def PLTGranulometry(self, paramPLT=None, StrTitleName=None, BStart=True, BEnd=True, BPourcent=True):
        """
        Plot of a granulometric curve based on the provided diameters and percentage of passers-by, 
        with options to customize the plot and to indicate if the y-axis is in percentage or ratio.
        
        Args:
        - paramPLT: Parameters of the plot
        - StrTitleName: Name of the granulometry to plot (e.g., "mix", "aggregate", etc.)
        - BStart: Boolean to indicate if the plot starts in a new figure
        - BEnd: Boolean to indicate if the plot ends and shows the figure
        - BPourcent: Boolean to indicate if the y-axis is in percentage (True) or ratio (False)
        Returns:
            Plot of the granulometry of the mix
        """
        PLTGranulometry(self.getGranuloDiam, self.getGranuloRatio, paramPLT=paramPLT, StrTitleName=StrTitleName, 
                        BStart=BStart, BEnd=BEnd, BPourcent=BPourcent)

# Generic computation function of granulometric curve


# Generic plotting function of granulometric curve
def PLTGranulometry(GranuloDiam, GranuloRatio, paramPLT=None, StrTitleName=None, BStart=True, BEnd=True, BPourcent=True):
    """
    Plot of a granulometric curve based on the provided diameters and percentage of passers-by, 
    with options to customize the plot and to indicate if the y-axis is in percentage or ratio.
        
    Args:
    - GranuloDiam: Vector of diameters of the granulometry to plot [mm]
    - GranuloRatio: Vector of the percentage of passers-by of the granulometry to plot [-] or [%]
    - paramPLT: Parameters of the plot
    - StrTitleName: Name of the granulometry to plot (e.g., "mix", "aggregate", etc.)
    - BStart: Boolean to indicate if the plot starts in a new figure
    - BEnd: Boolean to indicate if the plot ends and shows the figure
    - BPourcent: Boolean to indicate if the y-axis is in percentage (True) or ratio (False)

    Returns:
        Plot of the granulometry of the mix
    """
    if paramPLT is None:
        paramPLT = DefaultParamPLT()

    if BStart:
        StartPlots()

    # Convert to percentage if needed
    if not BPourcent:
        GranuloRatio = GranuloRatio * 100.0

    # Plot the granulometry of the mix
    PLTPlot(GranuloDiam, GranuloRatio, paramPLT)

    if StrTitleName is not None:
        paramPLT.getTitle = "Particle size distribution of the " + StrTitleName
    else:
        paramPLT.getTitle = "Particle size distribution"

    paramPLT.getXScaleType = 1

    paramPLT.getXLabel = "Particle size (mm)"

    if BPourcent:
        paramPLT.getYLabel = "Percentage of passers-by (%)"
    else:
        paramPLT.getYLabel = "Ratio of passers-by (-)"

    if BEnd:
        PLTShow(paramPLT)
