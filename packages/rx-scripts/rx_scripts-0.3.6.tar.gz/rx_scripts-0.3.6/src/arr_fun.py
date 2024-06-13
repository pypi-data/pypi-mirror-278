import math
import numpy

#-----------------------------------------------
def repeat_arr(arr_val, ftimes):
    '''
    Will repeat elements inn an array a non integer nuumber of times. 

    arr_val: 1D array of objects
    ftimes (float): Number of times to repeat it.
    '''

    a = math.floor(ftimes)
    b = math.ceil(ftimes)
    c = ftimes

    p = (c - b) / (a - b)

    size_t = len(arr_val)
    size_1 = int(p * size_t)

    arr_ind_1 = numpy.random.choice(size_t, size=size_1, replace=False)
    arr_val_1 = arr_val[arr_ind_1]

    arr_ind_2 = numpy.setdiff1d(numpy.arange(size_t), arr_ind_1)
    arr_val_2 = arr_val[arr_ind_2]

    arr_val_1 = numpy.repeat(arr_val_1, a)
    arr_val_2 = numpy.repeat(arr_val_2, b)

    return numpy.concatenate([arr_val_1, arr_val_2])
#-----------------------------------------------
