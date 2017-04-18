#!/bin/bash

python pca_svm.py
python decisiontree.py
python docstovector.py
python combine_results.py ../output/query_opt.output ../output/decisiontree.output ../output/pca_svm.output
python event_date_filter.py 2017-03-01 ../output/combined_result.csv ../output/final.csv
