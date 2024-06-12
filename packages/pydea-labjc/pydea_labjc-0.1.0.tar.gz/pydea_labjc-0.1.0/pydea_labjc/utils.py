
import pandas as pd
import numpy as np


## Perform various operations on sequence objects
## while preserving the order of the elements.


def dedupe(arr) :

    deduped = []
    for elt in arr :
        if elt not in deduped :
            deduped.append(elt)

    return deduped


def remove_all(arr, target_elt) : 
    
    removed = []
    for elt in arr :
        if elt != target_elt :
            removed.append(elt)
        
    return removed


def replace_all(arr, from_elt, to_elt) :
    
    replaced = []
    for elt in arr :
        if elt == from_elt :
            replaced.append(to_elt)
        else :
            replaced.append(elt)
        
    return replaced


def multiply_all(arr) :
    
    result = 1
    for elt in arr :
        result *= elt
        
    return result


def combine_all(arrs) :
    
    combined = []
    for arr in arrs :
        combined += list(arr)
        
    return combined


def arr_substract(arr1, arr2) :
    
    substed = []
    for elt in arr1 :
        if elt not in arr2 :
            substed.append(elt)
    
    return sub


def geometric_mean(arr) :
    
    n = len(arr)
    gmean = multiply_all(arr)
    gmean = gmean**(1/n)
    
    return gmean
    

## Group row names with the same record(row vector) together. 
def group_rownames(df) :
    
    """
    parameters
    ----------
    df : pandas.DataFrame
    """
    
    colnames = list(df.columns)
    groups = df.groupby(colnames).groups
    groups = list(groups.values())
    
    return groups



