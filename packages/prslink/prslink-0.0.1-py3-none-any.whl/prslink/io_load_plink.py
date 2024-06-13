import pandas as pd
import os
from prslink.g_Log import Log

# plink2
# #FID	IID	ALLELE_CT	NAMED_ALLELE_DOSAGE_SUM	SCORE1_AVG	SCORE1_SUM
def _load_plink(dataset, 
				score_list,
				path,
				name="SCORE",
				avg=False,
				version="PLINK2",
				log=Log(),
				**arg):
	
	log.write("Start loading {} format scores...".format(version))
	
	if version == "PLINK2" :
		# plink2
		# #FID	IID	ALLELE_CT	NAMED_ALLELE_DOSAGE_SUM	SCORE1_AVG	SCORE1_SUM
		score_sum = "SCORE1_SUM"
		score_avg = "SCORE1_AVG"
		allele_count = "ALLELE_CT"
	elif version == "PLINK1.9" :
		# plink1
		# FID       IID  PHENO    CNT   CNT2    SCORE
		score_sum = "SCORESUM"
		score_avg = "SCORE"
		allele_count = "CNT"
	
	log.write("- Dataset shape before loading : {}".format(dataset.shape))
	
	dtype={"#FID":"string", "IID":"string"}

	score_df = pd.DataFrame()
	
	# load plink data
	score_df = _load_plink_into_dataframe(path=path,
							dtype=dtype,
							arg=arg,
							version=version,
							log=log)
	
	if avg==True:
		# if calculate the averaged score
		score_df[score_sum] = score_df[score_sum] / score_df[allele_count]
		log.write("  - Calculate the average sum of scores : sum(scores) / sum(ALLELE_CT)")
	else:
		log.write("  - Calculate the raw sum of scores : sum(SCORE1_AVG * ALLELE_CT)")
	
	# check the names and get a rename dict
	rename_dic, score_list, name = _check_and_rename(name = name, 
						  							score_list = score_list, 
													score_sum = score_sum,
													log=log)

	

	# rename columns
	score_df = score_df.rename(columns=rename_dic)

	log.write("  - Overlapping IDs : {}".format(sum(score_df["IID"].isin(dataset["IID"]))))
	
	num_before = len(dataset)
	dataset = pd.merge(dataset, score_df.loc[:,["IID",name]], on="IID", how="outer", suffixes=("","r"))
	num_after = len(dataset)
	num_change = num_after - num_before
	
	if num_change >0:
		log.write("  - Added new IDs : {}".format(num_change))
	# return main dataset and loaded col list
	log.write("- Dataset shape after loading : {}".format(dataset.shape))
	log.write("Finished loading datasets...")
	return dataset, score_list

def isfile_casesensitive(path):
    if not os.path.isfile(path): 
        return False   # exit early
    directory, filename = os.path.split(path)
    return filename in os.listdir(directory)

def _check_and_rename(name, score_list, score_sum,log):
	# name : prs name to be loaded
	# current prs names in the dataset
	log.write("  - Loading score: " + name)
	# check number of col
	counter = len(score_list)
	
	# if name already exists, rename it
	if name in score_list:
		counter+=1
		new_name = "{}_{}".format(name,counter)
		log.write("  - {} already exists in datasets. Renaming {} to {}".format(name,name,new_name))
	else:
		new_name = name

	rename_dic={score_sum: new_name}
	
	
	new_score_list = score_list + [new_name]

	return rename_dic, new_score_list, new_name



def _load_plink_into_dataframe(path,dtype,arg,version,log):
	
	if version == "PLINK2" :
		score_sum = "SCORE1_SUM"
		score_avg = "SCORE1_AVG"
		allele_count = "ALLELE_CT"
	elif version == "PLINK1.9" :
		score_sum = "SCORESUM"
		score_avg = "SCORE"
		allele_count = "CNT"

	if "@" in path:
		log.write("- Batch loading {} data from file: {}".format(version , path))
		inpath_chr_num_list = list()
		inpath_chr_list = list()
		
		# detecting if the file exists
		for chromosome in list(range(1,26))+["x","y","X","Y","MT","mt","m","M"]:
			inpath_chr = path.replace("@",str(chromosome))  
			if isfile_casesensitive(inpath_chr):
				inpath_chr_num_list.append(str(chromosome))
				inpath_chr_list.append(inpath_chr)
		log.write("  - Chromosomes detected:",",".join(inpath_chr_num_list))
		
		# merging
		for index, chr_path in enumerate(inpath_chr_list):
			if index==0:
				score_df = pd.read_table(chr_path, dtype=dtype, sep="\s+",**arg)
				if score_sum not in score_df.columns:
					score_df[score_sum] = score_df[allele_count] * score_df[score_avg]
					continue
			else:
				score_df2 = pd.read_table(chr_path, dtype=dtype, sep="\s+",**arg)
				if score_sum not in score_df2.columns:
					score_df2[score_sum] = score_df2[allele_count] * score_df2[score_avg]
			
				score_df = pd.merge(score_df, score_df2,on="IID",suffixes=("","_r"),how="left")
				
				# update the total score
				score_df[allele_count] =  score_df[allele_count] + score_df[allele_count+"_r"]
				score_df[score_sum] =  score_df[score_sum] + score_df[score_sum + "_r"]
				score_df.drop([score_sum+"_r", allele_count+"_r"],axis=1, inplace=True)
	else:
		log.write("- Loading {} data from file: {}".format(version , path))
		score_df = pd.read_table(path, dtype=dtype, sep="\s+", **arg)
		if score_sum not in score_df.columns:
			score_df[score_sum] = score_df[allele_count] * score_df[score_avg]
		if score_avg in score_df.columns:
			score_df.drop([score_avg],axis=1, inplace=True)
	return score_df