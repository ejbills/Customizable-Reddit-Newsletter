import argparse
import re

from pywebio import start_server
from pywebio.input import input, input_group, actions
from pywebio.output import put_text, put_link

from server import csv_handler


def add_user_form():
    subreddit_prefs = ''

    user_email = input('Input your email', required=True, validate=validate_email)

    subreddit_prefs += format_subreddit_prefs()

    add_subreddit = actions('Would you like to add another subreddit?', ['Yes', 'No'])
    if add_subreddit == 'Yes':
        subreddit_prefs += '+' + format_subreddit_prefs()

    # TODO: Better server implementation
    csv_handler.add_user(user_email, subreddit_prefs)

    put_text('User info has been uploaded.')


def unsubscribe_user_form():
    user_email = input('Input email to unsubscribe', required=True, validate=validate_email)

    csv_handler.unsubscribe_user(user_email)

    put_text(user_email, 'has been unsubscribed.')


def format_subreddit_prefs():
    # Formats returned form data
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
    # Validate email using regex
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not re.match(regex, email_string):
        return 'Invalid email!'


def index():
    put_link('Sign up', app='add_user_form')  # Use `app` parameter to specify the task name
    put_link('Unsubscribe', app='unsubscribe_user_form')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server([index, add_user_form, unsubscribe_user_form], port=args.port)

