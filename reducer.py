#!/usr/bin/env python

from operator import itemgetter
import sys

current_date = None
sullivan_pos = 0
sullivan_neg = 0
dragas_pos = 0
dragas_neg = 0
num_discarded = 0
date = None

#takes input from the map phase and parses the tweetScore to determine total sentiment for that day
def parseScore(score):
  global sullivan_pos
  global sullivan_neg
  global dragas_pos
  global dragas_neg
  global num_discarded
  if (score == 1):
    sullivan_pos += 1
  elif (score == 2):
    sullivan_neg -= 1
  elif (score == 4):
    dragas_pos += 1
  elif (score == 5):
    dragas_neg -= 1
  else:
    num_discarded += 1
    
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    date, tweet_score = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        tweet_score = int(tweet_score)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_date == date:
        parseScore(tweet_score)
    else:
        if current_date:
            # write result to STDOUT
            print '%s,%s,%s,%s,%s' % (current_date, sullivan_pos, sullivan_neg, dragas_pos, dragas_neg)
        #reset all the variables for the new date
        sullivan_pos = 0
        sullivan_neg = 0
        dragas_pos = 0
        dragas_neg = 0
        current_date = date
        parseScore(tweet_score)

# do not forget to output the last word if needed!
if current_date == date:
  print '%s,%s,%s,%s,%s' % (current_date, sullivan_pos, sullivan_neg, dragas_pos, dragas_neg)
#diagnostic. Prints the number of tweets we discarded
print'Num discarded: %s' % (num_discarded)