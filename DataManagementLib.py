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



