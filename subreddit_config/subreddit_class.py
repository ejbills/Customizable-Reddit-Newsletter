import ast


class SubredditConfig:
    user_objects = {}

    def __init__(self, email):
        self.email = email
        self.subreddit_config = {}

        SubredditConfig.user_objects[self.email] = self

    def get_subreddits(self):
        return self.subreddit_config.keys()

    def put_flair_prefs(self, subreddit, flair_prefs):
        self.subreddit_config[subreddit] = dict(ast.literal_eval(flair_prefs))
