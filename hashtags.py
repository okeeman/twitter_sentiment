"""
Use the hashtags to weight the predictions, e.g. Trumpliespeopledie - negative, MAGA - add weight to the positive.

Could look at mentions too, e.g., @maddow - left wing, likely to be anti-Trump.
"""
import pandas as pd
from bs4 import BeautifulSoup
from find_extract_hashtag_text import find_hashtags

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
data = pd.read_csv('tweets_preprocessed.csv')
num_rows = len(data.index)

hashtags = []
#for index, row in data.iterrows():
for i in range(5):
    if not (data.loc[i, 'Retweet text'] == 'retweet_status NA'):
        tweet = BeautifulSoup(data.loc[i, 'Retweet text'], features="html.parser")
    else:
        tweet = BeautifulSoup(data.loc[i, 'Tweet'], features="html.parser")

    # TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
    # needs to be checked for Nan.
    hashtags.append(find_hashtags(tweet))

















