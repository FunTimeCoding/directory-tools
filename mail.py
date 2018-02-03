#!/usr/bin/env python3

from smtplib import SMTP, SMTPRecipientsRefused
from email.message import EmailMessage

message = EmailMessage()
message.set_content('This is a sample message.')
message['Subject'] = 'Sample message'
message['From'] = 'funtimecoding@gmail.com'
message['To'] = 'shiinto@me.com'
transport = SMTP('m2')

try:
    transport.send_message(message)
    transport.quit()
except ConnectionRefusedError as exception:
    print('Error: ' + str(exception))
except SMTPRecipientsRefused as exception:
    print('Error: ' + str(exception))
