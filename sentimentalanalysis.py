import nltk
from nltk import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist
import csv
import re, string
import random
import pandas as pd
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt')

ptweets = {}
with open('C:/Users/rokky/Documents/GitHub/Smash-Twitter-Bot/positive.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    iterator = 0
    for rows in reader:
        k = rows[0]
        ptweets[iterator] = k
        iterator += 1
ntweets = {}
with open('C:/Users/rokky/Documents/GitHub/Smash-Twitter-Bot/negative.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    iterator = 0
    for rows in reader:
        k = rows[0]
        ntweets[iterator] = k
        iterator += 1
tokenizer = TweetTokenizer()

stop_words = stopwords.words('english')

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)
#print(type(data[0]))
p_tweet_tokens = []
for tweet in range(len(ptweets)):
    p_tweet_tokens.append( tokenizer.tokenize(ptweets[tweet]))
#print(p_tweet_tokens)

n_tweet_tokens = []
for tweet in range(len(ntweets)):
    n_tweet_tokens.append( tokenizer.tokenize(ntweets[tweet]))
#print(ntweets[0])

clean_p_tokens = []
for tokens in p_tweet_tokens:
    clean_p_tokens.append(remove_noise(tokens, stop_words))
clean_n_tokens = []
for tokens in n_tweet_tokens:
    clean_n_tokens.append(remove_noise(tokens, stop_words))
#print(clean_p_tokens)
#print(clean_n_tokens)
all_pos_words = get_all_words(clean_p_tokens)
freq_dist_pos = FreqDist(all_pos_words)
p_tokens_for_model = get_tweets_for_model(clean_p_tokens)
n_tokens_for_model = get_tweets_for_model(clean_n_tokens)

p_set = [(tweet_dict, "Positive") for tweet_dict in p_tokens_for_model]
n_set = [(tweet_dict, "Negative") for tweet_dict in n_tokens_for_model]
dataset = p_set + n_set
print(len(dataset))
random.shuffle(dataset)
classifier = NaiveBayesClassifier.train(dataset)
custom_tweet = " is a very stinky character. He is bad."



etweets = {}
#CHANGE THIS TO THE CORRECT CHARACTER
with open('C:/Users/rokky/Documents/GitHub/Smash-Twitter-Bot/Character Tweets/wolf.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    iterator = 0
    for rows in reader:
        k = rows[0]
        etweets[iterator] = k
        iterator += 1

positivetweets = 0
totaltweets = 0
for i in etweets:
    print(etweets[i])
    custom_tweet = etweets[i]
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    if(classifier.classify(dict([token, True] for token in custom_tokens)) == ("Positive")):
        positivetweets += 1;
    totaltweets += 1;

print(positivetweets/totaltweets)