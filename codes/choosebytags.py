import csv
from collections import defaultdict
from collections import Counter
import operator
import string
import os
import re
import sys
import random
from query_optimize import stringToList
from events_filter import tag_filter



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python choosebytags.py csv_file tag1 tag2 tag3")
		sys.exit(0)

	csv_file = sys.argv[1]
	tags = []
	outputfile = ""
	for i in range(2, len(sys.argv)):
		print(sys.argv[i], i)
		tags.append(sys.argv[i])
		outputfile += sys.argv[i]
	outputfile = '../data/' + outputfile + '.csv'
	tag_filter(tags, csv_file, outputfile)
