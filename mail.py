#!/usr/bin/env python3

from smtplib import SMTP, SMTPRecipientsRefused
from email.message import EmailMessage

message = EmailMessage()
message.set_content('content')
message['Subject'] = 'subject'
message['From'] = 'example@example.org'
message['To'] = 'funtimecoding@gmail.com'
transport = SMTP('m2')

try:
    transport.send_message(message)
    transport.quit()
except ConnectionRefusedError as exception:
    print('Error: ' + str(exception))
except SMTPRecipientsRefused as exception:
    print('Error: ' + str(exception))
