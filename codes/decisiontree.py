import sys
from sklearn import tree
import numpy as np
import csv
from query_optimize import stringToList

def train(csv_file):
# This function extracts the tags from the data, trains the decision tree 
# based on the input data and outputs a tree and trainning accuracy
# Input: a csv file contains events with labels
# Output: trained decision tree, all extracted tags and trainning accuracy
  all_tags = []
  with open(csv_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      tags = stringToList(row['tags'])
      for tag in tags:
        if tag not in all_tags:
          all_tags.append(tag)

  X = []
  y = []
  with open(csv_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      temp = [0] * len(all_tags)
      tags = stringToList(row['tags'])
      for tag in tags:
        if tag in all_tags:
          temp[all_tags.index(tag)] = 1
      X.append(temp)
      y.append(1 if row['label'] == 'T' else 0)

  clf = tree.DecisionTreeClassifier(max_features=None, max_depth=None)
  clf = clf.fit(X, y)
  all_tags_np = np.array(all_tags)
  score = float(sum(np.array(y) & np.array(clf.predict(X)))) / sum(y)
  print ("train accuracy", score)
  return clf, all_tags, score

def test(clf, all_tags, csv_file):
# This function generate labels on the input data using a trained tree
# Input: a trained decision tree, tags used and test data in csv file
# Output: label of each event, and store all free food events in a csv file
  X = []
  with open(csv_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      temp = [0] * len(all_tags)
      tags = stringToList(row['tags'])
      for tag in tags:
        if tag in all_tags:
          temp[all_tags.index(tag)] = 1
      X.append(temp)

  res = clf.predict(X)
  with open(csv_file ,'r') as infile:
    with open('decisiontree.output', 'wb') as outfile:
      for idx, line in enumerate(infile):
        if idx == 0 or res[idx - 1]:
          outfile.write(line)
  return res

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("python decisiontree.py train_file, test_file")
    sys.exit(0)

  train_file = '../data/training.csv'
  test_file = '../data/test.csv'

  clf, all_tags, s = train(train_file)
  test(clf, all_tags, test_file)
  # tree.export_graphviz(clf, out_file='tree.dot')
