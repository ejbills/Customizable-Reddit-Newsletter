import ast


class SubredditConfig:
    user_objects = {}

    def __init__(self, email, subreddit_prefs):
        self.email = email
        self.subreddit_config = {}

        self.put_subreddits(subreddit_prefs)

        SubredditConfig.user_objects[self.email] = self

    def get_subreddits(self):
        return self.subreddit_config.keys()

    def put_subreddits(self, subreddit_prefs):
        for subreddit in subreddit_prefs:
            temp_subreddit_prefs = subreddit.split("=")

            self.subreddit_config[temp_subreddit_prefs[0]] = dict(ast.literal_eval(temp_subreddit_prefs[1]))
