import pandas as pd


def add_user(email, subreddit_prefs):
    # Adds formatted user data from web form to user csv file
    df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')

    df.loc[len(df.index)] = [email, subreddit_prefs]

    df.to_csv('./conf/user_preferences.csv', index=None, sep=';')


def update_user_email(original_email, updated_email):
    # Updates user email using vectorized pandas dataframe
    df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')

    df.loc[df['Email'] == original_email, 'Email'] = updated_email

    df.to_csv('./conf/user_preferences.csv', index=None, sep=';')


def unsubscribe_user(user_email):
    df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')

    user_row = df.loc[df['Email'] == user_email]
    df = df.drop(index=user_row.index)

    df.to_csv('./conf/user_preferences.csv', index=None, sep=';')


# def check_user_exists(user_email) -> bool:
#     df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')
#     return df['Email'] == user_email
