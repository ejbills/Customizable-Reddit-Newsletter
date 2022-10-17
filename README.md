
# Freebie Tracker

A python script that is meant to be run on a timer every x amount of time to scrape the top posts of the r/freebies subreddit. The script will send an email to the specified recipient(s) within the config file. The script is meant to be run no less than once a week as that is how it is scraping the top posts.

## Deployment

Configure application.yaml in the conf/ directory to specify the list of emails you want to send the results to.

To run this command, you will need to specify multiple key values as environment variables that the script will then pull in through the OS.
The required environment variables are as follows:
```bash
export CLIENT_ID='client_id'; \
export CLIENT_SECRET='client_secret'; \
export EMAIL='email'; \
export APP_PASS='app_pass'; 
```

To run this program on a cron schedule, specify **--cron True** (runs the weekly check). To run the cron job specified for the daily check, include **--cron True --daily True** in the build command.

If you wish to utilize the built-in scheduled freebies scrape, include no flags within the build command. This will default the program to run a check every Saturday at 6:00AM, with daily checks running once every day.

```bash
  py main.py --cron [True/False] --daily [True/False]
```

## Docker
To build the docker image:
```bash
docker build -t freebies:latest . 
```

To run the docker image, you must specify the key values as environment variables as follows:
```bash
docker run -e CLIENT_ID='client_id' \
-e CLIENT_SECRET='client_secret' \
-e EMAIL='email' \
-e APP_PASS='app_pass' \
freebies:latest
```

## Authors

- [@ejbills](https://github.com/ejbills)

