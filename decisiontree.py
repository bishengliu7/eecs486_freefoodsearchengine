import sys
from sklearn import tree
import numpy as np
import csv
from docstovector import stringToList

def train(all_tags, csv_file):
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
        temp[all_tags.index(tag)] = 1
      X.append(temp)
      y.append(1 if row['label'] == 'T' else 0)

  clf = tree.DecisionTreeClassifier(max_features=None, max_depth=None)
  clf = clf.fit(X, y)
  all_tags_np = np.array(all_tags)
  print (all_tags_np[clf.feature_importances_ != 0], clf.feature_importances_[clf.feature_importances_ != 0])
  score = float(sum(np.array(y) & np.array(clf.predict(X)))) / sum(y)
  print ("train accuracy", score)
  # print (1 - float(sum(y))/len(y))
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
  # print (float(sum(y == res)) / len(y))
  return res, score

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("python decisiontree.py csv_file")
    sys.exit(0)

  csv_file = sys.argv[1]

  all_tags = ['career', 'food', 'free', 'dance', 'multicultural', 'discussion',
       'music', 'north campus', 'family', 'theater', 'graduate',
       'undergraduate', 'concert', 'politics', 'social impact', 'umix',
       'spanish studies', 'film festival']
  clf, all_tags, s = train(all_tags, csv_file)
  test(clf, all_tags, "350.csv")

