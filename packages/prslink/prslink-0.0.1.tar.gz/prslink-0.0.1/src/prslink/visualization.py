import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import statsmodels.api as sm
import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import numpy as np
from prslink.g_Log import Log
from statsmodels.stats.multitest import multipletests
from prslink.qc import check_formula
from prslink.qc import filter_results
from prslink.visualization_auxiliary import configure_fig_args
from prslink.visualization_auxiliary import configure_plot_args
from prslink.visualization_auxiliary import configure_colors
from prslink.visualization_auxiliary import configure_legend
import matplotlib.colors as mc


def _plot_roc(dataset,phenos,scores,covars,cmap_head=0,cmap="tab10",cmap_tail=0):
# calculate the fpr and tpr for all thresholds of the classification
    
    for pheno in phenos:
        # extract data for checking
        cols_to_check = [pheno] +scores+ covars
        to_check = dataset.loc[~dataset[pheno].isna(),cols_to_check]
        to_check = to_check.dropna()

        output_hex_colors = configure_colors(n=len(scores), cmap_head=cmap_head, cmap=cmap, cmap_tail=cmap_tail )
        
        # only plot for binary pohenotypes
        if not pd.api.types.is_float_dtype(to_check.loc[:,pheno]):
            # null
            y = to_check.loc[to_check[pheno].isin([0,1]),pheno]
            x = to_check.loc[to_check[pheno].isin([0,1]),covars]
            x = sm.add_constant(x)

            mod = sm.Logit(y.astype(int),x.astype(float)).fit()
            
            preds = mod.predict(x.astype(float))
    
            fpr, tpr, threshold = metrics.roc_curve(y, preds)
    
            roc_auc = metrics.auc(fpr, tpr)
            
            #with plt.style.context('seaborn-v0_8'):
            fig,ax = plt.subplots(figsize=(5,5), dpi=200)

            ax.set_title('ROC curve for {}'.format(pheno))
            ax.plot(fpr, tpr, 'grey', label = 'AUC (null) = %0.3f' % roc_auc)
            ax.plot([0, 1], [0, 1],'--',c="grey")
            ax.set_xlim([0, 1])
            ax.set_ylim([0, 1])
            ax.set_ylabel('True Positive Rate')
            ax.set_xlabel('False Positive Rate')
            
            for index,score in enumerate(scores):			
                x = to_check.loc[to_check[pheno].isin([0,1]),covars+[score]]
                x[score] = (x[score] -np.mean(x[score])) / np.std(x[score])
                x = sm.add_constant(x)
                mod = sm.OLS(y.astype(int),x.astype(float)).fit()
                spreds = mod.predict(x.astype(float))
                fpr, tpr, threshold = metrics.roc_curve(y, spreds)
                roc_auc = metrics.auc(fpr, tpr)
                ax.plot(fpr, tpr, label = 'AUC ({}) = {:.3f}'.format(score, roc_auc), c=output_hex_colors[index])
            ax.legend(loc = "lower right")

###################################################################################################################################

def _plot_prs(dataset, scores, phenos=None,plot_args=None,fig_args=None,cmap_head=0, cmap="coolwarm", cmap_tail=0, width=5, **args):
    
    if phenos is None:
        phenos=[]

    plot_args = configure_plot_args(plot_args)
    fig_args  = configure_fig_args(fig_args ,width = width)
    output_hex_colors = configure_colors(n=2, cmap_head=cmap_head, cmap=cmap, cmap_tail=cmap_tail )
    
    #fig, ax = plt.subplots(layout='constrained',**fig_args)

    for score in scores:
        if len(phenos)==0:
             _plot_single_prs(dataset, score, pheno=None, output_hex_colors=output_hex_colors,fig_args=fig_args, **args)
        else:
            for pheno in phenos:
                _plot_single_prs(dataset, score, pheno=pheno, output_hex_colors=output_hex_colors,  fig_args=fig_args,**args)
    #return fig,ax

def _plot_single_prs(dataset, score, pheno=None, output_hex_colors=None, fig_args=None,**args):
    fig,ax = plt.subplots(**fig_args)
    
    if pheno is not None:
        cols_to_use = [score,pheno]
        args["hue"] =  pheno
        args["hue_order"] =  [0,1]
        args["palette"] =  output_hex_colors
    else:
        cols_to_use = [score]

    dataset_to_plot = dataset[cols_to_use].dropna()

    sns.histplot(data=dataset_to_plot, x=score, ax=ax, **args)
    
    if pheno is not None:
        
        mean0=dataset_to_plot.loc[dataset_to_plot[pheno]==0, score].mean()
        mean1=dataset_to_plot.loc[dataset_to_plot[pheno]==1, score].mean()
        ax.axvline(x=mean0, linestyle = "--",color = output_hex_colors[0])
        ax.axvline(x=mean1, linestyle = "--",color=  output_hex_colors[1] )
    else:
        ax.axvline(x=dataset_to_plot[score].mean(), linestyle = "--",color= output_hex_colors[0] )
    
    ax.set_xlabel("Polygenic scores : {}".format(score))
    n = len(dataset_to_plot)
    ax.set_ylabel("Count (N={})".format(n))



###################################################################################################################################

def _plot_q(dataset,phenos,qscore,covars,qcut,qref,y="BETA",norm=False,
            log=Log(),
            colors=None, 
            plot_args=None,
            fig_args=None,
            errorbar_args=None,
            offset_multiplier=None,
            cmap="Set1"):
    
    # prepare labels and cutpoint list
    dataset = check_formula(results=dataset, 
                            phenos=phenos,
                            scores=qscore, 
                            covars=covars, 
                            qcut=qcut,
                            qref=qref, 
                            norm=norm,
                            log=log)

    if type(qcut) is int:
        interval=1/qcut
        cut_points = [0] + [i*interval for i in range(1, qcut)] + [1]
        qcut_xtick_labels=['({:.2f},{:.2f}]'.format(cut_points[i],cut_points[i+1]) for i in range(0,len(cut_points)-1)]
        log.write(" - X_tick_labels: ", ",".join(qcut_xtick_labels))
    else:
        cut_points = list(qcut)
        qcut_xtick_labels=['({:.2f},{:.2f}]'.format(cut_points[i],cut_points[i+1]) for i in range(0,len(cut_points)-1)]
    
    # extract data to plot
    #target = (dataset["PHENO"].isin(phenos))&(dataset["Q_SCORE"]==qscore)&(dataset["Q_INTERVAL"]==qcut_list)&(dataset["NORM"]==norm)
    #dataset = dataset.loc[target,:].copy()
    #qlabel =  "Q_" + str(len(labels))
    
    # convert
    if y=="OR" or y=="HR":
        if y=="OR":
            dataset["OR"] = np.exp(dataset["BETA"])
        else:
            dataset["HR"] = np.exp(dataset["BETA"])
        dataset["CI_L"] = np.exp(dataset["CI_L"])
        dataset["CI_U"] = np.exp(dataset["CI_U"])
    
    # config figure options
    if fig_args is None:
        fig_args = {}
        fig_args["dpi"]=200
        fig_args["figsize"]=(dataset["Q"].nunique(),5)
    
    # config plot options
    if plot_args is None:
        plot_args = {}
    if errorbar_args is None:
        errorbar_args = {}
    
    colors_num = len(phenos)
    cmap_to_use = plt.cm.get_cmap(cmap)
    if cmap_to_use.N >100:
        rgba = cmap_to_use([i /colors_num  for i in range(colors_num)])
    else:
        rgba = cmap_to_use(range(colors_num))
    
    output_hex_colors=[]
    for i in range(len(rgba)):
        output_hex_colors.append(mc.to_hex(rgba[i]))
    if colors is None:
        colors = output_hex_colors
    
    # init plot
    fig, ax = plt.subplots(**fig_args)

    # create plot
    for i,pheno in enumerate(phenos):
        if offset_multiplier is None: 
            offset_multiplier= len(phenos) * 2
        #set to middle 
        offset = i*1/offset_multiplier - len(phenos)/offset_multiplier/2
        # for each phenotype, sort by qlabels
        to_plot= dataset.loc[dataset["PHENO"]==pheno,:].sort_values(by="Q")
        if colors is not None:
            color = output_hex_colors[i] #= colors[i%len(colors)]
            plot_args["color"]=color
        ax.scatter(to_plot["Q"] + offset, to_plot[y],**plot_args)
        if y=="BETA" or y=="OR" or  y=="HR":
            if colors is not None:
                color = output_hex_colors[i]#= colors[i%len(colors)]
                errorbar_args["color"]=color
            ax.errorbar(to_plot["Q"] + offset, to_plot[y],yerr=np.abs(to_plot[["CI_L","CI_U"]].T - to_plot[y].T ),label=pheno,**plot_args)
    
    # add 0/1 line
    if y=="OR" or y=="HR":
        ax.axhline(y=1,linestyle="dashed",color="grey")
    else:
        ax.axhline(y=0,linestyle="dashed",color="grey")

    # config other elements
    ax.set_ylabel(y)
    ax.set_xlabel("Polygenic risk score strata \n {}".format(qscore))
    ax.set_xticks(range(1,len(cut_points)))
    ax.set_xticklabels(qcut_xtick_labels,rotation=45)
    ax.legend()
    sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))
    return fig,ax

###################################################################################################################################

def _plot_all(dataset,phenos,scores=None,covars=None,best=None,colors=None,y="BETA",log=Log(),norm=True,plot_args=None,fig_args=None,errorbar_args=None,cmap="Set1",width=None,legend_args=None,**args):

    #
    dataset = check_formula(results=dataset, phenos=phenos,scores=scores, covars=covars, qcut=None, norm=norm,log=log)
    
    #try:
    #    target = (dataset["PHENO"].isin(phenos))&(dataset["Q_SCORE"].isna())&(dataset["NORM"]==norm)&(dataset["PRS"].isin(scores))
    #except:
    #    target = (dataset["PHENO"].isin(phenos))&(dataset["NORM"]==norm)&(dataset["PRS"].isin(scores))
    #dataset = dataset.loc[target,:].copy().sort_values(by=["PHENO","PRS"])
    
    # convert data
    if y=="OR" or y=="HR":
        if y=="OR":
            dataset["OR"] = np.exp(dataset["BETA"])
        else:
            dataset["HR"] = np.exp(dataset["BETA"])
        dataset["CI_L"] = np.exp(dataset["CI_L"])
        dataset["CI_U"] = np.exp(dataset["CI_U"])
    
    # config figure options
    if fig_args is None:
        fig_args = {}
        fig_args["dpi"]=200
        fig_args["figsize"]=(dataset["PHENO"].nunique(),5)
    
    # config plot options
    if plot_args is None:
        plot_args = {}
    
    colors_num = len(set(scores))
    cmap_to_use = plt.cm.get_cmap(cmap)
    if cmap_to_use.N >100:
        rgba = cmap_to_use([i /colors_num  for i in range(colors_num)])
    else:
        rgba = cmap_to_use(range(colors_num))
    
    output_hex_colors=[]
    for i in range(len(rgba)):
        output_hex_colors.append(mc.to_hex(rgba[i]))
    output_hex_colors

    if errorbar_args is None:
        errorbar_args = {}

    # init fig
    fig, ax = plt.subplots(**fig_args)
    
    # init x, width, and counter
    phenotypes = dataset["PHENO"].unique()
    
    x=np.arange(len(phenotypes))

    if width is None:
        width= 1/(len(scores)+2)
    multiplier=0

    # create plot
    for i,score in enumerate(scores):
        # x offset
        offset=width * multiplier
        
        # plot the results for each model for all phenotypes
        to_plot= dataset.loc[dataset["PRS"]==score,:].sort_values(by=["PHENO"])
        
        if colors is not None:
            color = colors[i%len(colors)]
            plot_args["color"]=color
            errorbar_args["color"]=color
        if y=="BETA" or y=="OR" or  y=="HR":
            ax.scatter(x+offset, to_plot[y],color=output_hex_colors[i],**plot_args)
        else:
            ax.bar(x+offset, height=to_plot[y], width=width,label=score,color=output_hex_colors[i],**plot_args)

        if y=="BETA" or y=="OR" or  y=="HR":
            ax.errorbar(x+offset, to_plot[y], yerr=np.abs(to_plot[["CI_L","CI_U"]].T - to_plot[y].T ),color=output_hex_colors[i],linewidth=0,elinewidth=3,label=score,**errorbar_args)
        multiplier+=1
    
    if y=="OR" or y=="HR":
        ax.axhline(y=1,linestyle="dashed",color="grey")
    else:
        ax.axhline(y=0,linestyle="dashed",color="grey")    
    
    ax.set_ylabel(y)
    ax.set_xlabel("Phenotype")
    ax.set_xticks(x+(len(scores)-1)/2*width, phenotypes)
    plt.xticks(rotation=40,ha="right")

    if legend_args is None:
        legend_args ={}
    if "position" not in legend_args.keys():
        legend_args["position"] = "upper left"
        legend_args["bbox_to_anchor"] = (1,1)
    configure_legend(ax=ax,**legend_args)
    
    #ax.legend()
    #sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))

###################################################################################################################################
def _plot_all_best(dataset,phenos,scores=None,covars=None,best=None,ascending=False,y="BETA",colors=None,log=Log(),norm=True,plot_args=None,fig_args=None,errorbar_args=None):
    
    # filters only PHENO and PRS
    if covars is None:
        dataset = filter_results(dataset,phenos=phenos,scores=scores,norm=norm,log=log)
    else:
        dataset = check_formula(results=dataset, phenos=phenos,scores=scores, covars=covars, qcut=None, norm=norm,log=log)

    # total number of test for plotting
    n_total=len(dataset)

    #calculate fdr
    dataset["FDR"] = multipletests(dataset["P"], method='fdr_bh')[1]

    # select best, drop others, sort again.
    dataset = dataset.sort_values(by=best,ascending=ascending).drop_duplicates(subset=["PHENO"]).sort_values(by=[best])
    
    # if OR, convert
    if y=="OR":
        dataset["OR"] = np.exp(dataset["BETA"])
        dataset["CI_L"] = np.exp(dataset["CI_L"])
        dataset["CI_U"] = np.exp(dataset["CI_U"])
    
    # config plot options
    # figure arguments
    if fig_args is None:
        fig_args = {}
        fig_args["dpi"]=200
        fig_args["figsize"]=(dataset["PHENO"].nunique(),5)

    # figure arguments
    if plot_args is None:
        plot_args = {}
    
    if errorbar_args is None:
        errorbar_args = {}

    fig, ax = plt.subplots(**fig_args)
    # significance
    
    best_models = dataset.sort_values(by=best,ascending=ascending)
    bon = best_models["P"]<0.05/n_total
    fdr = best_models["FDR"]< 0.05
    nom = best_models["P"]< 0.05
    other = ~(bon | fdr | nom)

    bon_models = best_models.loc[bon,:].sort_values(by=[y])
    fdr_models = best_models.loc[(~bon)&(fdr),:].sort_values(by=[y])
    nom_models = best_models.loc[(~bon)&(~fdr)&(nom),:].sort_values(by=[y])
    other_models = best_models.loc[~(bon | fdr | nom),:].sort_values(by=[y])
    
    log.write("Significant models (bon): {}".format(len(bon_models)))
    log.write("Significant models (fdr but not bon): {}".format(len(fdr_models)))
    log.write("Significant models (nom but not fdr): {}".format(len(nom_models)))
    log.write("Other models: {}".format(len(other_models)))
    
    if colors is not None:
        pass

    if len(other_models)>0:
        ax.scatter(other_models["PHENO"],other_models[y],c="grey",label="nonsignficant")
    if len(nom_models)>0:
        ax.scatter(nom_models["PHENO"],nom_models[y],c="#3366FF",label="P<0.05")
    if len(fdr_models)>0:    
        ax.scatter(fdr_models["PHENO"],fdr_models[y],c="#3333CC",label="FDR<0.05")
    if len(bon_models)>0:    
        ax.scatter(bon_models["PHENO"],bon_models[y],c="#330099",label="P_Bon<0.05")
    
    if y=="BETA" or y=="OR" or  y=="HR":
        if len(other_models)>0:
            ax.errorbar(other_models["PHENO"], other_models[y],yerr=np.abs(other_models[["CI_L","CI_U"]].T - other_models[y].T ),linewidth=0, elinewidth=3,c="grey")
        if len(nom_models)>0:
            ax.errorbar(nom_models["PHENO"], nom_models[y]    ,yerr=np.abs(nom_models[["CI_L","CI_U"]].T - nom_models[y].T ),linewidth=0, elinewidth=3,c="#3366FF")
        if len(fdr_models)>0:
            ax.errorbar(fdr_models["PHENO"], fdr_models[y]    ,yerr=np.abs(fdr_models[["CI_L","CI_U"]].T - fdr_models[y].T ),linewidth=0, elinewidth=3,c="#3333CC")
        if len(bon_models)>0:
            ax.errorbar(bon_models["PHENO"], bon_models[y]    ,yerr=np.abs(bon_models[["CI_L","CI_U"]].T - bon_models[y].T ),linewidth=0, elinewidth=3,c="#330099")
    
    if y=="OR" or y=="HR":
        ax.axhline(y=1,linestyle="dashed",color="grey")
    else:
        ax.axhline(y=0,linestyle="dashed",color="grey")

    ax.legend()
    plt.xticks(rotation=40,ha="right")
    ax.set_ylabel(y)
    ax.set_xlabel("Phenotype")
    ax.legend()
    sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))

###################################################################################################################################
def _plot_proportion_per_quantile(raw_dataset,phenos,score,qcut=None,total="all",mode="bar",
                                  stat= "Proportion", cmap="Set2",cmap_head=0,cmap_tail=0,
                                  log=Log(),width=None,pheno_order=None,plot_args=None,
                                  fig_args=None, ylabel=None, xlabel=None):
    
    log.write("Start to plot propotion-per-quantile plot...")
    log.write(" -Description: grouped bar plot showing the proportion of cases for specified phenotypes in each quantitle defined by qcut; the quantile is based on the specified prs...")

    dataset = raw_dataset.loc[:,["IID",score] + phenos].copy()

    labels= [i for i in range(1, qcut+1)]
	
    dataset["_QLABEL"] = pd.qcut(dataset[score],qcut,labels=labels)
    
    if total == "all":
        ndic={ i: sum(dataset["_QLABEL"]==i) for i in range(1, qcut+1)}
    elif total =="case":
        ndic={ i: sum(dataset.loc[~dataset[i].isna(),i]==1) for i in phenos}
    
    dataset = pd.melt(dataset, id_vars=['IID','_QLABEL'], value_vars= phenos).reset_index()

    dataset = dataset.loc[dataset["value"]==1,:]    
    
    dataset = dataset.groupby(["variable","_QLABEL"]).agg("count").reset_index()

#     variable _QLABEL  index  IID  value
#0   Height_b0       1     27   27     27
#1   Height_b0       2     14   14     14
#2   Height_b0       3     10   10     10
#3   Height_b0       4     15   15     15
#4   Height_b0       5     13   13     13
#5   Height_b0       6     13   13     13
#6   Height_b0       7      6    6      6
#7   Height_b0       8      7    7      7
#8   Height_b0       9      6    6      6
#9   Height_b0      10      4    4      4
#10  Height_b1       1     17   17     17
#11  Height_b1       2     27   27     27
#12  Height_b1       3     31   31     31
    if stat == "Count":
        dataset["stat"] = dataset["value"] 
    elif stat == "Proportion":
        if total == "all":
            dataset["stat"] = dataset.apply(lambda x : x["value"] / ndic[x["_QLABEL"]],axis=1)
            dataset["n"] = dataset.apply(lambda x : ndic[x["_QLABEL"]],axis=1)
        else:
            dataset["stat"] = dataset.apply(lambda x : x["value"] / ndic[x["variable"]],axis=1)
            dataset["n"] = dataset.apply(lambda x : ndic[x["variable"]],axis=1)
#      index      IID _QLABEL   variable  value
#0         0  HG00096       1  Height_b1      1
#3         3  HG00101       5  Height_b1      1
#5         5  HG00103       9  Height_b1      1
#6         6  HG00105       4  Height_b1      1
#7         7  HG00107       4  Height_b1      1
#...     ...      ...     ...        ...    ...
#981     981  NA20822       6  Height_b2      1
#983     983  NA20827       7  Height_b2      1
    #
    
    #
#     variable _QLABEL  index  IID  value
#0   Height_b1       1     38   38     38
#1   Height_b1       2     27   27     27
#2   Height_b1       3     19   19     19
#3   Height_b1       4     23   23     23
#4   Height_b1       5     23   23     23
#5   Height_b1       6     27   27     27
#6   Height_b1       7     14   14     14
#7   Height_b1       8     17   17     17
#8   Height_b1       9     12   12     12
#9   Height_b1      10      9    9      9
#10  Height_b2       1      9    9      9
#11  Height_b2       2     21   21     21
#12  Height_b2       3     27   27     27
#13  Height_b2       4     22   22     22
#14  Height_b2       5     26   26     26
#15  Height_b2       6     21   21     21
#16  Height_b2       7     31   31     31
#17  Height_b2       8     31   31     31
#18  Height_b2       9     36   36     36
#19  Height_b2      10     39   39     39

    # config plot options
    plot_args = configure_plot_args(plot_args)
    fig_args  = configure_fig_args(fig_args ,width = qcut)
    output_hex_colors = configure_colors(n=dataset["variable"].nunique(), cmap_head=cmap_head, cmap=cmap, cmap_tail=cmap_tail )
    
    fig, ax = plt.subplots(layout='constrained',**fig_args)
    if mode=="bar":

        x = np.arange(qcut)
        multiplier=0
        if width is None:
            width= 1/(dataset["variable"].nunique()+2)
        if pheno_order is None:
            pheno_order = sorted(list(dataset["variable"].unique()))
        log.write(" -plotting phenotypes: {}".format(",".join(pheno_order)))
        for i, pheno in enumerate(pheno_order):
            offset=width * multiplier
            target_single = (dataset["variable"]==pheno)
            to_plot = dataset.loc[target_single,:].sort_values(by=["_QLABEL"])
            rects = ax.bar(x+offset, to_plot["stat"],width, label=pheno, color = output_hex_colors[i])
            multiplier+=1

            ax.set_xticks(x+(dataset["variable"].nunique()-1)/2*width, range(1, qcut+1))
            ax.legend()
            #sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))
            plt.xticks(rotation=40,ha="right")

    elif mode=="scatter":
        x = np.arange(qcut)
        if pheno_order is None:
            pheno_order = sorted(list(dataset["variable"].unique()))
        log.write(" -plotting phenotypes: {}".format(",".join(pheno_order)))
        for i, pheno in enumerate(pheno_order):
            target_single = (dataset["variable"]==pheno)
            to_plot = dataset.loc[target_single,:].sort_values(by=["_QLABEL"])
            rects = ax.scatter(x, to_plot["stat"], width, label=pheno, color = output_hex_colors[i])

            #ax.set_xticks(x+(dataset["variable"].nunique()-1)/2*width, range(1, qcut+1))
            ax.legend()
            #sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))   
    
    if ylabel is None:
        ax.set_ylabel(stat)
    else:
        ax.set_ylabel(ylabel)
    if xlabel is None:
        ax.set_xlabel("Polygenic risk score quantitle \n {}".format(score))
    else:
        ax.set_xlabel(xlabel)

    dataset = dataset.drop(columns=["index","IID"])
    dataset["PRS"] = score
    return dataset

def _plot_bar(dataset,phenos,scores,covars,y="BETA",log=Log(),norm=True,plot_args=None,fig_args=None,interval=2,cmap="Set2",width=None):

    try:
        target = (dataset["PHENO"].isin(phenos))&(dataset["Q_SCORE"].isna())&(dataset["NORM"]==norm)&(dataset["PRS"].isin(scores))
    except:
        target = (dataset["PHENO"].isin(phenos))&(dataset["NORM"]==norm)&(dataset["PRS"].isin(scores))
    dataset = dataset.loc[target,:].copy().sort_values(by=["PHENO","PRS"])
    
    # config plot options
    if plot_args is None:
        plot_args = {}

    if fig_args is None:
        fig_args = {}
        fig_args["dpi"]=200
        fig_args["figsize"]=(dataset["PHENO"].nunique(),5)

    fig, ax = plt.subplots(**fig_args)

    if y=="OR":
        dataset["OR"] = np.exp(dataset["BETA"])
        dataset["CI_L"] = np.exp(dataset["CI_L"])
        dataset["CI_U"] = np.exp(dataset["CI_U"])
    
    phenotypes = list(dataset["PHENO"].unique())
    phenotypes.sort()

    colors_num = dataset["PRS"].nunique()
    cmap_to_use = plt.cm.get_cmap(cmap)
    if cmap_to_use.N >100:
        rgba = cmap_to_use([i /colors_num  for i in range(colors_num)])
    else:
        rgba = cmap_to_use(range(colors_num))
    
    output_hex_colors=[]
    for i in range(len(rgba)):
        output_hex_colors.append(mc.to_hex(rgba[i]))
    output_hex_colors


    x=np.arange(len(phenotypes))

    if width is None:
        width= 1/(len(scores)+2)

    multiplier=0
    for i, model in enumerate(dataset["PRS"].unique()):
        offset=width * multiplier
        target_single = (dataset["PRS"]==model)
        to_plot = dataset.loc[target_single,:].sort_values(by=["PHENO","PRS"])
        rects=ax.bar(x+offset,to_plot[y],width, label=model, color = output_hex_colors[i])
        multiplier+=1

    ax.set_ylabel(y)
    ax.set_xlabel("Phenotypes")
    
    if y=="OR" or y=="HR":
        ax.axhline(y=1,linestyle="dashed",color="grey")
    else:
        ax.axhline(y=0,linestyle="dashed",color="grey")
    
    ax.set_xticks(x+(len(scores)-1)/2*width, phenotypes)
    ax.legend()
    sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))
    plt.xticks(rotation=40,ha="right")

def _plot_heatmap(dataset,phenos,scores=None,covars=None,best=None,colors=None,
                  y="BETA",log=Log(),norm=True,
                  plot_args=None,fig_args=None,
                  errorbar_args=None,sig_level=0.05):
    
    if fig_args is None:
        width = len(scores)
        height = len(phenos)
        fig_args = {"figsize":(width, height),"dpi":500}
    else:
        for key,value in fig_args.items():
            fig_args[key] = value

    if plot_args is None:
        plot_args = {"cmap":"RdBu","center":0}
    else:
        for key,value in plot_args.items():
            plot_args[key] = value
    
    dataset = check_formula(results=dataset, phenos=phenos,scores=scores, covars=covars, qcut=None, norm=norm,log=log)
    
    dataset["P_BON"] = dataset["P"] * len(dataset)
    dataset["FDR"] = multipletests(dataset["P"],method="fdr_bh")[1]

    dataset.loc[dataset["P"]<sig_level,"P_ANNOT"] = "*"
    dataset.loc[dataset["FDR"]<sig_level,"P_ANNOT"] = "**" 
    dataset.loc[dataset["P_BON"]<sig_level,"P_ANNOT"] = "***" 

    y_matrix = dataset.pivot(index="PHENO",columns="PRS",values=y)
    panno_matrix = dataset.pivot(index="PHENO",columns="PRS",values="P_ANNOT")

    fig, ax = plt.subplots(**fig_args)
    sns.heatmap(y_matrix,annot=panno_matrix,fmt="s",ax=ax,**plot_args)
    ax.set_ylabel("Phenotype")
    ax.set_xlabel("PRS model")


def _plot_ratio_per_quantile(raw_dataset,phenos,score,ratios,qcut=None,total="all",mode="bar",
                                  stat= "Proportion", cmap="Set2",cmap_head=0,cmap_tail=0,
                                  log=Log(),width=None,pheno_order=None,plot_args=None,
                                  fig_args=None, ylabel=None, xlabel=None):
    
    log.write("Start to plot propotion-per-quantile plot...")
    log.write(" -Description: grouped bar plot showing the proportion of cases for specified phenotypes in each quantitle defined by qcut; the quantile is based on the specified prs...")

    dataset = raw_dataset.loc[:,["IID",score] + phenos].copy()

    labels= [i for i in range(1, qcut+1)]
	
    dataset["_QLABEL"] = pd.qcut(dataset[score], qcut, labels=labels)

    
    if total == "all":
        ndic={ i: sum(dataset["_QLABEL"]==i) for i in range(1, qcut+1)}
    elif total =="case":
        ndic={ i: sum(dataset.loc[~dataset[i].isna(),i]==1) for i in phenos}
    
    dataset = pd.melt(dataset, id_vars=['IID','_QLABEL'], value_vars= phenos).reset_index()

    dataset = dataset.loc[dataset["value"]==1,:]    
    
    dataset = dataset.groupby(["variable","_QLABEL"]).agg("count").reset_index().sort_values(by=["variable","_QLABEL"])

    dataset_ratios = dataset.loc[dataset["variable"] == phenos[0],["_QLABEL"]].reset_index()
    
    ratio_strings = []
    for i in ratios:
        ratio_string = "{}_{}".format(i[0],i[1])
        ratio_strings.append(ratio_string)    
        dataset_ratios[ratio_string] = dataset.loc[dataset["variable"] == i[0],"value"].values / dataset.loc[dataset["variable"] ==i[1],"value"].values
    print(dataset_ratios)
#     variable _QLABEL  index  IID  value
#0   Height_b0       1     27   27     27
#1   Height_b0       2     14   14     14
#2   Height_b0       3     10   10     10
#3   Height_b0       4     15   15     15
#4   Height_b0       5     13   13     13
#5   Height_b0       6     13   13     13
#6   Height_b0       7      6    6      6
#7   Height_b0       8      7    7      7
#8   Height_b0       9      6    6      6
#9   Height_b0      10      4    4      4
#10  Height_b1       1     17   17     17
#11  Height_b1       2     27   27     27
#12  Height_b1       3     31   31     31
    #if stat == "Count":
    #    dataset["stat"] = dataset["value"] 
    #elif stat == "Proportion":
    #    if total == "all":
    #        dataset["stat"] = dataset.apply(lambda x : x["value"] / ndic[x["_QLABEL"]],axis=1)
    #        dataset["n"] = dataset.apply(lambda x : ndic[x["_QLABEL"]],axis=1)
    #    else:
    #        dataset["stat"] = dataset.apply(lambda x : x["value"] / ndic[x["variable"]],axis=1)
    #        dataset["n"] = dataset.apply(lambda x : ndic[x["variable"]],axis=1)
#      index      IID _QLABEL   variable  value
#0         0  HG00096       1  Height_b1      1
#3         3  HG00101       5  Height_b1      1
#5         5  HG00103       9  Height_b1      1
#6         6  HG00105       4  Height_b1      1
#7         7  HG00107       4  Height_b1      1
#...     ...      ...     ...        ...    ...
#981     981  NA20822       6  Height_b2      1
#983     983  NA20827       7  Height_b2      1
    #
    
    #
#     variable _QLABEL  index  IID  value
#0   Height_b1       1     38   38     38
#1   Height_b1       2     27   27     27
#2   Height_b1       3     19   19     19
#3   Height_b1       4     23   23     23
#4   Height_b1       5     23   23     23
#5   Height_b1       6     27   27     27
#6   Height_b1       7     14   14     14
#7   Height_b1       8     17   17     17
#8   Height_b1       9     12   12     12
#9   Height_b1      10      9    9      9
#10  Height_b2       1      9    9      9
#11  Height_b2       2     21   21     21
#12  Height_b2       3     27   27     27
#13  Height_b2       4     22   22     22
#14  Height_b2       5     26   26     26
#15  Height_b2       6     21   21     21
#16  Height_b2       7     31   31     31
#17  Height_b2       8     31   31     31
#18  Height_b2       9     36   36     36
#19  Height_b2      10     39   39     39

    # config plot options
    plot_args = configure_plot_args(plot_args)
    fig_args  = configure_fig_args(fig_args ,width = qcut)
    output_hex_colors = configure_colors(n=len(ratio_strings), cmap_head=cmap_head, cmap=cmap, cmap_tail=cmap_tail )
    
    fig, ax = plt.subplots(layout='constrained',**fig_args)
    if mode=="bar":

        x = np.arange(qcut)
        multiplier=0
        if width is None:
            width= 1/(len(ratio_strings)+2)
        if pheno_order is None:
            pheno_order = sorted(ratio_strings)
        log.write(" -plotting phenotypes: {}".format(",".join(pheno_order)))
        for i, pheno in enumerate(pheno_order):
            offset=width * multiplier
            to_plot = dataset_ratios[pheno]
            #to_plot = dataset.loc[target_single,:].sort_values(by=["_QLABEL"])
            rects = ax.bar(x+offset, to_plot, width, label=pheno, color = output_hex_colors[i])
            multiplier+=1

            ax.set_xticks(x+(len(ratio_strings)-1)/2*width, range(1, qcut+1))
            ax.legend()
            #sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))
            plt.xticks(rotation=40,ha="right")

    #elif mode=="scatter":
    #    x = np.arange(qcut)
    #    if pheno_order is None:
    #        pheno_order = sorted(list(dataset["variable"].unique()))
    #    log.write(" -plotting phenotypes: {}".format(",".join(pheno_order)))
    #    for i, pheno in enumerate(pheno_order):
    #        target_single = (dataset["variable"]==pheno)
    #        to_plot = dataset.loc[target_single,:].sort_values(by=["_QLABEL"])
    #        rects = ax.scatter(x, to_plot["stat"], width, label=pheno, color = output_hex_colors[i])
#
    #        #ax.set_xticks(x+(dataset["variable"].nunique()-1)/2*width, range(1, qcut+1))
    #        ax.legend()
    #        #sns.move_legend(ax,"upper left", bbox_to_anchor=(1, 1))   
    
    if ylabel is None:
        ax.set_ylabel(stat)
    else:
        ax.set_ylabel(ylabel)
    if xlabel is None:
        ax.set_xlabel("Polygenic risk score quantitle \n {}".format(score))
    else:
        ax.set_xlabel(xlabel)

    dataset = dataset.drop(columns=["index","IID"])
    dataset["PRS"] = score
    return dataset
