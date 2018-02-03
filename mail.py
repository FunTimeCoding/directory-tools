#!/usr/bin/env python3

from smtplib import SMTP
from email.message import EmailMessage

message = EmailMessage()
message.set_content('content')
message['Subject'] = 'subject'
message['From'] = 'example@example.org'
message['To'] = 'funtimecoding@gmail.com'
transport = SMTP('localhost')
transport.send_message(message)
transport.quit()
