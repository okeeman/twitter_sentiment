from flask import Flask, render_template, request
from twitter_auth import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import tweepy
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
import csv
import pandas as pd
import re
from word_clouds import get_pos_neg_words
from bubble_packed import get_bubble_data, create_js_data
from tweets_by_state import show_tweets_by_state
import plotly
import dash
import dash_html_components as html
from drilldown import drilldown_data
from sentiment_count import sentiment_count_files
from dashboard import get_file_date

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
app = Flask(__name__)


# route means which page it is going to, here root, / # this is MVC like in Tallaght.
@app.route('/', methods=['GET', 'POST'])
def process_query():
    if request.method == 'POST':
        query = request.form['query'] # Trump
        '''
        all_tweets = [['Tweet ID',
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
                       # put in RT id 
                       # id_str = retweeted_status.id_str
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
                        'Entire Object']]
        '''
        all_tweets = []

        for tweet_object in tweepy.Cursor(api.search, q=query, lang='en', result_type='recent',
                                          tweet_mode='extended').items(300):
            if hasattr(tweet_object, 'retweeted_status'):
                if hasattr(tweet_object.retweeted_status, 'full_text'):
                    retweet_status = tweet_object.retweeted_status.full_text
                else:
                    retweet_status = 'retweet_status NA'
            else:
                retweet_status = 'retweet_status NA'

            if hasattr(tweet_object, 'retweeted_status'):
                if hasattr(tweet_object.retweeted_status, 'author'):
                    retweet_author = tweet_object.retweeted_status.author
                else:
                    retweet_author = 'retweet_author NA'
            else:
                retweet_author = 'retweet_author NA'

            if hasattr(tweet_object, 'place'):
                if hasattr(tweet_object.place, 'coordinates'):
                    place_coords = tweet_object.place.coordinates
                else:
                    place_coords = 'Place coords NA'
            else:
                place_coords = 'Place coords NA'

            if hasattr(tweet_object, 'coordinates'):
                if tweet_object.coordinates:
                    object_coords = tweet_object.coordinates
                else:
                    object_coords = 'Object coords NA'
            else:
                object_coords = 'Object coords NA'

            if hasattr(tweet_object.user, 'url'):
                user_url = tweet_object.user.url
            else:
                user_url = 'URL NA'

            if hasattr(tweet_object.user, 'in_reply_to_user_id'):
                in_reply_to_user_id = tweet_object.in_reply_to_user_id
            else:
                in_reply_to_user_id = 'in_reply_to_user_id NA'

            if hasattr(tweet_object, 'possibly_sensitive'):
                possibly_sensitive = tweet_object.possibly_sensitive
            else:
                possibly_sensitive = 'possibly_sensitive NA'

            if hasattr(tweet_object, 'quote_count'):
                quote_count = tweet_object.quote_count
            else:
                quote_count = 'quote_count NA'

            if hasattr(tweet_object, 'entities'):
                if hasattr(tweet_object.entities, 'hashtags'):
                     hashtags = tweet_object.entities.hashtags
                else:
                    hashtags = 'hashtags NA'
            else:
                hashtags = 'hashtags NA'

            if hasattr(tweet_object, 'entities'):
                if hasattr(tweet_object.entities, 'user_mentions'):
                    user_mentions = tweet_object.entities.user_mentions
                else:
                    user_mentions = 'user_mentions NA'
            else:
                user_mentions = 'user_mentions NA'

            if hasattr(tweet_object, 'retweeted_status'):
                soup = BeautifulSoup(retweet_status)
            else:
                soup = BeautifulSoup(tweet_object.full_text)

            all_tweets.append([
                               tweet_object.id,
                               tweet_object.full_text,
                               tweet_object.created_at,
                               tweet_object.source,
                               tweet_object.favorite_count,
                               tweet_object.retweet_count,
                               tweet_object.retweeted,
                               quote_count,
                               in_reply_to_user_id,
                               possibly_sensitive,

                               hashtags,
                               user_mentions,

                               retweet_status, # Text of a retweet if present.
                               retweet_author,

                               tweet_object.user.name,
                               tweet_object.user.screen_name,
                               tweet_object.user.location,
                               user_url,
                               tweet_object.user.description,
                               tweet_object.user.verified,
                               tweet_object.user.followers_count,
                               tweet_object.user.friends_count,
                               tweet_object.user.listed_count,
                               tweet_object.user.created_at,
                               tweet_object.user.utc_offset,
                               tweet_object.user.time_zone,
                               tweet_object.user.geo_enabled,
                               tweet_object.user.lang,

                               place_coords,
                               object_coords,
                               'Sentiment NOT RATED',
                               'Polarity NOT RATED',
                               'Subjectivity NOT RATED',
                               tweet_object])

        #all_tweets = pd.DataFrame(all_tweets, columns=['Text', 'Time', 'Location', 'Account_Desc', 'Verified',
                                                       #'Followers', 'Friends', 'Lists', 'Sentiment']) # dtype = "string"



        #with open('raw_tweets.csv', 'w', newline='', encoding="utf-8") as data:
        with open('raw_tweets_0408.csv', 'a', newline='', encoding="utf-8") as data:
            writer = csv.writer(data)
            writer.writerows(all_tweets)

        return render_template('results.html', tweets=all_tweets, query=query)
    else:
        return render_template('index.html')


@app.route('/sent_column/')
def sent_column():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv', 'raw_tweets_0408_labelled.csv']
    for file in files:
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
    return render_template('sent_column.html', pos=pos, neu=neu, neg=neg)


@app.route('/line/')
def line():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv', 'raw_tweets_0408_labelled.csv']
    for file in files:
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
    return render_template('line.html', pos=pos, neu=neu, neg=neg)


@app.route('/word_cloud/')
def word_cloud():
    # Tip : select View in full screen, then exit, for bigger version of word cloud.
    pos_str = ''
    neg_str = ''
    with open('word_clouds_sentiment.csv', encoding="utf-8") as data_file:
        # Bypass header.
        data_file.readline()
        for file_line in data_file:
            pos_str, neg_str = file_line.split(',')
            # Remove line breaks.
            neg_str = neg_str.replace('\n', ' ').replace('\r', '')
    return render_template('word_cloud.html', positive_words=pos_str, negative_words=neg_str)


@app.route('/bubble_packed/')
def bubble_packed():
    pos_data, neg_data = create_js_data(get_bubble_data())
    return render_template('bubble_packed.html', pos_data=pos_data, neg_data=neg_data)


@app.route('/tweets_by_state/')
def tweets_by_state():
    states_data = show_tweets_by_state()
    return render_template('tweets_by_state.html', states_data=states_data)


@app.route('/drilldown/')
def drilldown():
    pos_data, neg_data, pos_percentage, neg_percentage = drilldown_data()
    return render_template('drilldown.html', pos_data=pos_data, neg_data=neg_data, pos_percentage=pos_percentage,
                           neg_percentage=neg_percentage)


@app.route('/sunburst/')
def sunburst():
    return render_template('sunburst_tweet_object.html')


@app.route('/column_stacked/')
def column_stacked():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv', 'raw_tweets_0408_labelled.csv']
    for file in files:
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
    return render_template('column_stacked.html', pos=pos, neu=neu, neg=neg)


@app.route('/windrose/')
def windrose():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv', 'raw_tweets_0408_labelled.csv']
    for file in files:
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
    return render_template('windrose.html', pos=pos, neu=neu, neg=neg)


@app.route('/heatmap/')
def heatmap():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv', 'raw_tweets_0408_labelled.csv']
    for file in files:
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
    return render_template('heatmap.html', pos=pos, neu=neu, neg=neg)


@app.route('/piechart/')
def piechart():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv']
    for file in files:
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
    return render_template('piechart.html', pos=pos, neu=neu, neg=neg)


@app.route('/dashboard/')
def dashboard():
    pos = []
    neu = []
    neg = []
    files = ['raw_tweets.csv']
    image = ''
    for file in files:
        date = get_file_date(file)
        pos_, neu_, neg_ = sentiment_count_files(file)
        pos.append(pos_)
        neu.append(neu_)
        neg.append(neg_)
        if pos_ > neg_:
            image = 'smiley_face.jpg'
        elif neg_ > pos_:
            image = 'frowning-face.png'
        else:
            image = 'poker_face.jpg'

    pos_str = ''
    neg_str = ''
    with open('word_clouds_sentiment.csv', encoding="utf-8") as data_file:
        # Bypass header.
        data_file.readline()
        for file_line in data_file:
            pos_str, neg_str = file_line.split(',')
            # Remove line breaks.
            neg_str = neg_str.replace('\n', ' ').replace('\r', '')

    states_data = show_tweets_by_state()
    pos_data, neg_data, pos_percentage, neg_percentage = drilldown_data()
    return render_template('dashboard.html', date=date, pos=pos, neu=neu, neg=neg, image=image, positive_words=pos_str,
                           negative_words=neg_str, states_data=states_data, pos_data=pos_data, neg_data=neg_data,
                           pos_percentage=pos_percentage, neg_percentage=neg_percentage)

#=======================================================================================================================
if __name__ == '__main__':
    app.run()