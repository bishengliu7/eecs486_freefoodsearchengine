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

from preprocess import removeSGML, tokenizeText, removeStopwords, stemWords


def stringToList(input):
	#transfer a string list to a python list
	out = ast.literal_eval(input.lower())
	out = [n.strip() for n in out]
	return out

def tokensToVector(tokens):
	#transfer a list of tokens to a vector
	vector = defaultdict(float)
	for token in tokens:
		vector[token] += 1.0
	# total = 0.0
	# for key in vector.keys():
	# 	total += vector[key] * vector[key]
	# # for key in vector.keys():
	# # 	vector[key] /= total**0.5

	return vector

def getCos(vec1, vec2):
	# return the cosine similarity score between two vectors
	score = 0.0
	for key in vec1.keys():
		score += vec1[key] * vec2[key]
	return score

def opt_query(csv_file, alpha, beta, gamma):
	#optimize the query in Standard Rocchio method with specific alpha, beta and gamma
	# with manually evaluated training sets
	relevant_vec = defaultdict(float)
	irrelevant_vec = defaultdict(float)
	relevant_doc = 0.0
	irrelevant_doc = 0.0

	with open(csv_file, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			desc = row['desc']
			desc = re.sub("[^a-zA-Z$']+", " ", desc).lower()
			label = row['label']
			desc_token = tokenizeText(desc)
			desc_token = removeStopwords(desc_token)
			if not desc_token:
				continue
			#get the vector from tokens in the event description
			vector = tokensToVector(desc_token)

			#combine all the relevant docs and irrelevant docs
			if label == 'F':
				irrelevant_doc += 1
				for key in vector.keys():
					irrelevant_vec[key] += vector[key]
			else: 
				relevant_doc += 1
				for key in vector.keys():
					relevant_vec[key] += vector[key]

	#default query: normalized "free food"
	query = defaultdict(float)
	query['free'] = 0.707 * alpha
	query['food'] = 0.707 * alpha

	#get the final score
	for key in relevant_vec.keys():
		query[key] += relevant_vec[key] * beta / relevant_doc
	for key in irrelevant_vec.keys():
		query[key] -= irrelevant_vec[key] * gamma / irrelevant_doc

	return query




if __name__ == "__main__":

	csv_file = '../data/training.csv'
	beta = 1.0
	gamma = 1.0
	alpha = 1.0

	query = opt_query(csv_file, alpha, beta, gamma)

	doc_scores = sorted(query.items(), key=operator.itemgetter(1))
	doc_scores.reverse()

	csv_dict = defaultdict()

	test = '../data/test.csv'
	result = defaultdict(float)
	labels = defaultdict()
	#test the optimizied query with our labeled testcases
	with open(test, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			docid = row['id']
			csv_dict[docid] = row

			desc = row['desc']
			desc = re.sub("[^a-zA-Z$']+", " ", desc).lower()
			label = row['label']
			desc_token = tokenizeText(desc)
			desc_token = removeStopwords(desc_token)

			if not desc_token:
				continue
			vector = tokensToVector(desc_token)
			#cos simularity is the final score of the 
			cos = getCos(vector, query)
			result[docid] = cos
			labels[docid] = label

	scores = sorted(result.items(), key=operator.itemgetter(1))
	scores.reverse()
	total = 0.0
	correct = 0.0
	score = []

	csvfile_out = open("../output/query_opt.output", 'wb')
	eventwriter = csv.writer(csvfile_out, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label', 'score'])

	#output the events with positive score
	for x in scores:
		if x[1] > 0.0:
			row = csv_dict[x[0]]
			eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
			   row['date'], row['tags'], row['label'], x[1] / highest])

	if len(sys.argv) == 1:
		#output all the scores for reranking scheme
		csvfile_out = open("../output/query_opt.scores", 'wb')
		eventwriter = csv.writer(csvfile_out, delimiter=',')
		eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label', 'score'])
		highest = scores[0][1]
		lowest = scores[-1][1]
		ranges = highest - lowest
		for x in scores:
			row = csv_dict[x[0]]
			eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
			   row['date'], row['tags'], row['label'], (x[1] - lowest) / ranges])
			total += 1
			if labels[x[0]] == 'T':
				correct += 1
				score.append(correct / total)

		print(correct, total)
		print(score)
		print("final map: " + str(sum(score) / correct))






