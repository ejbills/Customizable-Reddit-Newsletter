import pandas as pd


def update_user_email(original_email, updated_email):
    # Updates user email using vectorized pandas dataframe
    df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')

    df.loc[df['Email'] == original_email, 'Email'] = updated_email

    df.to_csv('./conf/user_preferences.csv', index=None, sep=';')


# def check_user_exists(user_email) -> bool:
#     df = pd.read_csv('./conf/user_preferences.csv', delimiter=';')
#     return df['Email'] == user_email

# print(check_user_exists('asdkjahsdkjashdkjhasdf@gmail.com'))
# update_user_email('example1@gmail.com', 'fsdfsdfsdffffffffffffffff@gmail.com')