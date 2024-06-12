
import warnings
import pandas as pd
import numpy as np
from normalization import cpm, mor
from utils import *
from prework import *
from stats import *


## I referred to the code in the link below :
## https://github.com/owkin/PyDESeq2


class pydea_dataset :
    
    """
    parameters
    ----------
    count_data : pandas.DataFrame containing raw counts.
            Rows correspond to genes and columns correspond to samples.
            The count value must be 0 or a positive integer.
                
    metadata : pandas.DataFrame containing levels.
            Rows correspond to samples and columns correspond to factors.
    
    design : string in the form of '~ x1 + x2 + x3 + x2:x3 +.....+ xn(condition)' where xi is the design factor.
            See the 'design' part of the DESeq2 document.
    """
    
    warnings.filterwarnings('ignore')
    
    def __init__(self, count_data, metadata, design) :
            
        check_count_data(count_data)                            
        check_metadata(metadata, count_data)                      
        design_factors = obtain_design_factors(design, metadata)
        design_matrix = design_factors_to_matrix(design_factors, metadata)
        genes = count_data.index
        samples = metadata.index    
    
        self.count_data = count_data
        self.metadata = metadata
        self.design = design
        self.design_factors = design_factors
        self.design_matrix = design_matrix
        self.genes = genes
        self.samples = samples
        
    def normalization(self, norm_method) :
        
        """
        parameters
        ----------
        norm_method : string
                    norm_method must be one of 'cpm' or 'mor'
        """
        
        norm_functions = {'cpm' : cpm, 'mor' : mor}
        
        if norm_method not in norm_functions.keys() :
            raise ValueError("Normalization method must be one of 'cpm' or 'mor'")
        else :
            normalized, size_factors = norm_functions[norm_method](self.count_data)
            
        return normalized, size_factors
        
    def PyDEA(self, norm_method='mor') :
        
        normalized, size_factors = self.normalization(norm_method)
        print('Finished estimating size factors.\n')
        
        means, varns, disps = estimate_dispersions(self.count_data)
        print('Finished estimating gene-wise dispersions.\n')
        
        fitted_disps = fit_dispersions(means, disps)
        print('Finished fitting dispersion estimates.\n')
        
        # full model
        print('Fitting GLM for each gene....\n')
        sample_groups = group_rownames(self.design_matrix)
        likelihood_full_model = pd.DataFrame(index=self.genes, columns=['l1'])
        for gene in self.genes :
            counts = self.count_data.loc[gene,:]
            full_model = glm_fit(counts, self.design_matrix, sample_groups)
            likelihood = full_model.llf
            likelihood_full_model.loc[gene,'l1'] = likelihood
        print('Finished fitting GLM for each gene.')
        
        self.norm_method = norm_method
        self.normalized = normalized
        self.size_factors = size_factors
        
        self.means = means
        self.varns = varns
        self.disps = disps
        self.fitted_disps = fitted_disps
        self.l1 = likelihood_full_model
        

def results(pdd, contrast) :

    """
    parameters
    ----------
    pdd : pydea_dataset after running PyDEA() method.
    
    contrast : sequence 
            The first element is condition, second element is control, third element is treat.
            condition must be the last design factor of the design formula.
            control and treat must be different levels, each belonging to the condition.
    """

    warnings.filterwarnings('ignore')
    
    check_contrast(contrast, pdd.design_factors, pdd.metadata)
    condition, control, treat = contrast[0], contrast[1], contrast[2]
    
    # reduced model
    reduced_metadata = pdd.metadata.copy()
    reduced_metadata[condition] = replace_all(reduced_metadata[condition], treat, control)
    reduced_design_factors = obtain_design_factors(pdd.design, reduced_metadata)
    reduced_design_matrix = design_factors_to_matrix(reduced_design_factors, reduced_metadata)

    print('Performing hypothesis testing....\n')
    sample_groups = group_rownames(reduced_design_matrix)
    likelihood_reduced_model = pd.DataFrame(index=pdd.genes, columns=['l2'])
    for gene in pdd.genes :
        counts = pdd.count_data.loc[gene,:]
        reduced_model = glm_fit(counts, reduced_design_matrix, sample_groups)
        likelihood = reduced_model.llf
        likelihood_reduced_model.loc[gene,'l2'] = likelihood
    pdd.l2 = likelihood_reduced_model

    # p-value
    dof = 1
    p_values = pd.DataFrame(index=pdd.genes, columns=['pvalue'])
    for gene in pdd.genes :
        l1 = pdd.l1.loc[gene,'l1']
        l2 = pdd.l2.loc[gene,'l2']
        p_value = lrt(l1, l2, dof=dof)
        p_values.loc[gene,'pvalue'] = p_value           

    # adjusted p-value
    adj_p_values = pd.DataFrame({'padj' : fdr(list(p_values['pvalue']))}, index=pdd.genes)
    print('Finished hypothesis testing.\n')

    # basemean
    basemean = pdd.means
    basemean.columns = ['baseMean']

    # LFC
    log2_fold_change = obtain_lfc(pdd.count_data, pdd.metadata, contrast)
    print('Finished obtaining LFCs.\n')

    # result
    pdd.contrast = contrast
    pdd.pvalue = p_values
    pdd.dof = dof
    pdd.padj = adj_p_values
    pdd.basemean = basemean
    pdd.lfc = log2_fold_change

    result = pd.concat([pdd.lfc, pdd.basemean, pdd.varns, pdd.disps, pdd.pvalue, pdd.padj], axis=1)
    pdd.result = result

    print('Log2 fold change & Likelihood-ratio test & p-value : {} {} vs {}\n'.format(condition, control, treat))
    print(result.head())
    return {'pdd':pdd, 'result':result}


