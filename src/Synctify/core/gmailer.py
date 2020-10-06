import smtplib
import ssl

port = 465  # For SSL


class Gmailer(object):
    """
      Object to send gmail
    """


def __init__(self, password, username="therealjasmit"):
    self.username = username
    self.password = password

    self.context = ssl.create_default_context()


def send(self, recipent_list, message):
    with smtplib.SMTP_SSL(
        "smtp.gmail.com", port, context=self.context
            ) as server:
        server.login(self.username, self.password)
        server.sendmail("therealjasmit@gmail.com", recipent_list, message)
