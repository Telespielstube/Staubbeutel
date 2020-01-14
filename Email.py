import smtplib
from email.mime.text import MIMEText
from socket import gaierror

class Email():
    def __init__(self):
        self.smtp_port = 587
        self.smtp_server = "smtp.mailtrap.io"
        self.smtp_username = "72856b122bb1ef"
        self.smtp_password = "8bf33cb3c6c803"
        self.sender = "noreply@sqlite.db"
        self.receiver = "info@example.com"

    # Sends an error message to a fake SMTP Server
    def sendErrorMessage(self):
        msg = MIMEText('Publisher unexpectedly disconnected from network. Check the publishers connection."""')
        msg['Subject'] = 'Error Message'
        msg['To'] = self.receiver
        msg['From'] = self.sender

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender, self.receiver, str(msg))
            print("Sent error mail to " + str(self.receiver))
        except ConnectionRefusedError as e:
            print("Failed to connect to server." + str(e))
        except smtplib.SMTPException as e:
            print("SMTP error: " + str(e))
