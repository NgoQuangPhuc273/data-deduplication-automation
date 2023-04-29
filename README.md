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

## Usage:
To run this project, follow these steps:

- Run 
```bash
 pip install -r requirements.txt 
 ``` 
in your terminal to install the required dependencies.

- Run `main.py` to start the program.

A prompt will then appear in the terminal, asking you to compare two records.

For example:


| Record | NAMELAST      | NAMEFIRST | NAMEMID |
| ------ | -------------| ---------| ------- |
| 1      | ammahtagoer  | aku      | None    |
| 2      | amahtagoe    | akul     | m       |

You will be asked to answer whether these two records refer to the same visitor, with the options of "y" for yes, "n" for no, "u" for unsure, or "f" for finished.

For this example, it will be a "y".

Repeat this process until you have answered at least 10 positive and 10 negative cases.

Once you have answered 10 positive and 10 negative cases, you can answer "f" to start the program training.

The program will then output the deduplicated visitor records.

For more information on the full dataset used in this example, please visit the White House Visitor Records page on The White House archives website: https://obamawhitehouse.archives.gov/goodgovernment/tools/visitor-records


## 2. Detailed Description:


### 1. Import and extracting data:
We read the data from a CSV file through Pandas, the select and extract the desired columns/ metrics that need to be deduplicated.


### 2. Data pre-processing: 

The program starts by pre-processing the data to standardize and clean it. This includes removing unnecessary characters and formatting the data to a consistent structure.

- Redundant information: The program first removes any irrelevant or redundant information from the data that is not useful for deduplication. This may include removing data that is missing or incomplete, as well as any columns that are not needed for the analysis.

- Standardizing data formats: The program then standardizes the format of the data to a consistent structure. For example, if the data contains addresses, the program standardizes them to a common format (e.g., we write "123 Main St" instead of "123 Main Street").

### 3. Model training: 
The program uses a supervised learning approach to train its model. The user provides a small sample of the data (typically 500 to 1000 records), which is labeled as either a match or a non-match. The model is trained to identify patterns in the labeled data and use these patterns to identify duplicates in the rest of the dataset.

- Blocking: The program first groups records together that are likely to be duplicated. This is known as record blocking and helps to reduce the number of pairs of records that need to be compared by the model. This is a very important step in the process that ensure the program to cluster similar records in a very big data

- Comparison: The features are then compared between records to calculate a similarity score. This score indicates how similar the records are to each other based on their features.

- Labeling: The user reviews the similarity scores and labels each pair of records as a match or a non-match based on their own judgment.

- Model training: The labeled data is then used to train the model. The model learns to identify patterns in the labeled data and use those patterns to identify duplicates in the rest of the dataset.

### 4. Active learning: 
After training the model, the program uses an active learning approach to continue improving its accuracy. The model is presented with pairs of records and asked to determine whether they are a match or a non-match. The user provides feedback on the accuracy of the model's predictions, and the model is updated accordingly.

- Pair selection: The program selects pairs of records from the dataset that the model is uncertain about. These are typically pairs that have a similarity score that is close to the threshold that the user has set for a match or a non-match.

- User labeling: The user reviews each pair of records and provides feedback on whether they are a match or a non-match. This feedback is used to update the model.

- Iteration: The process of pair selection, user labeling, and model update is repeated until the model's accuracy reaches an acceptable level.


### 5. Clustering: 
The clustering algorithm uses the model's similarity scores to group records that are likely to be duplicates. This step is quite similar to the model training step.


# III. References:
1. Duplicate Clustering (biokic.github.io): https://biokic.github.io/symbiota-docs/coll_manager/dup/

2. Performing Deduplication with Record Linkage and Supervised Learning | by Sue Lynn | Towards Data Science: https://towardsdatascience.com/performing-deduplication-with-record-linkage-and-supervised-learning-b01a66cc6882

3. Machine Learning and Deduplication: https://downsub.com/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D3kGKQqNVibQ%26t%3D874s%26ab_channel%3DChicagoPythonUsersGroup

4. vintasoftware/deduplication-slides: "1 + 1 = 1 or Record Deduplication with Python" Jupyter Notebook (github.com): https://github.com/vintasoftware/deduplication-slides

5. Dedupe.io - De-duplicate and find matches in your Excel spreadsheet or database: https://dedupe.io/

6. A step-by-step guide to implementing data deduplication | TechTarget: https://www.techtarget.com/searchdatabackup/tutorial/A-step-by-step-guide-to-implementing-data-deduplication

7. Deduplicating records — is Machine Learning the answer? | by Sonal Goyal | Medium: https://medium.com/@sonalgoyal/deduplicating-records-is-machine-learning-the-answer-e9579cfda935



