'''
    Some robust statistics routines implementing 
    sigma-clipping to remove outliers.
'''

import numpy as np, numpy.ma as ma
from astropy.stats import sigma_clip
from scipy.interpolate import interp1d
from copy import copy

def array_process(idata, sigcut, compress = False):
    '''Create the sigma-clipped data array.'''
    data = copy(idata)
    scut = np.clip(sigcut, 1.0, sigcut) #if we clip too low, this will never end

    good_data = sigma_clip(data, scut, iters=None)
    if compress:
        return good_data.compressed()
    return good_data

def robust_mean(inputdata, sigcut = 4.0, axis = None):
    data = array_process(inputdata, sigcut)
    # np.nanmean(data, axis = axis)
    return ma.mean(data, axis=axis)


def robust_sigma(inputdata, sigcut = 3.0, axis = None):
    data = array_process(inputdata, sigcut)
    return np.nanstd(data, axis = axis)

def interp_x(points, targ_x):
    fpoints = interp_nan(points)
    x, y = zip(*fpoints)
    x = np.array(x)
    y = np.array(y)
    f = interp1d(x, y, kind='cubic')
    return f(targ_x)

def interp_nan(points):
    #use interpolation to remove nans
    x, y = zip(*points)
    x = np.array(x)
    y = np.array(y)
    nans, x2 = np.isnan(y), lambda z: z.nonzero()[0]
    y[nans] = interp1d(x2(~nans), y[~nans], kind='cubic', bounds_error=False)(x2(nans))
    return zip(x, y)
    
def idlhash(a, b, list = False):
    c = np.outer(a,b)
    if list:
        return c.tolist()
    return c

def med_normal(arr):
    med = np.median(arr)
    return arr - med
    
    