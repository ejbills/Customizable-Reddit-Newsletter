
# Freebie Tracker

A python script that is meant to be run on a timer every x amount of time to scrape the top posts of the r/freebies subreddit. The script will send an email to the specified recipient(s) within the config file. The script is meant to be run no less than once a week as that is how it is scraping the top posts.

## Deployment

Configure application.yaml in the conf/ directory (be careful not to add this into your own git repo).

To run this program on a cron schedule, specify **--cron True** (runs the weekly check). To run the cron job specified for the daily check, include **--cron True --daily True** in the build command.

If you wish to utilize the built-in scheduled freebies scrape, include no flags within the build command. This will default the program to run a check every Saturday at 10:00AM, with daily checks every hour.

```bash
  py main.py --cron [True/False] --daily [True/False]
```

## Authors

- [@ejbills](https://github.com/ejbills)

