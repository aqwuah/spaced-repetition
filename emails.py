from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl, smtplib, datetime, emoji

SENDER = ""
RECEIVER = ""
PASSWORD = ""

def construct_email(info, subjects, hw_tests):
    # Construct multipart email
    message = MIMEMultipart("alternative")
    message["Subject"] = f"{datetime.datetime.today().strftime('%A')}'s Recap"
    message["From"] = SENDER
    message["To"] = RECEIVER

    # Make text and html variants
    text = "HTML has not rendered. Please wait."
    html = open("email_template.txt", "r").read()

    # Format HTML to include dynamic content
    html = html.format(name="Thomas", day=datetime.datetime.today().strftime('%A'), tada=emoji.emojize(":partying_face:"), memo=emoji.emojize(":memo:"), books=emoji.emojize(":books:"), pencil=emoji.emojize(":pencil:"), subject1=subjects[0], subject2=subjects[1], subject3=subjects[2], subject1url=info[0]["url"], subject1title=info[0]["title"], subject1topic=info[0]["topic"], subject1created=info[0]["created"], subject1term=info[0]["term"], subject2url=info[1]["url"], subject2title=info[1]["title"], subject2topic=info[1]["topic"], subject2created=info[1]["created"], subject2term=info[1]["term"], subject3url=info[2]["url"], subject3title=info[2]["title"], subject3topic=info[2]["topic"], subject3created=info[2]["created"], subject3term=info[2]["term"], hw=hw_tests[0], tests=hw_tests[1])

    # Attach to message object
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    return message

def send_email(message):
    # Use SSL for security
    context = ssl.create_default_context()

    # Login to SMTP and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, message.as_string())
