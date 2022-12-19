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
        sender="Customized Reddit Newsletter",
        html="""
        <td class="esd-block-spacer es-p10t es-p10b esd-hover-drag-disabled" style="font-size:0" align="center">
            <table width="100%" height="100%" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td class="esd-structure es-p20t es-p20r es-p20l" align="left">
                            <table width="100%" cellspacing="0" cellpadding="0">
                                <tbody>
                                    <tr>
                                        <td class="esd-container-frame" width="560" valign="top" align="center">
                                            <table width="100%" cellspacing="0" cellpadding="0">
                                                <tbody>
                                                    <tr>
                                                        <td class="esd-block-text" align="center">
                                                            <h2>Customized Reddit Newsletter<br></h2>
                                                            <tr>
                                                                <td style="border-bottom: 2px solid #53c7b4; background: none; height: 1px; width: 100%; margin: 0px;"></td>
                                                            </tr>
                                                            
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <p align="center" style="color: #2e6c80;">
                                <strong>
                                    Please see below for the posts that fit your criteria this week!<br /><br /><br />
                                </strong>
                            </p>
                        </td>
                    </tr>
                </tbody>
            </table>
        </td> 
        """ +
             formatted_html
        + """
        <p>
            <p align="center"><strong>
                If you want to edit your subreddit preferences, please visit <a href="">this website</a> and be sure to save your changes.
            </strong><br/></p>
        </p>
        
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
