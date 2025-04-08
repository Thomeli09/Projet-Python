# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:39:19 2025

@author: Thommes Eliott
"""

# Data management function Library

# Other Lib
import numpy as np

# Custom Lib


def LenData(Data):
    """
    Count the number of elements in a given data structure.

    Parameters:
        data: tuple, list, numpy.ndarray, set, dict, or other iterable types
            The input data structure.

    Returns:
        int: Number of elements in the data structure.

    Raises:
        TypeError: If the data type is not supported.
    """
    if isinstance(Data, (tuple, list, set)):
        # For tuple, list, or set, simply return the length
        return len(Data)
    elif isinstance(Data, dict):
        # For dict, count the number of keys
        return len(Data.keys())
    elif isinstance(Data, np.ndarray):
        # For NumPy arrays, handle both row and column vectors
        if Data.ndim == 1:
            return Data.size
        elif Data.ndim == 2:
            # Row vector: shape (1, n), Column vector: shape (n, 1)
            if 1 in Data.shape:
                return Data.size
            else:
                print("Error: Data should not be a matrix.")
        else:
            print("Error: Data should not be a matrix.")
    elif hasattr(Data, '__len__'):
        # For other iterable types, try using len
        return len(Data)
    else:
        print(f"Error: Unsupported data type: {type(Data)}")
    return 0


# List management functions
def ListSort(L1, L2=False):
    """
    Sort a list of numbers or pairs of values based on the first list.
    """
    if not L2:  # Sorting a list of numbers
        L1 = sorted(L1)
        return L1
    else:  # Sorting pairs of values based on the first list
        if LenData(L1)==LenData(L2):
            L1, L2 = zip(*sorted(zip(L1, L2)))
            return L1, L2
        else:
            print("Error: The two lists should have the same length.")

def ListFindFirstMaxPair(L1, L2):
    """
    Finds the first occurrence of the maximum value in list1 
    and returns the paired value from list2.
    
    Parameters:
        L1 (list): The list to find the max value in.
        L2 (list): The paired list to retrieve the corresponding value.

    Returns:
        tuple: (max_value, paired_value) or None if lists are empty or mismatched.
    """
    if not L1 or not L2 or not isinstance(L1,list) or not isinstance(L1,list) or len(L1) != len(L2):
        print("Error: There is not 2 lists ot the two lists should have the same length.")
        return None

    MaxIndex = L1.index(max(L1))  # Find the index of the first max value
    return L1[MaxIndex], L2[MaxIndex]  # Return (max_value, paired_value)


def ListMult(Val, ListVal, BPrint=True):
    """
    Multiply a list of values by a constant value.
    """
    MultListVal = [Val*i for i in ListVal]
    if BPrint:
        print("Multiplication of list by value:", MultListVal)
    return MultListVal


def ListSum(ListOfSumList, BPrint=True):
    """
    Sum a list of lists of values.
    """
    SumListVal = [sum(x) for x in zip(*ListOfSumList)]
    if BPrint:
        print("Sum of lists:", SumListVal)
    return SumListVal

# Text management functions

# Vector management functions
def VectorSelectVal(Vector, Val, AbsTol=1e-6, BFirst=False):
    """
    Select values in a numpy array that are equal to a given value within a tolerance and return the indices.
    If BFirst is True, return the first occurrence only.
    """
    IndexVect = np.where(np.isclose(Vector, Val, atol=AbsTol))[0]
    SelectedVal = Vector[IndexVect]

    if BFirst:
        if IndexVect.size == 0:
            print("Error: Value not found.")
            return None, None
        IndexVect = IndexVect[0]
        SelectedVal = SelectedVal[0]

    return SelectedVal, IndexVect

def VectorSelectClosestVal(Vector, Val, BFirst=False):
    """
    Select values in a numpy array that are the closest to a given value and return the indices.
    If BFirst is True, return the first occurrence only.
    """
    IndexVect = np.argmin(np.abs(Vector - Val))
    SelectedVal = Vector[IndexVect]

    if IndexVect.size == 0:
        print("Error: Value not found.")

    return SelectedVal, IndexVect

# Matrix management functions
def MatrixSelectRowOrColumn(Matrix, Index, Axis=0):
    """
    Select a row or column from a 2D numpy array.
    """
    # Check if the index is within the matrix dimensions
    if Axis == 0 and (Index >= Matrix.shape[0] or Index < 0):
        print("Error: Row index out of bounds.")
        return None
    elif Axis == 1 and (Index >= Matrix.shape[1] or Index < 0):
        print("Error: Column index out of bounds.")
        return None

    # Select the row or column
    if Axis == 0:  # Selecting a row
        return Matrix[Index, :]
    elif Axis == 1:  # Selecting a column
        return Matrix[:, Index]
    else:
        print("Error: Axis should be 0 or 1.")
        return None
