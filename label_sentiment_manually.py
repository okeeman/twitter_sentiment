"""
This code was use to hand label the sentiments using the console and writing the results to file.
Duplicates retweets were removed before labelling sentiment.
"""
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

data = pd.read_csv('labelled_tweets_no_dups.csv')

try:
    for i in range(len(data.index)):
        if not (data.loc[i, 'Retweet text'] == 'retweet_status NA'):
            tweet = data['Retweet text'].loc[i]
        else:
            tweet = data['Tweet'].loc[i]

        print(f'Tweet:{tweet}')
        print('----------------')
        print(f"data['User Description']:{data['Description'].loc[i]}")
        print('-----------------')
        print(f"Current data['Sentiment']:{data.loc[i, 'Sentiment']}")
        data.loc[i, 'Sentiment'] = input('Enter sentiment: ')
        print()
        print('=========== End Tweet =============================================================================================')
        print()
finally:
    data.to_csv('relabelled_tweets_no_dups.csv', index=False)

