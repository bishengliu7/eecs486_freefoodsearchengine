'''
Name: Jiachen Wang
UniqName: jiachenw
'''


import re
import PorterStemmer
import preprocess_helper
import sys
import glob
from collections import Counter

def removeSGML(string):
	return re.sub('<.*?>', '', string);

contractions = {"aren\'t" : "are not", "can\'t": "cannot", 
		"could\'ve": "could have", "couldn\'t": "could not", 
		"didn\'t": "did not", "doesn\'t" : "does not", 
		"don\'t": "do not", "gonna": "going to", "hadn\'t": "had not", 
		"hasn\'t": "has not", "haven\'t": "have not", "\'ll": "will", 
		"isn\'t": "is not", "i\'m": "i am", "it\'d": "it would",
		"would\'ve": "would have", "mightn\'t": "might not", "mustn\'t": "must not",
		"shan\'t": "shall not", "should\'ve": "should have", "shouldn\'t": "should not",
		"there\'re": "there are", "they\'d\'ven\'t": "they would not have",
		"wasn\'t": "was not", "weren\'t": "were not", "you\'re": "you are",
		};
contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()));

def expand_contractions(string, contractions = contractions):
	def replace(match):
		return contractions[match.group(0)];
	return contractions_re.sub(replace, string);

def tokenizeText(string):

	string = string.lower();

	''' Assume special cases only happen with '\.' '\'', '\-', '\,'
		replace all the character other than alphanumeric and these above with whitespace '''

	string = re.sub(r'[^a-z0-9.,\'-/]', r' ', string)


	''''''''''''''''''''''''' tokenization of "\'" '''''''''''''''''''''''''''

	# contractions
	string = expand_contractions(string);

	# possessive: if some alphanumeric word is followed by ''s' and a whitespace, 
	# ''s' is considered to be possessive. 
	# someone's => someone 's
	string = re.sub(r'([0-9a-z]+)(\'s) ', r'\1 \2', string);
	# when some alphanumeric word ending with 's' is followed by ''s' and a whitespace,
	# the word is regarded as a plural form
	# girls' => girls 's
	string = re.sub(r'([0-9a-z]+[s])(\') ', r'\1 \2s', string);

	# tokenize quotation: when there are some words beteen 2 '\'', it is considered to be quotation
	# 'some words here' => some words here
	string = re.sub(r'[\'](^[\']+)[\'](^[0-9a-z])', r' \1 ', string);




	''''''''''''''''''''''''' tokenization of date '''''''''''''''''''''''''''

	# for all the dates, january 18, 2017 => jan.18.2017
	# replace the month with its abbreviation
	month = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];
	monthabbre = ["jan.", "feb.", "mar.", "apr.", "may", "june", "july", "aug.", "sept.", "oct.", "nov.", "dec."];
	for i in range(len(month)):
		string = re.sub(month[i] + r' {1}([0-9]{1,2}), ([0-9]{4})', monthabbre[i] + r'\1.\2', string);





	''''''''''''''''''''''''' tokenization of "\." '''''''''''''''''''''''''''

	# When there are both whitespace before and after '.', it works as a period.
	# then it will be replaced by a whitespace
	punct = '\.';
	string = preprocess_helper.checkPeriod(punct, string);






	''''''''''''''''''''''''' tokenization of "\," '''''''''''''''''''''''''''

	# ',' is part of a number if the three characters after it are all digits, the fourth one is non-digit and the previous character is also digit.
	# keep 100,000 as 100,000. 
	# for cases like "some words, and some words", replace the comma with whitespace
	punct = ',';
	pattern1 = re.compile('^([0-9][0-9][0-9]\D)');
	pattern2 = re.compile('([0-9])$');
	string = preprocess_helper.checkComma(punct, string, pattern1, pattern2);




	''''''''''''''''''''''''' tokenization of "\-" '''''''''''''''''''''''''''

	# if hyphen is between two alphanumeric characters, it is considered to be part of phrases.
	# otherwise, replace it with a whitespace
	punct = '\-';
	string = preprocess_helper.checkHyphen(punct, string);





	string = string.strip();
	mylist = re.split('\s+', string);

	return mylist;




def removeStopwords(mylist):
	with open('stopwords') as f:
		stopwords = f.readlines();
	stopwords = [word.strip() for word in stopwords]
	mylist = [word for word in mylist if word not in stopwords];
	return mylist;





def stemWords(mylist):
	p = PorterStemmer.PorterStemmer();
	for index in range(1,len(mylist)):
		newword = p.stem(mylist[index], 0, len(mylist[index])-1);
		if newword != mylist[index]:
			mylist[index] = newword;
	return mylist;


	

if __name__ == '__main__':
	
	path = './' + sys.argv[1] + '*';
#	path = './cranfieldDocs/*';
	files = glob.glob(path);
	finallist = [];
	i = 1;
	for file in files:
		f = open(file, 'r');
		contents = f.read();
		

		string = removeSGML(contents); # input: string, output: string
		string = string + " ";
		mylist = tokenizeText(string); # input: string, output: list

		mylist = removeStopwords(mylist); # input: list, output: list
		mylist = stemWords(mylist); # input: list, output: list
		f.close();
		finallist.extend(mylist);

	totalCount = len(finallist);
	vocabCount = len(list(set(finallist)));

	f = open('preprocess.output', 'w');

	f.write("Words " + str(totalCount) + '\n');
	f.write("Vocabulary " + str(vocabCount) + '\n');
	f.write("Top 50 words\n")
	counts = Counter(finallist);
	for word, count in counts.most_common(50):
		f.write(word + ' ' + str(count) + '\n');

	# minimum number of unique words accounting for 25% of the total words
	freqSum = 0;
	numwords = 0
	for word, count in counts.most_common(vocabCount):
		freqSum += count;
		numwords = numwords + 1;
		if freqSum >= totalCount * 0.25:
			break;
	print (numwords);

