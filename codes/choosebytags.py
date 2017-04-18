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
		print("python choosebytags.py csv_file")
		sys.exit(0)

	csv_file = sys.argv[1]
	tag_filter(['free', 'food'], csv_file, '../data/events_with_food_and_free_tags.csv')
