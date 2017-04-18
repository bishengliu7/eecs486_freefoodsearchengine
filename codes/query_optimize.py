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
			# desc_token = stemWords(desc_token)

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
	query['free'] = 1.0 * alpha
	query['food'] = 1.0 * alpha
	# print(relevant_doc, irrelevant_doc)
	for key in relevant_vec.keys():
		query[key] += relevant_vec[key] * beta / relevant_doc
	for key in irrelevant_vec.keys():
		query[key] -= irrelevant_vec[key] * gamma / irrelevant_doc

	return query




if __name__ == "__main__":


	csv_file = 'combined.csv'
	beta = 1.0
	gamma = 1.0
	alpha = 0.707

	query = opt_query(csv_file, alpha, beta, gamma)

	doc_scores = sorted(query.items(), key=operator.itemgetter(1))
	doc_scores.reverse()
	for x in doc_scores:
		print(x)

	csv_dict = defaultdict()

	test = 'sample_tagged_200.csv'
	result = defaultdict(float)
	labels = defaultdict()
	with open(test, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			docid = row['id']
			csv_dict[docid] = row
			# title = row['title']
			# tags = stringToList(row['tags'])
			desc = row['desc']
			desc = re.sub("[^a-zA-Z$']+", " ", desc).lower()
			
			label = row['label']

			desc_token = tokenizeText(desc)
			desc_token = removeStopwords(desc_token)
			if not desc_token:
				continue
			# desc_token = stemWords(desc_token)


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
	larger0 = 0
	l_0_t = 0

	csvfile_out = open("output/query_opt.scores", 'wb')
	eventwriter = csv.writer(csvfile_out, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label', 'score'])
	highest = scores[0][1]
	lowest = scores[-1][1]
	ranges = highest - lowest
	for x in scores:
		row = csv_dict[x[0]]
		eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
		   row['date'], row['tags'], row['label'], (x[1] - lowest) / ranges])
		if x[1] > 0.0:
			print(x[0], x[1], labels[x[0]])
			larger0 += 1
			if labels[x[0]] == 'T':
				l_0_t += 1

		level += 1
		if labels[x[0]] == 'T':
			correct += 1
			score.append(correct / level)

			max_score = max(max_score, sum(score) / correct)

	print(l_0_t, larger0)

	print(correct, level)
	print(score)

	print("max: " + str(max_score))
	print("final: " + str(sum(score) / correct))

	csvfile_out = open("output/query_opt.output", 'wb')
	eventwriter = csv.writer(csvfile_out, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label', 'score'])

	highest = scores[0][1]

	for x in scores:
		if x[1] > 0.0:
			row = csv_dict[x[0]]
			eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
			   row['date'], row['tags'], row['label'], x[1] / highest])




