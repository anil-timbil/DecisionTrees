# COM307 | Project 3
# April 5, 2020
# Anil Timbil
# This program creates a set of decision trees and outputs one of them
# randomly for use. In order to select  best splits, we iterate every column 
# and its distinct values to evaluate their gini index. Then, we recursively
# create decision trees using bootstraping method. 

# Import libraries
import pandas as pd
from random import randint

# Calculates the weighted gini score for a given group of data.
def calculate_gini(group, dataframe_len, classes):

	# Get the length of group.
	size = len(group.index)
	if size == 0:
		return 0

	# Find proportion of each class 
	gini_score = 0
	for class_item in classes:
		proportion = len(group[group['col35']==class_item]) / size
		gini_score += proportion * proportion

	# Calculate weighted gini score
	weighted_score = (1.0 - gini_score) * (size / dataframe_len)
	return weighted_score

# Returns the gini index and split groups for a given pair of split parameters.
def gini_index(split_col, split_val, dataframe):

	classes = list(set(dataframe['col35'].values))
	total_observations = len(dataframe.index)

	# Create split groups and their gini indexes.
	group1 = dataframe[dataframe[split_col]<=split_val]
	group1_gini = calculate_gini(group1, total_observations, classes)

	group2 = dataframe[dataframe[split_col]>split_val]
	group2_gini = calculate_gini(group2, total_observations, classes)

	gini = group1_gini + group2_gini

	return gini, group1, group2

# Returns the best split looping through every variable and its distinct values.
def find_best_split(dataframe):

	#initialize variables
	min_col = dataframe.columns[0]
	min_split = dataframe.iloc[0,0]
	min_gini = 0.5 # max gini index possible
	group1 = -1
	group2 = -1

	# Loop through each variable and its uniquie value.
	for col in dataframe.columns:

		if col!='col35':
			values = list(set(dataframe[col].values)) #Distinct values in the column

			for split in values:

				gini_val, g1, g2 = gini_index(col, split, dataframe)

				# Update variables if a smaller gini index is found.
				if gini_val <= min_gini:
					min_col = col
					min_split = split
					min_gini = gini_val
					group1 = g1
					group2 = g2

	return min_col, min_split, min_gini, group1, group2

# Creates a decision tree recursively by finding split points
def create_tree(dataframe, min_size, max_depth, depth):

	### Find the best split using Gini Index ##
 	split_col, split_val, split_gini, group1, group2 = find_best_split(dataframe)
 	print("split: ", split_col, split_val, split_gini, depth)


 	### Base Cases ###

 	# Max depth is reached
 	if depth==max_depth:
 		print("G1: ", set(group1['col35'].values))
 		print("G2: ", set(group2['col35'].values))
 		return

 	# Perfect split
 	if split_gini==0:
 		print("G1: ", set(group1['col35'].values))
 		print("G2: ", set(group2['col35'].values))
 		#print("Class: ", set(dataframe['col35'].values), "Gini")
 		return

 	# Small dataset
 	if len(dataframe.index)<=min_size:
 		print("G1: ", set(group1['col35'].values))
 		print("G2: ", set(group2['col35'].values))
 		#print("Class: ", set(dataframe['col35'].values), "min_size")
 		return

 	### Recursive cases ###
 	else:
 		create_tree(group1, min_size, max_depth, depth+1) #left child
 		create_tree(group2, min_size, max_depth, depth+1) #right child

# Loads the dataset, selects m random predictor variables, and creates a decision tree.
def main(m):

	# Import ionosphere data
	observations = pd.read_csv("ionosphere.csv") 
	total = len(observations)
	print("Datafile is load...")

	# Pick m random predictors
	variables = []
	for i in range(m):
		col = 'col'+str(randint(1,34))
		while col in variables:
			col = 'col'+str(randint(1,34))
		variables.append(col)
	variables.append('col35')
	print("Selected the following m random variables:\n", variables)

	
	# Bootstraping and decision trees
	min_size = 5
	max_depth = 6
	dataframe = observations[variables]
	create_tree(dataframe, min_size, max_depth, 1)


	# First random tree

main(10)