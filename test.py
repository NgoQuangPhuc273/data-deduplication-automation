import csv
import re
import logging
import argparse
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import numpy as np


def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """
    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    # If data is missing, indicate that by setting the value to `None`
    if not column:
        column = None
    return column


def read_data(filename):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clean_row = {k: preProcess(v) for (k, v) in row.items()}
            data.append(clean_row)
    return data


if __name__ == '__main__':
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Perform record linkage on a dataset')
    parser.add_argument('input_file', help='input CSV file')
    parser.add_argument('output_file', help='output CSV file')
    args = parser.parse_args()

    # Read in the data
    print('Importing data...')
    data = read_data(args.input_file)

    # Extract the relevant fields
    fields = ['name', 'email', 'phone', 'address']
    records = [{k: v for k, v in d.items() if k in fields} for d in data]

    # Vectorize the records
    print('Vectorizing records...')
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([r[field] for field in fields] for r in records)

    # Cluster the records
    print('Clustering records...')
    dbscan = DBSCAN(eps=0.5, min_samples=2, metric='cosine')
    clusters = dbscan.fit_predict(vectors)

    # Add the cluster labels to the records
    for i, record in enumerate(records):
        record['cluster'] = clusters[i]

    # Write the output to a CSV file
    print('Writing results...')
    with open(args.output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(fields) + ['cluster']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
