#  numpy is a faster alternative to lists which provides more functions for numpy lists

import numpy as np  # imports numpy

a = np.array([1, 2, 3], dtype='int16')  # creates a numpy list. can manually change the datatype of values

a.ndim  # prints the number of dimensions of the list

a.shape  # prints the shape of the list (number of entries for each axis i.e. columns/rows)

a.dtype # prints the datatype for values default int32 (4 bytes)

a.size  # number of items

a.itemsize  # number of bytes of one item

a.nbytes  # total number of bytes