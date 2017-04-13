'''
Name: Jiachen Wang
UniqName: jiachenw
'''

import re
import preprocess
import numpy as np
import math
import sys
import glob
import operator

def indexDocument (content, inverted_index, doc_id):
	word_list = preprocessing(content);
	for word in word_list:
		if word in inverted_index.keys():
			if doc_id in inverted_index[word]:
				inverted_index[word][doc_id] += 1;
			else:
				inverted_index[word].update({doc_id:1});
		else:
			inverted_index.update({word:dict()});
			inverted_index[word].update({doc_id:1});
	return inverted_index;

def preprocessing (content):
	content = preprocess.removeSGML(content);
	content = content + " ";
	word_list = preprocess.tokenizeText(content);
	# word_list = preprocess.removeStopwords(word_list);
	# word_list = preprocess.stemWords(word_list);
	return word_list;	

def indexTest (content, inverted_index, doc_id, test_index):
	word_list = preprocessing(content);
	for word in word_list:
		if word in inverted_index.keys():
			if word in test_index.keys():
				if doc_id in test_index[word]:
					test_index[word][doc_id] += 1
				else:
					test_index[word].update({doc_id:1})
			else:
				test_index.update({word:dict()})
				test_index[word].update({doc_id:1})




def cal_doc_length(inverted_index, idf, doc_id):
	length = 0;
	for word in inverted_index.keys():
		if doc_id in inverted_index[word].keys():
			length += math.pow(inverted_index[word][doc_id] * idf[word], 2);
	return math.sqrt(length);

def retrieveDocuments(query, inverted_index, weight_documents, weight_query, doc_length, idf, num_doc):
	query_list = preprocessing(query);

	# calculate inverted index for query
	query_index = {};
	for word in query_list:
		if word in query_index:
			query_index[word] += 1;
		else:
			query_index.update({word:1});

	# determine documents containing >=1 token from query
	doc_list = [];
	for word in query_list:
		if word in inverted_index.keys():
			doc_list = list(set(doc_list) | set(inverted_index.get(word, {}).keys()));
	doc_list = list(set(doc_list));


	if weight_query == 'tfidf':
		return retrieveDocuments_tfidf(inverted_index, doc_length, idf, doc_list, query_index);
	else:
		return retrieveDocuments_fully(inverted_index, doc_length, idf, doc_list, query_index);


def retrieveDocuments_tfidf(inverted_index, doc_length, idf, doc_list, query_index):
	# calculate query length
	score = {};
	query_length = 0;
	for word in query_index.keys():
		if word in inverted_index.keys():
			query_length += math.pow(query_index[word] * idf[word], 2);
	query_length = math.sqrt(query_length);

	# calculate the similarity
	for doc_id in doc_list:
		dot_product = cal_dot_product(inverted_index, query_index, doc_id, idf);
		similarity = dot_product / (query_length * doc_length[doc_id]);
		score.update({int(doc_id) : similarity});
	sorted_score = sorted(score.items(), key = operator.itemgetter(1), reverse = True);
	return sorted_score;

def retrieveDocuments_fully(inverted_index, doc_length, idf, doc_list, query_index):
	maxtf = max(query_index.values());
	for word in query_index.keys():
		query_index[word] = 0.5 + 0.5 * query_index[word] / maxtf;

	# calculate the similarity
	score = {};
	for doc_id in doc_list:
		dot_product = cal_dot_product(inverted_index, query_index, doc_id, idf);
		similarity = dot_product / doc_length[doc_id];
		score.update({int(doc_id): similarity});
	sorted_score = sorted(score.items(), key = operator.itemgetter(1), reverse = True);
	return sorted_score;


def cal_dot_product(inverted_index, query_index, doc_id, idf):
	dot_product = 0;
	for word in query_index:
		if word in inverted_index.keys() and doc_id in inverted_index[word].keys():
			queryweight = query_index[word] * idf[word];
			docweight = inverted_index[word][doc_id] * idf[word];
			dot_product += queryweight * docweight;
	return dot_product;


# def main():
# 	weight_scheme_doc = sys.argv[1];
# 	weight_scheme_query = sys.argv[2];
# 	docfile = sys.argv[3];
# 	queryfile = sys.argv[4];

# 	# read all the files, compute inverted index
# 	path = './' + docfile + '*';
# 	files = glob.glob(path);
# 	num_doc = 0;
# 	inverted_index = {};
# 	doc_collection = [];
# 	for file in files:
# 		f = open(file, 'r');
# 		content = f.read();
# 		doc_id = re.search(r'\d+', content).group();
# 		doc_collection = np.append(doc_collection, doc_id);
# 		content = content.replace(doc_id, "", 1);
# 		inverted_index = indexDocument(content, weight_scheme_doc, weight_scheme_query, inverted_index, doc_id);
# 		num_doc += 1;
# 	# print (num_doc);

# 	# calculte idf
# 	idf = {};
# 	for word in inverted_index.keys():
# 		idf.update({word:math.log10(float(num_doc) / len(inverted_index[word]))});

# 	# calculate document length
# 	doc_length = {};
# 	for doc_id in doc_collection:
# 		doc_length.update({doc_id: cal_doc_length(inverted_index, idf, doc_id)});

# 	# read each queries, calculate similarity
# 	output = open('cranfield.fullydoc.fullyquery.output', 'w');
# 	with open(queryfile) as f:
# 		for query in f:
# 			queryid = re.search(r'\d+', query).group();
# 			query = query.replace(queryid, "", 1);
# 			sorted_score = retrieveDocuments(query, inverted_index, weight_scheme_doc, weight_scheme_query, doc_length, idf, num_doc);
# 			for doc_id, score in sorted_score:
# 				output.write(str(queryid + " " + str(doc_id) + " " + str(score) + '\n'));

# if __name__ == '__main__':
# 	main();



