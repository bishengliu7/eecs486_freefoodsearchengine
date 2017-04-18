import sys
import csv
from collections import defaultdict
from collections import Counter
import operator
import string
import os
import re
import sys
import random
import ast
import numpy as np

def map(scores, csv_dict):
	#calculate the moving average precision of the output scores
	result = []
	curr = 0.0
	correct = 0.0
	for x in scores:
		curr += 1
		if csv_dict[x[0]]['label'] == 'T':
			correct += 1
			result.append(correct / curr)
	# print(result)
	return sum(result) / correct

if __name__ == "__main__":
	csv_dict = defaultdict()
	correct = 0.0
	with open('../data/test.csv', 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			csv_dict[row['id']] = row
			if row['label'] == 'T':
				correct += 1

	#calculate map for query optimization
	query_opt_score = defaultdict()
	with open('../output/query_opt.scores', 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			query_opt_score[row['id']] = row['score']
	q_opt_scores = sorted(query_opt_score.items(), key=operator.itemgetter(1))
	q_opt_scores.reverse()
	print("q_opt_scores")
	print(map(q_opt_scores, csv_dict))

	#calculate map for pca_svm
	pca_svm_score = defaultdict()
	with open('../output/pca_svm.scores', 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			pca_svm_score[row['id']] = row['score']
	pca_svm_scores = sorted(pca_svm_score.items(), key=operator.itemgetter(1))
	pca_svm_scores.reverse()
	print("pca_svm_scores")
	print(map(pca_svm_scores, csv_dict))

	#calculate map for combined score with different alpha ranging form 0.0 to 1.0 stepped by 0.1
	alphas = np.arange(0,1.1,0.1)
	score = []
	for alpha in alphas:
		combined_scores = defaultdict(float)
		for eid in query_opt_score.keys():
			combined_scores[eid] = alpha * float(query_opt_score[eid]) + (1 - alpha) * float(pca_svm_score[eid])
		scores = sorted(combined_scores.items(), key=operator.itemgetter(1))
		scores.reverse()
		score.append(map(scores, csv_dict))
	print(alphas)
	print(score)


