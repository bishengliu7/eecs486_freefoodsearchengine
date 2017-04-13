import csv
from collections import defaultdict
from collections import Counter
import operator
import string
import os
import re
import sys
import random
from docstovector import stringToList



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python choosebytags.py csv_file")
		sys.exit(0)

	csv_file = sys.argv[1]
	writecsv = open('events_with_food_and_free_tags.csv', 'wb')
	eventwriter = csv.writer(writecsv, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label'])

	with open(csv_file, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if 'food' in stringToList(row['tags'].lower()) and 'free' in stringToList(row['tags'].lower()):
				eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
				   row['date'], row['tags'], 'T'])



