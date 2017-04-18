import csv
from collections import defaultdict
from collections import Counter
from sets import Set
import operator
import string
import os
import re
import sys
import random
from query_optimize import stringToList

def combine_csv(csv_file_1, csv_file_2, output):
	#combine two csv files into one file
	writecsv = open(output, 'wb')
	eventwriter = csv.writer(writecsv, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label'])

	ids = Set()

	with open(csv_file_1, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['id'] not in ids:
				eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'], row['date'], row['tags'], 'T'])
				ids.add(row['id'])

	with open(csv_file_2, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['id'] not in ids:
				eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'], row['date'], row['tags'], row['label']])
				ids.add(row['id'])


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python csv_combine.py csv_file_1 csv_file_2 output_csv")
		sys.exit(0)

	csv_file_1 = sys.argv[1]
	csv_file_2 = sys.argv[2]
	combine_csv(csv_file_1, csv_file_2, '../data/combined.csv')

	
