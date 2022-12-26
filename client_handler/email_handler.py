import smtplib
import pandas as pd

from datetime import date
from os import environ

from css_inline import CSSInliner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_user = environ['EMAIL']
password = environ['APP_PASS']


def send_email(daily_check, email, parsed_posts_dict):
    # Sends email
    msg = MIMEMultipart('alternative')

    msg['Subject'] = 'Your Reddit Newsletter for ' + date.today().strftime('%B %d, %Y')
    msg['From'] = f'Custom Reddit Newsletter <{ email_user }>'
    msg['To'] = email

    formatted_tables = ''

    for subreddit in parsed_posts_dict.keys():  # Convert data into HTML table
        formatted_tables += array_to_html(subreddit, parsed_posts_dict[subreddit]) + '<br>'

    html = f"""
    <h1 style="color: #7099c2">Customized Reddit Newsletter</h1>
    <h2 style="color: #7099c2">{ "There is some popular posts from your subreddit list today, see them below!" 
                                 if daily_check else 
                                 "Please see below for the posts that fit your criteria this week!" }</h2>
    """ + formatted_tables + """
    <p>
        <strong>
            If you want to edit your subreddit preferences, please visit 
            <a href="https://ethanbills.com/">this website</a> and be sure to save your changes.<br/>
        </strong>
        <strong>
            Enjoy!<br/>
        </strong>
        <a href="https://ethanbills.com/unsubscribe">Click here to unsubscribe</a>
    </p>
    """

    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.ehlo()
        s.starttls()
        s.login(email_user, password)

        s.send_message(msg)


def array_to_html(subreddit_name, mail_body):
    # Formats the parsed reddit data and returns an email-friendly HTML body
    data = []

    for i in range(len(mail_body)):
        data.append(
            {
                'Title': mail_body[i][0],
                'URL': f'<a href="{ mail_body[i][1] }">URL</a>',
            }
        )

    df = pd.DataFrame(data)

    styles = [
        dict(selector='tr:nth-child(even)', props=[('background-color', '#f5f5f5')]),
        dict(selector='th', props=[('padding-top', '0.3em'),
                                   ('padding-bottom', '0.3em'),
                                   ('background-color', '#f5f5f5'),
                                   ('font-size', '18px'),
                                   ('width', '100%')
                                   ]),
        dict(selector='td', props=[('font-size', '14px'),
                                   ('padding', '4px'),
                                   ('border-width', '0'),
                                   ('margin', '0'),
                                   ]),
    ]

    style = df.style.set_table_styles(styles)\
                    .hide(axis='index')\
                    .set_caption(f'Results from the <b>{ subreddit_name }</b> subreddit')

    return CSSInliner().inline(style.to_html())
