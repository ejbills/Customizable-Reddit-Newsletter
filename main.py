import conf.config

import argparse
import itertools
import math
import schedule
import time
import threading
import pandas as pd

from client_handler import email_handler, freebies_scrape
from subreddit_config import subreddit_class
from multiprocessing.dummy import Pool as ThreadPool


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


def scrape_then_email(is_daily_check, index):
    temp_user_obj = list(subreddit_class.SubredditConfig.user_objects.values())

    for user_obj in temp_user_obj[index[0]:index[1]]:
        parsed_posts = {}

        for subreddit, flair_filter in user_obj.subreddit_config.items():
            temp_scrape = freebies_scrape.scrape_top_posts(is_daily_check,
                                                           flair_filter,
                                                           subreddit)

            if len(temp_scrape) > 0:  # Check if any results were returned
                parsed_posts[subreddit] = temp_scrape

        if parsed_posts:  # Check if final output is not empty
            print('Sending daily freebies') if is_daily_check else print('Sending weekly freebies')

            email_handler.send_email(user_obj.email, parsed_posts)

def user_pool_handler(is_daily_check):
    # Handles execution of scraping posts and sending email to mailing list
    df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')

    # Create user objects in place
    [subreddit_class.SubredditConfig(email, subreddit_prefs.split('+'))
     for email, subreddit_prefs in zip(df['Email'], df['Subreddits'])]

    thread_amount = 4 if len(subreddit_class.SubredditConfig.user_objects) >= 4 else len(subreddit_class.SubredditConfig.user_objects)

    user_len = math.floor(len(subreddit_class.SubredditConfig.user_objects) / thread_amount)
    index_array = []

    index_tracker = 0
    for _ in range(len(subreddit_class.SubredditConfig.user_objects)):
        index_array.append([index_tracker, index_tracker + user_len])
        index_tracker += user_len

    pool = ThreadPool(thread_amount)
    pool.starmap(scrape_then_email, zip(itertools.repeat(is_daily_check), index_array))

    conf.config.scraped_subreddits = {}  # Remove submissions from completed subreddit query


def time_event(is_daily_check):
    # Handles scheduler/cron specifications
    if arguments.cron is False:  # Bypass scheduler for cron
        if not is_daily_check:  # Weekly check
            schedule.every().week.saturday.at('06:00').do(user_pool_handler, is_daily_check)

            while True:
                schedule_handler(schedule, 30)

        else:  # Daily check
            schedule.every().day.at('18:00').do(user_pool_handler, is_daily_check)

            while True:
                schedule_handler(schedule, 30)

    else:  # cron schedule specified
        user_pool_handler(arguments.daily)


def schedule_handler(schedule_obj, sleep_time):
    # Checks if there is a pending scheduled job every X (specified as sleep_time) minutes
    schedule_obj.run_pending()

    time.sleep(sleep_time * 60)


# Threading needs the extra comma in the args field or else it thinks it is more than one argument (requires tuple)
main_thread = threading.Thread(target=main)
daily_check_thread = threading.Thread(target=time_event, args=(True,))

if __name__ == '__main__':
    main_thread.start()

    if not arguments.cron:
        daily_check_thread.start()
