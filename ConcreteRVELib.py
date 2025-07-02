# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:21:57 2025

@author: Thommes Eliott
"""

# Concrete RVE Library



# Custom Lib


class RVE:
    def __init__(self):
        # Temp
        self.NRows = False

    # 
    @property
    def getNRows(self):
        return self.NRows

    @getNRows.setter
    def getNRows(self, NRows):
        self.NRows = NRows