from datetime import datetime
import sys
import csv
from docstovector import stringToList


def event_filter(date_obj, csv_in, csv_out):
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



if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("python event_date_filter.py date(YY-mm-dd) csv_in csv_out")
		sys.exit(0)
	date_obj = datetime.strptime(sys.argv[1], "%Y-%m-%d")
	csv_in = sys.argv[2]
	csv_out = sys.argv[3]
	event_filter(date_obj, csv_in, csv_out)
