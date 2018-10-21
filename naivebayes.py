# -*- coding: utf-8 -*-
import string
from itertools import chain

from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier as nbc
from nltk.corpus import CategorizedPlaintextCorpusReader
import nltk
import sys
import os

mydir_train = '.\\Docs-txt\\train'
mydir_test = '.\\Docs-txt\\test'
featureVector_train = []
featureVector_test = []

mr_train = CategorizedPlaintextCorpusReader(mydir_train, r'(?!\.).*\.txt', cat_pattern=r'(Analyst Report|Case Study|Datasheets|Technical Brief|Whitepaper)/.*')
mr_test = CategorizedPlaintextCorpusReader(mydir_test, r'(?!\.).*\.txt', cat_pattern=r'(Analyst Report|Case Study|Datasheets|Technical Brief|Whitepaper)/.*')

stop = stopwords.words('english')

with open('.\\stopwords.txt') as f:
    stop = f.read().splitlines()

documents_train = [([w for w in mr_train.words(i) if w.lower() not in stop and w.lower() not in string.punctuation], i.split('/')[0]) for i in mr_train.fileids() if os.path.getsize(os.path.join(mydir_train,i)) > 0]
documents_test = [([w for w in mr_test.words(i) if w.lower() not in stop and w.lower() not in string.punctuation], i.split('/')[0]) for i in mr_test.fileids() if os.path.getsize(os.path.join(mydir_test,i)) > 0]

word_features_train = FreqDist(chain(*[i for i,j in documents_train]))
word_features_train = list(word_features_train.keys())[:1000]

word_features_test = FreqDist(chain(*[i for i,j in documents_test]))
word_features_test = list(word_features_test.keys())[:1000]

for w in word_features_train:
    if (w in stop):
        continue
    else:        
        featureVector_train.append(w.lower())

for w in word_features_test:
    if (w in stop):
        continue
    else:        
        featureVector_test.append(w.lower())

train_set = [({i:(i in tokens) for i in featureVector_train}, tag) for tokens, tag in documents_train]
test_set = [({i:(i in tokens) for i in featureVector_test}, tag) for tokens, tag in documents_test]

print
classifier = nbc.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
print
classifier.show_most_informative_features(5)
print
for doc, gold_label in test_set:
    tagged_label = classifier.classify(doc)
    print(tagged_label + " " + gold_label)
    
