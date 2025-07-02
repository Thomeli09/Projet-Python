# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:20:09 2024

@author: Thommes Eliott
"""

# Lagamine library for data management  

# Other Lib
from ast import Index
from typing import Counter
import numpy as np
import pandas as pd
from pathlib import Path

# Custom Lib


"""
DataLag

# Improvement to be done:
- Ability to load multiple files at the same time
- Ability to merge the data of different files
- Ability to read DAE files from Yokogawa software
- Ability to read Excel files
"""
class DataLag:
    def __init__(self):
        # File
        self.FileName = None
        self.ApprovedFiles = ['ipe', 'IPE', 'ipn', 'IPN', '.csv', '.txt', '.f71', '.F71']

        # Data
        self.Data = None
        self.DataMatrix = None

        # Data Analysis and Visualization
        self.AbsCol = None
        self.OrdCol = None
        self.TimeCol = None
        self.SelectCol = None

        self.AbsVal = None
        self.OrdVal = None
        self.TimeVal = None

        self.PLTIndex = None
        self.PLTDataMatrix = None

        self.TimeStepArray = None

    # File
    @property
    def getFileName(self):
        return self.FileName

    @getFileName.setter
    def getFileName(self, value):
        self.FileName = value

    @property
    def getApprovedFiles(self):
        return self.ApprovedFiles

    @property
    def BoolApprovedFiles(self):
        """Returns True if the filename is in the approved list, otherwise False."""
        if self.FileName is not None:
            return any(self.getFileName.endswith(ext) for ext in self.getApprovedFiles)
        return False
    
    # Data
    @property
    def getData(self):
        return self.Data

    @getData.setter
    def getData(self, value):
        self.Data = value

    @property
    def getDataMatrix(self):
        return self.DataMatrix

    @getDataMatrix.setter
    def getDataMatrix(self, Matrix):
        self.DataMatrix = Matrix

    @property
    def getNRow(self):
        """
        Returns the number of rows in the data matrix.
        """
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return None
        print("Number of rows: [ 0 ;", self.getDataMatrix.shape[0], "]")

        return self.getDataMatrix.shape[0]

    @property
    def getNRowSimpli(self):
        """
        Returns the number of rows in the data matrix. Simplified version, without print
        """
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return None

        return self.getDataMatrix.shape[0]

    @property
    def getNCol(self):
        """
        Returns the number of columns in the data matrix.
        """
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return None
        print("Number of columns: [ 0 ;", self.getDataMatrix.shape[1], "]")

        return self.getDataMatrix.shape[1]

    @property
    def getNColSimpli(self):
        """
        Returns the number of columns in the data matrix. Simplified version, without print
        """
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return None

        return self.getDataMatrix.shape[1]

    @property
    def getNStep(self):
        """
        Returns the number of time steps in the data matrix.
        """
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return None

        if self.getTimeCol is None:
            print("Error: No time column selected.")
            return None

        # Extract the time steps
        if self.getTimeStepArray is None:
            TimeStepArray = self.SetTimeStepArray
        else:
            TimeStepArray = self.getTimeStepArray

        # Count the number of time steps
        NStep = len(TimeStepArray)

        print("Number of time steps: [ 0 ;", NStep, "]")
        return NStep

    @property
    def getNStepSimpli(self):
        """
        Returns the number of time steps in the data matrix. Simplified version, without print
        """
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return None

        if self.getTimeCol is None:
            print("Error: No time column selected.")
            return None

        # Extract the time steps
        if self.getTimeStepArray is None:
            TimeStepArray = self.SetTimeStepArray
        else:
            TimeStepArray = self.getTimeStepArray

        # Count the number of time steps
        NStep = len(TimeStepArray)

        return NStep


    # Data Analysis and Visualization
    @property
    def getAbsCol(self):
        return self.AbsCol

    @getAbsCol.setter
    def getAbsCol(self, value):
        self.AbsCol = value

    @property
    def getOrdCol(self):
        return self.OrdCol

    @getOrdCol.setter
    def getOrdCol(self, value):
        self.OrdCol = value

    @property
    def getTimeCol(self):
        return self.TimeCol

    @getTimeCol.setter
    def getTimeCol(self, value):
        self.TimeCol = value

    @property
    def getSelectCol(self):
        return self.SelectCol

    @getSelectCol.setter
    def getSelectCol(self, value):
        self.SelectCol = value

    @property
    def getAbsVal(self):
        return self.AbsVal

    @getAbsVal.setter
    def getAbsVal(self, Array):
        self.AbsVal = Array

    @property
    def getOrdVal(self):
        return self.OrdVal

    @getOrdVal.setter
    def getOrdVal(self, Array):
        self.OrdVal = Array

    @property
    def getTimeVal(self):
        return self.TimeVal

    @getTimeVal.setter
    def getTimeVal(self, Array):
        self.TimeVal = Array

    @property
    def getPLTIndex(self):
        return self.PLTIndex

    @getPLTIndex.setter
    def getPLTIndex(self, Array):
        self.PLTIndex = Array

    @property
    def getPLTDataMatrix(self):
        return self.PLTDataMatrix

    @getPLTDataMatrix.setter
    def getPLTDataMatrix(self, Matrix):
        self.PLTDataMatrix = Matrix

    @property
    def ResetPLTIndex(self):
        """ Resets the index selection array."""
        self.PLTIndex = np.arange(self.getNRowSimpli)
        self.getPLTDataMatrix = self.getDataMatrix

    @property
    def getTimeStepArray(self):
        return self.TimeStepArray

    @getTimeStepArray.setter
    def getTimeStepArray(self, Array):
        self.TimeStepArray = Array

    @property
    def SetTimeStepArray(self):
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return False

        if self.getTimeCol is None:
            print("Error: No time column selected.")
            return False

        # Extract the time values
        TimeVal = self.getDataMatrix[:, self.getTimeCol]

        # Extract the unique time steps
        self.getTimeStepArray = np.unique(TimeVal)
        return self.getTimeStepArray

    """
    # Methods
    """
    # File loading
    def LoadFile(self, BLoadMatrix=False):
        """
        Reads the file and extracts numerical data, keeping row structure intact.
        """
        if not self.BoolApprovedFiles:
            print("Error: File format not approved.")
            return None

        # Handling CSV and TXT files
        if self.FileName.endswith(('.csv', '.txt')):
            try:
                self.getData = pd.read_csv(self.FileName, delim_whitespace=True, header=None).values

                if BLoadMatrix:
                    self.LoadDataMatrix()
                return self.getData

            except Exception as e:
                print(f"Error reading file {self.FileName}: {e}")
                return None

        # Handling IPE and IPN files
        elif self.FileName.endswith(('ipe', 'IPE', 'ipn', 'IPN')):
            try:
                with open(self.FileName, 'r') as file:
                    lines = file.readlines()

                # Detect where numeric data starts and store rows properly
                DataRows = []
                for line in lines:
                    try:
                        DataRows.append([float(Num) for Num in line.split()])
                    except ValueError:
                        continue  # Skip non-numeric lines

                self.getData = DataRows

                if BLoadMatrix:
                    self.LoadDataMatrix()
                return self.getData

            except Exception as e:
                print(f"Error reading file {self.FileName}: {e}")
                return None

        # Handling f71 and F71 files
        elif self.FileName.endswith(('.f71', '.F71')):
            try:
                with open(self.FileName, 'r') as file:
                    lines = file.readlines()

                DataRows = []
                CurrentGroup = []
                Capturing = False # Flag to indicate if we are capturing data (Initially not capturing data)
                for line in lines:
                    line = line.strip() # Remove leading/trailing whitespace
                    if not line: 
                        continue  # Skip empty lines
                    try:
                        # Attempt to parse floats from line
                        Values = [float(Val) for Val in line.split()]
                        if not Capturing: # If have finished loading data then create a new current group
                            CurrentGroup = []
                            Capturing = True
                        CurrentGroup.extend(Values) # Add the values to the current group
                    except ValueError:
                        # Line is not numeric
                        if Capturing: # If we are capturing data and encouter a new group
                            if CurrentGroup:
                                DataRows.append(CurrentGroup)
                                CurrentGroup = []
                            Capturing = False
                        # If there are data after the non-numeric line, we need to add them to the current group. If not, we can skip the line.
                        # Try to extract any numeric values from the non-numeric line
                        Values = []
                        for val in line.split():
                            try:
                                Values.append(float(val))
                            except ValueError:
                                continue
                        if Values:
                            if not Capturing: # If have finished loading data then create a new current group
                                CurrentGroup = []
                                Capturing = True
                            CurrentGroup.extend(Values)
                # Append last group if still capturing
                if CurrentGroup:
                    DataRows.append(CurrentGroup)          

                self.getData = DataRows

                if BLoadMatrix:
                    self.LoadDataMatrix()
                return self.getData

            except Exception as e:
                print(f"Error reading Fortran file {self.FileName}: {e}")
                return None

  
    def LoadDataMatrix(self):
        """
        Returns the extracted data as a NumPy matrix.
        """
        if self.getData is None:
            print("Error: No data to convert.")
            return False

        self.getDataMatrix = np.array(self.getData)
        return self.getDataMatrix

    # Data Analysis and Visualization
    def SelectIndex(self, Col=None, Val=None, Tol=0.001, AbsTol=None, ValMin=None, ValMax=None, BClosest=False):
        """
        Selects rows based on the values in a column and updates the index selection array.

        Args:
            Col (int): Column index to select by.
            Val (float): Value to select.
            Tol (float): Tolerance for selection.
            AbsTol (float): Absolute tolerance for selection.
            ValMin (float): Minimum value for selection.
            ValMax (float): Maximum value for selection.
            BClosest (bool): If True, selects the closest value to val value instead of exact match.
        
        Improvements:
        - Add the possibility to extract the values directly from the pltDataMatrix
        """
        # Verify that the data matrix is not empty
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return False

        # Select the column to select by
        if Col is None:
            if self.getSelectCol is None:
                print("Error: No column selected.")
                return False
            Col = self.getSelectCol

        # Extract the values of the selected column inside the data matrix
        ArrayExtractedVal = self.getDataMatrix[:, Col]

        # Select rows based on the values in the column
        if Val is not None and BClosest is False:
            # Get the accepted tolerance
            if AbsTol is None:
                AbsTol = np.abs(Tol*Val)

            # Get the indexes of the values that are within the tolerance to the given value
            NewPLTIndex = np.where(np.abs(ArrayExtractedVal - Val) <= AbsTol)[0]

        elif ValMin is not None and ValMax is not None:
            # Select the values in the range [ValMin, ValMax]
            NewPLTIndex = np.where((ArrayExtractedVal >= ValMin) & (ArrayExtractedVal <= ValMax))[0]

        elif BClosest:
            # Find the index of the closest value to the given value
            IndexClosestVal = np.argmin(np.abs(ArrayExtractedVal - Val))

            # Get the first closest value to the given value and will be used to select the values within the tolerance
            ValClosest = ArrayExtractedVal[IndexClosestVal]

            # Get the accepted tolerance
            if AbsTol is None:
                AbsTol = np.abs(Tol*ValClosest)

            # Get the indexes of the values that are within the tolerance to the closest value (Close enough to the given value)
            NewPLTIndex = np.where(np.abs(ArrayExtractedVal - ValClosest) <= AbsTol)[0]

        else:
            print("Error: No value or range selected.")
            return False

        # Update the index selection array
        if self.getPLTIndex is not None and NewPLTIndex is not None:
            self.getPLTIndex = np.intersect1d(self.getPLTIndex, NewPLTIndex)
        else:
            self.getPLTIndex = NewPLTIndex

        # Verifies that the selection is not empty
        if len(self.getPLTIndex) == 0:
            print("Warning: No data selected.")

        # Update the PLTDataMatrix
        if self.getPLTDataMatrix is not None:
            self.getPLTDataMatrix = self.getDataMatrix[self.getPLTIndex, :]
        else:
            self.getPLTDataMatrix = self.getDataMatrix[self.getPLTIndex, :]

    def SelectTime(self, Val=None, Tol=0, AbsTol=None, ValMin=None, ValMax=None, BClosest=False):
        self.SelectIndex(Col=self.getTimeCol,
                         Val=Val, Tol=Tol, AbsTol=AbsTol,
                         ValMin=ValMin, ValMax=ValMax, BClosest=BClosest)

    def SelectAbs(self, Val=None, Tol=0, AbsTol=None, ValMin=None, ValMax=None, BClosest=False):
        self.SelectIndex(Col=self.getAbsCol,
                         Val=Val, Tol=Tol, AbsTol=AbsTol,
                         ValMin=ValMin, ValMax=ValMax, BClosest=BClosest)

    def SelectOrd(self, Val=None, Tol=0, AbsTol=None, ValMin=None, ValMax=None, BClosest=False):
        self.SelectIndex(Col=self.getOrdCol,
                         Val=Val, Tol=Tol, AbsTol=AbsTol,
                         ValMin=ValMin, ValMax=ValMax, BClosest=BClosest)

    def SelectIndexNoDuplicate(self, Col=None, Tol=0.001, AbsTol=None, ValPolicy=0):
        """
        From the selected index, select the unique values in the given column.

        Args:
            Col (int): Column index to select by.
            Tol (float): Tolerance for selection.
            AbsTol (float): Absolute tolerance for selection.
            ValPolicy (int): Policy for selecting the value to keep in case of duplicates. (-1: last, 0: first, x: x+1th value)
        
        Improvements:
        - Add the possibility to extract the values directly from the pltDataMatrix
        """
        # Verify that the data matrix is not empty
        if self.getDataMatrix is None:
            print("Error: No data matrix.")
            return False

        # Select the column to select by
        if Col is None:
            if self.getSelectCol is None:
                print("Error: No column selected.")
                return False
            Col = self.getSelectCol

        # Extract the values of the selected column inside the data matrix
        ArrayExtractedVal = self.getDataMatrix[:, Col]

        # In case AbsTol is None, the tolerance is set based on the relative tolerance
        if AbsTol is None:
            BRelTol = True
        else:
            BRelTol = False

        # Sort the values and keep the indices
        SortedIndices = np.argsort(ArrayExtractedVal)
        SortedArrayExtractedVal = ArrayExtractedVal[SortedIndices]

        # Append a dummy value to trigger final group processing
        if BRelTol:
            DummyVal = SortedArrayExtractedVal[-1] + 10 * np.abs(Tol * (SortedArrayExtractedVal[-1] + 1))
        else:
            DummyVal = SortedArrayExtractedVal[-1] + 10 * AbsTol

        SortedArrayExtractedVal = np.append(SortedArrayExtractedVal, DummyVal)
        SortedIndices = np.append(SortedIndices, -1) # dummy index to match length

        NewPLTIndex = []  # Index kept for the unique values
        TempIndexList = []  # List to keep temporarily the indices of the duplicates
        Counter = 0  # Counter for duplicates

        for i in range(len(SortedArrayExtractedVal) - 1):
            CurrentVal = SortedArrayExtractedVal[i]
            NextVal = SortedArrayExtractedVal[i + 1]

            # Get the accepted absolute tolerance if not given. Based on the relative tolerance
            if BRelTol:
                AbsTol = np.abs(Tol * CurrentVal)

            # Check if the difference between the current and previous value is greater than the absolute tolerance
            if np.abs(NextVal - CurrentVal) > AbsTol:
                # The value is unique
                if Counter == 0:
                    # If the value is unique, keep it
                    NewPLTIndex.append(SortedIndices[i])
                else:
                    # If there are duplicates values

                    # Add the last index of the duplicates in the temporary list
                    TempIndexList.append(SortedIndices[i])

                    # Choose the index to be kept
                    KeptSubIndex = ValPolicy

                    if KeptSubIndex >= len(TempIndexList):
                        # If the number of duplicates is less than the value to keep, take the last one
                        KeptSubIndex = -1
                    elif KeptSubIndex < -1:
                        # If the value to keep is negative, take the last one
                        KeptSubIndex = -1

                    if TempIndexList[KeptSubIndex] != -1:
                        NewPLTIndex.append(TempIndexList[KeptSubIndex])

                # Reset the list of temporary indexess
                TempIndexList = []
                # Reset the counter
                Counter = 0

            else:
                # The value is not unique and needs to be kept to check after wich one to choose
                TempIndexList.append(SortedIndices[i])  # Keep the index of the duplicate value
                # Update the counter
                Counter += 1

        # Sort the index of the kept values by resorting the original array
        NewPLTIndex = np.array(NewPLTIndex)
        NewPLTIndex = np.sort(NewPLTIndex)

        # Update the index selection array
        if self.getPLTIndex is not None and NewPLTIndex is not None:
            self.getPLTIndex = np.intersect1d(self.getPLTIndex, NewPLTIndex)
        else:
            self.getPLTIndex = NewPLTIndex

        # Verifies that the selection is not empty
        if len(self.getPLTIndex) == 0:
            print("Warning: No data selected.")

        # Update the PLTDataMatrix
        if self.getPLTDataMatrix is not None:
            self.getPLTDataMatrix = self.getDataMatrix[self.getPLTIndex, :]
        else:
            self.getPLTDataMatrix = self.getDataMatrix[self.getPLTIndex, :]

    def SortResults(self, Col=None):
        """
        Sorts the differents values by a given column.

        Improvements:
        - Add the possibility to extract the values directly from the pltDataMatrix
        """
        # Verify that the index selection array is not empty
        if self.getPLTIndex is None:
            print("Error: No index selected.")
            return False

        # Select the column to sort by
        if Col is None:
            if self.getSelectCol is None:
                print("Error: No column selected.")
                return False
            Col = self.getSelectCol

        # Sort the data
        # Extract the values to sort by
        ArrayExtratedVal = self.getDataMatrix[self.getPLTIndex, Col]

        # Sort the PLTIndex array by the values in the selected column
        IndexOrder = np.argsort(ArrayExtratedVal)
        self.getPLTIndex = self.getPLTIndex[IndexOrder]

        # Sort the PLTDataMatrix
        if self.getPLTDataMatrix is not None:
            self.getPLTDataMatrix = self.getDataMatrix[IndexOrder, :]
        else:
            self.getPLTDataMatrix = self.getDataMatrix[IndexOrder, :]

    def PLTPreprocessing(self):
        """
        Preprocesses data for plotting by putting them into the right variables.
        """
        # Verify that the index selection array is not empty
        if self.getPLTIndex is None:
            print("Warning: No index selected. Resetting the index.")
            self.ResetPLTIndex

        if self.getAbsCol is None:
            print("Error: No abscissa column selected.")
            return False

        if self.getOrdCol is None:
            print("Error: No ordinate column selected.")
            return False

        # Extract the data to plot
        # Extract the abscissa
        self.getAbsVal = self.getDataMatrix[self.getPLTIndex, self.getAbsCol]

        # Extract the ordinate
        self.getOrdVal = self.getDataMatrix[self.getPLTIndex, self.getOrdCol]

        # Extract the time
        if self.getTimeCol is not None:
            self.getTimeVal = self.getDataMatrix[self.getPLTIndex, self.getTimeCol]
        else:
            self.getTimeVal = None
            print("Warning: No time column selected.")

def TimeStep2Time(self):
    pass
    # permet de faire la traduction de time step ? un temps

    # S'aider de la colonne de unique time step

def Time2TimeStep(self):
    pass
    # permet de faire la traduction de temps ? un time step

    # S'aider de la colonne de unique time step

"""
-Improvement to be done:
- Add the possibility to extract the values directly from the pltDataMatrix
- Add the capability to use the data of different files at the same time
    - Add the ability to merge the data of different files
"""
# Fonction import de donn?
# Fonction de traitement des donn?es
# Fonction d'affichage
# Fonction d'export de donn?e

