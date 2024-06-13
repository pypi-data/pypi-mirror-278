import pandas as pd
import numpy as np
import os
from prslink.g_Log import Log

def _load_data(dataset, 
				score_list ,
				mode, 
				path, 
				iid, 
				scores,  
				names = list(),
				types="Q",
				match_dict = [pd.DataFrame(),"_ID_TO_CONVERT","_ID_MAIN"],
				log=Log(),
				**arg):
	
	pheno_types = dict()
	log.write("Start loading datasets...")
	log.write("- Dataset shape before loading : {}".format(dataset.shape))
	if scores is list:
		col_list = [iid] + scores
	else:
		scores = list(scores)
		col_list = [iid] + scores
	
	log.write("- Loading {} data from file: {}".format(mode ,path))
	log.write("  - Setting ID:{}".format(iid))
	log.write("  - Loading {}:{}".format(mode," ".join(scores)))

	# load score
	if "sep" not in arg.keys():
		sep="\t"
	df = pd.read_table(path,usecols=col_list, dtype={iid:"string"},**arg)
	
	if types=="B":
		for score in scores:
			df[score] = np.floor(pd.to_numeric(df[score], errors='coerce')).astype('Int64')
		
	# renaming
	rename_dic={iid:"IID"}
	
	if len(match_dict[0])>0:
		log.write(" - Converting IDs using matching dictionary before merging with main dataset...")
		log.write("  - from file-raw-ID:{} to merging-ID:{}".format(match_dict[1], match_dict[2]))
		#rename raw file id
		df = df.rename(columns={iid:"_ID_TO_CONVERT"})
		#merge with dict from_id
		df = pd.merge(df , match_dict[0].loc[:,[match_dict[1],match_dict[2]]], left_on="_ID_TO_CONVERT",right_on=match_dict[1], how="inner", suffixes=("_l",""))
		#extract data
		#df = df.loc[:,scores + [match_dict[2]]]
		df = df.drop(["_ID_TO_CONVERT",match_dict[1]],axis=1)
		# rename iid to raw iid
		df = df.rename(columns={match_dict[2]:iid})

	# if scores and names match
	if len(names) == len(scores):
		# create rename
		for i in range(len(names)):
			rename_dic[scores[i]] = names[i]
		scores = names
	df = df.rename(columns=rename_dic)

	
	# check col
	counter = len(score_list)
	loaded_cols = []
	for i in scores:
		if i in df.columns:
			if i in score_list:
				counter+=1
				df = df.rename(columns={i:"{}_{}".format(i,counter)})
				loaded_cols.append("{}_{}".format(i,counter))
				pheno_types["{}_{}".format(i,counter)]=types
			else:
				loaded_cols.append(i)
				pheno_types[i]=types

	log.write("  - Loaded columns:"," ".join(loaded_cols))
	log.write("  - Overlapping IDs:{}".format(sum(df["IID"].isin(dataset["IID"]))))
	
	
	# merge score to main dataset
	log.write("  - Merging to main dataset...")
	num_before = len(dataset)
	# check pheno and covar overlap
	dataset = pd.merge(dataset , df, on="IID", how="outer", suffixes=("","r"))
	num_after = len(dataset)
	num_change = num_after - num_before
	if num_change >0:
		log.write("  - Added new IDs : {}".format(num_change))
	# merge score to main dataset
	log.write("- Loading finished successfully!")
	log.write("- Dataset shape after loading : {}".format(dataset.shape))
	
	# return main dataset and loaded col list
	# if pheno , alsor return pheno_types
	log.write("Finished loading datasets...")
	if mode =="pheno":
		return dataset, score_list + loaded_cols, pheno_types
	else :
		return dataset, score_list + loaded_cols

