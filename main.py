import csv
import re
import logging
import optparse

import dedupe
from unidecode import unidecode
import deduplication

def preProcess(column):
    """
    Data Cleaning
    """
    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()

    if not column:
        column = None
    return column


def readData(filename):
    """
    Reading the data from a csv file
    Create a dictionary of records where the key is a unique record ID and each value is dict
    """

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            row_id = int(row['Id'])
            data_d[row_id] = dict(clean_row)

    return data_d


if __name__ == '__main__':
    """
    I.Setting up files
    """

    input = 'csv_example/id_whitehouse_final.csv'
    output = 'csv_example/whitehouse_csv_example_output.csv'
    settings = 'csv_example/csv_example_learned_settings'
    training = 'csv_example/csv_example_training.json'

    print('Importing Data')

    data_d = readData(input)
    deduplication = deduplication()
        
    fields = [
        {'field': 'NAMELAST','type': 'String'},
        {'field': 'NAMEFIRST','type': 'String'},
        {'field': 'NAMEMID','type': 'String'},
    ]

    """
    Create a new deduper object and pass our data model to it.
    """
    deduper = dedupe.Dedupe(fields)

    deduper.prepare_training(data_d)

    """
    II.Active Learning

    Deduplication finds the next pair of records.

    It is least certain about and ask you to label them as duplicates or not.

    Use 'y', 'n' and 'u' keys to flag duplicates.

    Press 'f' when you are finished
    """

    print('Active Labeling')

    dedupe.console_label(deduper)

    deduper.train()

    with open(training, 'w') as tf:
        deduper.write_training(tf)

    with open(settings, 'wb') as sf:
        deduper.write_settings(sf)

    """
    Clustering

    Now, `partition` method will return sets of records that deduplication believes are all referring to the same entity.
    """

    print('Start Clustering')
    clustered_dupes = deduper.partition(data_d, 0.5)

    print('Total number of duplicate sets:', len(clustered_dupes))

    """Writing Results

    Write our original data back out to a CSV with a new column called
    'Cluster ID' which indicates which records refer to each other.
    """

    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score
            }

    with open(output, 'w') as f_output, open(input) as f_input:

        reader = csv.DictReader(f_input)
        fieldnames = ['Cluster ID', 'confidence_score'] + reader.fieldnames

        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row_id = int(row['Id'])
            row.update(cluster_membership[row_id])
            writer.writerow(row)
