"""
The model created from the training data is used to label new, unseen tweets.
"""
import pandas as pd
import pickle
from beau_soup_4 import preprocess_tweets


data = pd.read_csv('raw_tweets_0408.csv')
# Perform preprocessing on the tweets, remove mentions, stop words, etc.
preprocessed_tweets = preprocess_tweets(data)
# Load the pipeline, (count vectoriser,, tfidf, classifier), from pickle.
svc_pipeline_pkl_filename = 'svc_pipeline_20200410.pkl'
svc_pipeline_pkl = open(svc_pipeline_pkl_filename, 'rb')
svc_pipeline = pickle.load(svc_pipeline_pkl)

preds = []
for i in range(len(preprocessed_tweets)):
    # Put the tweet into a data frame as this is what the model was trained on. 3 sets of brackets: list of rows, each
    # row, then finally the preprocessed tweet text which at this stage is a list of stemmed words.
    preds.append(svc_pipeline.predict(pd.DataFrame([[[preprocessed_tweets[i]]]], columns=['Tweet'])))

i = 0
for pred in preds:
    data.loc[i, 'Sentiment'] = pred
    i += 1

data.to_csv('raw_tweets_0408_labelled.csv', index=False)