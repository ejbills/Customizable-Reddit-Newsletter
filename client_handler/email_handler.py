import smtplib
import yaml

from email.message import EmailMessage

conf = yaml.safe_load(open('./conf/application.yaml'))

email = conf['email_user']['email']
password = conf['email_user']['app_password']


def send_email(mail_list, mail_body):
    # Sends email
    email_message = EmailMessage()

    email_message['Subject'] = 'Freebies Mailing List'
    email_message['From'] = email
    email_message['To'] = mail_list
    email_message.set_content(format_email(mail_body))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(email_message)


def format_email(mail_body):
    # Formats the parsed freebie data, data comes in a nested array
    formatted_data = ""

    for i in range(len(mail_body)):
        formatted_data += mail_body[i][0] + " : " + mail_body[i][1] + "\n \n"

    return formatted_data
