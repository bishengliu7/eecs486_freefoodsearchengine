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
	out = ast.literal_eval(input.lower())
	out = [n.strip() for n in out]
	return out

def normalizedVector(tokens):
	vector = defaultdict(float)
	for token in tokens:
		vector[token] += 1.0
	total = 0.0
	for key in vector.keys():
		total += vector[key] * vector[key]
	# for key in vector.keys():
	# 	vector[key] /= total**0.5

	return vector

def getCos(vec1, vec2):
	score = 0.0
	for key in vec1.keys():
		score += vec1[key] * vec2[key]
	return score

def opt_query(csv_file, alpha, beta, gamma):

	relevant_vec = defaultdict(float)
	irrelevant_vec = defaultdict(float)
	relevant_doc = 0.0
	irrelevant_doc = 0.0

	with open(csv_file, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			# docid = row['id']
			# title = row['title']
			# tags = stringToList(row['tags'])
			desc = row['desc']
			desc = re.sub("[^a-zA-Z$']+", " ", desc).lower()
			
			label = row['label']

			desc_token = tokenizeText(desc)
			desc_token = removeStopwords(desc_token)
			if not desc_token:
				continue
			desc_token = stemWords(desc_token)

			vector = normalizedVector(desc_token)

			if label == 'F':
				irrelevant_doc += 1
				for key in vector.keys():
					irrelevant_vec[key] += vector[key]
			else: 
				relevant_doc += 1
				for key in vector.keys():
					relevant_vec[key] += vector[key]


	query = defaultdict(float)
	query['free'] = 0.707 * alpha
	query['food'] = 0.707 * alpha
	# print(relevant_doc, irrelevant_doc)
	for key in relevant_vec.keys():
		query[key] += relevant_vec[key] * beta / relevant_doc
	for key in irrelevant_vec.keys():
		query[key] -= irrelevant_vec[key] * gamma / irrelevant_doc

	return query




if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python choosebytags.py csv_file")
		sys.exit(0)

	csv_file = sys.argv[1]
	beta = 1.0
	gamma = 1.0
	alpha = 1.0

	query = opt_query(csv_file, alpha, beta, gamma)

	# doc_scores = sorted(query.items(), key=operator.itemgetter(1))
	# doc_scores.reverse()
	# print(doc_scores)
	query['pm'] = 0
	query['am'] = 0

	test = 'sample_tagged_200.csv'
	result = defaultdict(float)
	labels = defaultdict()
	with open(test, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			docid = row['id']
			# title = row['title']
			# tags = stringToList(row['tags'])
			desc = row['desc']
			desc = re.sub("[^a-zA-Z$']+", " ", desc).lower()
			
			label = row['label']

			desc_token = tokenizeText(desc)
			desc_token = removeStopwords(desc_token)
			if not desc_token:
				continue

			vector = normalizedVector(desc_token)

			cos = getCos(vector, query)
			result[docid] = cos
			labels[docid] = label

	scores = sorted(result.items(), key=operator.itemgetter(1))
	scores.reverse()
	level = 0.0
	correct = 0.0
	score = []
	max_score = 0.0
	for x in scores:
		print(x[0], x[1], labels[x[0]])
		level += 1
		if labels[x[0]] == 'T':
			correct += 1
			score.append(correct / level)
			max_score = max(max_score, sum(score) / correct)
	print(correct, level)
	print(score)

	print(sum(score) / correct)
	print('max_map')




