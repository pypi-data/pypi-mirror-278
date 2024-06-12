
import pandas as pd
import numpy as np
import itertools
import statsmodels.api as sm
from utils import dedupe, remove_all, combine_all


## I referred to the code in the link below :
## https://github.com/owkin/PyDESeq2/blob/main/pydeseq2/utils.py


def check_count_data(count_data) :
    
    if isinstance(count_data, pd.DataFrame) :
        
        if count_data.isna().any().any() :
            raise ValueError("Missing values are not allowed.")  
        elif not set(count_data.dtypes) <= {np.dtype('int64'), np.dtype('float64')} :
            raise ValueError("Only numbers are allowed.")
        elif len(set(count_data.columns)) != len(count_data.columns) :
            raise ValueError('Same column names are not allowed.')
        elif len(set(count_data.index)) != len(count_data.index) :
            raise ValueError('Same row names are not allowed.')
    else :
        raise ValueError('count_data must be pandas.DataFrame.')
    
    if ((count_data % 1 != 0).any() | (count_data < 0).any()).any() :
        raise ValueError("Only positive integers(or 0) are alllowed")   
    elif (count_data.sum(axis=0) == 0).any() or (count_data.sum(axis=1) == 0).any() :
        raise ValueError('There is a row or column whose sum is 0.')
        

# after check_count_data
def check_metadata(metadata, count_data) :
    
    if isinstance(metadata, pd.DataFrame) : 
        
        if metadata.isna().any().any() :
            raise ValueError("Missing values are not allowed.")
        elif len(set(metadata.columns)) != len(metadata.columns) :
            raise ValueError('Same column names are not allowed.')
        elif len(set(metadata.index)) != len(metadata.index) :
            raise ValueError('Same row names are not allowed.')
        elif not set(metadata.index) <= set(count_data.columns) :
            raise ValueError('Samples of metadata must belong to the samples of count_data.')
    else :
        raise ValueError('metadata must be pandas.DataFrame.')
        
    for colname in metadata.columns :
        if '~' in colname or '+' in colname or ':' in colname :
            raise ValueError("Any column name of metadata must not contain '~', '+', ':'")
            

# after check_metadata
# design : "~ x1(factor) + x2 + x3 + x2:x3 +.....+ xn(condition)"
def obtain_design_factors(design, metadata) :
    
    if design.strip()[0] != '~' :
        raise ValueError("The design formula must start with tilde(~).")
    
    table = design.maketrans({'~' : ' ', '+' : ' '})
    design_factors = design.translate(table).split(' ')
    design_factors = remove_all(design_factors, '')
    if design_factors == [] :
        raise ValueError('There are no factors in the design formula.')
        
    entire = []
    inters = []
    for factor in design_factors :
        if ':' in factor :
            inter = factor.split(':')
            if len(inter) != 2 or len(set(inter)) != 2 :
                raise ValueError('A interaction term must contain only two different factors.')
            else :
                inters.append(set(inter))
        else :
            entire.append(factor)
    
    if len(dedupe(entire)) != len(entire) :
        raise ValueError('Same design terms are not allowed.')
    elif not set(entire) <= set(metadata.columns) :
        raise ValueError('The entire design factors must be the subset of the factors of metadata.')
        
    if len(dedupe(inters)) != len(inters) :
        raise ValueError('Same interaction terms are not allowed')
    else :
        inters = [list(inter) for inter in inters]
        
    for inter in inters : 
        factor1, factor2 = inter
        if factor1 not in entire or factor2 not in entire :
            raise ValueError('The innteraction factors must be the subset of the entire design factors.')    
            
    design_factors = {'entire' : entire, 'inters' : inters}
    
    return design_factors


# after obtain_design_factors
def design_factors_to_matrix(design_factors, metadata) :
           
    entire = design_factors['entire']
    inters = design_factors['inters']  
    
    non_inters = entire
    for factor in dedupe(combine_all(inters)) :
        non_inters = remove_all(non_inters, factor)
    
    design_matrix = metadata[non_inters]
    design_matrix = pd.get_dummies(design_matrix, dtype='int', drop_first=True)
    
    if inters != [] :
        for inter in inters :
            factor1, factor2 = inter 
            to_add1 = pd.get_dummies(metadata[factor1], dtype='int', drop_first=True)
            to_add2 = pd.get_dummies(metadata[factor2], dtype='int', drop_first=True)
            to_add = pd.concat([to_add1,to_add2], axis=1)
            for level1, level2 in itertools.product(to_add1.columns, to_add2.columns) :
                to_add3 = to_add1[level1]*to_add2[level2]
                to_add = pd.concat([to_add,to_add3], axis=1)
            design_matrix = pd.concat([design_matrix,to_add], axis=1)
            
    design_matrix = sm.add_constant(design_matrix)
    
    return design_matrix


def check_contrast(contrast, design_factors, metadata) :

    if len(contrast) != 3 :
        raise ValueError('contrast must be length of 3.')
    else :
        condition, control, treat = contrast[0], contrast[1], contrast[2]   
        
    if condition != design_factors['entire'][-1] :
        raise ValueError('condition must be the last design factor of the design formula.')
    else :
        levels = dedupe(metadata[condition])
        
    if control == treat :
        raise ValueError('control and treat must be different.')
    elif control not in levels or treat not in levels :
        raise ValueError('control and treat must belong to the levels of the condition.')
        



