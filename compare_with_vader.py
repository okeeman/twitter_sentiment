"""
Vader classified  almost all of the tweets as neutral. Only one was classified negative.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

analyser = SentimentIntensityAnalyzer()
sentiments = ['neg', 'neu', 'pos']


def vader_prediction(tweet_text):
    score = analyser.polarity_scores(tweet_text)
    neg_score = score['neg']
    neu_score = score['neu']
    pos_score = score['pos']
    scores = [neg_score, neu_score, pos_score]
    max_index = np.argmax(scores)
    return sentiments[max_index]


data = pd.read_csv('tweets_preprocessed.csv')
for i in range(len(data.index)):
    # If a retweet, use the retweet text, else use the actual tweet.
    if not (data.loc[i, 'Retweet text'] == 'retweet_status NA'):
        tweet = data['Retweet text'].loc[i]
    else:
        tweet = data['Tweet'].loc[i]
    data.loc[i, 'Tweet text'] = tweet

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(data, data['Sentiment']):
    strat_train_set = data.loc[train_index]
    strat_test_set = data.loc[test_index]

X_train = strat_train_set['Tweet text']
X_test = strat_test_set['Tweet text']
y_train = strat_train_set.loc[:, 'Sentiment']
y_test = strat_test_set.loc[:, 'Sentiment']

y_pred = []
for row in X_test:
    # Each row is a tweet.
    vader_class = vader_prediction(row)
    y_pred.append(vader_class)
print(y_pred)

# Calculate accuracy, i.e., correct predictions divided by total number of instances in the test set.
correct = 0
y_test = list(y_test)
for i in range(len(y_pred)):
    if y_pred[i] == y_test[i]:
        correct += 1

accuracy_score = correct / len(y_pred)
print(f'Vader score is : {accuracy_score:0.4f}')

y_test_sentiment_count = {'neg': 0, 'neu': 0, 'pos': 0}
y_preds_sentiment_count = {'neg': 0, 'neu': 0, 'pos': 0}

for sentiment in y_test:
    if sentiment == 'neg':
        y_test_sentiment_count['neg'] += 1
    elif sentiment == 'neu':
        y_test_sentiment_count['neu'] += 1
    elif sentiment == 'pos':
        y_test_sentiment_count['pos'] += 1

for sentiment in y_pred:
    if sentiment == 'neg':
        y_preds_sentiment_count['neg'] += 1
    elif sentiment == 'neu':
        y_preds_sentiment_count['neu'] += 1
    elif sentiment == 'pos':
        y_preds_sentiment_count['pos'] += 1

print(f'Actual labels: {y_test_sentiment_count}')
print(f'Vader labels:  {y_preds_sentiment_count}')







