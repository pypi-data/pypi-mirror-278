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
import matplotlib.colors as mc

def configure_fig_args(fig_args, dpi=360, width=5, height=5, log=Log()):
    if fig_args is None:
        fig_args = {}
        fig_args["dpi"]=dpi
        fig_args["figsize"]=(width,height)
    log.write(" -Figure args: {}".format(fig_args))
    return fig_args

def configure_plot_args(plot_args, log=Log()):
    if plot_args is None:
        plot_args = {}
    log.write(" -Plot args: {}".format(plot_args))
    return plot_args

def configure_errorbar_args():
    pass

def configure_colors(n, cmap="turbo", cmap_head=0, cmap_tail=0,log=Log()):
    colors_num = n + cmap_head + cmap_tail
    cmap_to_use = plt.cm.get_cmap(cmap)

    log.write(" -Color map: {}".format(cmap))
    log.write(" -Color number: {} (head: {}; tail: {})".format(colors_num, cmap_head, cmap_tail))
    
    if cmap_to_use.N >100:
        numbers = [i /(colors_num -1)  for i in range(colors_num)]
        rgba = cmap_to_use(numbers)
    else:
        numbers = range(colors_num)
        rgba = cmap_to_use(numbers)
    log.write(" -Color map norm: {}".format(numbers))
    output_hex_colors=[]
    
    for i in range(cmap_head, len(rgba)-cmap_tail):
        output_hex_colors.append(mc.to_hex(rgba[i]))
    log.write(" -Color to use: {}".format(output_hex_colors))
    return output_hex_colors

def configure_legend(ax, position=None, **legend_args):
    
    ax.legend(**legend_args)
    
    if position is not None:
        sns.move_legend(ax, position, **legend_args)
    return ax