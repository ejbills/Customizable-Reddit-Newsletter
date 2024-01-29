import conf.config

import praw

from os import environ

client_id = environ['CLIENT_ID']
client_secret = environ['CLIENT_SECRET']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent='Scrape posts for data collection'
)


def scrape_top_posts(daily_check, filter_dict, query) -> list:
    # Execute subreddit praw call with filter logic
    parsed_submissions = []
    temp_submission_stream = []  # Handle saving subreddit stream to prevent duplicate praw calls

    is_search = filter_dict['is_search'] if 'is_search' in filter_dict else False
    subreddit_scope = query if not is_search else 'all'  # determine scope for query, if it's a search -> search all

    time_filter = 'day' if daily_check else 'week'

    # Check if subreddit previously scraped
    if query not in conf.config.prev_searched_queries.keys():
        if is_search:
            subreddit_stream = reddit.subreddit(subreddit_scope).top(time_filter)
        else:
            subreddit_stream = reddit.subreddit(subreddit_scope).search(query, sort='top', time_filter=time_filter)

    else:
        subreddit_stream = conf.config.prev_searched_queries[query]

    for submission in subreddit_stream:
        temp_submission_stream.append(submission)  # Save submissions to prevent repeating search

        if not daily_check:
            if contains_flairs(filter_dict, submission) and not is_stickied(submission):
                parsed_submissions.append([submission.title, submission.url,
                                           reddit.config.reddit_url + submission.permalink])

        else:
            if is_urgent(submission) and contains_flairs(filter_dict, submission) and not is_stickied(submission):
                parsed_submissions.append([submission.title, submission.url,
                                           reddit.config.reddit_url + submission.permalink])

    conf.config.prev_searched_queries[query] = temp_submission_stream

    return parsed_submissions


def contains_flairs(filter_dict, submission) -> bool:
    # Checks if the post flair passes validation based on dictionary flair values
    stripped_filter_dict = filter_dict

    if 'is_search' in filter_dict: stripped_filter_dict.pop('is_search')  # we can ignore the search element

    if all(len(flair_prefs) > 0 for flair_prefs in stripped_filter_dict.values()):
        if submission.link_flair_text is not None:
            required_flairs = any(
                flair in submission.link_flair_text.lower() for flair in filter_dict['required_flairs'])
            restricted_flairs = not any(
                flair in submission.link_flair_text.lower() for flair in filter_dict['restricted_flairs'])

            return required_flairs and restricted_flairs  # Everything passed, post is valid

        else:  # No flairs in post, can default to invalid
            return False
    else:  # No flair prefs, every post will be valid
        return True


def is_stickied(submission) -> bool:
    # Checks if a post is stickied (by the mods of the subreddit), can skip if true
    return submission.stickied


def is_urgent(submission) -> bool:
    # Checks if a post is considered as "urgent" - this is defined as over 200 up-votes on the post in a given day
    return submission.score > 200
