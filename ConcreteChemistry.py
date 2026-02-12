# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 11:24:54 2026

@author: Thommes Eliott
"""

# Concrete chemistry library


# Other
import re
from ConcreteLib import CemMat


# Custom Lib
from ExperimentLib import Experiment


"""
ChemExp : Chemical experiment object
"""
class ChemExp(Experiment):
    def __init__(self, Name, ID, ExpType):
        super().__init__(Name, ID, ExpType)

"""
ChemModel : Chemical model object for concrete chemistry
"""
class ChemModel(Experiment):
    def __init__(self, Name, ID, ModelType):
        super().__init__(Name, ID, ModelType)


# Methods
def CMPTUltHydration(Concrete: CemMat):
    """
    Compute the ultimate hydration degree of a cement at a given time
    Args:
    - Concrete (CemMat): Cementious material object

    Returns:
    - Ultimate hydration degree (float)
    """
    ECRatio = Concrete.getMWater / Concrete.getMCement
    AlphaHydrationUltimate = (1.031 * ECRatio) / (0.194 + ECRatio)

    return AlphaHydrationUltimate