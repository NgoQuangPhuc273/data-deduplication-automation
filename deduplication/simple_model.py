import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

import matplotlib.pyplot as plt

data = pd.read_csv('id_whitehouse_final.csv')

data.drop_duplicates(inplace=True)
data.dropna(inplace=True)


X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train['text'])
X_test_vectorized = vectorizer.transform(X_test['text'])


kmeans = KMeans(n_clusters=2, max_iter=600, algorithm = 'auto')
kmeans.fit(X_train_vectorized)

similarities = cosine_similarity(X_test_vectorized)

duplicates = set()
for i in range(len(similarities)):
    for j in range(i+1, len(similarities)):
        if similarities[i][j] > 0.9:
            duplicates.add(i)
data.drop(data.index[list(duplicates)], inplace=True)

plt.scatter(data['x'], data['y'])
