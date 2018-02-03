#!/usr/bin/env python3

from smtplib import SMTP, SMTPRecipientsRefused
from email.message import EmailMessage


class EmailSender:
    def __init__(self, server: str, sender: str):
        self.server = server
        self.sender = sender

    def send(self, subject: str, recipient: str, body: str):
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = recipient
        transport = SMTP(host=self.server)

        try:
            transport.send_message(msg=message)
            transport.quit()
        except ConnectionRefusedError as exception:
            print('Error: ' + str(exception))
        except SMTPRecipientsRefused as exception:
            print('Error: ' + str(exception))
