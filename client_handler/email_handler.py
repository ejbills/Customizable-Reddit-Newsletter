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

    html = """
    <html>
      <body style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
        <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Ding! Your newsletter is ready.</span>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f6f6f6; width: 100%;" width="100%" bgcolor="#f6f6f6">
          <tr>
            <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
            <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; max-width: 580px; padding: 10px; width: 580px; margin: 0 auto;" width="580" valign="top">
              <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 580px; padding: 10px;">
    
                <!-- START CENTERED WHITE CONTAINER -->
                <table role="presentation" class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background: #ffffff; border-radius: 3px; width: 100%;" width="100%">
    
                  <!-- START MAIN CONTENT AREA -->
                  <tr>
                    <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;" valign="top">
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">
                        <tr>
                          <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">
                             <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">
                            """ + f"""
                                <h1 style="font-family: sans-serif; font-size: 28px; vertical-align: top; color: ded4b8;" valign="top">Customized Reddit Newsletter</h1>
                                <h2 style="font-family: sans-serif; font-size: 20px; vertical-align: top; color: ded4b8;" valign="top">{ "There are some popular posts from your subreddit list today. See them below!" 
                                 if daily_check else 
                                 "Please see below for the posts that fit your criteria this week!" }</h2>
                            """ + """
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; width: 100%;" width="100%">
                              <tbody>
                                <tr>
                                """ + formatted_tables + """
                                </tr>
                              </tbody>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
    
                <!-- END MAIN CONTENT AREA -->
                </table>
                <!-- END CENTERED WHITE CONTAINER -->
    
                <!-- START FOOTER -->
                <div class="footer" style="clear: both; margin-top: 10px; text-align: center; width: 100%;">
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">
                    <tr>
                      <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #999999; font-size: 12px; text-align: center;" valign="top" align="center">
                        <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">Made by Ethan Bills in Los Angeles, CA</span>
                      </td>
                    </tr>
                  </table>
                </div>
                <!-- END FOOTER -->
    
              </div>
            </td>
            <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
          </tr>
        </table>
      </body>
    </html>
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
                'See it on Reddit': f'<a href="{ mail_body[i][2] }">Reddit Link</a>'
            }
        )

    df = pd.DataFrame(data)

    styles = [
        dict(selector='table', props=[('border-collapse', 'separate'),
                                      ('border-radius', '25px')]),
        dict(selector='th', props=[('background-color', '#c9c7c7'),
                                   ('padding', '10px 15px 10px 15px'),
                                   ('font-size', '17px')]),
        dict(selector='th:first-child', props=[('border-radius', '25px 0 0 0')]),
        dict(selector='th:last-child', props=[('border-radius', '0 25px 0 0')]),
        dict(selector='tr:last-child td:first-child', props=[('border-radius', '0 0 0 25px')]),
        dict(selector='tr:last-child td:last-child', props=[('border-radius', '0 0 25px 0;'), ]),
        dict(selector='tr:nth-child(even)', props=[('background-color', '#f5f5f5')]),
        dict(selector='td', props=[('border-width', '0'),
                                   ('margin', '0'),
                                   ('padding', '15px 15px 15px 15px')])
    ]

    style = df.style.set_table_styles(styles)\
                    .hide(axis='index')\
                    .set_caption(f'Results from <b>{ subreddit_name }</b>')

    return CSSInliner().inline(style.to_html())
