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
        html="""
        <div style="margin: 15%;">
            <h1 style="color: #5e8ea0; text-align: center;">Customized Reddit Newsletter</h1>
            <hr style="width:80%">
            <h2 style="color: #5e8ea0;">Please see below for the posts that fit your criteria this week!</h2>
            """
                 + formatted_html +
            """
            <p><strong>If you want to edit your subreddit preferences, please visit <a 
            href="https://ethanbills.com/">this website</a> and be sure to save your changes.</strong><br 
            /><strong>Enjoy!</strong></p>
        </div>
        """,
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
                'URL': f"""<a href="{ mail_body[i][1] }">URL</a>""",
            }
        )

    return pd.DataFrame(data)


def format_html_body(subreddit_list):
    # Dynamically formats list of subreddit dataframes into html body for redmail to parse
    output_string = ""

    for subreddit in subreddit_list:
        temp_subreddit = '{{ ' + subreddit + ' }}'

        output_string += f"""
        Results from the <b>{ subreddit }</b> subreddit:
        
        { temp_subreddit }
        <br>
        <br>
        """

    return output_string
