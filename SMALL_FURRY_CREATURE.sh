#!/bin/sh

./classifier.py
cat ./tweet_file.txt | ./mapper.py  2> inconclusive_tweets.txt | ./reducer.py > output.csv
