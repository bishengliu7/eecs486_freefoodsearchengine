from datetime import datetime
import sys
import csv
from query_optimize import stringToList


def date_filter(date, csv_in, csv_out):
	#write all the events happen after the input date in csv_in to csv_out
	date_obj = datetime.strptime(date, "%Y-%m-%d")

	csvfile_out = open(csv_out, 'wb')
	eventwriter = csv.writer(csvfile_out, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags'])
	with open(csv_in, 'rU') as csvfile_in:
		reader = csv.DictReader(csvfile_in)
		for row in reader:
			match = False
			date_list = stringToList(row['date'])
			for e_date in date_list:
				e_date_obj = datetime.strptime(e_date, "%Y-%m-%d %H:%M")
				if e_date_obj > date_obj:
					match = True
					break
			if match:
				eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
				   row['date'], row['tags']])

def tag_filter(tags, csv_in, csv_out):
	#choose the events having all specific tags 
	writecsv = open(csv_out, 'wb')
	eventwriter = csv.writer(writecsv, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags', 'label'])

	with open(csv_in, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			event_tags = stringToList(row['tags'].lower())
			valid = True
			for tag in tags:
				if tag not in event_tags:
					valid = False
			if valid:
				eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
				   row['date'], row['tags'], 'T'])



if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("python event_filter.py date(YY-mm-dd) csv_in csv_out")
		sys.exit(0)
	date = sys.argv[1]
	csv_in = sys.argv[2]
	csv_out = sys.argv[3]
	date_filter(date, csv_in, csv_out)
