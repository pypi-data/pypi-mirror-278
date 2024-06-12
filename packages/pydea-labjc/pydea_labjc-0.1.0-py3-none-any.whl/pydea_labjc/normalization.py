
import numpy as np
import pandas as pd
from utils import geometric_mean


# counts per million
def cpm(count_data, log=False) :

    normalized = count_data.copy()
    
    size_factors = normalized.sum()/10**6
    normalized /= size_factors
    
    if log == True :
        normalized = np.log(normalized)

    return normalized, size_factors


# median of ratios
def mor(count_data, log = False) :

    normalized = count_data.copy()
        
    reference = [geometric_mean(count_data.loc[gene,:]) for gene in count_data.index]
    ratios = normalized.T/reference
    ratios = ratios.T

    size_factors = ratios.median()
    normalized /= size_factors
    
    if log == True :
        normalized = np.log(normalized)

    return normalized, size_factors

