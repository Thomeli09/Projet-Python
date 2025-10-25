# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:43:03 2025

@author: Thommes Eliott
"""

# Material library


# Other Lib


# Custom Lib


"""
Material : Default class for all the material data
"""
class Material:
    def __init__(self, Name, ID, Type):
        # Metadata
        self.Name = Name
        self.ID = ID
        self.Type = Type

        # Graphics
        self.Color = None
        self.Hatch = None

        # Batch Information
        self.LBatches = []
        
        # Properties
        

        # Mechanical Properties
        self.CompStrengthCK = None  # Compressive Strength Characteristic
        self.TensStrengthCK = None  # Tensile Strength Characteristic

        # Experiments
        self.LExperiments = []

    # Metadata
    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getID(self):
        return self.ID

    @getID.setter
    def getID(self, ID):
        self.ID = ID

    @property
    def getType(self):
        return self.Type

    @getType.setter
    def getType(self, Type):
        self.Type = Type

    # Graphics
    @property
    def getColor(self):
        return self.Color

    @getColor.setter
    def getColor(self, Color):
        self.Color = Color

    # Batch Information
    @property
    def getLBatches(self):
        return self.LBatches

    @getLBatches.setter
    def getLBatches(self, Batch):
        self.LBatches.append(Batch)
        Batch.AddMaterial = self

    def AddBatch(self, Batch):
        self.LBatches.append(Batch)

    # Properties

    # Mechanical Properties
    @property
    def getCompStrengthCK(self):
        return self.CompStrengthCK

    @getCompStrengthCK.setter
    def getCompStrengthCK(self, CompStrengthCK):
        self.CompStrengthCK = CompStrengthCK

    @property
    def getTensStrengthCK(self):
        return self.TensStrengthCK

    @getTensStrengthCK.setter
    def getTensStrengthCK(self, TensStrengthCK):
        self.TensStrengthCK = TensStrengthCK

    # Experiments
    @property
    def getExperiments(self):
        return self.LExperiments

    @getExperiments.setter
    def getExperiments(self, Experiment):
        self.LExperiments.append(Experiment)
