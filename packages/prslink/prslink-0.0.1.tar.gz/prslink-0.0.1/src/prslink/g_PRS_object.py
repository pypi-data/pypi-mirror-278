import pandas as pd
import numpy as np
from prslink.io_load_data import _load_data
#from prslink.loadplink import _load_plink2
#from prslink.loadplink import _load_plink1
from prslink.io_load_plink import _load_plink
from prslink.model_evaluate import _evaluate
from prslink.model_evaluate import _evaluate_q
from prslink.visualization import _plot_prs
from prslink.visualization import _plot_roc
from prslink.visualization import _plot_q
from prslink.visualization import _plot_all
from prslink.visualization import _plot_bar
from prslink.visualization import _plot_all_best
from prslink.visualization import _plot_heatmap
from prslink.visualization import _plot_proportion_per_quantile
from prslink.visualization import _plot_ratio_per_quantile
from prslink.g_Log import Log
from prslink.g_version import _show_version

class PRS():
	
	def __init__(self):
		# init a Log object
		self.log = Log()
		
		_show_version(log=self.log)

		self.data = pd.DataFrame(columns=["IID"])
		self.pheno_cols = list()
		self.score_cols = list()
		self.covar_cols = list()

		# binary triat population prevalence
		self.pheno_K = dict()
		self.pheno_type = dict()
		
		# binary and quant models
		self.bmodels  = dict()
		self.qmodels  = dict()
		
		# binary and quant results
		self.bresults = pd.DataFrame()
		self.qresults = pd.DataFrame()
		
		
		
	def summary(self):
		pass

	# view data
	def phenos(self):
		return self.data.loc[:, ["IID"] + self.pheno_cols]
	def scores(self):
		return self.data.loc[:, ["IID"] + self.score_cols]
	def covars(self):
		return self.data.loc[:, ["IID"] + self.covar_cols]

	## add data
	def add_score(self, path,iid, scores, names=list(), match_dict=[pd.DataFrame(),"_ID_TO_CONVERT","_ID_MAIN"],**arg):
		mode= "score"
		self.data, self.score_cols = _load_data(dataset = self.data, 
							score_list = self.score_cols, 
							mode = mode, 
							path = path, 
							iid = iid, 
							scores = scores, 
							names = names,
							match_dict = match_dict,
							log=self.log,
							**arg)
	
	def add_pheno(self, path,iid, phenos, names=list(), match_dict=[pd.DataFrame(),"_ID_TO_CONVERT","_ID_MAIN"], types="Q",  **arg):	
		mode= "pheno"
		self.data, self.pheno_cols, pheno_types  = _load_data(dataset = self.data, 
									score_list = self.pheno_cols, 
									mode = mode, 
									path = path, 
									iid = iid, 
									scores = phenos, 
									names = names, 
									types = types,
									match_dict=match_dict,
									log=self.log,
									**arg)
		self.pheno_type.update(pheno_types)

	def add_covar(self, path,iid, covars, names=list(),match_dict=[pd.DataFrame(),"_ID_TO_CONVERT","_ID_MAIN"],**arg):
		mode= "covar"
		self.data, self.covar_cols = _load_data(dataset = self.data, 
							score_list = self.covar_cols, 
							mode = mode, 
							path = path, 
							iid = iid, 
							scores = covars, 
							names = names,
							match_dict = match_dict,
							log=self.log,
							**arg)
	
	def add_plink(self, path, name="SCORE", avg=False , version="PLINK2", **arg):
		self.data, self.score_cols = _load_plink(dataset = self.data, 
							score_list = self.score_cols, 
							path = path,
							name = name,
							avg = avg,
							version = version,
							log=self.log,
							**arg)
	def add_plink2(self, path, name="SCORE", avg=False ,**arg):
		self.data, self.score_cols = _load_plink(dataset = self.data, 
							score_list = self.score_cols, 
							path = path,
							name = name,
							avg = avg,
							version = "PLINK2",
							log=self.log,
							**arg)
	def add_plink1(self, path, name="SCORE", avg=False ,**arg):
		self.data, self.score_cols = _load_plink(dataset = self.data, 
							score_list = self.score_cols, 
							path = path,
							name = name,
							avg = avg,
							version = "PLINK1.9",
							log=self.log,
							**arg)

	def set_k(self, dic):
		for key,value in dic.items():
			self.pheno_K[key] = value

	## functions
	def evaluate(self,phenos,scores,covars,r2_lia=False,norm=True):
		
		# results for binary phenotypes, 
		# results for quantative phenotypes,
		# fitted binary models
		# fitted quantative models

		bresults,qresults,bmodels,qmodels = _evaluate(self.data,
							phenos = phenos,
							scores = scores,
							covars = covars,
							r2_lia = r2_lia,
							pheno_K =self.pheno_K,
							norm=norm,
							log=self.log)
		
		# update the object attributes
		self.bresults=pd.concat([self.bresults,bresults],ignore_index=True).drop_duplicates() 
		self.qresults=pd.concat([self.qresults,qresults],ignore_index=True).drop_duplicates() 
		self.bmodels.update(bmodels)
		self.qmodels.update(qmodels)

		# return the current run results
		return pd.concat([bresults,qresults],ignore_index=True)
	def evaluate_q(self,phenos,qscore,covars,qcut,qref=1,r2_lia=False,norm=False):
		
		# results for binary phenotypes, 
		# results for quantative phenotypes,
		# fitted binary models
		# fitted quantative models
		scores = [qscore]
		bresults,qresults,bmodels,qmodels = _evaluate_q(self.data,
							phenos = phenos,
							scores = scores,
							covars = covars,
							r2_lia = r2_lia,
							pheno_K =self.pheno_K,
							qcut=qcut,
							qref=qref,
							qscore=qscore,
							norm=norm,
							log=self.log)
		
		# update the object attributes
		self.bresults=pd.concat([self.bresults,bresults],ignore_index=True).drop_duplicates() 
		self.qresults=pd.concat([self.qresults,qresults],ignore_index=True).drop_duplicates() 
		self.bmodels.update(bmodels)
		self.qmodels.update(qmodels)

		# return the current run results
		return pd.concat([bresults,qresults],ignore_index=True)
	
	def plot_q(self,phenos,qscore,covars, qcut=10,qref=1, y="BETA",norm=False,colors=None,plot_args=None,fig_args=None,errorbar_args=None,offset_multiplier=2,**args):
		
		# results for binary phenotypes, 
		# results for quantative phenotypes,
		# fitted binary models
		# fitted quantative models
		result = pd.concat([self.bresults,self.qresults],ignore_index=True).drop_duplicates() 
		scores = [qscore]
		_plot_q(result,
	           phenos=phenos,
			  qscore=qscore,
			  covars=covars,
			  qcut=qcut,
			  qref=qref,
			  y=y,
			  norm=norm,
			  plot_args = plot_args,
			  fig_args = fig_args,
			  errorbar_args=errorbar_args,
			  colors=colors,
			  log=self.log,
			  offset_multiplier=offset_multiplier,
			  **args)
	def plot_proportion_per_quantile(self,phenos,score,qcut=None,plot_args=None,fig_args=None,**args):
		dataset = _plot_proportion_per_quantile(raw_dataset=self.data,
							   phenos=phenos,
							   score=score,
							   qcut=qcut,
							   log=self.log,
							   plot_args=plot_args,
							   fig_args=fig_args,
							   **args)
		return dataset
	def plot_ratio_per_quantile(self,phenos,score,ratios,qcut=None,plot_args=None,fig_args=None,**args):
		dataset = _plot_ratio_per_quantile(raw_dataset=self.data,
							   phenos=phenos,
							   score=score,
							   ratios=ratios,
							   qcut=qcut,
							   log=self.log,
							   plot_args=plot_args,
							   fig_args=fig_args,
							   **args)
	def plot_all(self,phenos,scores,covars, y="BETA",norm=True,colors=None,plot_args=None,fig_args=None,errorbar_args=None,width=None,**args):
		
		# results for binary phenotypes, 
		# results for quantative phenotypes,
		# fitted binary models
		# fitted quantative models

		result = pd.concat([self.bresults,self.qresults],ignore_index=True).drop_duplicates() 
		_plot_all(result,
	           phenos=phenos,
			  scores=scores,
			  covars=covars,
			  y=y,
			  norm=norm,
			  plot_args = plot_args,
			  fig_args = fig_args,
			  errorbar_args=errorbar_args,
			  colors=colors,
			  width=width,
			  log=self.log,
			  **args)

	
	def plot_all_best(self,phenos,scores=None,covars=None,best="P",ascending=True, y="BETA",colors=None,norm=True,plot_args=None,fig_args=None,errorbar_args=None,**args):
		
		# results for binary phenotypes, 
		# results for quantative phenotypes,
		# fitted binary models
		# fitted quantative models
		
		if scores is None:
			scores = self.score_cols
		if covars is None:
			covars = self.covar_cols

		result = pd.concat([self.bresults,self.qresults],ignore_index=True).drop_duplicates() 
		
		_plot_all_best(result,
	           phenos=phenos,
			  scores=scores,
			  covars=covars,
			  y=y,
			  best=best,
			  ascending=ascending,
			  norm=norm,
			  plot_args = plot_args,
			  fig_args = fig_args,
			  errorbar_args=errorbar_args,
			  colors=colors,
			  log=Log(),**args)
	
	def plot_bar(self,phenos,scores,covars, y="BETA",norm=True,plot_args=None,fig_args=None,**arg):
		result = pd.concat([self.bresults,self.qresults],ignore_index=True).drop_duplicates() 
		# results for binary phenotypes, 
		# results for quantative phenotypes,
		# fitted binary models
		# fitted quantative models
		_plot_bar(result,
	           phenos=phenos,
			  scores=scores,
			  covars=covars,
			  y=y,
			  norm=norm,
			  plot_args = plot_args,
			  fig_args = fig_args,
			  log=Log(),
			  **arg)	

	def plot_heatmap(self,phenos,scores=None,covars=None,best=None,colors=None,y="BETA",log=Log(),norm=True,plot_args=None,fig_args=None,errorbar_args=None,sig_level=0.05,**args):
		result = pd.concat([self.bresults,self.qresults],ignore_index=True).drop_duplicates() 
		_plot_heatmap(result,
	           phenos=phenos,
			  scores=scores,
			  covars=covars,
			  y=y,
			  norm=norm,
			  plot_args = plot_args,
			  fig_args = fig_args,
			  errorbar_args=errorbar_args,
			  colors=colors,
			  log=Log(),
			  sig_level=sig_level,**args)

	def plot_roc(self,phenos,scores,covars,**args):
		_plot_roc(self.data, phenos,scores,covars,**args)
		
	def auc_roc(self):
		pass
	def plot_prs(self, scores,**args):
		_plot_prs(self.data, scores, **args)
