import argparse
import schedule
import time
import yaml
import threading

from client_handler import email_handler, freebies_scrape

conf = yaml.safe_load(open('./conf/application.yaml'))

mail_list = conf['recipient_list']['users']

# Handle arguments in command line
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--cron", default=False,
                    help="specify if using cron to schedule app functions (bypass scheduler)")
parser.add_argument("-d", "--daily", default=False,
                    help="specify if daily check (limited use for cron scheduler)")

arguments = parser.parse_args()


def main():
    # Start program
    if not arguments.cron:
        print("cron not specified, defaulting to running once a week (every Saturday @ 6AM LOCAL) with daily checks")
        time_event(False)

    else:
        print("Weekly process running") if not arguments.daily else print("Daily process running")
        print("cron specified, defaulting to running script once per script run")

        time_event(arguments.daily)


def send_freebies(is_daily_check):
    # Handles execution of scraping posts and sending email to mailing list
    parsed_posts = {}

    parsed_posts['freebies'] = freebies_scrape.scrape_top_posts(is_daily_check,
                                                                {'required_flairs': ['us only'],
                                                                 'restricted_flairs': ['expired']},
                                                                'freebies')

    parsed_posts['frugalmalefashion'] = freebies_scrape.scrape_top_posts(is_daily_check,
                                                                {'required_flairs': ['asfsadklfjhsdhjkfg'],
                                                                 'restricted_flairs': ['expired']},
                                                                'frugalmalefashion')

    parsed_posts['frugalfemalefashion'] = freebies_scrape.scrape_top_posts(is_daily_check,
                                                                {'required_flairs': ['sadfsdkfjsdfikhj'],
                                                                 'restricted_flairs': ['expired']},
                                                                'frugalfemalefashion')

    print(str(len(parsed_posts)) + " results returned")

    if parsed_posts:  # Check if any results are returned
        print("Sending daily freebies") if is_daily_check else print("Sending weekly freebies")

        email_handler.send_email(mail_list, parsed_posts)


def time_event(is_daily_check):
    # Handles scheduler/cron specifications
    if arguments.cron is False:  # Bypass scheduler for cron
        if not is_daily_check:  # Weekly check
            schedule.every().week.saturday.at("06:00").do(send_freebies, is_daily_check)

            while True:
                schedule_handler(schedule, 30)

        else:  # Daily check
            schedule.every().day.at("18:00").do(send_freebies, is_daily_check)

            while True:
                schedule_handler(schedule, 30)

    else:  # cron schedule specified
        send_freebies(arguments.daily)


def schedule_handler(schedule_obj, sleep_time):
    # Checks if there is a pending scheduled job every X (specified as sleep_time) minutes
    schedule_obj.run_pending()

    time.sleep(sleep_time * 60)


# Threading needs the extra comma in the args field or else it thinks it is more than one argument (requires tuple)
main_thread = threading.Thread(target=main)
daily_check_thread = threading.Thread(target=time_event, args=(True,))

if __name__ == "__main__":
    main_thread.start()

    if not arguments.cron:
        daily_check_thread.start()
