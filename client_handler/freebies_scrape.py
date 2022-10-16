import praw

from os import environ

client_id = environ['CLIENT_ID']
client_secret = environ['CLIENT_SECRET']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="Freebies scrape"
)


def scrape_top_posts(is_daily_check) -> list:
    parsed_submissions = []

    if not is_daily_check:
        for submission in reddit.subreddit("freebies").top("week"):
            if contains_flair(submission) and not is_stickied(submission):
                parsed_submissions.append([submission.title, submission.url])
    else:
        for submission in reddit.subreddit("freebies").top("day"):
            if is_urgent(submission) and contains_flair(submission) and not is_stickied(submission):
                parsed_submissions.append(["HOT TODAY : " + submission.title, submission.url])

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
    # Checks if a post is considered as "urgent" - this is defined as over 200 upvotes on the post in a given day
    return submission.score > 200
