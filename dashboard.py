import pandas as pd
import datetime


def get_file_date(file):
    data = pd.read_csv(file)
    date_time_str = data.loc[0, 'Created at']
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    date = date_time_obj.strftime('%d %b %Y')
    return date
