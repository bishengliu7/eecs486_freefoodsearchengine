import csv
import vectorspace
import math
import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC

def read_data():
  	with open('combined.csv', 'rb') as csvfile:
	  	read = csv.reader(csvfile, delimiter = ',')
	  	doc = [];
	  	i = 0
	  	id_dic = {}
	  	label = []
	  	for row in read:
	  		id_dic[i] = row[0]
	  		# event = {'id': row[0], 'desc': row[2], 'tags': row[5]}
	  		doc.append(row[2] + " " + row[5])
	  		label.append(row[6])
	  		i += 1
  	return id_dic, doc, label

def tfidf(corpus):
	inverted_index = {}
	num_doc = len(corpus)
	for i in range(num_doc):
		content = corpus[i]
		vectorspace.indexDocument(content, inverted_index, i)
	word_vec = np.zeros((num_doc, len(inverted_index)))
	print (word_vec.shape)
	# calculate idf
	idf = {}
	for word in inverted_index.keys():
		idf.update({word:math.log10(float(num_doc) / len(inverted_index[word]))})
	# calculate document length
	doc_length = {}
	for i in range(num_doc):
		doc_length.update({i: vectorspace.cal_doc_length(inverted_index, idf, i)})
	# weight = tf * idf / doc_length
	for i in range(num_doc):
		j = 0
		for word in inverted_index.keys():
			if i in inverted_index[word]:
				idx = inverted_index[word]
				word_vec[i,j] = idx[i] * idf[word] / doc_length[i]
			else:
				word_vec[i,j] = 0
			j += 1
	# print (np.sum(word_vec[0,:]))
	return word_vec, inverted_index, idf

def tfidf_test(corpus, inverted_index, idf):
	test_index = {}
	test_vec = np.zeros((len(corpus), len(inverted_index)))
	for i in range(len(corpus)):
		content = corpus[i]
		vectorspace.indexTest(content, inverted_index, i, test_index)
	doc_length = {}
	for i in range(len(corpus)):
		doc_length.update({i: vectorspace.cal_doc_length(test_index, idf, i)})

	for i in range(len(corpus)):
		j = 0
		for word in inverted_index.keys():
			if word in test_index.keys():
				if i in test_index[word]:
					test_vec[i,j] = test_index[word][i] * idf[word] / doc_length[i]
				else:
					test_vec[i,j] = 0
			else:
				test_vec[i,j] = 0
			j += 1
	return test_vec

def export_csv(idx):
	output = open('svm_output.csv', 'wb')

	with open ('combined.csv', 'rb') as csvfile:
		read = csv.reader(csvfile, delimiter = ',')
		i = 0
		# print (type(i))
		# print (type(idx))
		for row in read:
			# print ((row))
			row = ','.join(row)
			if i in idx:
				output.write(row + '\n')
			i += 1

if __name__ == "__main__":
	# id_dic: a dictionary mapping index to the event id
	# corpus: a list. description + tag
	id_dic, corpus, label = read_data()
	# print (label)
	for i in range(len(label)):
		if label[i] == 'T':
			label[i] = 1
		else:
			label[i] = 0
	# print (label)
	corpus_train = corpus[:549]
	corpus_test = corpus[549:]
	label_train = label[:549]
	label_test = label[549:]

	# calculate tfidf for each documents
	word_vec, inverted_index, idf = tfidf(corpus_train)

	# use pca to reduce dimension
	pca = PCA(n_components = 300)
	new_feature_vector = pca.fit_transform(word_vec)
	print (new_feature_vector.shape)

	# train SVM with linear kernel
	clf = SVC(kernel = 'linear', class_weight = {0: 1, 1: 0.4})
	clf.fit(new_feature_vector, label_train)

	# test 
	test_vec = tfidf_test(corpus_test, inverted_index, idf)
	new_test_feature = pca.transform(test_vec)

	label_pred = clf.predict(new_test_feature)
	acc = float(sum(label_pred == label_test)) / len(label_test)
	print ("Accuracy: " + str(acc))
	print ("free food events in test data: " + str(sum(label_pred == 1)))
	# print (sum(label_test == 1)
	print ("ground truth free food events: " + str(sum(label_test)))
	# print ("non free food ")
	# calculate recall
	correct_pred = 0
	for i in range(len(label_test)):
		if (label_pred[i] == label_test[i] and label_pred[i] == 1):
			correct_pred += 1
	precision = float(correct_pred) / sum(label_pred)
	print ("correctly retrieved: " + str(correct_pred))
	print ("Precision: " + str(precision))


	# export to csv
	idx = np.array(np.where(label_pred == 1))
	export_csv(idx)