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
from PlotLib import ParamPLT, StartPlots, CloseALLPlots, PLTShow, PLTPie

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
        StartPlots()

        Val = [10.156, 10.156, 10.156]
        LLegends= ['Rouge', 'Vert', 'Bleu']
        LColors= ['r', 'g', 'b']
        # Une couleur par élément de la composition et ensuite des variantes de couleurs

        paramPLT = ParamPLT(colour=LColors, linetype=0, marker=0, linesize=2, fontsize=15)
        paramPLT.getLegends = LLegends
        paramPLT.getTitle = 'Composition du '+self.Name

        PLTPie(Val, paramPLT, TypeAutopct=1, PrecisionPct=0, AbsUnit="kg/m^3", PrecisionAbs=1, 
               Radius=1, StartAngle=0, LabelDist=1.25, PctDist=0.6, BShadow=False, explode=None, 
               EnableAnnotations=True)

        PLTShow(paramPLT)



"""
Ingredients : Genrals ingredients for cementious materials
"""
class Ingredients:
    def __init__(self, Name, MatType, Color=False):
        self.Name = Name
        self.MatType = MatType
        self.Color = Color # Bleu pour l'eau, gris pour le ciment, des variantes de marron pour les agrégats, des variantes de vert pour les adjuvants


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