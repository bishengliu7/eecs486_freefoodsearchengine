'''
Name: Jiachen Wang
UniqName: jiachenw
'''


import re

def checkComma(punct, string, pattern1, pattern2):
	punctlist = [m.start() for m in re.finditer(punct, string)];
	#print punctlist;
	for index in punctlist:
		word = string[index+1:];
		if pattern1.match(word):
			continue;
		else:
			string = string[:index] + " " + string[index+1 :];
		word = string[:index];
		if pattern2.match(word):
			continue;
		else:
			string = string[:index] + " " + string[index+1 :];
	return string;


def checkPeriod(punct, string):
	punctlist = [m.start() for m in re.finditer(punct, string)];
	for index in punctlist:
		word1 = string[index+1:];
		word2 = string[:index];
		if (string[index-1] == " ") & (string[index+1] == " "):
			string = word2 + " " + word1;
	return string;	


def checkHyphen(punct, string):
	punctlist = [m.start() for m in re.finditer(punct, string)];
	for index in punctlist:
		word1 = string[index+1:];
		word2 = string[:index];
		if ((not string[index-1].isalnum) | (not string[index+1].isalnum)):
			string = word2 + " " + word1;
	return string;






