'''
This code is used to preprocess the tweets.
'''
from bs4 import BeautifulSoup
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()


def tokenize_and_stem(text):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in word_tokenize(text)]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

#data = pd.read_csv('relabelled_tweets_no_dups.csv')

def preprocess_tweets(data):
    num_rows = len(data.index)

    data['Preprocessed tweet'] = pd.Series('Preprocessed tweet NA', index=data.index)
    data['Preprocessed tweet'] = data['Preprocessed tweet'].astype('object')

    for i in range(num_rows):
        if not (data.loc[i, 'Retweet text'] == 'retweet_status NA'):
            soup = BeautifulSoup(data.loc[i, 'Retweet text'], features="html.parser")
        else:
            soup = BeautifulSoup(data.loc[i, 'Tweet'], features="html.parser")

        # HTML decoding, e.g. &amp; to &
        tweet = soup.get_text()

        # Remove mentions.
        tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)

        # Remove URLS.
        tweet = re.sub('https?://[A-Za-z0-9./]+', '', tweet)

        # Remove pound from hashtags but kep the text.
        tweet = tweet.replace('#', '')

        tokens = word_tokenize(tweet)

        # Stop words.
        tokens_stopped = [w for w in tokens if not w in stop_words]

        # All lower case now
        stems = []
        for t in tokens_stopped:
            stems.append(porter.stem(t))

        # remove punctuation
        stemmed_no_punc = [stem for stem in stems if stem.isalpha()]

        # Remove keyword
        keyword_removed = [token for token in stemmed_no_punc if token not in ('trump')]

        # Assign a list to a cell in Pandas.
        data.at[i, 'Preprocessed tweet'] = keyword_removed

    headers = ['Tweet ID',
                           'Tweet',
                           'Created at',
                           'Source',
                           'Favorite count', # Number of times this tweet has been liked by other users.
                           'Retweet count', # Number of times this tweet has been retweeted.
                           'Retweeted', # Is this tweet a retweet.
                           'Quote count', # Nullable. This object is only available with the Premium and Enterprise tier products.
                           'In reply to user ID', # If this is a reply to a user, that user's ID.
                           'Possibly sensitive', # Nullable. This field only surfaces when a Tweet contains a link.
                           'Hashtags',
                           'User mentions',  # Other users mentioned in the tweet.

                           ## Retweet and
                           'Retweet text',
                           'Retweet author',

                           ## End retweet info

                           ## User object data ##
                           'Name',
                           'Screen name',
                           'Location',
                           'User URL',
                           'Description',
                           'Verified',
                           'Followers',
                           'Friends',
                           'Lists',
                           'Account created',
                           'UTC offset',
                           'Time zone',
                           'Geo enabled',
                           'Language',
                            ## End user object ##

                            'Place coords',
                            'Object coords',

                            'Sentiment',
                            'Polarity',
                            'Subjectivity',
                            'Entire Object',
                            'Retweet ID',
                            'Preprocessed tweet']

#data.to_csv('tweets_preprocessed.csv', columns=headers, index=False)

    return data['Preprocessed tweet']




