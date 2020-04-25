"""
The idea of this code is to search the tweet text for hashtags and use these to create a feature to improve
classification accuracy. Examples: Trump positive: #MAGA, #KAG; Trump negative: #TrumpLiesPeopleDie.

Could look at mentions too, e.g., @maddow - left wing, likely to be anti-Trump.
"""
def find_hashtags(tweet_text):
    start_index = 0
    hashtags = []

    while True:
        hashtag = tweet_text.find('#', start_index)
        if hashtag == -1:
            break
        else:
            hashtag_end = tweet_text.find(' ', hashtag)
            hashtag_text = tweet_text[hashtag+1:hashtag_end]
            hashtags.append(hashtag_text)
            start_index = hashtag_end
    return hashtags

#=======================================================================================================================
if __name__ == '__main__':
    print(find_hashtags('This is a sample. #MAGA Thank you Mr. President! #KAG 2020 re-election.'))
