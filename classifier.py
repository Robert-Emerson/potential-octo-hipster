#!/usr/bin/env python

#Creates the Bayesian Classified, then writes it to a file to be used by Map-Reduce

import sys
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle
 
def word_feats(words):
    return dict([(word, True) for word in words])
 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

#Separates reviews into positive and negative
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
 
 #Trains the Bayesian Classifier on these reviews
trainfeats = negfeats + posfeats
classifier = NaiveBayesClassifier.train(trainfeats)

#Writes classifier to a file
fileHandle = open("classifier.pyc", 'w')
pickle.dump(classifier, fileHandle)