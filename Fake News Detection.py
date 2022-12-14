import pandas as pd
df=pd.read_csv('train.csv')
df.head()

X=df.drop(‘label’,axis=1) # Features
y=df['label']             # Target

df=df.dropna()

messages=df.copy()
messages.reset_index(inplace=True)
messages.head(10)

messages['text'][6]

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
ps = PorterStemmer()
corpus = [] 
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['text'][i])
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')] 
    review = ' '.join(review)
    corpus.append(review)

corpus[3]

## TFidf Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_v = TfidfVectorizer(max_features=5000,ngram_range=(1,3))
X=tfidf_v.fit_transform(corpus).toarray()y=messages['label']

tfidf_v.get_feature_names()[:20]

## Divide the dataset into Train and Test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

count_df = pd.DataFrame(X_train, columns=tfidf_v.get_feature_names())
count_df.head()

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np
import itertools
from sklearn.metrics import plot_confusion_matrix

classifier=MultinomialNB()
classifier.fit(X_train, y_train)
pred = classifier.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(y_test, pred)
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])

previous_score=0
for alpha in np.arange(0,1,0.1):
    sub_classifier=MultinomialNB(alpha=alpha)
    sub_classifier.fit(X_train,y_train)
    y_pred=sub_classifier.predict(X_test)
    score = metrics.accuracy_score(y_test, y_pred)
    if score>previous_score:
        classifier=sub_classifier
    print("Alpha: {}, Score : {}".format(alpha,score))

## Get Features names
feature_names = cv.get_feature_names()

### Most real
sorted(zip(classifier.coef_[0], feature_names), reverse=True)[:20]

### Most real
sorted(zip(classifier.coef_[0], feature_names))[:20]
