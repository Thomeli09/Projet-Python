# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:35:04 2025

@author: Thommes Eliott
"""

# Voltorb Game Solver Library

from operator import index
from queue import Empty
import matplotlib.pyplot as plt
import numpy as np


# Custom Lib
import numpy as np
import itertools

# Custom Lib
from TimeLib import Chrono
from PlotLib import ParamPLT, StartPlots, CloseALLPlots, PLTShow, DefaultParamPLT
from PlotLib import PLTUpdateLayout, PLTScreenMaximize, PLTImShow

class VoltorbGameGrid:
    def __init__(self):
        # Game parameters
        self.NRows = None
        self.NCols = None
        self.MaxVal = 3 # All values are between 0 and MaxVal included

        # Game initial data
        self.ArrayXPoints = None
        self.ArrayXVoltorbes = None
        self.ArrayYPoints = None
        self.ArrayYVoltorbes = None
        
        # Game optional data
        self.MatrixDataTiles = None # Matrix to hold the data of the tiles
        # Values below 0 are hidden tiles, values above 0 are the values of the revealed tiles

        # Computed data
        self.LPossibleGrid = []  # List to hold possible grids

        self.MatrixProb = None # Matrix to hold the probability of each tile being a 0

        self.MatrixCmptScores = None # Matrix to hold the computed scores to choose the best tile to reveal

    # Game parameters
    @property
    def getNRows(self):
        return self.NRows

    @getNRows.setter
    def getNRows(self, NRows):
        self.NRows = NRows

    @property
    def getNCols(self):
        return self.NCols

    @getNCols.setter
    def getNCols(self, NCols):
        self.NCols = NCols

    @property
    def getMaxVal(self):
        return self.MaxVal

    @getMaxVal.setter
    def getMaxVal(self, MaxVal):
        self.MaxVal = MaxVal

    # Game initial data
    @property
    def getXPoints(self):
        return self.ArrayXPoints

    @getXPoints.setter
    def getXPoints(self, ArrayVal):
        self.ArrayXPoints = ArrayVal

    @property
    def getXVoltorbes(self):
        return self.ArrayXVoltorbes

    @getXVoltorbes.setter
    def getXVoltorbes(self, ArrayVal):
        self.ArrayXVoltorbes = ArrayVal

    @property
    def getYPoints(self):
        return self.ArrayYPoints

    @getYPoints.setter
    def getYPoints(self, ArrayVal):
        self.ArrayYPoints = ArrayVal

    @property
    def getYVoltorbes(self):
        return self.ArrayYVoltorbes

    @getYVoltorbes.setter
    def getYVoltorbes(self, ArrayVal):
        self.ArrayYVoltorbes = ArrayVal
    
    # Game optional data
    @property
    def getMatrixDataTiles(self):
        if self.MatrixDataTiles is None:
            # Initialize the matrix with -1 (hidden tiles)
            self.MatrixDataTiles = np.zeros((self.getNRows, self.getNCols)) - 1
        return self.MatrixDataTiles

    @getMatrixDataTiles.setter
    def getMatrixDataTiles(self, MatrixDataTiles):
        self.MatrixDataTiles = MatrixDataTiles

    def AddTile2MatrixDataTiles(self, Val, Row, Column):
        Matrix = self.getMatrixDataTiles
        Matrix[Row, Column] = Val
        self.getMatrixDataTiles = Matrix

    # Computed data
    @property
    def getLPossibleGrid(self):
        return self.LPossibleGrid

    @getLPossibleGrid.setter
    def getLPossibleGrid(self, LPossibleGrid):
        self.LPossibleGrid = LPossibleGrid

    @property
    def getMatrixProb(self):
        if self.MatrixProb is None:
            # Initialize the matrix with 1 (100% probability of being a 0) because no data is known
            self.MatrixProb = np.zeros((self.getNRows, self.getNCols)) + 1
        return self.MatrixProb

    @getMatrixProb.setter
    def getMatrixProb(self, MatrixProb):
        self.MatrixProb = MatrixProb

    @property
    def getMatrixCmptScores(self):
        if self.MatrixCmptScores is None:
            # Initialize the matrix with 0
            self.MatrixCmptScores = np.zeros((self.getNRows, self.getNCols))
        return self.MatrixCmptScores

    @getMatrixCmptScores.setter
    def getMatrixCmptScores(self, MatrixCmptScores):
        self.MatrixCmptScores = MatrixCmptScores

    # Methods

    # Data aquisition methods

    # Computations methods
    def CmptGridsGeneration(self):
        """
        Generate all plausible matrices based on the given constraints and the current knowledge.
        Returns:
            List of plausible matrices satisfying the constraints.
        """
        Rows, Cols = self.getNRows, self.getNCols
        MaxValue = self.getMaxVal
        PlausibleMatrices = []

        # Dynamically slice the Points and Voltorbes vectors to match the current grid size
        XPointsSubset = self.getXPoints[0, :Cols].flatten()  # Take the first `Cols` elements
        YPointsSubset = self.getYPoints[0, :Rows].flatten()  # Take the first `Rows` elements
        XVoltorbesSubset = self.getXVoltorbes[0, :Cols].flatten()  # Take the first `Cols` elements
        YVoltorbesSubset = self.getYVoltorbes[0, :Rows].flatten()  # Take the first `Rows` elements

        # Verify that the sum of the points and voltorbes in X and Y vectors match
        if np.sum(YPointsSubset) != np.sum(XPointsSubset) or np.sum(YVoltorbesSubset) != np.sum(XVoltorbesSubset):
            print("Error: Different total number of points or voltorbes on the whole matrix.")
            self.getLPossibleGrid = []  # Update the possible grid list
            return []

        # Precompute valid row combinations
        def ValidRowCombinations(RowSum, Zeros, Length, MaxVal):
            """
            Generate all valid row combinations given constraints.
            """
            ValidCombinations = []
            for Comb in itertools.product(range(MaxVal + 1), repeat=Length):
                if sum(Comb) == RowSum and Comb.count(0) == Zeros:
                    ValidCombinations.append(Comb)
            return ValidCombinations

        # Generate valid rows and columns based on constraints
        ValidRows = [ValidRowCombinations(YPointsSubset[i], YVoltorbesSubset[i], Cols, MaxValue) for i in range(Rows)]

        # Recursive function to construct matrices row by row
        def ConstructMatrix(Matrix, RowIdx):
            if RowIdx == Rows:
                # Validate column constraints
                if (
                    np.all(np.sum(Matrix, axis=0) == XPointsSubset) and
                    np.all(np.sum(Matrix == 0, axis=0) == XVoltorbesSubset)
                ):
                    PlausibleMatrices.append(Matrix.copy())
                return

            for row in ValidRows[RowIdx]:
                Matrix[RowIdx, :] = row
                ConstructMatrix(Matrix, RowIdx + 1)

        # Initialize an empty matrix and start backtracking
        matrix = np.zeros((Rows, Cols), dtype=int)
        ConstructMatrix(matrix, 0)

        self.getLPossibleGrid = PlausibleMatrices  # Update the possible grid list
        return PlausibleMatrices

    def CmptElem2MatricesSelection(self, Row, Col, Val):
        """
        Update the possible matrices by assigning a specific Val to an element.

        Args:
            Row (int): The Row index of the element.
            Col (int): The Column index of the element.
            Val (int): The Val to assign to the element.

        Returns:
            None
        """
        if not (0 <= Row < self.getNRows and 0 <= Col < self.getNCols):
            print("Error: Invalid position ({Row}, {Col}). Must be within grid dimensions.")

        # Filter plausible matrices
        UpdatedMatrices = []
        for Matrix in self.getLPossibleGrid:
            if Matrix[Row, Col] == Val:
                UpdatedMatrices.append(Matrix)

        # Check if no matrices are left after the update
        if not UpdatedMatrices:
            print("Warning: No plausible matrices remain after the update. Check the input values.")
            return False

        # Update the list of plausible matrices
        self.getLPossibleGrid = UpdatedMatrices
        self.AddTile2MatrixDataTiles(Val=Val, Row=Row, Column=Col)
        return True

    def CmptProba(self):
        """
        Calculate the probability of finding a 0 at each position in the grid
        based on the list of possible grids.
        Returns:
            A 2D NumPy array representing the probability of a 0 at each grid position.
        """
        if not self.getLPossibleGrid:
            print("Error: LPossibleGrid is empty.")
            return None
        # Stack all grids into a 3D NumPy array for efficient computation
        MatricesStack = np.array(self.getLPossibleGrid)  # Shape: (num_grids, Rows, Cols)

        # Compute the probability of 0 at each position
        PMatrix = np.mean(MatricesStack == 0, axis=0)*100

        self.getMatrixProb = PMatrix

        return PMatrix

    # Display methods
    def PLTDataTiles(self, paramPLT=None):
        if paramPLT is None:
            paramPLT = DefaultParamPLT()
        if self.getMatrixDataTiles is None:
            print("Error: MatrixDataTiles is empty.")
            return
        PLTImShow(ValMatrix=self.getMatrixDataTiles, paramPLT=paramPLT, FInterpolType=2)
        return paramPLT

    def PLTProba(self, paramPLT=None):
        if paramPLT is None:
            paramPLT = DefaultParamPLT()
        PLTImShow(ValMatrix=self.getMatrixProb, paramPLT=paramPLT, FInterpolType=2)
        return paramPLT

    def PLTCmptScores(self, paramPLT=None):
        if paramPLT is None:
            paramPLT = DefaultParamPLT()
        if self.getMatrixCmptScores is None:
            print("Error: MatrixCmptScores is empty.")
        PLTImShow(ValMatrix=self.getMatrixCmptScores, paramPLT=paramPLT, FInterpolType=2)
        return paramPLT

    def PLTProbaAndTiles(self, paramPLT=None):
        if paramPLT is None:
            paramPLT = DefaultParamPLT()
        PLTUpdateLayout(1, 2)
        self.PLTProba(paramPLT=paramPLT)
        self.PLTDataTiles(paramPLT=paramPLT)
        return paramPLT

    def PLTProbaScoresTiles(self, paramPLT=None):
        if paramPLT is None:
            paramPLT = DefaultParamPLT()
        PLTUpdateLayout(1, 3)
        self.PLTProba(paramPLT=paramPLT)
        self.PLTCmptScores(paramPLT=paramPLT)
        self.PLTDataTiles(paramPLT=paramPLT)
        return paramPLT

    # Solver methods
    def VoltorbGameSolver(self, NumMethod=0):
        """
        Solve the Voltorb game using the specified method.

        Policy:
        Request the value of the reward at a given place (least probability),
        recompute the probability matrix from this knowledge, and show the new 
        probability matrix.
        """

        self.CmptGridsGeneration()

        Status = True
        i = 1
        while Status:
            # Compute probabilities
            self.CmptProba()

            # Retrieve the probability matrix
            ProbMatrix = self.getMatrixProb

            # Find the position with the least probability
            DataMatrix = self.getMatrixDataTiles
            TempProbMatrix = np.where(DataMatrix != 0, np.inf, ProbMatrix)
            row, col = np.unravel_index(np.argmin(TempProbMatrix), TempProbMatrix.shape)

            # Display the current state
            print(f"Step {i}:")
            print(f"Number of plausible matrices: {len(self.getLPossibleGrid)}")
            print("Probability matrix (likelihood of 0 in each position):")
            print(TempProbMatrix)
            print(f"Querying value at position ({row+1}, {col+1})")
            # Ask for the value at the selected position
            value = int(input())

            if value == 0 or value is False:
                Status = False
                print("Info: Terminating solver as value is 0 or False.")
            elif len(self.getLPossibleGrid) == 1:  # Assuming checkCompletion verifies if the task is finished
                Status = False
                print("Info: Solver completed successfully (only one possibility).")
            else:
                # Update the plausible matrices with the new knowledge
                Success = self.CmptElem2MatricesSelection(row, col, value)
                if not Success:
                    Status = True
                    print("Error: Wrong value")

            # Increment the step counter
            i += 1





