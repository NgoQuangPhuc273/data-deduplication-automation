# CSCI 374: Data Deduplication using Machine Learning

Phuc Ngo

# I. Introduction:
In this project, we will apply machine learning techniques to the problem of data deduplication. Data deduplication is the process of identifying and removing duplicate records from a dataset, such as customer profiles, product listings, or medical records. Data deduplication is important for data quality, data integration, and data analysis.

However, data deduplication is challenging because real-world data is often noisy, incomplete, inconsistent, and heterogeneous. For example, two records that refer to the same entity may have different spellings, formats, abbreviations, or missing values. Therefore, simple string matching or rule-based methods are not sufficient to handle the complexity and diversity of data.

Machine learning can help to overcome these challenges by learning from examples of duplicate and non-duplicate pairs of records, and by generalizing to unseen cases. Machine learning can also leverage various features and similarity measures to capture the semantic and syntactic similarities between records.

# II. Description:


## 1. Overall Description

The project focuses on deduplicating the names of visitors from the White House Visitor Records dataset, which contains approximately 100,000 records.

However, for simplicity and speed, we will only use the first 2,700 records. The three variables used to identify a visitor are NAMELAST, NAMEFIRST, and NAMEMID.

The approach to achieve this goal includes: 
- importing the dataset
- selecting and extracting data
- pre-processing the data
- training the model
- active learning
- clustering 
- merging.

## Usage:
To run this project, follow these steps:

Run 
```bash
 pip install -r requirements.txt 
 ``` 
in your terminal to install the required dependencies.

Run `main.py` to start the program.


A prompt will then appear in the terminal, asking you to compare two records.

For example:

Record 1: 

NAMELAST: ammahtagoer, 

NAMEFIRST: aku, 

NAMEMID: None

Record 2: 

NAMELAST: amahtagoe, 

NAMEFIRST: akul, 

NAMEMID: m

You will be asked to answer whether these two records refer to the same visitor, with the options of "y" for yes, "n" for no, "u" for unsure, or "f" for finished.

Repeat this process until you have answered at least 10 positive and 10 negative cases.

Once you have answered 10 positive and 10 negative cases, you can answer "f" to start the program training.

The program will then output the deduplicated visitor records.

For more information on the full dataset used in this example, please visit the White House Visitor Records page on The White House archives website: https://obamawhitehouse.archives.gov/goodgovernment/tools/visitor-records


## 2. Detailed Description:





