import praw
import yaml

conf = yaml.safe_load(open('./conf/application.yaml'))

client_id = conf['reddit_user']['client_id']
client_secret = conf['reddit_user']['client_secret']
user_agent = conf['reddit_user']['user_agent']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


def scrape_top_posts(is_daily_check) -> list:
    parsed_submissions = []

    if not is_daily_check:
        for submission in reddit.subreddit("freebies").top("week", limit=20):
            if contains_flair(submission) and not is_stickied(submission):
                parsed_submissions.append([submission.title, submission.url])
    else:
        for submission in reddit.subreddit("freebies").hot():
            if is_urgent(submission) and contains_flair(submission) and not is_stickied(submission):
                parsed_submissions.append(["ONLY TODAY : " + submission.title, submission.url])

    return parsed_submissions


def contains_flair(submission) -> bool:
    # Checks if the post flair contains the US and is not expired
    us_in_flair = "us " in submission.link_flair_text.lower()
    expired_not_in_flair = "expired" not in submission.link_flair_text.lower()

    return us_in_flair and expired_not_in_flair


def is_stickied(submission) -> bool:
    # Checks if a post is stickied (by the mods of the subreddit), can skip if true
    return submission.stickied


def is_urgent(submission) -> bool:
    # Checks if a post title contains "today" keyword, marked as urgent if true
    return "today" in submission.title.lower()
