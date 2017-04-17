import sys
import csv
from collections import defaultdict
from collections import Counter

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("python combine_results.py query_opt.csv decisiontree.csv pca_svm.csv")
		sys.exit(0)
	result_csv = []
	for i in range(1, len(sys.argv)):
		result_csv.append(sys.argv[i])

	csv_dict = defaultdict()
	csv_counter = Counter()

	for filename in result_csv:
		with open(filename, 'rU') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['id'] not in csv_dict.keys():
					csv_dict[row['id']] = row
				csv_counter[row['id']] += 1

	csvfile_out = open('combined_result.csv', 'wb')
	eventwriter = csv.writer(csvfile_out, delimiter=',')
	eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags'])

	total_T = 0
	result_dict = defaultdict()
	with open("sample_tagged_200.csv", 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			result_dict[row['id']] = row
			if row['label'] == 'T':
				total_T += 1
	print(total_T)

	total = 0
	true = 0
	false = 0

	for event_id in csv_counter.keys():
		if csv_counter[event_id] >= 1:
			row = csv_dict[event_id]
			label = result_dict[event_id]['label']
			print(event_id, label)
			total += 1
			if label == 'T':
				true += 1
			else:
				false += 1
			eventwriter.writerow([row['id'], row['title'], row['desc'], row['loc'],
			   row['date'], row['tags']])

	print(total, true, false)
