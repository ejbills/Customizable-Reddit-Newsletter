
# Customizable Reddit Newsletter

Turn any list of subreddits into a custom newsletter with support for flair filters and multiple user emails!

## Deployment

Configure user_preferences.csv in the conf/ directory to specify the list of emails and their preferences you want to send the results to. Base the formatting off of the example users inside the file.

To run this command, you will need to specify multiple key values as environment variables that the script will then pull in through the OS.
The required environment variables are as follows:
```bash
export CLIENT_ID='client_id'; \
export CLIENT_SECRET='client_secret'; \
export EMAIL='email'; \
export APP_PASS='app_pass'; 
```
*note:*
- Client ID and Client Secret are generated through reddit via "creating an app." You can do that [through this URL.](https://www.reddit.com/prefs/apps)
- Email is going to be the email you are sending the newsletter from, this codebase has only been tested and verified to work through Gmail accounts.
- App Password is the application password for the gmail account you will be sending the newsletter from. You can generate an app password by [following this Google documentation.](https://support.google.com/accounts/answer/185833?hl=en)

To run this program on a cron schedule, specify **--cron True** (runs the weekly check). To run the cron job specified for the daily check, include **--cron True --daily True** in the build command.

If you wish to utilize the built-in scheduled reddit scrape, include no flags within the build command. This will default the program to run a check every Saturday at 6:00AM, with daily checks running once every day.

```bash
  py main.py --cron [True/False] --daily [True/False]
```

## Docker
To build the docker image:
```bash
docker build -t newsletter:latest . 
```

To run the docker image, you must specify the key values as environment variables as follows:
```bash
docker run -e CLIENT_ID='client_id' \
-e CLIENT_SECRET='client_secret' \
-e EMAIL='email' \
-e APP_PASS='app_pass' \
newsletter:latest
```

## Authors

- [@ejbills](https://github.com/ejbills)

