# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:20:09 2024

@author: Thommes Eliott
"""

# Lagamine library for data management  

# Other Lib
from webbrowser import get
import numpy as np
import pandas as pd
from pathlib import Path

# Custom Lib


"""
DataLag
"""
class DataLag:
    def __init__(self):
        # File
        self.FileName = None
        self.ApprovedFiles = ['ipe', 'IPE', 'ipn', 'IPN', '.csv', '.txt']

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

        self.PLTDataMatrix = None
        self.PLTIndex = None

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
        return self.getDataMatrix.shape[0]

    @property
    def getNCol(self):
        return self.getDataMatrix.shape[1]

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
    def getPLTDataMatrix(self):
        return self.PLTDataMatrix

    @getPLTDataMatrix.setter
    def getPLTDataMatrix(self, Matrix):
        self.PLTDataMatrix = Matrix

    @property
    def getPLTIndex(self):
        return self.PLTIndex

    @getPLTIndex.setter
    def getPLTIndex(self, Array):
        self.PLTIndex = Array

    @property
    def ResetPLTIndex(self):
        """ Resets the index selection array."""
        self.PLTIndex = np.arange(self.getNRow)

    # to be done

    # Methods
    # File loading
    def LoadFile(self):
        """Reads the file and extracts numerical data, keeping row structure intact."""
        if not self.BoolApprovedFiles:
            print("Error: File format not approved.")
            return None

        # Handling CSV and TXT files
        if self.FileName.endswith(('.csv', '.txt')):
            try:
                self.getData = pd.read_csv(self.FileName, delim_whitespace=True, header=None).values
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
                return self.getData
            except Exception as e:
                print(f"Error reading file {self.FileName}: {e}")
                return None
  
    def LoadDataMatrix(self):
        """Returns the extracted data as a NumPy matrix."""
        if self.getData is None:
            print("Error: No data to convert.")
            return False

        self.getDataMatrix = np.array(self.getData)
        return self.getDataMatrix

    # Data Analysis and Visualization

    def SelectIndex(self, Col=None, Val=None, ValTol=0, ValMin=None, ValMax=None):
        """Selects rows based on the values in a column and updates the index selection array."""
        # Verify that the index selection array is not empty
        if Col is None:
            if self.getSelectCol is None:
                print("Error: No column selected.")
                return False
            Col = self.getSelectCol

        # Extract the values of the selected column inside the data matrix
        ArrayExtractedVal = self.getDataMatrix[:, Col]

        # Select rows based on the values in the column
        if Val is not None:
            NewPLTIndex = np.where(np.abs(ArrayExtractedVal - Val) <= ValTol)[0]

        elif ValMin is not None and ValMax is not None:
            NewPLTIndex = np.where((ArrayExtractedVal >= ValMin) & (ArrayExtractedVal <= ValMax))[0]

        # Update the index selection array
        if self.getPLTIndex is not None and NewPLTIndex is not None:
            self.getPLTIndex = np.intersect1d(self.getPLTIndex, NewPLTIndex)
        else:
            self.getPLTIndex = NewPLTIndex

    def SelectTime(self, TimeVal=None, Tol=0, TimeMin=None, TimeMax=None):
        self.SelectIndex(Col=self.getTimeCol,
                         Val=TimeVal, ValTol=Tol,
                         ValMin=TimeMin, ValMax=TimeMax)

    def SelectAbs(self, AbsVal=None, Tol=0, AbsMin=None, AbsMax=None):
        self.SelectIndex(Col=self.getAbsCol,
                         Val=AbsVal, ValTol=Tol,
                         ValMin=AbsMin, ValMax=AbsMax)

    def SelectOrd(self, OrdVal=None, Tol=0, OrdMin=None, OrdMax=None):
        self.SelectIndex(Col=self.getOrdCol,
                         Val=OrdVal, ValTol=Tol,
                         ValMin=OrdMin, ValMax=OrdMax)

    def PLTPreprocessing(self):
        """Preprocesses data for plotting by putting them into the right variables."""
        # Verify that the index selection array is not empty
        if self.getPLTIndex is None:
            print("Error: No index selected.")
            return False

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

    def SortResults(self):
        """Sorts the differents values by a given column."""
        # Verify that the index selection array is not empty
        if self.getPLTIndex is None:
            print("Error: No index selected.")
            return False

        # Sort the data
        # Select the column to sort by
        if self.getSelectCol is None:
            print("Error: No column selected.")
            return False
        # Extract the values to sort by
        ArrayExtratedVal = self.getDataMatrix[self.getPLTIndex, self.getSelectCol]

        # Sort the PLTIndex array by the values in the selected column
        self.getPLTIndex = self.getPLTIndex[np.argsort(ArrayExtratedVal)]

# Fonction import de donné
#'Savoir donné des fichiers IPE, IPN, LAG'
#'Détecter le type de fichiers'
#'Comprendre le contenu'

# Fonction de traitement des données

# Fonction d'affichage

# Fonction d'export de donnée

