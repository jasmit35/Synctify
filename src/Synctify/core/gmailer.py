import smtplib
import ssl

port = 465  # For SSL


class Gmailer(object):

    def __init__(self, password, username="therealjasmit@gmail.com"):
        self.username = username
        self.password = password

        self.context = ssl.create_default_context()


    def send(self, recipent_list, message):
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", port, context=self.context
                ) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, recipent_list, message)
