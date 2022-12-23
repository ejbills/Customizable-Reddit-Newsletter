import re

from pywebio import start_server
from pywebio.input import input, input_group, actions
from pywebio.output import put_text

import csv_handler


def form():
    subreddit_prefs = ''

    user_email = input('Input your email', required=True, validate=validate_email)

    subreddit_prefs += format_subreddit_prefs()

    add_subreddit = actions('Would you like to add another subreddit?', ['Yes', 'No'])
    if add_subreddit == 'Yes':
        subreddit_prefs += '+' + format_subreddit_prefs()

    csv_handler.add_user(user_email, subreddit_prefs)
    put_text('User info has been uploaded')


def format_subreddit_prefs():
    output_string = ''
    flair_prefs = {}

    subreddit_info = input_group('Subreddit info', [
        input('Input subreddit', name='subreddit'),
        input('Input required flairs', name='required_flairs'),
        input('Input restricted flairs', name='restricted_flairs')
    ])

    flair_prefs['required_flairs'] = []
    flair_prefs['restricted_flairs'] = []

    for flair in subreddit_info['required_flairs'].split(','):
        if len(flair) > 0:
            flair = flair.strip()

            flair_prefs['required_flairs'].append(flair)

    for flair in subreddit_info['restricted_flairs'].split(','):
        if len(flair) > 0:
            flair = flair.strip()

            flair_prefs['restricted_flairs'].append(flair)

    output_string += subreddit_info['subreddit'] + "=" + str(flair_prefs)

    return output_string


def validate_email(email_string):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not re.match(regex, email_string):
        return 'Invalid email!'


if __name__ == '__main__':
    start_server(form, port=443)

