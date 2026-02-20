# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:21:57 2025

@author: Thommes Eliott
"""

# CemMat RVE Generation
"""
Improovements :
- 
"""

# Other Lib


# Custom Lib
from ConcreteLib import CemMat
from ConcreteRVELib import RVE

class RVEGeneration:
    def __init__(self):
        # CemMat
        self.CemMat = None # CemMat object to generate the RVE from

        # RVE Object
        self.RVE = None # RVE object to generate

    # Concrete
    @property
    def getCemMat(self):
        """Getter for the Concrete object to generate the RVE from."""
        return self.CemMat

    @getCemMat.setter
    def getCemMat(self, CemMat):
        """Setter for the Concrete object to generate the RVE from."""
        self.CemMat = CemMat
        
    # RVE
    @property
    def getRVE(self):
        """Getter for the RVE object to generate."""
        return self.RVE

    @getRVE.setter
    def getRVE(self, RVE):
        """Setter for the RVE object to generate."""
        self.RVE = RVE

    # CMPT RVE Generation
    def CMPTRVEGeneration(self):
        """
        Computation of the RVE from the Concrete object using the CMPTRVEGeneration method.
        """
        pass



