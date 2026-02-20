# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:21:57 2025

@author: Thommes Eliott
"""

# Concrete Aggregate RVE Library for 2D case
"""
Improovements :

"""

# Other Lib
import numpy as np

# Custom Lib
from MaterialLib import Material
from ConcreteRVELib import RVE

class Agg(Material):
    def __init__(self, Name, ID, MatType):
        # Initialize the material
        super().__init__(Name=Name, ID=ID, MatType=MatType)

        # Parent RVE   
        self.RVE = None

        # Shape
        self.Vertexes = None # Vector of the vertexes of the aggregate [mm]

        # Mesh
        self.Mesh = None # Mesh of the aggregate for the CMPT analysis
        
        # Inner Phase
        self.VectPhaseMesh = None # Vector of the contained mesh phases in the aggregate



         



    # Parent RVE
    @property
    def getRVE(self):
        return self.RVE

    @getRVE.setter
    def getRVE(self, RVE):
        self.RVE = RVE

    # properties
    # Shape
    @property
    def getVertexes(self):
        """Getter for the vector of the vertexes of the aggregate [mm]."""
        return self.Vertexes

    @getVertexes.setter
    def getVertexes(self, Vertexes):
        """Setter for the vector of the vertexes of the aggregate [mm]."""
        if isinstance(Vertexes, list):
            self.Vertexes = np.asarray(Vertexes, dtype=float)
        elif isinstance(Vertexes, np.ndarray):
            self.Vertexes = Vertexes.astype(float)
        else:
            raise ValueError("Error: Vertexes must be a list or a numpy array.")


    # CMPT Properties

    # Center of Mass


    # Aggregate cut
    def CMPTCutAGGFromPointPlane(self, PlanePoint, PlaneNormal):
        """
        Cut the aggregate with a plane defined by a point and a normal vector and return the cut part of the aggregate and a new aggregate with the remaining part of the aggregate.
        Args:
            PlanePoint: Point on the plane to cut the aggregate [mm]
            PlaneNormal: Normal vector of the plane to cut the aggregate [-]
        Returns:
            CutAgg: New aggregate object containing the cut part of the aggregate
            RemainAgg: New aggregate object containing the remaining part of the aggregate
        """
        # Compute the intersection point between the plane defined by the two points and the aggregate

        # Generate the new and remaining aggregates based on the intersection point and the plane defined by the two points
        pass

    def CMPTCutAGGFromPoints(self, Point1, Point2):
        """
        Cut the aggregate with a plane defined by three points and return the cut part of the aggregate and a new aggregate with the remaining part of the aggregate.
        Args:
            Point1: First point on the plane to cut the aggregate [mm]
            Point2: Second point on the plane to cut the aggregate [mm]
        Returns:
            CutAgg: New aggregate object containing the cut part of the aggregate
            RemainAgg: New aggregate object containing the remaining part of the aggregate
        """
        # Compute the intersection point between the plane defined by the two points and the aggregate

        # Generate the new and remaining aggregates based on the intersection point and the plane defined by the two points
        pass



