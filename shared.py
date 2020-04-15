
CACHETIMESECONDS = 3600 * 3  # be nice to the API to not get banned

APIURL = 'https://coronavirus-tracker-api.herokuapp.com/all'
FILENAME = 'covid-19_data.json'

import datetime
import numpy as np
import scipy.ndimage.interpolation  # shift function
import math

import world_data

def delay(npArray, days):
    """shift to right, fill with 0, values fall off!"""
    return scipy.ndimage.interpolation.shift(npArray, days, cval=0)


def get_offset_X(XCDR_data, D_model, dataOffset='auto'):
    X_days = world_data.dates_to_days(XCDR_data[:,0])
    X_days = np.array(X_days) - min(X_days)
    if dataOffset == 'auto':
        assert (max(X_days) - min(X_days) + 1) == len(X_days)  # continous data
        D_data = XCDR_data[:,2]

        # log to emphasize lower values (relative error)   http://wrogn.com/curve-fitting-with-minimized-relative-error/
        D_data = np.log(np.array(D_data, dtype='float64') + 1)
        D_model = np.log(D_model + 1)

        mini = 9e9
        miniO = None
        for o in range(0,150):  # todo: dat number...
            oDd = np.pad(D_data, (o, 0))  # different than delay/shift, extends length
            oDm = D_model[:len(D_data) + o]
            rms = np.sqrt(np.mean(np.square((oDd - oDm))/(1 + oDm)))  # hacky but seems to do the job
            if rms < mini:
                mini = rms
                miniO = o
        print("date offset:", miniO)
        dataOffset = miniO
    return dataOffset

def model_to_world_time(X, XCDR_data):
    X2 = np.array(X, dtype=np.dtype('M8[D]'))
    for i, x in enumerate(X):
        X2[i] = min(XCDR_data[:,0]) + datetime.timedelta(days=int(x))
    return X2
