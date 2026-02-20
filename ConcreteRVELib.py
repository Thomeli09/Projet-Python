# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:21:57 2025

@author: Thommes Eliott
"""

# Concrete RVE Library
"""
Improovements :
- Save data in a file after computation
"""

# Other Lib


# Custom Lib
from ConcreteLib import CemMat

class RVE:
    def __init__(self):
        # CemMat
        self.CemMat = None # CemMat object to generate the RVE from

        # Geometry
        self.Geometry = None # Geometry of the RVE in [mm]
        self.Dimension = "2D" # Dimension of the RVE (2D or 3D)
        self.SpatialResolution = None # Spatial resolution of the RVE in [mm]

        # Content
        # Aggregates
        self.VectAgg = None # Vector of the contained aggregates in the RVE

        # Mortar
        self.VectMortar = None # Vector of the contained mortar in the RVE

        # Properties


    # CemMat
    @property
    def getCemMat(self):
        """Getter for the Concrete object to generate the RVE from."""
        return self.CemMat

    @getCemMat.setter
    def getCemMat(self, CemMat):
        """Setter for the Concrete object to generate the RVE from."""
        self.CemMat = CemMat

    # Geometry
    @property
    def getGeometry(self):
        """Getter for the geometry of the RVE in [mm]."""
        return self.Geometry

    @getGeometry.setter
    def getGeometry(self, Geometry):
        """Setter for the geometry of the RVE in [mm]."""
        self.Geometry = Geometry

    @property
    def getDimension(self):
        """Getter for the dimension of the RVE (2D or 3D)."""
        return self.Dimension

    @getDimension.setter
    def getDimension(self, Dimension):
        """Setter for the dimension of the RVE (2D or 3D)."""
        if Dimension in ["2D", "3D"]:
            self.Dimension = Dimension
        else:
            raise ValueError("Error: Dimension must be either '2D' or '3D'.")

    @property
    def getSpatialResolution(self):
        """Getter for the spatial resolution of the RVE in [mm]."""
        return self.SpatialResolution

    @getSpatialResolution.setter
    def getSpatialResolution(self, SpatialResolution):
        """Setter for the spatial resolution of the RVE in [mm]."""
        self.SpatialResolution = SpatialResolution

    # Content
    # Aggregates
    @property
    def getVectAgg(self):
        """Getter for the vector of the contained aggregates in the RVE."""
        return self.VectAgg

    @getVectAgg.setter
    def getVectAgg(self, VectAgg):
        """Setter for the vector of the contained aggregates in the RVE."""
        self.VectAgg = VectAgg

    # Mortar
    @property
    def getVectMortar(self):
        """Getter for the vector of the contained mortar in the RVE."""
        return self.VectMortar

    @getVectMortar.setter
    def getVectMortar(self, VectMortar):
        """Setter for the vector of the contained mortar in the RVE."""
        self.VectMortar = VectMortar





