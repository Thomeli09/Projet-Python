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
        pass


"""
Ingredients : Genrals ingredients for cementious materials
"""
class Ingredients:
    def __init__(self, MatType):
        self.MatType = MatType
        
        self.Data = False


"""
Cement
"""
class Cement(Ingredients):
    def __init__(self, MatType):
        super().__init__(MatType)

"""
Eau
"""
class Eau(Ingredients):
    def __init__(self, MatType):
        super().__init__(MatType)

"""
Aggregat
"""
class Aggregat(Ingredients):
    def __init__(self, MatType):
        super().__init__(MatType)

"""
Adjuvant
"""
class Adjuvant(Ingredients):
    def __init__(self, MatType):
        super().__init__(MatType)