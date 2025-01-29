# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:39:19 2025

@author: Thommes Eliott
"""

# Check function Library

# Other Lib


# Custom Lib
import numpy as np

def count_elements(data):
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
    if isinstance(data, (tuple, list, set)):
        # For tuple, list, or set, simply return the length
        return len(data)
    elif isinstance(data, dict):
        # For dict, count the number of keys
        return len(data.keys())
    elif isinstance(data, np.ndarray):
        # For NumPy arrays, handle both row and column vectors
        if data.ndim == 1:
            return data.size
        elif data.ndim == 2:
            # Row vector: shape (1, n), Column vector: shape (n, 1)
            if 1 in data.shape:
                return data.size
            else:
                print("The array is not a row or column vector.")
        else:
            print("The array has more than 2 dimensions.")
    elif hasattr(data, '__len__'):
        # For other iterable types, try using len
        return len(data)
    else:
        print(f"Unsupported data type: {type(data)}")

# Example usage:
if __name__ == "__main__":
    # Examples with different data structures
    tuple_example = (1, 2, 3)
    list_example = [1, 2, 3, 4, 5]
    array_example = np.array([[1, 2, 3], [4, 5, 6]])
    row_vector = np.array([[1, 2, 3]])  # 1x3 row vector
    column_vector = np.array([[1], [2], [3]])  # 3x1 column vector
    set_example = {1, 2, 3}
    dict_example = {'a': 1, 'b': 2, 'c': 3}

    print("Tuple count:", count_elements(tuple_example))
    print("List count:", count_elements(list_example))
    print("Array count:", count_elements(array_example))
    print("Row vector count:", count_elements(row_vector))
    print("Column vector count:", count_elements(column_vector))
    print("Set count:", count_elements(set_example))
    print("Dict count:", count_elements(dict_example))

