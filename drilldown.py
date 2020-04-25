"""
This code is used for display purposes. The user's Location data is used to find US states. The positive and negative
sentiment counts per state are used to determine if a state is Trump positive or negative. The drilldown shows the
percentage of the tweets per state.
"""
import pandas as pd

counts = pd.read_csv('sentiment_count_first_file.csv')
pos_count = counts.loc[0, 'Positive']
neg_count = counts.loc[0, 'Negative']
total = pos_count + neg_count
pos_percentage = pos_count / total * 100
neg_percentage = neg_count / total * 100

data = pd.read_csv('tweets_preprocessed.csv')
us_states_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
                   'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                   'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                   'WI', 'DC']
us_states_names = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                   'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                   'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                   'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                   'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                   'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                   'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia']
us_states_codes_lower = [state.lower() for state in us_states_codes]
us_states_names_lower = [state.lower() for state in us_states_names]
tweet_us_states = []
sentiment_by_state = {}


# Example,'New York' to 'ny'. This code is sent to the Highcharts drilldown chart.
def us_state_name_to_code(state_text):
    if state_text.lower() in us_states_names_lower:
        state_index = us_states_names_lower.index(state_text.lower())
        return us_states_codes_lower[state_index]
    else:
        return state_text.lower()


def get_state_tweets_by_sentiment():
    for index, row in data.iterrows():
        location = data.loc[index, 'Location']
        # Avoid Nan.
        if isinstance(location, str):
            # Looking for location data in the form 'city, state'.
            comma = location.find(',')
            if comma != -1:
                state = location[comma + 1:].strip()

                # Check if the data found was a US state.
                if state.lower() in us_states_codes_lower or state.lower() in us_states_names_lower:
                    # Convert, e.g., 'new york' to 'ny'
                    state = us_state_name_to_code(state)
                    state_index = us_states_codes.index(state.upper())
                    state = us_states_names[state_index]
                    tweet_us_states.append(state)
                    sentiment = data.loc[index, 'Sentiment']

                    # Do a count of positive/negative sentiment by state.
                    if state in sentiment_by_state:
                        if sentiment == 'pos':
                            first_element_value = sentiment_by_state[state][0]
                            second_element_value = sentiment_by_state[state][1]
                            sentiment_by_state[state] = (first_element_value + 1, second_element_value)
                        elif sentiment == 'neg':
                            first_element_value = sentiment_by_state[state][0]
                            second_element_value = sentiment_by_state[state][1]
                            sentiment_by_state[state] = (first_element_value, second_element_value + 1)
                    else:
                        if sentiment == 'pos':
                            sentiment_by_state[state] = (1, 0)
                        elif sentiment == 'neg':
                            sentiment_by_state[state] = (0, 1)

    # sentiment_by_state has two elements, the first is a string of the state name as a code, the second is a tuple in
    # the form (positive sentiment count, negative sentiment count).
    return sentiment_by_state


def drilldown_data():
    # This is a list of tuples of the form (state, positive sentiment count).
    pos_tweet_count_by_state = []
    # This is a list of tuples of the form (state, negative sentiment count).
    neg_tweet_count_by_state = []
    sentiment_by_state = get_state_tweets_by_sentiment()
    total_pos_tweets = 0
    total_neg_tweets = 0

    for state in sentiment_by_state:
        pos_tweet_count_by_state.append((state, sentiment_by_state[state][0]))
        neg_tweet_count_by_state.append((state, sentiment_by_state[state][1]))
        # Get the total counts in order to determine percentages.
        total_pos_tweets += sentiment_by_state[state][0]
        total_neg_tweets += sentiment_by_state[state][1]

    pos_tweet_percent_by_state = []
    for state in pos_tweet_count_by_state:
        percent = state[1] / float(total_pos_tweets) * 100
        pos_tweet_percent_by_state.append((state[0], percent))

    neg_tweet_percent_by_state = []
    for state in neg_tweet_count_by_state:
        percent = state[1] / float(total_neg_tweets) * 100
        neg_tweet_percent_by_state.append((state[0], percent))

    # Create JavaScript data for drilldowns.
    pos_data = ''
    for state, percent in pos_tweet_percent_by_state:
        pos_data += '["' + state + '",' + str(percent) + '],'

    # Remove last comma
    pos_data = pos_data[:-1]

    neg_data = ''
    for state, percent in neg_tweet_percent_by_state:
        neg_data += '["' + state + '",' + str(percent) + '],'

    # Remove last comma
    neg_data = neg_data[:-1]

    return pos_data, neg_data, pos_percentage, neg_percentage
