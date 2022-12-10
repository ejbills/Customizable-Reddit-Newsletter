import praw

from os import environ

client_id = environ['CLIENT_ID']
client_secret = environ['CLIENT_SECRET']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="Freebies scrape"
)


def scrape_top_posts(is_daily_check, filter_dict, subreddit) -> list:
    parsed_submissions = []

    if not is_daily_check:
        for submission in reddit.subreddit(subreddit).top("week"):
            if contains_flairs(filter_dict, submission) and not is_stickied(submission):
                parsed_submissions.append([submission.title, submission.url])
    else:
        for submission in reddit.subreddit(subreddit).top("day"):
            if is_urgent(submission) and contains_flairs(filter_dict, submission) and not is_stickied(submission):
                parsed_submissions.append(["HOT TODAY : " + submission.title, submission.url])

    return parsed_submissions


def contains_flairs(filter_dict, submission) -> bool:
    # Checks if the post flair passes validation based on dictionary flair values

    for val in filter_dict['required_flairs']:
        if val not in submission.link_flair_text.lower():
            return False

    for val in filter_dict['restricted_flairs']:
        if val in submission.link_flair_text.lower():
            return False

    return True  # Everything passed, post is valid


def is_stickied(submission) -> bool:
    # Checks if a post is stickied (by the mods of the subreddit), can skip if true
    return submission.stickied


def is_urgent(submission) -> bool:
    # Checks if a post is considered as "urgent" - this is defined as over 200 upvotes on the post in a given day
    return submission.score > 200
