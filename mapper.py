#!/usr/bin/env python

import sys
import json
import pickle

def word_feats(words):
    return dict([(word, True) for word in words])
    
#loads the bayesian classifier from a file. Helps to speed up the more hadoopy version
classifier = pickle.load(open("classifier.pyc", 'r'))

#tags were found by quick analyses of data
#most of the anti-Dragas tags. there are a lot. some  are cut off as their longest common substring is listed
neg_dragas_tags = ["thingsthatwillhappenbeforebov","boardpleaseresign","boodragas","#dictatordrago","#ditchdragas","#donewithdragas","#donotreappointdragos","dontdragasmyu","#dragasfail","#dragasgate","dragasmust","dragasresign","#dragasout","#dragass","#dragonfiredragas","dragsresign","#dumpdragas","#emperordragas","#entirebovneedstoresign","#fightuniversitycorporatization","#firedragas","#firethewholeboard","#grinchdragastookmybeloveduniversity","#pleaseseethedoordragas","#resigndragas","#saygoodbyetodragas","#shakedragasoff","#sicsemperdragas","#unseatdragas","#unvisitdragas", "rallyforhonor", "rally4honor", "vigilforhonor"]
#most of the pro-Sully tags. Some with <3 occurences were omitted
pos_sully_tags = ["reinstate","beersonsullivan","bringbacksull","freesull","hoos4sull","hoosforsull","reinstatesull","sullivanscomingback","teamsull","welcomebacksull"]
dragas = "dragas"
dragas_references = ["dragas", "rector", "board", "bov", "helen", "visitors"]
sullivan = "sullivan"
sullivan_references = ["sullivan", "president", "teresa", "theresa", "sully", "tsull", "sull"]

#counter for tweets. equal_references tells us the number of tweets where dragas and sully are mentioned equally
#neg_dragas_count is the number of tweets immediately set as anti-dragas based on hashtags
#pos_sully_count is the number of tweets immediately set as pro-sully based on hashtags
equal_references = 0
neg_dragas_count = 0
pos_sully_count = 0

#counters used to keep track of the number of tweets for dragas and sullivan
dragas_tweet = 0
sullivan_tweet = 0
  
#This is the path to where all the json file tweets are stored
tweetFilePath = "/home/robert/4501/success/"

#finds the subject of the tweet based on who is mentioned more in the tweet text
def find_subject_of_tweet(text):
  global dragas_references
  global sullivan_references
  global equal_references
  global sullivan
  global dragas
  
  global dragas_tweet
  global sullivan_tweet
  
  dragas_count = 0
  for mention in dragas_references:
    dragas_count += text.count (mention)

  sullivan_count = 0
  for mention in sullivan_references:
    sullivan_count += text.count (mention)
    
    if (sullivan_count > dragas_count):
	sullivan_tweet += 1
	return sullivan;
    elif (dragas_count > sullivan_count):
	dragas_tweet += 1
	return dragas;
    elif (dragas_count > 0 and sullivan_count > 0):
	# counter for number of equal references
	equal_references += 1
	return None;
    else:
	return None;

# input comes from STDIN (standard input)
for line in sys.stdin:
    #useful variables. tweet_score is the exit code, neg_dragas tells us if the tweet is anti-dragas
    #pos_sully tells us if the tweet is pro-sully
    tweet_score = 0
    neg_dragas = False
    pos_sully = False
    
    # remove white space from line
    line.strip()
    # open json file. Take substring to remove newline at end
    json_data = open(tweetFilePath+line[:len(line)-1])
    # get text from the json text field and set it to lower case
    data = json.load(json_data)
    data_line = data["text"].encode('utf8')
    words = data_line.lower()
    
    #checks if the tweet is automatically pro-Sullivan based on hashtags
    for hashtag in pos_sully_tags:
      if ( hashtag in words and not pos_sully):
	pos_sully = True
	
    #checks if the tweet is automatically anti-Dragas based on hashtags
    for hashtag in neg_dragas_tags:
      if ( hashtag in words and not pos_sully and not neg_dragas):
	neg_dragas = True
	
    if (pos_sully):
      tweet_score = 1
      pos_sully_count += 1
    elif (neg_dragas):
      tweet_score = 5
      neg_dragas_count += 1
    
    #if hashtags are inconclusive, we have to actually analyze the tweet
    else:
      #classifies the tweet as positive or negative
      sentiment = classifier.classify(word_feats(words.split()))
      #finds the subject of the tweet
      person = find_subject_of_tweet(words)
      
      #Create a tweet score if person is defined. Toss tweet if it's not.
      if (person):
	
	if (sentiment == 'pos'):
	  tweet_score += 1
	else:
	  tweet_score += 2
	#adds 3 to the tweet score to denote the subject is dragas
	if (person is dragas):
	  tweet_score += 3
      else:
	  tweet_score = 0
    date = data["created_at"][3:10];
    print '%s\t%s' % (date, tweet_score)
    
#diagnostic. The number of times Sullivan and Dragas are mentioned equally in text
sys.stderr.write('Num of equal references: %s\n' % equal_references)
sys.stderr.write('Num of sullivan tweets: %s\n' % sullivan_tweet)
sys.stderr.write('Num of dragas tweets: %s\n' % dragas_tweet)