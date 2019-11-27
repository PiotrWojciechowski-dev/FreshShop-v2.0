import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from django.conf import settings

class Email:
    @staticmethod
    def sendSignUpConfirmation(request, to_username, to_user_email):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Account successfully created!!!!"
        msg["From"] = "ffffff@gmail.com"
        msg['Date'] = formatdate(localtime=settings.EMAIL_USE_LOCALTIME)
        msg["To"] = str(to_user_email)
        # Create the plain-text and html version of your message
        html = """<html><body><h2>Account has been created! Account Name: {}</h2></body></html>""".format(to_username)
        # Turn the message into a plain/html MIMETEXT object
        content = MIMEText(html, "html")
        # Add HTML/plain=text parts to MIMEMultipart message
        msg.attach(content)
        #call the method to connect with the server and send email
        Email.send_email(to_user_email, msg)

    
    @staticmethod
    def send_email(request, message):
        port = 25
        smtp_server = "localhost"
        sender_email = "ffffff@hotmail.com"
        server = smtplib.SMTP(smtp_server)
        server.sendmail("rrrrrrrrr@hotmail.com", str(request), message.as_string())