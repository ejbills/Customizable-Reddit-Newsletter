import conf.config

import argparse
import ast
import schedule
import time
import pandas as pd

from multiprocessing import Process
from prawcore import PrawcoreException, Forbidden

from client_handler import email_handler, subreddit_scrape

# Handle arguments in command line
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--cron', default=False,
                    help='specify if using cron to schedule app functions (bypass scheduler)')
parser.add_argument('-d', '--daily', default=False,
                    help='specify if daily check (limited use for cron scheduler)')

arguments = parser.parse_args()


def main():
    # Start program
    if not arguments.cron:
        print('cron not specified, defaulting to running once a week (every Saturday @ 6AM LOCAL) with daily checks')
        time_event(False)

    else:
        print('Weekly process running') if not arguments.daily else print('Daily process running')
        print('cron specified, defaulting to running script once per script run')

        time_event(arguments.daily)


def parse_reddit(daily_check):
    # Handles execution of scraping posts and sending email to mailing list
    df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')

    for index, row in df.iterrows():
        email = row['Email']
        queries = row['Query'].split('+')  # queries are grouped into one category, separated by +

        parsed_posts = {}

        for query in queries:
            query_term, query_config = query.split('=')
            query_config = dict(ast.literal_eval(query_config))  # query will be in python dict format

            temp_scrape = []

            try:
                temp_scrape = subreddit_scrape.scrape_top_posts(daily_check,
                                                                query_config,
                                                                query_term)
            except Forbidden as e:
                print("Forbidden, continuing.", e)

            except PrawcoreException as e:
                print("Critical API call error - passing empty subreddit stream.", e)

            if len(temp_scrape) > 0:  # Check if any results were returned
                parsed_posts[query_term] = temp_scrape

        if parsed_posts:  # Check if final output is not empty
            print('Sending daily email') if daily_check else print('Sending weekly email')

            email_handler.send_email(daily_check, email, parsed_posts)

    conf.config.prev_searched_queries = {}  # Remove submissions from completed subreddit query


def time_event(is_daily_check):
    # Handles scheduler/cron specifications
    if arguments.cron is False:  # Bypass scheduler for cron
        if not is_daily_check:  # Weekly check
            schedule.every().week.saturday.at('06:00').do(parse_reddit, is_daily_check)

            while True:
                schedule_handler(schedule, 30)

        else:  # Daily check
            schedule.every().day.at('18:00').do(parse_reddit, is_daily_check)

            while True:
                schedule_handler(schedule, 30)

    else:  # cron schedule specified
        parse_reddit(arguments.daily)


def schedule_handler(schedule_obj, sleep_time):
    # Checks if there is a pending scheduled job every X (specified as sleep_time) minutes
    schedule_obj.run_pending()

    time.sleep(sleep_time * 60)


if __name__ == '__main__':
    # Start threads
    weekly_thread = Process(target=main)
    daily_thread = Process(target=time_event, args=(True,))

    weekly_thread.start()

    if not arguments.cron:
        daily_thread.start()
        daily_thread.join()

    weekly_thread.join()
