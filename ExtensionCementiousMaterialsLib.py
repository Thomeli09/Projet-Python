# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:17:57 2025

@author: Thommes Eliott
"""

# Experiment extension to cementious materials library

# Other Lib
import pandas as pd
import numpy as np
from ExperimentLib import Composition

# Custom Lib

"""
CemMaterials : Cementious materials objects
"""
class CemMaterials(Composition):
    def __init__(self, Val, Name, ProductionDate, Experiments):
        super().__init__(Name=Name, ProductionDate=ProductionDate,
                         Experiments=Experiments)

    def CmptComposition(self):
        pass

    def PLTComposition(self):
        # Plot a pie chart with the composition
        PLTPie(Val, paramPLT, Radius=1, explode=None, TypeAutopct=0, LabelDist=1.25, PctDist=0.6, BShadow=False, StartAngle=0, 
           BShowAbs=False, AbsUnit="", PrecisionPct=1, PrecisionAbs=0, AnnotateTextSize=10, EnableAnnotations=False)
        pass


"""
Ingredients : Genrals ingredients for cementious materials
"""
class Ingredients:
    def __init__(self, Name, MatType):
        self.Name = Name
        self.MatType = MatType

        



"""
Cement
"""
class Cement(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Cement")


"""
Eau
"""
class Eau(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Cement")

"""
Aggregat
"""
class Aggregat(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Aggregat")

"""
Adjuvant
"""
class Adjuvant(Ingredients):
    def __init__(self, Name):
        super().__init__(Name=Name, MatType="Adjuvant")