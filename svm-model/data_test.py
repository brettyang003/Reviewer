import json
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



class Sentiment:
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"

class Review:
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.sentiment = self.get_sentiment()

    def get_sentiment(self):
        if self.score <= 2:
            return Sentiment.NEGATIVE
        elif self.score == 3:
            return Sentiment.NEUTRAL
        else:
            return Sentiment.POSITIVE

class ReviewContainer:
    def __init__(self, reviews):
        self.reviews = reviews

    def get_text(self):
        return [x.text for x in self.reviews]


    def get_sentiment(self):
        return [x.sentiment for x in self.reviews]

    def evenly_distribute(self):
        negative = list(filter(lambda x: x.sentiment == Sentiment.NEGATIVE, self.reviews))

        positive = list(filter(lambda x: x.sentiment == Sentiment.POSITIVE, self.reviews))

        positive_shrunk = positive[:len(negative)]
        self.reviews = negative + positive_shrunk
        random.shuffle(self.reviews)






file_name = "./data/sentiment/Books_small_10000.json"


reviews_so_far = []
with open(file_name) as f:
    for line in f:
        review = json.loads(line)
        list.append(reviews_so_far, Review(review["reviewText"], review["overall"]))


# Prep data
training, test = train_test_split(reviews_so_far, test_size = 0.33, random_state= 42)

train_container = ReviewContainer(training)

test_container = ReviewContainer(test)


train_container.evenly_distribute()

train_x = train_container.get_text()
train_y = train_container.get_sentiment()

test_container.evenly_distribute()

test_x = test_container.get_text()
test_y = test_container.get_sentiment()




# Bag of words

# This book is great !
# This book was so bad
vectorizer = TfidfVectorizer() # allows to weight importances of words by
# less common = important /// more common = less important
train_x_vectors = vectorizer.fit_transform(train_x)

test_x_vectors = vectorizer.transform(test_x)

#  Classification
#  Linear SVM

from sklearn import svm


clf_svm = svm.SVC(kernel = "linear")
clf_svm.fit(train_x_vectors, train_y)


clf_svm.predict(test_x_vectors[0])

# Decision Tree
#from sklearn.tree import DecisionTreeClassifier

#clf_dec = DecisionTreeClassifier()
#clf_dec.fit(train_x_vectors, train_y)
#print(clf_dec.predict(test_x_vectors[0]))

# Naive Bayes

#from sklearn.naive_bayes import GaussianNB
#clf_gnb = GaussianNB()
#clf_gnb.fit(train_x_vectors, train_y)
#print(clf_gnb.predict(test_x_vectors[0]))


# Logistic Regressions

#from sklearn.linear_model import LogisticRegression
#clf_log = LogisticRegression()
#clf_log.fit(train_x_vectors, train_y)
#print(clf_log.predict(test_x_vectors[0]))

#  Evaluation


# Mean Accuracy
print(clf_svm.score(test_x_vectors, test_y))
#print(clf_dec.score(test_x_vectors, test_y))
#print(clf_gnb.score(test_x_vectors, test_y))
#print(clf_log.score(test_x_vectors, test_y))

# F1 Scores

from sklearn.metrics import f1_score

print(f1_score(test_y, clf_svm.predict(test_x_vectors), average = None, labels=[Sentiment.POSITIVE, Sentiment.NEGATIVE]))



# test set
test_set = ["i hate this bad book", "i have a crush on this loving book amazing book", "trash bad terrible book"]
new_test = vectorizer.transform(test_set)

print(clf_svm.predict(new_test))


# Tuning our model (with Grid Search)

from sklearn.model_selection import GridSearchCV # testing different configs to maximize performance


parameters = {'kernel': ('linear', 'rbf'), 'C': (1,4,8,16,32)}

svc = svm.SVC()

clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(train_x_vectors, train_y)

print(clf.score(test_x_vectors, test_y))

print(f1_score(test_y, clf.predict(test_x_vectors), average = None, labels=[Sentiment.POSITIVE, Sentiment.NEGATIVE]))

# good! and good

# Saving Model

import pickle

with open('./models/sentiment_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)

# Load model


with open('./models/sentiment_classifier.pkl', 'rb') as f:
    loaded_clf = pickle.load(f)

print(test_x[0])
print(loaded_clf.predict(test_x_vectors[0]))