import os
import re
from sets import Set
import sys
from stem import PorterStemmer
import operator
import string

# Name: Bisheng Liu
# uniqname: bisheng


months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
		 'sep', 'oct', 'nov', 'dec']


def removeSGML(input):
	out = ""
	tag = False
	quote = False
	for c in input:
		if c == '<' and not quote:
			tag = True
		elif c == '>' and not quote:
			tag = False
		elif (c == '"' or c == "'") and tag:
			quote = not quote
		elif not tag:
			out += c
	return out


def tokenizeText(input):
	input = input.strip()
	input = input.lower()
	temp = re.split('\s+', input)
	tokens = []
	for word in temp:
		if word == '' or word in string.punctuation:
			continue
		tocheck = []
		tocheck.append(word)
		for i in range(0, len(tocheck)):
			w = tocheck[0]
			tocheck.pop(0)
			if ',' in w:
				commasplit = re.split('\,', w)
				alldigit = True
				clean = ""
				# remove comma in digits to make sure digits are in the same format
				for x in commasplit: 
					if x.isdigit():
						if clean != "":
							clean += ',' + x
						else:
							clean += x
					if x != '' and (not x.isdigit()):
						alldigit = False

				if alldigit:
					tocheck.append(clean)
				else:
					for x in commasplit:
						if x != '':
							tocheck.append(x)
			else:
				tocheck.append(w)


		for i in range(0, len(tocheck)):
			w = tocheck[0]
			tocheck.pop(0)
			if '.' in w:
				dotsplit = re.split('\.', w)
				if '' in dotsplit:
					alldigit = True
					toadd = ""
					#remove extra dot at the end of numbers
					for i in range(0, len(dotsplit) - 1):
						if toadd != "":
							toadd += '.'
						if not dotsplit[i].isdigit():
							alldigit = False
							break
						toadd += dotsplit[i]
					if alldigit:
						tocheck.append(toadd)
					else:
						tocheck.append(w) #acronyms, abbreviations

				else:
					for x in dotsplit:
						tocheck.append(x)
			else:
				tocheck.append(w)

		for i in range(0, len(tocheck)):
			w = tocheck[0]
			tocheck.pop(0)
			if "'" in w:
				if w == "i'm":
					tocheck += ['i', 'am']
					continue

				quotesplit = w.split("'")
				
				for j in range(0, len(quotesplit)):
					if quotesplit[j] != '':
						if quotesplit[j] == 's':
							tocheck.append("'s")
						elif quotesplit[j] == 're':
							tocheck.append("are")
						else:
							tocheck.append(quotesplit[j])
				
			else:
				tocheck.append(w)

		tokens += tocheck

	toreturn = []
	for word in tokens:
		if word != "":
			toreturn.append(word)

	return toreturn

def removeStopwords(tokens):
	f = open("stopwords")
	stopwords = []
	for line in f:
		stopwords.append(line.strip())
	f.close()
	cleaned = []
	for token in tokens:
		if token not in stopwords:
			cleaned.append(token)
	return cleaned

def stemWords(tokens):
	p = PorterStemmer()
	result = []
	for token in tokens:
		stemmed = p.stem(token, 0, len(token) - 1)
		result.append(stemmed)
	return result



if __name__ == '__main__':

	if len(sys.argv) > 1:
		

		directory = sys.argv[1]
		files = os.listdir(directory)

		vocabulary = 0
		words = 0
		counter = {}

		for fn in files:
			f = open(directory + fn)
			for line in f:
				temp = removeSGML(line)
				tokens = tokenizeText(temp)
				tokens = removeStopwords(tokens)
				if tokens:
					tokens = stemWords(tokens)
					for w in tokens:
						words += 1
						if str(w) not in counter.keys():
							vocabulary += 1
							counter[str(w)] = 1
						else:
							counter[str(w)] += 1
			f.close()
			
		sorted_dict = sorted(counter.items(), key=operator.itemgetter(1))	
		sorted_dict.reverse()

		output = open("preprocess.output", 'w')
		output.write("Words " + str(words) + '\n')
		output.write("Vocabulary " + str(vocabulary) + '\n')
		output.write("Top 50 Words" + '\n')
		for i in range(0, 50):
			output.write(str(sorted_dict[i][0]) + " " + str(sorted_dict[i][1]) + "\n")




