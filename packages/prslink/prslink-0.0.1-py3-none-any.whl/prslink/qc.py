import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import statsmodels.api as sm
import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import numpy as np
from prslink.g_Log import Log
from statsmodels.stats.multitest import multipletests

def filter_results(results, phenos=None, scores=None, qcut=None,qref=1, norm=None, log=Log()):
    dataset = results.copy()
    log.write("-Start to filter results ignoring covars... ")

    dataset["_TARGET"]=True
    target = dataset["_TARGET"]

    if phenos is not None:
        target = target&(dataset["PHENO"].isin(phenos))
        log.write( " -PHENOS : {}".format(",".join(sorted(scores))))
    
    if scores is not None:
        target = target&(dataset["PRS"].isin(scores))
        log.write( " -SCORES : {}".format(",".join(sorted(phenos))))

    if qcut is not None:
        if "Q_SCORE" in dataset.columns:
            target = target&(~dataset["Q_SCORE"].isna())
        if "Q_REF" in dataset.columns:    
            target = target&(~(dataset["Q_REF"]==qref)) 
        if "Q_INTERVAL" in dataset.columns:
            if type(qcut) is list: 
                qcut_str = ",".join(map(str, qcut.copy()))
            else:
                qcut_str = str(qcut)
            log.write( " -QCUT LIST : {}".format(qcut_str))
            target = target&(~dataset["Q_INTERVAL"]==qcut_str)

    if norm is not None:
        target = target& (dataset["NORM"]==norm)
        log.write( " -PRS NORM : {} ".format(norm))

    output = dataset.loc[target,:]
    log.write( " -Filtered in models: {} ".format(len(output)))
    return output


def check_formula(results, phenos, scores, covars, qcut=None, qref=1, norm=True, log=Log()):
    if type(phenos) is not list: phenos = [phenos]
    if type(scores) is not list: scores = [scores]
    if type(covars) is not list: covars = [covars]
    covars_string = "+".join(sorted(covars))
    
    dataset = results.copy()

    log.write("-Start to filter results by formula... ")
    log.write( " -SCORES : {}".format(",".join(sorted(scores ))))
    log.write( " -PHENOS : {}".format(",".join(sorted(phenos ))))
    log.write( " -COVARS : {}".format(covars_string))
    # filter normalization
    dataset = dataset.loc[dataset["NORM"]==norm,:]
    log.write( " -PRS NORM : {} ".format(norm))

    # filter q
    if qcut is None:
        log.write( " -QCUT LIST skip.")
        pass
    elif type(qcut) is int:
        qcut_list = str(qcut)
        nqcut=qcut
        log.write( " -QCUT LIST : {}".format(qcut_list))
    else:
        qcut_list = ",".join(map(str, qcut.copy()))
        nqcut = len(qcut)-1
        log.write( " -QCUT LIST : {}".format(qcut_list))
    
    # construct formulas
    formulas=set()
    for pheno in phenos:
        for score in scores:
            if qcut is not None:
                for i in range(1,nqcut+1):
                    # base formula
                    formula = "{}~{}+{}".format(pheno, score, covars_string)
                    
                    # full formula
                    formula = formula +'({}-{}-{})[{}]'.format(qref, i, nqcut,qcut_list)
                    
                    # add into set
                    formulas.add(formula)
            else:
                # base formula
                formula = "{}~{}+{}".format(pheno, score, covars_string)
            formulas.add(formula)

    log.write(" -Filtered-in formulas: ", end="")
    
    # print formulas
    for index, formula in enumerate(formulas):
        if index >3:
            # formula >3, skip
            log.write("...", end="",show_time=False)
            break
        else:
            log.write(formula, end=", ",show_time=False)
    log.write(".",show_time=False)

    #extract formulas
    output = dataset.loc[dataset["FULL_formula"].isin(formulas),:]

    # output summary
    log.write( " -Filtered-in results: {} ".format(len(output)))
    log.write( "  -N_score: {} ".format(output["PRS"].nunique()))
    log.write( "  -N_pheno: {} ".format(output["PHENO"].nunique()))
    log.write( "  -N_covar: {} ".format(len(covars)))
    log.write("-Finished filtering results by formula... ")
    return output