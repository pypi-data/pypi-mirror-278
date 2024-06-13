import statsmodels.api as sm
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from prslink.util_r2_conversion import r2_obs_to_r2_lia
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from prslink.g_Log import Log

def _evaluate(dataset, 
	       	phenos, 
			scores, 
			covars, 
			r2_lia=False, 
			pheno_K=dict(), 
			sortby=["PHENO","Delta_R2"],
			norm=True,
			log=Log()):
	log.write("Strat to evaluate PRS performance...")
	dataset = dataset.copy()

	# initiate DataFrame and determine datatype for both quantitative trait and binary traits
	qdtype, qresults = get_dtype_df("Q")
	bdtype, bresults = get_dtype_df("B",r2_lia=r2_lia)
	
	# initiate a dictonay to strore the fitted models
	bmodels=dict()
	qmodels=dict()

	covars = sorted(covars)
	# for each phenotype
	for pheno in phenos:
		
		# extract data for checking
		cols_to_check = [pheno] +scores+ covars

		# extract a slice of the needed data
		to_check = dataset.loc[~dataset[pheno].isna(),cols_to_check]
		
		# dropna
		to_check = to_check.dropna()
		
		# quantitative ###################################################################################
		if pd.api.types.is_float_dtype(to_check.loc[:,pheno]):
			qmodels[pheno] = dict()
			qresults = _evaluate_quantitative(to_check = to_check, 
				     						pheno = pheno, 
											scores = scores, 
											covars = covars, 
											qmodels = qmodels, 
											qdtype =qdtype,
											qresults = qresults,
											norm=norm,
											log=log)
		else:
		# binary###################################################################################
			bmodels[pheno] = dict()
			bresults = _evaluate_binary(to_check = to_check, 
			       						pheno = pheno, 
										scores = scores, 
										covars =covars, 
										r2_lia =r2_lia, 
										pheno_K =pheno_K, 
										bmodels =bmodels, 
										bdtype =bdtype,
										bresults = bresults,
										norm=norm,
										log=log )
	log.write(" - Fitted models have been stored into .bmodels and .qmodels")
	log.write(" - Results have been stored into .bresults and .qresults")
	log.write("Finished evaluating PRS performance...")
	return bresults.sort_values(by=sortby), qresults.sort_values(by=sortby), bmodels, qmodels

def _evaluate_q(dataset, 
	       	phenos, 
			scores, 
			covars, 
			qscore,
			qcut=10,
			r2_lia=False, 
			pheno_K=dict(), 
			sortby=["PHENO","Delta_R2"],
			norm=True,
			qref=1,
			log=Log()):

	dataset = dataset.copy()

	# initiate DataFrame and determine datatype for both quantitative trait and binary traits
	qdtype, qresults = get_dtype_df("Q")
	bdtype, bresults = get_dtype_df("B",r2_lia=r2_lia)
	
	# initiate a dictonay to strore the fitted models
	bmodels=dict()
	qmodels=dict()
	
	covars = sorted(covars)
	
	qcut_list = None
	if type(qcut) is int:
		# labels = [1,2,3 ... , 10]
		labels= [i for i in range(1, qcut+1)]
		dataset["_QLABEL"] = pd.qcut(dataset[qscore],qcut,labels=labels)
		qcut_list = str(qcut)
	else:
		labels= ['({},{})'.format(qcut[i],qcut[i+1]) for i in range(len(qcut)-1)]
		dataset["_QLABEL"] = pd.qcut(dataset[qscore],qcut,labels=labels)
		qcut_list = ",".join(map(str, qcut.copy()))
		qcut = len(labels)

	for i in range(1,len(labels)+1):
		qcut_current = i

		# extract ref and current q
		dataset_q = dataset.loc[(dataset["_QLABEL"]==labels[qref-1])|(dataset["_QLABEL"]==labels[i-1]),:].copy()

		log.write(' -qscore :{} ({}-{})'.format( qscore, qcut_current, qcut))
		# for each phenotype
		for pheno in phenos:
			
			# extract data for checking
			cols_to_check = [pheno] +scores+ covars +["_QLABEL"]

			# extract a slice of the needed data
			to_check = dataset_q.loc[~dataset_q[pheno].isna(),cols_to_check]
			
			# dropna
			to_check = to_check.dropna()
			
			# quantitative ###################################################################################
			if pd.api.types.is_float_dtype(to_check.loc[:,pheno]):
				qmodels[pheno] = dict()
				qresults = _evaluate_quantitative(to_check = to_check, 
												pheno = pheno, 
												scores = scores, 
												covars = covars, 
												qmodels = qmodels, 
												qdtype =qdtype,
												qresults = qresults,
												qcut_current=qcut_current,
												qcut=qcut,
												qscore=qscore,
												qcut_list=qcut_list,
												norm=norm,
												qref=qref,
												log=log)
			else:
			# binary###################################################################################
				bmodels[pheno] = dict()
				bresults = _evaluate_binary(to_check = to_check, 
											pheno = pheno, 
											scores = scores, 
											covars =covars, 
											r2_lia =r2_lia, 
											pheno_K =pheno_K, 
											bmodels =bmodels, 
											bdtype =bdtype,
											bresults = bresults,
											qcut_current=qcut_current,
											qcut=qcut,
											qscore=qscore,
											qcut_list=qcut_list,
											norm=norm,
											qref=qref,
											log=log )

	return bresults.sort_values(by=sortby), qresults.sort_values(by=sortby), bmodels, qmodels



def _evaluate_quantitative(to_check, pheno, scores, covars, qmodels, qdtype,qresults,log, norm=True, qcut_current=None, qcut=None,qscore=None,qcut_list=None,qref=1):
    
	# null model
	y = to_check[[pheno]]
	x = to_check.loc[:,covars]

	# statsmodel, add intercept
	x = sm.add_constant(x)
	mod = sm.OLS(y,x).fit()
	formula = "{}~{}".format(pheno, "+".join(covars))
	if qcut is not None:
		formula = formula +'({}-{}-{})[{}]'.format(qref, qcut_current, qcut, qcut_list)
	log.write(" - Fitting Null Linear : {}".format(formula))
	null_formula = formula
	# store null model
	#if pheno not in qmodels.keys():
#		qmodels[pheno] = {}
	qmodels[pheno][formula] = mod
	
	# rsq for null model
	r2_null = mod.rsquared


	# evaluate each PRS
	for score in scores:

		formula = "{}~{}+{}".format(pheno, score, "+".join(covars))
		
		if qcut is not None:
			formula = formula +'({}-{}-{})[{}]'.format(qref, qcut_current, qcut, qcut_list)
		log.write(" - Fitting Full Linear : {}".format(formula))
		
		if qcut is not None:
			if qcut_current!=qref:
				to_check.loc[to_check["_QLABEL"]==qref,score] = 0
				to_check.loc[to_check["_QLABEL"]==qcut_current,score] = 1
			else:
				row_dict={   "PHENO":pheno,
					"PRS":score,
					"TYPE": "Q",
					"N":len(y),
					"BETA":0,
					"SE":0,
					"CI_L":None,
					"CI_U":None,
					"P":None,
					"R2_null": None,
					"R2_full": None,
					"Delta_R2": None,
					"NULL_formula": null_formula,
					"FULL_formula":formula,
					"NORM":norm}
				row_dict["Q"]=qcut_current
				row_dict["Q_SCORE"]=qscore
				row_dict["Q_REF"]=qref
				row = pd.Series(row_dict).to_frame().T.astype(qdtype)
				qresults = pd.concat([qresults, row],ignore_index=True)
				continue

		# full model
		x = to_check.loc[:,covars+[score]]
		
		## normalize score
		x[score] = normalize_x(x, score, norm)	
		
		# statsmodel, add intercept
		x = sm.add_constant(x)
		mod = sm.OLS(y,x).fit()
		
		# store full model
		qmodels[pheno][formula] = mod
		
		# rsq for full model
		r2_full = mod.rsquared
		
		row_dict={   "PHENO":pheno,
						"PRS":score,
						"TYPE": "Q",
						"N":len(y),
						"BETA":mod.params[score],
						"SE":mod.bse[score],
						"CI_L":mod.conf_int().loc[score,0],
						"CI_U":mod.conf_int().loc[score,1],
						"P":mod.pvalues[score],
						"R2_null": r2_null,
						"R2_full": r2_full,
						"Delta_R2": r2_full - r2_null,
						"NULL_formula": null_formula,
						"FULL_formula":formula,
						"NORM":norm}
		
		if qcut is not None:
			row_dict["Q"]=qcut_current
			row_dict["Q_SCORE"]=qscore
			row_dict["Q_REF"]=qref
		# format the row dictionary to a dataframe 
		row = pd.Series(row_dict).to_frame().T.astype(qdtype)

		# add the results to the predefined dataframe
		qresults = pd.concat([qresults, row],ignore_index=True)
	
	return qresults

def _evaluate_binary(to_check, pheno, scores, covars, r2_lia, pheno_K, bmodels, bdtype,bresults,log, norm=True,qcut_current=None,qcut=None,qscore=None,qcut_list=None,qref=1):
	# extract only binary phenotype reconds
	is_binary = ~to_check[pheno].isna() 
	y = to_check.loc[is_binary,pheno].astype("int64")
	x = to_check.loc[is_binary,covars].astype("float64")
	#clf0 = LogisticRegression(fit_intercept=True,solver="lbfgs", random_state=0,penalty='none').fit(x, y.values.ravel())
	#auc0 = roc_auc_score(y, clf0.predict_proba(x)[:, 1])

	# statsmodel, add intercept
	x = sm.add_constant(x)
	mod = sm.Logit(y,x).fit()

	formula = "{}~{}".format(pheno, "+".join(covars))
	if qcut is not None:
		formula = formula +'({}-{}-{})[{}]'.format(qref, qcut_current, qcut, qcut_list)
	log.write(" - Fitting Null Logistic: {}".format(formula))
	null_formula = formula

	# store null model
	#if pheno not in bmodels.keys():
	#	bmodels[pheno] = {}
	bmodels[pheno][formula] = mod

	# calculate ROC for null model
	auc0 = roc_auc_score(y, mod.predict(x))
	
	# if r2_lia==True, calculate liability-scaled rsq
	if r2_lia:
		mod_OLS = sm.OLS(y,x).fit()
		r2_obs_null = mod_OLS.rsquared

	# calculate nagelkerke rsq
	prsq_nage_null = (1 - np.exp((mod.llnull - mod.llf) * (2 / mod.nobs))) / (1 - np.exp( mod.llnull * (2 / mod.nobs)))

	


	for score in scores:
		formula = "{}~{}+{}".format(pheno, score, "+".join(covars))
		if qcut is not None:
			formula = formula +'({}-{}-{})[{}]'.format(qref, qcut_current, qcut, qcut_list)
		log.write(" - Fitting Full Logistic : {}".format(formula))
		
		if qcut is not None:
			if qcut_current!=qref:
				to_check.loc[to_check["_QLABEL"]==qref,score] = 0
				to_check.loc[to_check["_QLABEL"]==qcut_current,score] = 1
			else:
				row_dict = { "PHENO":pheno,
					"PRS":score,
					"TYPE": "B",
					"N_CASE": len(to_check.loc[to_check[pheno]==1,:]),
					"N":len(y),
					"BETA":0,
					"SE":0,
					"CI_L":None,
					"CI_U":None,
					"P":None,
					"R2_null": None,
					"R2_full": None,
					"Delta_R2": None,
					"AUC_null": None ,
					"AUC_full": None ,
					"Delta_AUC": None ,
					"NULL_formula": null_formula,
					"FULL_formula":formula,
					"NORM":norm}
				if r2_lia:
					row_dict["R2_lia_null"] = None
					row_dict["R2_lia_full"] = None
					row_dict["Delta_R2_lia"] = None
				row_dict["Q"]=qcut_current
				row_dict["Q_SCORE"]=qscore
				row_dict["Q_REF"]=qref
				if qcut_list is not None:
					row_dict["Q_INTERVAL"]=qcut_list
				row = pd.Series(row_dict).to_frame().T.astype(bdtype)
				bresults = pd.concat([bresults, row],ignore_index=True)
				continue

		# full model
		x = to_check.loc[to_check[pheno].isin([0,1]),covars+[score]]
		
		# normalize score
		x[score] = normalize_x(x, score, norm)	

		#clf1 = LogisticRegression(fit_intercept=True,solver="lbfgs", random_state=0,penalty='none').fit(x, y.values.ravel())
		#auc1 = roc_auc_score(y, clf1.predict_proba(x)[:, 1])

		
		# statsmodel, add intercept
		x = sm.add_constant(x)
		mod = sm.Logit(y,x).fit()
		
		bmodels[pheno][formula] = mod
		
		# calculate ROC for full model
		auc1 = roc_auc_score(y, mod.predict(x))

		if r2_lia:
			mod_OLS = sm.OLS(y,x).fit()
			r2_obs_full = mod_OLS.rsquared
			
		prsq_nage_full = (1 - np.exp((mod.llnull - mod.llf) * (2 / mod.nobs))) / (1 - np.exp( mod.llnull * (2 / mod.nobs)))
		row_dict = {   "PHENO":pheno,
						"PRS":score,
						"TYPE": "B",
						"N_CASE": len(to_check.loc[to_check[pheno]==1,:]),
						"N":len(y),
						"BETA":mod.params[score],
						"SE":mod.bse[score],
						"CI_L":mod.conf_int().loc[score,0],
						"CI_U":mod.conf_int().loc[score,1],
						"P":mod.pvalues[score],
						"R2_null": prsq_nage_null,
						"R2_full": prsq_nage_full,
						"Delta_R2": prsq_nage_full - prsq_nage_null,
						"AUC_null": auc0 ,
						"AUC_full": auc1 ,
						"Delta_AUC": auc1 - auc0,
						"NULL_formula": null_formula,
						"FULL_formula":formula,
						"NORM":norm}
		
		if qcut is not None:
			row_dict["Q"]=qcut_current
			row_dict["Q_SCORE"]=qscore
			row_dict["Q_REF"]=qref
			if qcut_list is not None:
				row_dict["Q_INTERVAL"]=qcut_list
		
		p= len(to_check.loc[to_check[pheno]==1,:])/len(y)

		if r2_lia:
			if pheno in pheno_K.keys():
				K = pheno_K[pheno]
				log.write(" - Population prevalence for {} : {}".format(pheno,K))
			else:
				K = y.sum() / len(y)
				log.write(" - Population prevalence not defined. Use sample prevalence instead for {} : {}".format(pheno,K))
			r2_lia_null = r2_obs_to_r2_lia(R2O=r2_obs_null, K = K, P = p)
			r2_lia_full = r2_obs_to_r2_lia(R2O=r2_obs_full, K = K, P = p)
			row_dict["R2_lia_null"] = r2_lia_null
			row_dict["R2_lia_full"] = r2_lia_full
			row_dict["Delta_R2_lia"] = r2_lia_full - r2_lia_null

		row = pd.Series(row_dict).to_frame().T.astype(bdtype)
		#print(row)
		bresults = pd.concat([bresults, row],ignore_index=True)
	return bresults




def normalize_x(x, score, norm):
	if norm == True:
		x[score] = (x[score] -np.mean(x[score])) / np.std(x[score])	
	return x[score]





def get_dtype_df(mode,r2_lia=False):
	if mode=="Q":
		dtype={
				"PHENO":"string",
				"PRS":"string",
				"TYPE":"string",
				"BETA":"float64",
				"N":"Int64",
				"SE":"float64",
				"CI_L":"float64",
				"CI_U":"float64",
				"P":np.float64,
				"R2_null":"float64",
				"R2_full":"float64",
				"Delta_R2":"float64",
				"NULL_formula":"string",
				"FULL_formula":"string",
				"NORM":"boolean"}
		columns=["PHENO","TYPE","PRS","N","BETA","SE","CI_L","CI_U","P", "R2_null","R2_full","Delta_R2"]
		results = pd.DataFrame(columns=columns)
	else:
		dtype={
			"PHENO":"string",
			"PRS":"string",
			"TYPE":"string",
			"N_CASE":"Int64",
			"N":"Int64",
			"BETA":"float64",
			"SE":"float64",
			"CI_L":"float64",
			"CI_U":"float64",
			"P":np.float64,
			"R2_null":"float64",
			"R2_full":"float64",
			"Delta_R2":"float64",
			"AUC_null":"float64",
			"AUC_full":"float64",
			"Delta_AUC":"float64",
			"NULL_formula":"string",
			"FULL_formula":"string",
			"NORM":"boolean"}
		columns=["PHENO","TYPE","PRS","N_CASE","N","BETA","SE","CI_L","CI_U","P", "R2_null","R2_full","Delta_R2","AUC_null","AUC_full","Delta_AUC"]
		if r2_lia:
			dtype["R2_lia_null"]="float64"
			dtype["R2_lia_full"]="float64"
			dtype["Delta_R2_lia"]="float64"
			columns = columns + ["R2_lia_null","R2_lia_full","Delta_R2_lia"]
		results = pd.DataFrame(columns = columns)
	return dtype, results
