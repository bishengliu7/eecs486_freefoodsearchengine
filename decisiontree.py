import sys
from sklearn import tree
import numpy as np
import csv
from docstovector import stringToList

def train(csv_file):
  all_tags = []
  with open(csv_file, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      tags = stringToList(row['tags'])
      for tag in tags:
        if tag not in all_tags:
          all_tags.append(tag)
  # all_tags.remove('free')
  # all_tags.remove('food')
  # all_tags.remove('free food')
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
  print (all_tags_np[clf.feature_importances_ != 0], clf.feature_importances_[clf.feature_importances_ != 0])
  score = float(sum(np.array(y) & np.array(clf.predict(X)))) / sum(y)
  print ("train accuracy", score)
  return clf, all_tags, score

def test(clf, all_tags, csv_file):
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

  res = clf.predict(X)
  score = float(sum(np.array(y) & np.array(res))) / sum(y)
  print ("test recall", score)
  print ("test precision", float(sum(np.array(y) & np.array(res))) / sum(res))
  print ("test accuracy", float(sum(y == res)) / len(y))
  with open(csv_file ,'r') as infile:
    with open('output/decisiontree.output', 'wb') as outfile:
      for idx, line in enumerate(infile):
        if idx == 0 or res[idx - 1]:
          outfile.write(line)
  return res, score

if __name__ == "__main__":
  # if len(sys.argv) < 2:
  #   print("python decisiontree.py csv_file")
  #   sys.exit(0)

  csv_file = 'combined.csv'

  # all_tags = ['career', 'food', 'free', 'dance', 'multicultural', 'discussion',
  #      'music', 'north campus', 'family', 'theater', 'graduate',
  #      'undergraduate', 'concert', 'politics', 'social impact', 'umix',
  #      'spanish studies', 'film festival']
  clf, all_tags, s = train(csv_file)
  test(clf, all_tags, "sample_tagged_200.csv")
  tree.export_graphviz(clf, out_file='tree.dot')
