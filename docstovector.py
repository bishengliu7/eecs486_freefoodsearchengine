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
	for key in vector.keys():
		vector[key] /= total**0.5

	return vector



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python choosebytags.py csv_file")
		sys.exit(0)

	csv_file = sys.argv[1]
	beta = 1.0
	gamma = 1.0
	alpha = 1.0

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
	for key in relevant_vec.keys():
		query[key] += relevant_vec[key] * beta / relevant_doc
	for key in irrelevant_vec.keys():
		query[key] += irrelevant_vec[key] * gamma / irrelevant_doc

	for key in query.keys():
		print(key, query[key])




