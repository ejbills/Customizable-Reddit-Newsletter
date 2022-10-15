import pandas as pd

from redmail import gmail
from datetime import date
from os import environ

email_user = environ['EMAIL']
password = environ['APP_PASS']


def send_email(mail_list, mail_body):
    # Sends email

    gmail.username = email_user
    gmail.password = password

    formatted_mail = format_email(mail_body)

    gmail.send(
        subject="Freebies for " + date.today().strftime("%B %d, %Y"),
        receivers=mail_list,
        html="{{ formatted_mail }}",
        body_tables={
            'formatted_mail': formatted_mail
        }
    )


def format_email(mail_body):
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


