
CACHETIMESECONDS = 3600 * 3  # be nice to the API to not get banned

APIURL = 'https://coronavirus-tracker-api.herokuapp.com/all'
FILENAME = 'covid-19_data.json'

import numpy as np

import scipy.ndimage.interpolation  # shift function
def delay(npArray, days):
    """shift to right, fill with 0, values fall off!"""
    return scipy.ndimage.interpolation.shift(npArray, days, cval=0)


def get_offset_X(XCDR_data, D_model, dataOffset='auto'):
    X_data = XCDR_data[:,0] - min(XCDR_data[:,0])
    if dataOffset == 'auto':
        assert (max(X_data) - min(X_data) + 1) == len(X_data)  # continous data
        D_data = XCDR_data[:,2]
        mini = 9e9
        miniO = None
        for o in range(0,150):  # todo: dat number...
            oDd = np.pad(D_data, (o, 0))  # different than delay/shift, extends length
            oDm = D_model[:len(D_data) + o]
            rms = np.sqrt(np.mean(np.square(oDd - oDm)))
            if rms < mini:
                mini = rms
                miniO = o
        print("date offset:", miniO)
        return X_data + miniO
    else:
        return X_data + dataOffset
