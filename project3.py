# Project 3
# Anil Timbil
# ...

# Import libraries
import pandas as pd
from random import randint


def calculate_gini(group, dataframe_len, classes):

	size = len(group.index)
	if size == 0:
		return 0

	gini_score = 0
	for class_item in classes:
		proportion = len(group[group['col35']==class_item]) / size
		gini_score += proportion * proportion

	weighted_score = (1.0 - gini_score) * (size / dataframe_len)
	return weighted_score

def gini_index(split_col, split_val, dataframe):

	classes = list(set(dataframe['col35'].values))

	total_observations = len(dataframe.index)

	group1 = dataframe[dataframe[split_col]<=split_val]
	group1_gini = calculate_gini(group1, total_observations, classes)

	group2 = dataframe[dataframe[split_col]>split_val]
	group2_gini = calculate_gini(group2, total_observations, classes)

	gini = group1_gini + group2_gini

	#print(gini)

	return gini, group1, group2


def find_best_split(dataframe):

	#initialize
	min_col = dataframe.columns[0]
	min_split = dataframe.iloc[0,0]
	min_gini = 0.5
	group1 = -1
	group2 = -1

	for col in dataframe.columns:

		if col!='col35':
			values = list(set(dataframe[col].values))

			for split in values:
				#print(col, split)
				gini_val, g1, g2 = gini_index(col, split, dataframe)

				#if gini_val == 0:
				#	return col, split
				if gini_val <= min_gini:
					min_col = col
					min_split = split
					min_gini = gini_val
					group1 = g1
					group2 = g2
				#print(min_col, min_split, min_gini)
	return min_col, min_split, min_gini, group1, group2




def create_tree(dataframe, min_size, max_depth, depth):

	# Gini index
 	split_col, split_val, split_gini, group1, group2 = find_best_split(dataframe)
 	print("split: ", split_col, split_val, split_gini, depth)

 	#print("********Group 1*********")
 	#print(group1)
 	#print("********Group 2*********")
 	#print(group2)

 	# Base Cases
 	if depth==max_depth:
 		print("G1: ", set(group1['col35'].values))
 		print("G2: ", set(group2['col35'].values))
 		#print("Class: ", set(dataframe['col35'].values), "max_depth")
 		return

 	if split_gini==0:
 		print("G1: ", set(group1['col35'].values))
 		print("G2: ", set(group2['col35'].values))
 		#print("Class: ", set(dataframe['col35'].values), "Gini")
 		return

 	if len(dataframe.index)<=min_size:
 		print("G1: ", set(group1['col35'].values))
 		print("G2: ", set(group2['col35'].values))
 		#print("Class: ", set(dataframe['col35'].values), "min_size")
 		return

 	# Recursive cases
 	else:
 		create_tree(group1, min_size, max_depth, depth+1) #left child
 		create_tree(group2, min_size, max_depth, depth+1) #right child

 	# if len(group1.index)<=min_size:
 	# 	print("G1: ", set(group1['col35'].values))
 	# 	print("G2: ", set(group2['col35'].values))
 	# 	print("Class: ", set(dataframe['col35'].values), "min_size")
 	# 	return
 	# else:
 	# 	create_tree(group1, min_size, max_depth, depth+1)

 	# if len(group2.index)<=min_size:
 	# 	print("G1: ", set(group1['col35'].values))
 	# 	print("G2: ", set(group2['col35'].values))
 	# 	print("Class: ", set(dataframe['col35'].values), "min_size")
 	# 	return
 	# else:
 	# 	create_tree(group2, min_size, max_depth, depth+1)
	 	

 			#for i in range(len(dataframe[col])):
 			#	value = dataframe[col].iloc[i]
 			#	print(value, type(value))
			

	#base case

	#recursive case



def main(m):

	# ionosphere data
	print("Reading in the datafile...")
	observations = pd.read_csv("ionosphere.csv") 
	total = len(observations)

	

	# Pick random m variables
	variables = []
	for i in range(m):

		col = 'col'+str(randint(1,34))
		while col in variables:
			col = 'col'+str(randint(1,34))
		variables.append(col)
	variables.append('col35')
	print(variables)

	dataframe = observations[variables]
	#dataframe = observations[['col28', 'col9', 'col30', 'col32', 'col19', 'col26', 'col4', 'col2', 'col31', 'col23', 'col35']]
	#print(dataframe)

	create_tree(dataframe, 5, 6, 1)
	
	# Bootstraping and tree function



	# First random tree

main(10)