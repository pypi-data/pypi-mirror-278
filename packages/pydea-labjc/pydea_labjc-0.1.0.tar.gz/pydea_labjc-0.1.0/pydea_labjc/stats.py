
import import_ipynb
import numpy as np
import pandas as pd
from scipy.stats import chi2
from scipy.special import gammaln, psi, factorial
from scipy.optimize import fmin_l_bfgs_b as optim
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod.families import NegativeBinomial
from utils import group_rownames


## I referred to the code in the link below :
## https://github.com/gokceneraslan/fit_nbinom


## Fit negative binomial distribution using the maximum likelihood estimation. 

def log_likelihood(params, X, neg=-1):
    
    """
    parameters
    ----------
    params : sequence
        The first value is r and the second value is p.
        r : float greater than or equal to 0. The number of success. 
        p : float between 0 and 1. The probability of a single success.
    
    X : sequence 
        The observed data.
    
    neg : float 
        Negative value to be multiplied by the log-likelihood.
    """
    
    infinitesimal = np.finfo(float).eps
    
    r, p = params 
    if r < 0 :
        raise ValueError('r must be positive or 0')
    elif p < 0 or p > 1 :
        raise ValueError('p must be between 0 and 1')
    
    # Refer http://en.wikipedia.org/wiki/Negative_binomial_distribution#Maximum_likelihood_estimation
    N = len(X)
    ll = np.sum(gammaln(X + r)) \
        - np.sum(np.log(factorial(X))) \
        - N*(gammaln(r)) \
        + N*r*np.log(p) \
        + np.sum(X*np.log(1-(p if p < 1 else 1-infinitesimal)))

    return neg*ll


def log_likelihood_deriv(params, X):
    
    infinitesimal = np.finfo(float).eps
    
    r, p = params
    if r < 0 :
        raise ValueError('r must be positive or 0')
    elif p < 0 or p > 1 :
        raise ValueError('p must be between 0 and 1')

    # Refer http://en.wikipedia.org/wiki/Negative_binomial_distribution#Maximum_likelihood_estimation
    N = len(X)
    pderiv = (N*r)/p - np.sum(X)/(1-(p if p < 1 else 1-infinitesimal))
    rderiv = np.sum(psi(X + r)) \
            - N*psi(r) \
            + N*np.log(p)

    return np.array([rderiv, pderiv])


def mle_nbinom(data) :
    
    """
    parameters
    ----------
    data : sequence 
        The Observed data.
    """
    
    infinitesimal = np.finfo(float).eps 
    
    if any([True if val < 0 else False for val in data]) :
        raise ValueError('Only values greater than or equal to 0 must be contained in the data.')
    
    mu = np.mean(data)
    var = np.var(data)
    r = (mu**2)/((var - mu) if var > mu else 10)
    p = r/(r + mu)

    r0 = r
    p0 = p
    initial_params = np.array([r0, p0])
       
    bounds = [(infinitesimal, None), (infinitesimal, 1)]    # ( min of r, max of r ), ( min of p, max of p )
    optimres = optim(log_likelihood,
                    x0=initial_params,
                    fprime=log_likelihood_deriv,
                    args=(np.array(data),),
                    approx_grad=1,
                    bounds=bounds)
    
    return optimres[0]
        

## Estimate gene-wise dispersions.

def estimate_dispersions(count_data) : 
    
    """
    parameters
    ----------
    count_data : pandas.DataFrame containing raw counts.
        DESeq2 seems to use raw count data to estimate dispersions.
    """
    
    genes = count_data.index
    disps = pd.DataFrame(index=genes, columns=['disp'])
    means = pd.DataFrame(index=genes, columns=['mean'])
    for gene in genes :
        r, p = mle_nbinom(count_data.loc[gene,:])
        mean = r*(1-p)/p
        disp = 1/r
        disps.loc[gene,'disp'] = disp
        means.loc[gene,'mean'] = mean

    varns = means + disp*(means**2)
        
    return means, varns, disps


## Fit curve to gene-wise dispersion estimates.

def fit_dispersions(means, disps) :
    
    """
    parameters
    ----------
    means : pandas.DataFrame 
        The first dataframe obtained after running the estimate_dispersions(count_data).

    disps : pandas.DataFrame 
        The third dataframe obtained after running the estimate_dispersions(count_data).
    """
    
    fitted_disps = pd.DataFrame(index=disps.index, columns=['fitted disp'])
    
    groups = group_rownames(means)
    for group in groups :
        fitted_disps.loc[group,'fitted_disp'] = np.mean(disps.loc[group,'disp'])
    
    return fitted_disps
    

## GLM fit for each gene.

def glm_fit(counts, design_matrix, sample_groups, family='nbinom') :
    
    """
    parameters
    ----------
    counts : sequence object containing raw counts.
    
    sample_groups : sequence
                The result obtained after running the group_rownames(design_matrix).
    """
    
    exog = design_matrix
    endog = pd.Series(index=design_matrix.index)
    for sample_group in sample_groups :
        endog[sample_group] = np.mean(counts[sample_group])
        
    model = GLM(endog=endog, exog=exog, family=NegativeBinomial())
    res = model.fit()
        
    return res


# Likelihood-ratio test
def lrt(l1, l2, dof, log=True) :
    
    """
    parameters
    ----------
    l1 : float
        Likelihood of model1.
    
    l2 : float
        Likelihood of model2.
                
    dof : integer
        Degree of freedom.
    
    log : boolean
        log=True means that the l1 and l2 are the logarithms of the original likelihoods.
    """

    if log == True :
        lr = 2*(l1 - l2)
    else :
        lr = 2*(np.log(l1/l2))

    p_val = chi2.sf(lr, dof)

    return p_val


# False Discovery Rate
def fdr(p_values) :
    
    """
    parameters
    ----------
    p_values : sequence object containing the p-values.
    """

    sorted_p_values = sorted(p_values)
    ranks = [sorted_p_values.index(p_value) + 1 for p_value in p_values]
    
    N = len(p_values)
    adj_p_values = [p_values[i]*(N/ranks[i]) for i in range(N)]

    return adj_p_values


# Log2 fold change
def obtain_lfc(count_data, metadata, contrast) :
    
    """
    parameters
    ----------
    contrast : sequence 
            The first element is condition, second element is control, third element is treat.
            condition must be the last design factor of the design formula.
            control and treat must be different levels, each belonging to the condition.
    """
    
    samples = metadata.index
    condition, control, treat = contrast[0], contrast[1], contrast[2]
    
    control_samples = metadata[metadata[condition]==control].index
    treat_samples = metadata[metadata[condition]==treat].index     
    control_counts = count_data[control_samples]
    treat_counts = count_data[treat_samples]

    control_counts += 0.01
    treat_counts += 0.01
    
    log2_fold_change = np.log2(control_counts.mean(axis=1)/treat_counts.mean(axis=1))
    log2_fold_change = log2_fold_change.to_frame(name='lfc')

    return log2_fold_change



