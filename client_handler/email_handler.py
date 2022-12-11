import pandas as pd

from redmail import gmail
from datetime import date
from os import environ

email_user = environ['EMAIL']
password = environ['APP_PASS']


def send_email(email, parsed_posts_dict):
    # Sends email

    gmail.username = email_user
    gmail.password = password

    subreddit_list = parsed_posts_dict.keys()

    formatted_html = format_html_body(subreddit_list)
    formatted_tables = {}

    for subreddit in parsed_posts_dict.keys():  # Convert data into pandas dataframe
        formatted_tables[subreddit] = format_array(parsed_posts_dict[subreddit])

    gmail.send(
        subject="Generated mail for " + date.today().strftime("%B %d, %Y"),
        receivers=email,
        html=formatted_html,
        body_tables=formatted_tables,
        body_params={
            "subreddit_list": subreddit_list,
        },
    )


def format_array(mail_body):
    # Formats the parsed freebie data, data comes in a nested array

    data = []

    for i in range(len(mail_body)):
        data.append(
            {
                'Title': mail_body[i][0],
                'Link': mail_body[i][1],
            }
        )

    return pd.DataFrame(data)


def format_html_body(subreddit_list):
    # Dynamically formats list of subreddit dataframes into html body for redmail to parse
    output_string = ""

    for subreddit in subreddit_list:
        temp_subreddit = '{{ ' + subreddit + ' }}'

        output_string += f"""
        Results from the <b>{subreddit}</b> subreddit:
        
        {temp_subreddit}
        <br>
        <br>
        """

    return output_string
