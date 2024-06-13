import scipy as sp

def r2_obs_to_r2_lia(R2O, K, P):
    '''
    R2O = r2 on the observed scale
    K = population prevalence
    P = proportion of cases in the case-control samples
    mv = zv/K  #mean liability for case
    thd = the threshold on the normal distribution which truncates the proportion of disease prevalence
    reference: Lee, S. H., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2012). A better coefficient of determination for genetic profile analysis. Genetic epidemiology, 36(3), 214-224.
    '''
    
    thd = sp.stats.norm.ppf(1-K, loc=0, scale=1)
    #thd = -qnorm(K,0,1)
    
    zv = sp.stats.norm.pdf(thd, loc=0, scale=1)
    #zv = dnorm(thd) #z (normal density)
    
    mv = zv/K  
    #mean liability for case

    theta = mv*(P-K)/(1-K)*(mv*(P-K)/(1-K)-thd) #θ in equation 15
    
    cv = K*(1-K)/(zv**2) * K*(1-K)/(P*(1-P))  #C inequation 15
    
    R2 = R2O*cv/(1+R2O*theta*cv)
    
    return R2