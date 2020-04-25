"""
This code is for data display purposes. As few of the tweets have geo data included, the Location text data was
processed to find instances where the user has provided US state data. The positive/negative sentiment per state is
analysed to determine if the state as a whole is positive or negative. Trump positive states are coloured red on a
Highcharts Packed Bubble chart and Trump negative states coloured blue.
"""
import pandas as pd


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


def us_state_name_to_code(state_text):
    if state_text.lower() in us_states_names_lower:
        state_index = us_states_names_lower.index(state_text.lower())
        return us_states_codes_lower[state_index]
    else:
        return state_text.lower()


def get_bubble_data():
    data = pd.read_csv('tweets_preprocessed.csv')
    tweet_us_states = []
    sentiment_by_state = {}
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

    # list of tuples (sentiment, state, number_tweets)
    sent_for_bubble = []
    index = 0
    for state in sentiment_by_state:
        positive_sentiment_count = sentiment_by_state[state][0]
        negative_sentiment_count = sentiment_by_state[state][1]
        total_tweets = positive_sentiment_count + negative_sentiment_count
        state = us_states_names[index]

        if positive_sentiment_count > negative_sentiment_count:
            sent_for_bubble.append(('Positive', state, total_tweets))
        else:
            sent_for_bubble.append(('Negative', state, total_tweets))
        index += 1
    return sent_for_bubble


# Create a JavaScript string of the state and sentiment data.
def create_js_data(sent_for_bubble):
    pos_js_string = ''
    neg_js_string = ''
    for state in sent_for_bubble:
        if state[0] == 'Positive':
            pos_js_string += '{name: "' + state[1]
            pos_js_string += '", value: ' + str(state[2])
            # Add bubble colour.
            pos_js_string += ", color: 'red'"
            pos_js_string += '}, '
        else:
            neg_js_string += '{name: "' + state[1]
            neg_js_string += '", value: ' + str(state[2])
            neg_js_string += ", color: 'blue'"
            neg_js_string += '}, '

    # Remove last comma and space.
    pos_js_string = pos_js_string[:-2]
    neg_js_string = neg_js_string[:-2]

    return pos_js_string, neg_js_string

