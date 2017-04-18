# EECS 486 Final Project: Free Food Search Engine

## Overview
Our project aimed to solve the insufficiency of event information by providing a collection of free food events, in order to let students quickly locate the events that they want to attend. Our final goal was to find all free food events held on campus. 

## Program Descpritions
### crawler.py
```
python crawler.py
```
Fetch all the events on events.umich.edu and generate a csv file collecting all the events at ```/data/final_events.csv```.

### sample.py
```
python sample.py csv_in sample_size csv_out
```
Randomly generate a sample with specific size.

### events_filter.py
```
python event_filter.py date(YY-mm-dd) csv_in csv_out
```
Provide functions to filter the events by tags and by date. The main function filter all the events in csv_in that happen after the input date.

### choosebytags.py
```
python choosebytags.py csv_in tag1 tag2 tag3 ...
```
Enable to filter the events by tags. Return the events containing all the mentioned tags at ```/data/tag1tag2tag3.csv```. 

### pca_svm.py
```
python pca_svm.py
```
Apply Principal Component Analysis (PCA) and Support Vector Machine (SVM) for dimension reduction, feature extraction and classification. Then choose the events classified as providing free food.    
Take ```/data/training.csv``` for training sets and ```/data/test.csv``` for testing sets. Write the events with all scores at ```/output/pca_svm.scores```. Generate the output of free food events at ```/output/pca_svm.output```

### decisiontree.py
```
python decisiontree.py train.csv test.csv
```
Apply decision tree on the event tags and create branches to classify each event using the information gain based on the Gini Impurity.   
Take ```/data/training.csv``` for training sets and ```/data/test.csv``` for testing sets. Generate the output of free food events at ```/output/decisiontree.output```

### query_optimize.py
```
python query_optimize.py
```
Apply query optimization with Standard Rocchio Method to improve the relevance of the query "free food". Then choose the events according to the similarity between the event description and the optimized query.    
Take ```/data/training.csv``` for training sets and ```/data/test.csv``` for testing sets. Write the events with all scores at ```/output/query_opt.scores```. Generate the output of free food events at ```/output/query_opt.output```

### csv_combine.py
```
python csv_combine.py csv_file_1 csv_file_2
```
Combine two csv and generate the combined file at ```/data/combined.csv```

### map.py
```
python map.py
```
Calculate the moving average precision for the scores in ```/output/pca_svm.scores```, ```/output/query_opt.scores```  as well as the re-ranking scheme that combining both scores. 

## Contributer

Jiachen Wang, Xinyi Wu, Shengjie Pan, Bisheng Liu
